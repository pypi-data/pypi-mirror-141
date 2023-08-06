import socket
import time
import threading

from PyQt5.QtCore import QObject, pyqtSignal

from common.utils import *
from common.errors import ServerError
from client.database import ClientStorage

logger = logging.getLogger('client')
sock_lock = threading.Lock()


class BaseClient(threading.Thread, QObject):
    new_message = pyqtSignal(str)
    message_205 = pyqtSignal()
    connection_lost = pyqtSignal()

    def __init__(self, server_address, server_port, database, username, password, keys):
        threading.Thread.__init__(self)
        QObject.__init__(self)

        self.server_address = server_address
        self.server_port = server_port
        self.database = database
        self.username = username
        self.password = password
        self.keys = keys
        self.transport = None
        self.init_connection()
        try:
            self.request_user_list()
            self.request_contacts_list()
        except OSError as err:
            if err.errno:
                logger.critical(f'Потеряно соединение с сервером.')
                raise ServerError('Потеряно соединение с сервером!')
            logger.error('Timeout соединения при обновлении списков пользователей.')
        except json.JSONDecodeError:
            logger.critical(f'Потеряно соединение с сервером.')
            raise ServerError('Потеряно соединение с сервером!')
            # Флаг продолжения работы транспорта.
        self.running = True

    def create_presence(self):
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.username
            }
        }
        logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {self.username}')
        return out

    def init_connection(self):
        logger.info(
            f'Запущен клиент с параметрами: адрес сервера: {self.server_address} , порт: {self.server_port}, '
            f'имя пользователя: {self.username}')
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.transport.settimeout(5)
        connected = False
        for i in range(5):
            logger.info(f'Попытка подключения №{i + 1}')
            try:
                self.transport.connect((self.server_address, self.server_port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                break
            time.sleep(1)

        if not connected:
            logger.critical('Не удалось установить соединение с сервером')
            raise ServerError('Не удалось установить соединение с сервером')

        logger.debug('Установлено соединение с сервером')

        try:
            with sock_lock:
                send_message(self.transport, self.create_presence())
                self.server_msg_handler(get_message(self.transport))
        except (OSError, json.JSONDecodeError):
            logger.critical('Потеряно соединение с сервером!')
            raise ServerError('Потеряно соединение с сервером!')

        logger.info('Соединение с сервером успешно установлено.')

    def server_msg_handler(self, message):
        logger.debug(f'Разбор сообщения от сервера: {message}')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return
            elif message[RESPONSE] == 400:
                raise ServerError(f'{message[ERROR]}')
            else:
                logger.debug(f'Принят неизвестный код подтверждения {message[RESPONSE]}')
        elif ACTION in message \
                and message[ACTION] == MESSAGE \
                and SENDER in message \
                and DESTINATION in message \
                and MESSAGE_TEXT in message \
                and message[DESTINATION] == self.username:
            logger.debug(f'Получено сообщение от пользователя {message[SENDER]}: '
                         f'{message[MESSAGE_TEXT]}')
            self.database.save_message(message[SENDER], self.username, message[MESSAGE_TEXT])
            self.new_message.emit(message[SENDER])

    def request_user_list(self):
        logger.debug(f'Запрос списка известных пользователей {self.username}')
        req = {
            ACTION: USERS_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with sock_lock:
            send_message(self.transport, req)
            ans = get_message(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 202:
            self.database.add_users(ans[LIST_INFO])
        else:
            logger.error('Не удалось обновить список известных пользователей.')

    def request_contacts_list(self):
        logger.debug(f'Запрос контакт листа для пользователя {self.username}')
        req = {
            ACTION: GET_CONTACTS,
            TIME: time.time(),
            USER: self.username
        }
        logger.debug(f'Сформирован запрос {req}')
        with sock_lock:
            send_message(self.transport, req)
            ans = get_message(self.transport)
            logger.debug(f'Получен ответ {ans}')
        if RESPONSE in ans and ans[RESPONSE] == 202:
            for contact in ans[LIST_INFO]:
                self.database.add_contact(contact)
            return ans[LIST_INFO]
        else:
            raise ServerError

    def add_contact(self, contact):
        logger.debug(f'Создание контакта {contact}')
        req = {
            ACTION: ADD_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with sock_lock:
            send_message(self.transport, req)
            self.server_msg_handler(get_message(self.transport))

    def del_contact(self, contact):
        logger.debug(f'Удаление контакта {contact}')
        req = {
            ACTION: REMOVE_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with sock_lock:
            send_message(self.transport, req)
            self.server_msg_handler(get_message(self.transport))

    def send_user_message(self, to, message):
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.username,
            DESTINATION: to,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        logger.debug(f'Сформирован словарь сообщения: {message_dict}')

        with sock_lock:
            send_message(self.transport, message_dict)
            self.server_msg_handler(get_message(self.transport))
            logger.info(f'Отправлено сообщение для пользователя {to}')
    def client_shutdown(self):
        self.running = False
        message = {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with sock_lock:
            try:
                send_message(self.transport, message)
            except OSError:
                pass
        logger.debug('Клиент завершает работу.')
        time.sleep(0.5)

    def run(self):
        logger.debug('Запущен процесс - приёмник сообщений с сервера.')
        while self.running:
            time.sleep(1)
            with sock_lock:
                try:
                    self.transport.settimeout(0.5)
                    message = get_message(self.transport)
                except OSError as err:
                    if err.errno:
                        # выход по таймауту вернёт номер ошибки err.errno равный None
                        # поэтому, при выходе по таймауту мы сюда попросту не попадём
                        logger.critical(f'Потеряно соединение с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                # Проблемы с соединением
                except (ConnectionError, ConnectionAbortedError,
                        ConnectionResetError, json.JSONDecodeError, TypeError):
                    logger.debug(f'Потеряно соединение с сервером.')
                    self.running = False
                    self.connection_lost.emit()
                # Если сообщение получено, то вызываем функцию обработчик:
                else:
                    logger.debug(f'Принято сообщение с сервера: {message}')
                    self.server_msg_handler(message)
                # finally:
                    self.transport.settimeout(5)


if __name__ == '__main__':
    database = ClientStorage('test1')
    client = BaseClient('127.0.0.1', 7777, database, 'User_test')
    client.run()

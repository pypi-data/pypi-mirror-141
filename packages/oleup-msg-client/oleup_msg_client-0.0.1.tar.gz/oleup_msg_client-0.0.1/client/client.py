import argparse

from PyQt5.QtWidgets import QApplication

from common.utils import *
from common.errors import ServerError
from client.core import BaseClient
from client.start_dialog import LoginDialog
from client.database import ClientStorage
from client.gui import ClientMainWindow

logger = logging.getLogger('client')


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)
    return server_address, server_port, client_name


def main():
    server_address, server_port, client_name = arg_parser()
    client_app = QApplication(sys.argv)
    if not client_name:
        start_dailog = LoginDialog()
        client_app.exec_()
        if start_dailog.ok_pressed:
            client_name = start_dailog.client_name.text()
            del start_dailog
    else:
        exit(0)
    logger.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address} , '
        f'порт: {server_port}, имя пользователя: {client_name}')
    database = ClientStorage(client_name)
    try:
        client_transport = BaseClient(server_address, server_port, database, client_name)
    except ServerError as e:
        print(e.text)
        exit(1)
    client_transport.setDaemon(True)
    client_transport.start()
    main_window = ClientMainWindow(database, client_transport)
    main_window.make_connection(client_transport)
    main_window.setWindowTitle(f'Чат-клиент alpha release - {client_name}')
    client_app.exec_()

    client_transport.client_shutdown()
    client_transport.join()

if __name__ == '__main__':
    main()

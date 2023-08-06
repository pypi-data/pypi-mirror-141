import sys
import logging

from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QApplication
from PyQt5.QtCore import Qt

sys.path.append('../')
logger = logging.getLogger('client_dist')


# Диалог выбора контакта для добавления
class AddContactDialog(QDialog):
    def __init__(self, client_instance, database_instance):
        super().__init__()
        self.transport = client_instance
        self.database = database_instance

        self.setFixedSize(350, 120)
        self.setWindowTitle('Выберите контакт для добавления:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт для добавления:', self)
        self.selector_label.setFixedSize(230, 20)
        self.selector_label.move(10, 5)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_refresh = QPushButton('Обновить список', self)
        self.btn_refresh.setFixedSize(120, 30)
        self.btn_refresh.move(60, 70)

        self.btn_ok = QPushButton('Добавить', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 30)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 70)
        self.btn_cancel.clicked.connect(self.close)

        self.create_possible_contacts()
        self.btn_refresh.clicked.connect(self.update_possible_contacts)

    def create_possible_contacts(self):
        self.selector.clear()
        contacts_list = set(self.database.get_contacts())
        users_list = set(self.database.get_users())
        users_list.remove(self.transport.username)
        self.selector.addItems(users_list - contacts_list)

    def update_possible_contacts(self):
        try:
            self.transport.request_user_list()
        except OSError:
            pass
        else:
            logger.debug('Обновление списка пользователей с сервера выполнено')
            self.create_possible_contacts()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    from database import ClientStorage

    database = ClientStorage('test1')
    from core import BaseClient

    transport = BaseClient(7777, '127.0.0.1', database, 'test1')
    window = AddContactDialog(transport, database)
    window.show()
    app.exec_()

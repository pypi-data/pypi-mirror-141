from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, qApp
from PyQt5.QtCore import QEvent


# Стартовый диалог с выбором имени пользователя
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.ok_pressed = False

        self.setWindowTitle('Привет!')
        self.setFixedSize(200, 130)

        self.label = QLabel('Введите имя пользователя:', self)
        self.label.setFixedSize(180, 10)
        self.label.move(10, 10)

        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(180, 20)
        self.client_name.move(10, 25)

        self.label = QLabel('Введите пароль:', self)
        self.label.setFixedSize(180, 10)
        self.label.move(10, 55)

        self.password = QLineEdit(self)
        self.password.setFixedSize(180, 20)
        self.password.move(10, 70)

        self.btn_ok = QPushButton('Войти', self)
        self.btn_ok.move(20, 100)
        self.btn_ok.clicked.connect(self.click)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(100, 100)
        self.btn_cancel.clicked.connect(qApp.exit)

        self.show()

    # Обработчик кнопки ОК, если поле ввода не пустое, ставим флаг и завершаем приложение.
    def click(self):
        if self.client_name.text() and self.password.text():
            self.ok_pressed = True
            qApp.exit()


if __name__ == '__main__':
    app = QApplication([])
    dial = LoginDialog()
    app.exec_()

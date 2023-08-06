import datetime

from sqlalchemy import create_engine, Column, Integer, String, DATETIME, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

from common.variables import *

Base = declarative_base()


class ClientStorage:
    class Users(Base):
        __tablename__ = 'all_users'

        id = Column(Integer, primary_key=True)
        username = Column(String, nullable=False, unique=True)

        def __init__(self, username):
            self.username = username

    class ContactList(Base):
        __tablename__ = 'contacts'

        id = Column(Integer, primary_key=True)
        username = Column(String, nullable=False, unique=True)

        def __init__(self, username):
            self.username = username

    class MessageHistory(Base):
        __tablename__ = 'message_history'

        id = Column(Integer, primary_key=True)
        from_user = Column(Integer, ForeignKey('contacts.id'))
        to_user = Column(Integer, ForeignKey('contacts.id'))
        message = Column(String, nullable=False)
        date_time = Column(DATETIME, default=datetime.datetime.now)

        def __init__(self, from_user, to_user, message):
            self.from_user = from_user
            self.to_user = to_user
            self.message = message

    def __init__(self, username):
        self.database_engine = create_engine(f'sqlite:///client_{username}_db.sqlite', echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})

        Base.metadata.create_all(self.database_engine)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.ContactList).delete()
        self.session.commit()

    def add_users(self, user_list):
        self.session.query(self.Users).delete()
        for user in user_list:
            user_row = self.Users(user)
            self.session.add(user_row)
        self.session.commit()

    def get_users(self):
        return [user[0] for user in self.session.query(self.Users.username).all()]

    def check_user(self, user):
        if self.session.query(self.Users).filter_by(username=user).count():
            return True
        else:
            return False

    def get_contacts(self):
        return [contact[0] for contact in self.session.query(self.ContactList.username).all()]

    def add_contact(self, contact):
        if contact not in self.get_contacts():
            contact_row = self.ContactList(contact)
            self.session.add(contact_row)
            self.session.commit()

    def del_contact(self, contact):
        self.session.query(self.ContactList).filter_by(username=contact).delete()
        self.session.commit()

    def check_contact(self, contact):
        if self.session.query(self.ContactList).filter_by(username=contact).count():
            return True
        else:
            return False

    def get_history(self, from_who=None, to_who=None):
        query = self.session.query(self.MessageHistory)
        if from_who:
            query = query.filter_by(from_user=from_who)
        if to_who:
            query = query.filter_by(to_user=to_who)
        return [(history_row.from_user, history_row.to_user, history_row.message, history_row.date_time)
                for history_row in query.all()]

    def save_message(self, from_user, to_user, message):
        message_row = self.MessageHistory(from_user, to_user, message)
        self.session.add(message_row)
        self.session.commit()


if __name__ == '__main__':
    test_db = ClientStorage('test_user1')
    test_db.add_users(['test_user1, test_user2', 'test_user3', 'test_user4'])
    print('___Список всех пользователей после добавления___')
    print(test_db.get_users())
    for i in ['test_user2', 'test_user3', 'test_user4']:
        test_db.add_contact(i)
    print('___Список контактов после добавления___')
    print(test_db.get_contacts())

    test_db.save_message('test_user1', 'test_user2',
                         f'Привет! я тестовое сообщение от {datetime.datetime.now()}!')
    test_db.save_message('test_user2', 'test_user1',
                         f'Привет! я другое тестовое сообщение от {datetime.datetime.now()}!')
    print('___История сообщений после добавления___')
    print(test_db.get_history())
    test_db.del_contact('test_user4')
    print('___Список контактов после удаления___')
    print(test_db.get_contacts())

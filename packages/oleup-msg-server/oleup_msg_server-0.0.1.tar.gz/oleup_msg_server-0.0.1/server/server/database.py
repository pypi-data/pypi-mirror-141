import datetime

from sqlalchemy import create_engine, Column, Integer, String, DATETIME, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

from common.variables import *

Base = declarative_base()


class ServerStorage:
    class User(Base):
        __tablename__ = 'all_users'

        id = Column(Integer, primary_key=True)
        name = Column(String, nullable=False, unique=True)
        last_login = Column(DATETIME, default=datetime.datetime.now)
        contacts = relationship('ContactList')

        def __init__(self, name):
            self.name = name

    class ActiveUser(Base):
        __tablename__ = 'active_users'

        id = Column(Integer, primary_key=True)
        user = Column(Integer, ForeignKey('all_users.id'), unique=True)
        ip_addr = Column(String, nullable=False)
        port = Column(Integer, nullable=False)
        login_time = Column(DATETIME)

        def __init__(self, user, ip_addr, port, login_time):
            self.user = user
            self.ip_addr = ip_addr
            self.port = port
            self.login_time = login_time

    class LoginHistory(Base):
        __tablename__ = 'login_history'

        id = Column(Integer, primary_key=True)
        name = Column(Integer, ForeignKey('all_users.id'))
        ip_addr = Column(String, nullable=False)
        port = Column(Integer, nullable=False)
        date_time = Column(DATETIME)

        def __init__(self, name, ip_addr, port, date_time):
            self.name = name
            self.ip_addr = ip_addr
            self.port = port
            self.date_time = date_time

    class ContactList(Base):
        __tablename__ = 'contacts_list'

        id = Column(Integer, primary_key=True)
        owner_id = Column(Integer, ForeignKey('all_users.id'))
        contact = Column(String, nullable=False)

        def __init__(self, owner_id, contact):
            self.owner_id = owner_id
            self.contact = contact

    def __init__(self, path):
        self.database_engine = create_engine(f'sqlite:///{path}', echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})

        Base.metadata.create_all(self.database_engine)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.ActiveUser).delete()
        self.session.commit()

    def user_login(self, username, ip_addr, port):
        user = self.session.query(self.User).filter_by(name=username).first()
        if user:
            user.last_login = datetime.datetime.now()
        else:
            user = self.User(username)
            self.session.add(user)
            self.session.commit()

        new_active_user = self.ActiveUser(user.id, ip_addr, port, datetime.datetime.now())
        self.session.add(new_active_user)

        history = self.LoginHistory(user.id, ip_addr, port, datetime.datetime.now())
        self.session.add(history)

        self.session.commit()

    def user_logout(self, username):
        user = self.session.query(self.User).filter_by(name=username).first()
        self.session.query(self.ActiveUser).filter_by(user=user.id).delete()
        self.session.commit()

    def users_list(self):
        return self.session.query(self.User.name, self.User.last_login).all()

    def active_users_list(self):
        return self.session.query(self.User.name, self.ActiveUser.ip_addr, self.ActiveUser.port,
                                  self.ActiveUser.login_time).join(self.User).all()

    def login_history(self, username=None):
        query = self.session.query(self.User.name, self.LoginHistory.date_time, self.LoginHistory.ip_addr,
                                   self.LoginHistory.port).join(self.User)
        if username:
            query = query.filter(self.User.name == username)
        return query.all()

    def add_contact(self, owner, contact):
        owner_in_db = self.session.query(self.User).filter_by(name=owner).first()
        contact_in_db = self.session.query(self.User).filter_by(name=contact).first()
        contacts = self.get_contacts(owner)
        if (contact not in contacts and contact_in_db):
            new_contact = self.ContactList(owner_in_db.id, contact)
            self.session.add(new_contact)
            self.session.commit()

    def get_contacts(self, owner):
        owner_in_db = self.session.query(self.User).filter_by(name=owner).first()
        return [value.contact for value in owner_in_db.contacts]

    def del_contact(self, owner, contact):
        owner_in_db = self.session.query(self.User).filter_by(name=owner).first()
        contact_in_db = self.session.query(self.User).filter_by(name=contact).first()
        if owner_in_db and contact_in_db:
            self.session.query(self.ContactList).filter(self.ContactList.owner_id == owner_in_db.id,
                                                        self.ContactList.contact == contact_in_db.name).delete()
            self.session.commit()


if __name__ == '__main__':
    from pprint import pprint

    test_db = ServerStorage('server_db.sqlite')

    test_db.user_login('User_1', '192.168.10.10', 8888)
    test_db.user_login('User_2', '192.168.10.11', 7777)
    test_db.user_login('User_3', '192.168.10.13', 9999)

    print('____Cписок активных пользователей____')
    pprint(test_db.active_users_list())

    test_db.user_logout('User_2')

    print('____Cписок активных пользователей после logout User_2____')
    pprint(test_db.active_users_list())

    print('____История входов пользователя User_!')
    pprint(test_db.login_history('User_1'))

    print('____Cписок всех пользователей___')
    pprint(test_db.users_list())

    test_db.add_contact('User_1', 'User_2')
    test_db.add_contact('User_1', 'User_3')
    test_db.add_contact('User_1', 'User_4')

    print('____Cписок контактов пользователя User_1____')
    pprint(test_db.get_contacts('User_1'))

    test_db.del_contact('User_1', 'User_3')

    print('____Cписок контактов пользователя User_1 после удаления контакта____')
    pprint(test_db.get_contacts('User_1'))
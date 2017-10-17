#Auxiliary Functions

import sqlalchemy
import os
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy import inspect


from model import User, Raw_data, Signal, Notification, Action
import model
from sqlalchemy import inspec

class ostools(object):
    def __initi__(self):
        self.os = ""
        self.user = ""
        self.ip = ""

    def rotina_atualizacao(self, ip):
        os.system('sudo apt-get update')
        os.system('sudo apt-get upgrade')

    def db_connection(self):
        engine = create_engine('postgresql://postgres:postgres@localhost/postgres')
        Session = scoped_session(sessionmaker())
        Session.configure(bind=engine)
        session = Session
        return session

class user_handler(object):
    def create_user(self, session, useremail, username, userpass, utype):
        newuser = model.User(email=useremail, name=username, password=userpass, \
                             usertype=utype)
        session.add(newuser)
        session.commit()
        session.flush()
        return newuser

    def delete_user(self, session, userid):
        deleteduser = session.query(User).filter_by(id=userid).delete()
        session.commit()
        session.flush()

    def get_user(self, session, searchemail):
        founduser = session.query(User).filter_by(email=searchemail).first()
        if not founduser:
            return False
        if founduser.email ==searchemail:
            return founduser
        else:
            return False

    def update_user_type(self, session, useremail):
        founduser = session.query(User).filter_by(email=useremail).first()
        if not founduser:
            return False
        if founduser.usertype == 0:
            founduser.type = 1
        if founduser.usertype == 1:
            founduser.type = 0
        session.commit()
        session.flush()
        return founduser

    def update_user_pass(self, session, usernewpass, useremail):
        founduser = session.query(User).filter_by(email=useremail).first()
        if not founduser:
            return False
        founduser.password = usernewpass
        session.commit()
        session.flush()
        return founduser

class data_handler(object):
    def create_data(self, session, data_price, data_date):
        new_data = model.Raw_data(price=data_price, date=data_date)
        session.add(new_data)
        session.commit()
        session.flush()
        return new_data

    def get_data(self, session, dataid):
        found_data = session.query(Raw_data).filter_by(id=dataid).first()
        if not found_data:
            return False
        if found_data.id == dataid:
            return found_data
        else:
            return False

    def get_daily_data(self, session, datadate):
        """Retorna lista de dados de uma determinada data"""
        found_datas = session.query(Raw_data).filter_by(date=datadate)
        for data in found_datas:
            if data.date != datadate:
                return False
        return found_datas

    def delete_data(self, session, dataid):
        found_data = session.query(Raw_data).filter_by(id=dataid).delete()
        session.commit()
        session.flush()

class signal_handler(object):
    def create_signal(self, session, signal_indicator, signal_date, signal_accuracy):
        new_signal = model.Signal(indicator=signal_indicator, date=signal_date,\
                                  accuracy=signal_accuracy)
        session.add(new_signal)
        session.commit()
        session.flush()
        return new_signal

    def get_signal(self, session, signal_id):
        found_signal = session.query(Signal).filter_by(id=signal_id).first()
        if not found_signal:
            return False
        if found_signal.id == signal_id:
            return found_signal
        else:
            return False

    def delete_signal(self, session, signalid):
        deleted_signal = session.query(Signal).filter_by(id=signalid).delete()
        session.commit()
        session.flush()

    def get_daily_signals(self, session, signal_date):
        """Retorna lista de sinais de uma determinada data"""
        found_signals = session.query(Signal).filter_by(date=signal_date)
        for signal in found_signals:
            if signal.date != signal_date:
                return False
        return found_signals

class notification_handler(object):
    def create_notification(self, session, notification_platform,\
                             notification_message):
        new_notification = model.Notification(platform=notification_platform,\
                                              message=notification_message)
        session.add(new_notification)
        session.commit()
        session.flush()
        return new_notification

    def get_notification(self, session, notification_id):
        found_notification = session.query(Notification).filter_by\
            (id=notification_id).first()
        if not found_notification:
            return False
        if found_notification.id == notification_id:
            return found_notification
        else:
            return False

    def delete_notification(self, session, notification_id):
        deleted_signal = session.query(Notification).filter_by\
            (id=notification_id).delete()
        session.commit()
        session.flush()

    def get_daily_notification(self, session, notification_date):
        """Retorna uma lista de notificacoes de uma determinada data"""
        found_notifications = session.query(Notification).filter_by\
            (date=notification_date)
        for notification in found_notifications:
            if notification.date != noitification_date:
                return False
        return found_notifications

class action_handler(object):
    def create_action(self, session, action_amount, action_date, action_user):
        new_action = model.Action(amount=action_amount, date=action_date, \
                                  performed_by=action_user)
        session.add(new_action)
        session.commit()
        session.flush()
        return new_action

    def get_action(self, session, action_id):
        found_action = session.query(Action).filter_by(id=action_id).first()
        if not found_action:
            return False
        if found_action.id == action_id:
            return found_action
        else:
            return False

    def delete_action(self, session, action_id):
        deleted_action = session.query(Action).filter_by(id=action_id).delete()
        session.commit()
        session.flush()

    def get_daily_actions(self, session, action_date):
        """Retorna uma lista de acoes de uma determinada data"""
        found_actions = session.query(Action).filter_by(date=action_date)
        for action in found_actions:
            if action.date != action_date:
                return False
        return found_actions


class indicator_handler(object):
    def create_indicator(self, session, indicator_name, indicator_date):
        new_indicator = model.Indicator(name=indicator_name, date=indicator_date)
        session.add(new_indicator)
        session.commit()
        session.flush()
        return new_indicator

    def get_indicator(self, sesison, indicator_id):
        found_indicator = session.query(Indicator).filter_by(id=indicator_id).first()
        if not found_indicator:
            return False
        if found_indicator.id == indicator_id:
            return found_indicator
        else:
            return False

    def delete_indicator(self, session, indicator_id):
        deleted_indicator = session.query(Indicator).filter_by(id=indicator_id).delete()
        session.commit()
        session.flush()

    def get_indicator_by_name(self, session, indicator_name):
        found_indicator = session.query(Indicator).filter_by(name=indicator_name).first()
        if not found_indicator:
            return False
        if found_indicator.name == indicator_name:
            return found_indicator
        else:
            return False



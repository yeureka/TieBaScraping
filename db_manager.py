#!/home/yeureka/.local/share/virtualenvs/TieBaScraping-CgIFm0CI/bin/python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sys import argv
from os import path

from config import config

Base = declarative_base()


class Topic(Base):
    __tablename__ = 'topic'

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, index=True)
    user_id = Column(Integer)
    reply_num = Column(Integer)
    user_name = Column(String(50))
    topic_title = Column(String(100))

    def __repr__(self):
        return "<Topic(id='{}', topic_id='{}', user_id='{})>'".format(self.id, self.topic_id, self.user_id)


class DBManager(object):
    def __init__(self, db):
        self.__engine = create_engine('sqlite:///{}'.format(db), echo=False)
        self.__Session = sessionmaker(bind=self.__engine)

    def create(self):
        Base.metadata.create_all(self.__engine)

    def session(self):
        return self.__Session()

    def add_record(self, record):
        sess = self.session()
        sess.add(record)
        sess.commit()

    def add_all_record(self, records):
        sess = self.session()
        sess.add_all(records)
        sess.commit()


class MonitorManager(DBManager):
    def __init__(self, db):
        super(MonitorManager, self).__init__(db)
        self.sess = self.session()

    def update_records(self, records):
        """
        check(id) -> add(dict) or update(dict)
        """
        for record in records:
            topic = self.check_topic_id(record['topic_id'])
            if topic:
                self.update_one_record(record)
            else:
                self.add_new_record(record)

    def check_topic_id(self, topic_id):
        topic = self.sess.query(Topic).filter(Topic.topic_id == topic_id).first()
        return topic

    def add_new_record(self, record):
        """
        create Topic -> add
        """
        topic = self.create_topic(record)
        self.add_record(topic)

    def update_one_record(self, record):
        sess = self.session()
        topic = sess.query(Topic).filter(Topic.topic_id == record['topic_id']).first()
        topic.reply_num = record['reply_num']
        topic.user_name = record['user_name']
        topic.topic_title = record['topic_title']
        sess.commit()

    @staticmethod
    def create_topic(record):
        topic = Topic(
            topic_id=record['topic_id'],
            user_id=record['user_id'],
            reply_num=record['reply_num'],
            user_name=record['user_name'],
            topic_title=record['topic_title']
        )
        return topic


if __name__ == '__main__':
    def create_db(name):
        if path.exists(name):
            print('同名数据库 {} 已存在'.format(name))
        else:
            db = DBManager(name)
            db.create()
            print('数据库 {} 创建成功'.format(name))

    if len(argv) == 1:
        db_name = config['database']
        create_db(db_name)
    elif argv[1] == 'monitor':
        db_name = config['monitor_database']
        create_db(db_name)
    else:
        print('参数错误，尝试 python db_manager [monitor]')

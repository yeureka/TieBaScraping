#!/Users/yeureka/.local/share/virtualenvs/TieBaScraping-QtiMVT_d/bin/python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import OperationalError
from sys import argv
from os import path

from config import config

Base = declarative_base()


class Topic(Base):
    __tablename__ = 'topic'

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer)
    user_id = Column(Integer)
    reply_num = Column(Integer)
    user_name = Column(String(50))
    topic_title = Column(String(100))

    def __repr__(self):
        return "<Topic(id='{}', topic_id='{}', user_id='{}'".format(self.id, self.topic_id, self.user_id)


class DBManager(object):
    def __init__(self, db):
        self.engine = create_engine('sqlite:///{}'.format(db), echo=False)
        self._Session = sessionmaker(bind=self.engine)

    def create(self):
        Base.metadata.create_all(self.engine)

    def session(self):
        return self._Session()

    def add_record(self, record):
        sess = self._Session()
        sess.add(record)
        sess.commit()

    def add_all_record(self, records):
        sess = self._Session()
        sess.add_all(records)
        sess.commit()

    def add_all_record_from_list(self, records):
        self.add_all_record(self.clean_up_list(records))

    @staticmethod
    def clean_up_list(record_list):
        cleaned_records = []
        for r in record_list:
            cleaned_records.append(
                Topic(topic_id=r['topic_id'],
                      user_id=r['user_id'],
                      reply_num=r['reply_num'],
                      user_name=r['user_name'],
                      topic_title=r['topic_title']
                      )
            )
        return cleaned_records


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

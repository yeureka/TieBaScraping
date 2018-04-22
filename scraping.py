#!/Users/yeureka/.local/share/virtualenvs/TieBaScraping-QtiMVT_d/bin/python
import time
from datetime import datetime
from random import randint
from sqlalchemy.exc import OperationalError
from sys import argv

from download_tool import Download
from log_tool import MyLog
from config import config
from extract_tool import get_topic_list, extract_info_topic_list
from db_manager import DBManager


def run(db, ba_name, start_page, end_page):
    download_session = Download()

    for i in range(start_page, end_page+1):
        try:
            r = download_session.page_download(ba_name, i)
        except Exception:
            log.error('页面下载错误，page {}'.format(i))
        else:
            try:
                topic_list = get_topic_list(r.text)
                topic_info_list = extract_info_topic_list(topic_list)
                db.add_all_record_from_list(topic_info_list)
                log.info('写入完成，page {}'.format(i))
            except OperationalError as e:
                log.error('数据库操作错误:', e.orig, '(When)', e.statement)
            except Exception:
                log.error('未获取到话题列表，page {}'.format(i))
                time.sleep(600)
        finally:
            if 0 < datetime.now().hour < 8:
                time.sleep(randint(30, 60))
            else:
                time.sleep(randint(20, 40))


if __name__ == '__main__':
    my_log = MyLog()
    log = my_log.my_log()
    name = config['ba_name']
    start = config['start_page']
    if len(argv) == 1:
        end = config['end_page']
        tieba_db = DBManager(config['database'])
        run(tieba_db, name, start, end)
    elif argv[1] == 'monitor':
        end = config['monitor_end_page']
        tieba_db = DBManager(config['monitor_database'])
        run(tieba_db, name, start, end)
    else:
        print('参数错误，尝试 python scraping monitor')

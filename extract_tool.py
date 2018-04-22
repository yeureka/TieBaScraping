import json
from bs4 import BeautifulSoup


def extract_info_topic(topic):
    topic_info = {}
    base_info = json.loads(topic.attrs['data-field'])
    topic_info['topic_id'] = base_info.get('id', None)
    topic_info['reply_num'] = base_info.get('reply_num', None)
    topic_info['user_name'] = base_info.get('author_name', None)
    topic_info['topic_title'] = topic.find(attrs={'class': 'j_th_tit'}).text.strip()
    topic_info['user_id'] = \
        json.loads(topic.find(attrs={'class': 'tb_icon_author'}).attrs['data-field']).get('user_id', None)
    return topic_info


def extract_info_topic_list(topic_list):
    topic_infos = []
    for topic in topic_list:
        topic_infos.append(extract_info_topic(topic))
    return topic_infos


def get_topic_list(text):
    soup = BeautifulSoup(text, 'html.parser')
    topic_list = soup.find_all(attrs={'class': 'j_thread_list'})
    return topic_list

from requests import Session


class Download(object):
    def __init__(self):
        self.url = 'http://tieba.baidu.com/f'
        self.s = Session()

    def page_download(self, ba_name, page_num):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'tieba.baidu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'god browser',
        }
        pn = (page_num - 1) * 50
        params = {
            'kw': ba_name,
            'le': 'utf-8',
            'pn': pn
        }
        r = self.s.get(self.url, params=params, headers=headers)
        return r

import logging


class MyLog(object):
    def __init__(self):
        # 创建一个日志记录器
        self.log = logging.getLogger("tieba_logger")
        self.log.setLevel(logging.DEBUG)

        # 创建一个日志处理器
        self.logHandler = logging.FileHandler(filename='tieba_scraping.log')
        self.logHandler.setLevel(logging.DEBUG)

        # 创建一个日志格式器
        self.formats = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')

        # 将日志格式器添加到日志处理器中
        self.logHandler.setFormatter(self.formats)

        # 将日志处理器添加到日志记录器中
        self.log.addHandler(self.logHandler)

    def my_log(self):
        return self.log

# 输出日志
# log = mylog()
# log.info("这是一个普通信息")
# log.debug("这是一个调试信息")
# log.warning("这是一个警告信息")
# log.error("这是一个错误信息")
# log.critical("这是一个危险信息")

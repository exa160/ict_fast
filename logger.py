import logging
import os
import sys
import time


def get_time():
    cur_time = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    return cur_time


def logger_init(debug):
    """
    初始化日志模块
    :param debug:bool：是否输出调试信息
    :return:
    """
    if debug:
        log_flag = logging.DEBUG
    else:
        log_flag = logging.INFO
    # cur_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    # log_path = os.path.join(cur_path, 'log', '{}.log'.format(get_time()))
    # os.makedirs(os.path.join(cur_path, 'log'), exist_ok=True)

    _logger = logging.getLogger(__name__)

    _logger.setLevel(level=log_flag)
    # handler = logging.FileHandler(log_path)
    # handler.setLevel(log_flag)
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d-[%(levelname)s]-[%(filename)s:%(lineno)d]: %(message)s',
                                  datefmt='%Y-%m-%d_%H:%M:%S')
    # handler.setFormatter(formatter)
    # _logger.addHandler(handler)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(log_flag)
    _logger.addHandler(console)

    return _logger

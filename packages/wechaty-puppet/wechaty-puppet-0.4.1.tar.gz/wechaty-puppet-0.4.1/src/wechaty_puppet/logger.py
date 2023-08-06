"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright Wechaty

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations
import logging
import os
from datetime import datetime


WECHATY_LOG_KEY = 'WECHATY_LOG'
WECHATY_LOG_FILE_KEY = 'WECHATY_LOG_FILE'


def _get_logger_level() -> str:
    """refer to : https://docs.python.org/3/library/logging.html#logging-levels

    fix: https://github.com/wechaty/python-wechaty/issues/192

    According to our Wechaty Specification <https://wechaty.js.org/docs/specs/wechaty>:
    The `WECHATY_LOG` should support the values of `silly`, `verbose`, `info`, `warn`, `silent`
    All Polyglot Wechaty should at least support the above names as an alias.
    Link to https://github.com/wechaty/wechaty/issues/2167
    """
    level_map = {
        'silly': 'CRITICAL',
        'verbose': 'INFO',
        'info': 'INFO',
        'warn': 'WARNING',
        'error': 'ERROR',
        'silent': 'NOTSET'
    }
    level: str = os.environ.get(WECHATY_LOG_KEY, 'INFO')
    return level_map.get(level, level)


def get_logger(name: str) -> logging.Logger:
    """
    configured Loggers
    """
    WECHATY_LOG = _get_logger_level()

    log_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create logger and set level to debug
    logger = logging.getLogger(name)
    logger.handlers = []
    logger.setLevel(WECHATY_LOG)
    logger.propagate = False

    # create file handler and set level to debug
    if WECHATY_LOG_FILE_KEY in os.environ:
        filepath = os.environ[WECHATY_LOG_FILE_KEY]
    else:
        base_dir = './logs'
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        time_now = datetime.now()
        time_format = '%Y-%m-%d-%H-%M'

        filepath = f'{base_dir}/log-{time_now.strftime(time_format)}.txt'

    file_handler = logging.FileHandler(filepath, 'a', encoding='utf-8')
    file_handler.setLevel(WECHATY_LOG)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    # create console handler and set level to info
    console_handler = logging.StreamHandler()
    console_handler.setLevel(WECHATY_LOG)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    return logger

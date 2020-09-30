""" helper for logging"""

import logging

Green = '\033[92m'
Red = '\033[91m'
Styles_end = '\033[0m'


class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler("logs/main.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.allow_log = True
        self.allow_print = True

    def prn_info(self, msg):
        if self.allow_print:
            print(f'{Green}{msg}{Styles_end}')

    def prn_err(self, msg):
        if self.allow_print:
            print(f'{Red}{msg}{Styles_end}')

    def log_err(self, msg):
        if self.allow_log:
            self.logger.error(msg)

    def log_info(self, msg):
        if self.allow_log:
            self.logger.info(msg)

    def prn_log_err(self, msg):
        self.log_err(msg)
        self.prn_err(msg)

    def prn_log_info(self, msg):
        self.log_info(msg)
        self.prn_info(msg)


if __name__ == "__main__":
    log = Logger(__name__)
    log.prn_log_info('Green')
    log.prn_log_err('Red')

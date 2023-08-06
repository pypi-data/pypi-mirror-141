import logging
import os

logger = None

class FileLogger:
    def __init__(self, logging_file_name):
        self.logging_file_name = logging_file_name
        self.logger = logging.getLogger()
        self.logger.setLevel(level=logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        self.file_handler = logging.FileHandler(self.logging_file_name)
        self.file_handler.setLevel(level=logging.INFO)
        self.file_handler.setFormatter(self.formatter)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logging.INFO)
        self.stream_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

    def reset_logging_file(self, logging_file_name):
        self.logging_file_name = logging_file_name
        self.logger.removeHandler(self.file_handler)
        self.file_handler = logging.FileHandler(self.logging_file_name)
        self.file_handler.setLevel(level=logging.INFO)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)



def createfilename():
    filelist = os.listdir("./")
    logging_index = 0
    logging_file_name = 'logging_'+str(logging_index)+'.log'
    while (logging_file_name in filelist):
        logging_index += 1
        logging_file_name = 'logging_' + str(logging_index) + '.log'
    return logging_file_name


def print(*infos):
    global logger
    if (type(logger) == type(None)):
        logging_file_name = createfilename()
        logger = FileLogger(logging_file_name)
    format_output = ""
    for item in infos:
        format_output += '{}'.format(item)
        format_output += '    '
    logger.logger.info(format_output)

def set_logging_file(logging_file_name):
    global logger
    if (type(logger) == type(None)):
        logging_file_name = logging_file_name
        logger = FileLogger(logging_file_name)
    else:
        logger.reset_logging_file(logging_file_name)









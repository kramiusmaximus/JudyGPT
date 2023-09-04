import logging
import logging.config
import yaml
import os
import shutil
import dotenv
dotenv.load_dotenv()
ROOT_DIR = os.getenv('ROOT_DIR')


class CustomFormatterColored(logging.Formatter):

    white = "\x1b[37;20m"
    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = '[%(asctime)s - %(levelname)s] %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'

    FORMATS = {
        logging.DEBUG: white + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.datefmt)
        return formatter.format(record)

class CustomFormatter(logging.Formatter):
    _format = '[%(asctime)s - %(levelname)s] %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'


    def format(self, record):
        formatter = logging.Formatter(self._format, datefmt=self.datefmt)
        return formatter.format(record)


class WarningFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno <= logging.WARNING

def setup():
    try:
        shutil.rmtree(ROOT_DIR + "/tmp")
    except FileNotFoundError:
        pass
    except Exception as e:
        raise e
    os.mkdir(ROOT_DIR + "/tmp")
    open(ROOT_DIR + "/tmp/out.log", 'a')
    open(ROOT_DIR + "/tmp/err.log", 'a')

    filename = 'logging.yaml'
    with open(ROOT_DIR + '/' + filename, 'rt') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)
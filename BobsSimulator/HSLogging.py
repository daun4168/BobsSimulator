import logging

LOG_DIR = 'logs'


class HSLogBugFilter(logging.Filter):

    def filter(self, record):
        return record.getMessage().find("폭풍 마나") == -1


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    handlers=[logging.FileHandler(THIS_LOG_FILE_NAME, 'w', 'utf-8')])

hslogger = logging.getLogger('HS')
logging = hslogger

f = HSBugFilter()
hslogger.addFilter(f)
hslogger.info("Program Start")

# BobsSimulator.log
# HSBattle.log
# HSLogHandler.log

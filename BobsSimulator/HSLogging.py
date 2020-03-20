import logging
import logging.config
import os
import json

class HSLogBugFilter(logging.Filter):

    def filter(self, record):
        return record.getMessage().find("폭풍 마나") == -1


# main_logger = logging.getLogger('main')
# main_logger_file_name = 'BobsSimulator.log'
# hsbattle_logger = logging.getLogger('hsbattle')
# hsbattle_logger_file_name = 'HSBattle.log'
# hsloghandler_logger = logging.getLogger('handler')
# handler_logger_file_name = 'HSLogHandler.log'
#
# handler_logger.level
# handler_logger.config(level=logging.DEBUG,
#                     format='%(asctime)s - %(levelname)s: %(message)s',
#                     datefmt='%m/%d/%Y %H:%M:%S',
#                     handlers=[logging.FileHandler(os.path.join(LOG_DIR, handler_logger_file_name), 'w', 'utf-8')])
#
# handler_logger

LOG_DIR = 'logs'
if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

with open('BobsSimulator/logging.json', 'rt') as f:
    config = json.load(f)

logging.config.dictConfig(config)

main_logger = logging.getLogger('main')
hsbattle_logger = logging.getLogger('hsbattle')
hsloghandler_logger = logging.getLogger('hsloghandler')

hsloghandler_logger.addFilter(HSLogBugFilter())

from BobsSimulator.Main import version_number

main_logger.info("Logging Start")
main_logger.info(f"Version: {version_number}")


if __name__ == '__main__':
    main_logger.info("HELLO Logger")
    main_logger.error("Logger Error")
    main_logger.debug("HIHI")
    hsbattle_logger.debug("HSBATTLE DEBUG")
    hsbattle_logger.info("HSBATTLE INFO")
    hsloghandler_logger.info("HSBATTLE INFO")
    hsloghandler_logger.debug("HSBATTLE debug")
    hsloghandler_logger.info("폭풍 마나나아아아아")
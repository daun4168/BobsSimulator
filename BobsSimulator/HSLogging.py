import logging
import logging.config
import os
import json

from BobsSimulator.Config import VERSION_NUMBER


class HSLogBugFilter(logging.Filter):

    def filter(self, record):
        return record.getMessage().find("폭풍 마나") == -1


LOG_DIR = 'logs'
if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

with open('BobsSimulator/logging.json', 'rt') as f:
    config = json.load(f)

logging.config.dictConfig(config)

main_logger = logging.getLogger('main')
hsbattle_logger = logging.getLogger('hsbattle')
hsloghandler_logger = logging.getLogger('hsloghandler')
simulator_logger = logging.getLogger('simulator')
console_logger = logging.getLogger('console')

hsloghandler_logger.addFilter(HSLogBugFilter())

main_logger.info("Logging Start")
main_logger.info(f"Version: {VERSION_NUMBER}")

simulator_logger.info("| 🌟 lv2 | 💀 deathrattle | ⚪ divine shield | ☣️ poisonous |  🛡️ taunt | 🎗️ reborn |\n")

if __name__ == '__main__':
    main_logger.info("HELLO Logger")
    main_logger.error("Logger Error")
    main_logger.debug("HIHI")
    hsbattle_logger.debug("HSBATTLE DEBUG")
    hsbattle_logger.info("HSBATTLE INFO")
    hsloghandler_logger.info("HSBATTLE INFO")
    hsloghandler_logger.debug("HSBATTLE debug")
    hsloghandler_logger.info("폭풍 마나나아아아아")

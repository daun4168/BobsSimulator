import os
import configparser


config = configparser.ConfigParser()
config.optionxform = str
config.read('config.ini')

VERSION_NUMBER = int(config['LIVE']['VERSION_NUMBER'])
LOCALE = config['LIVE']['LOCALE']
CARD_RES = config['LIVE']['CARD_RES']
HS_DIR = config['LIVE']['HS_DIR']



def set_hs_dir_config(hs_dir: str):
    config.set('LIVE', 'HS_DIR', hs_dir)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def set_use_power_log():
    localappdata_dir = os.getenv("LOCALAPPDATA")
    log_config_dir = os.path.join(localappdata_dir, 'Blizzard/Hearthstone')

    if not os.path.isdir(log_config_dir):
        os.makedirs(log_config_dir, exist_ok=True)

    log_config_path = os.path.join(log_config_dir, 'log.config')
    if not os.path.isfile(log_config_path):
        with open(log_config_path, 'w') as file:
            pass

    log_config = configparser.ConfigParser()
    log_config.optionxform = str
    log_config.read(log_config_path)

    sections = log_config.sections()
    if 'Power' not in sections:
        log_config.add_section('Power')

    log_config.set('Power', 'LogLevel', '1')
    log_config.set('Power', 'FilePrinting', 'True')
    log_config.set('Power', 'ConsolePrinting', 'False')
    log_config.set('Power', 'ScreenPrinting', 'False')
    log_config.set('Power', 'Verbose', 'True')

    with open(log_config_path, 'w') as file:
        log_config.write(file)



set_use_power_log()



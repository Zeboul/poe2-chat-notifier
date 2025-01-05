#!/usr/bin/env python3
import configparser
import logging
from pathlib import Path
import re
import sys
import time

from notifier import create_notifier


CONFIG_PATH = Path('./config.ini')


class LogEntry:
    def __init__(self, log_line):
        # Check that the line matches the typical format.
        if re.match(r'\d+/\d+/\d+ \d+:\d+:\d+ \d+ [a-zA-Z0-9]+ \[.*\]',
                    log_line, flags=re.ASCII) is not None:
            self._message = log_line.split(']')[1].strip()
            self._type = log_line.split()[3]
            # I've seen two different identifiers for chat messages in PoE2
            chat_ids = ['3ef2336f', '3ef2336d']
            if self._type.lower() in chat_ids:
                self._type = 'chat'
        else:
            self._type = 'unknown'
            self._message = ''

    @property
    def type(self):
        return self._type

    @property
    def message(self):
        return self._message


def readline_blocking(f) -> str:
    POLL_INTERVAL_S = .1
    line = ''
    while not line.endswith('\n'):
        next_characters = f.readline()
        if next_characters == '':
            time.sleep(POLL_INTERVAL_S)
            continue
        line += next_characters
    return line


def is_not_outgoing_dm(message):
    return (len(message) < 1 or
            not (message[0] == '@' and 'To' == message[1:].split()[0]))


def is_filtered(message, filtering_cfg) -> bool:
    info = message.split(':')[0]
    # Always filter system messages and empty usernames
    if len(info) < 2:
        return True
    if (filtering_cfg.getboolean('ONLY_SHOW_DIRECT_MESSAGES') and
            info[0] != '@'):
        return True
    return False


def check_config(cfg, logger):
    structure = {
        'Game': ['POE2_DIRECTORY'],
        'Notifications': [
            'ENABLE_NOTIFICATIONS',
            'ALWAYS_PLAY_NOTIFICATION_SOUND'
        ],
        'Filtering': ['ONLY_SHOW_DIRECT_MESSAGES'],
    }
    for section in structure.keys():
        if section not in cfg:
            logger.error(f'Missing "{section}" section in config file.')
            return False
    for section, options in structure.items():
        for option in options:
            if option not in cfg[section]:
                logger.error(
                    f'Missing "{option}" option in "{section}" section.')
                return False
    return True


def unhandled_exception_hook(logger, type, value, traceback):
    if type == KeyboardInterrupt:
        logger.info('Exiting')
        sys.exit(0)
    else:
        logger.critical('Unhandled exception',
                        exc_info=(type, value, traceback))
        sys.exit(3)


def main() -> int:
    logging.basicConfig(filename='poe2-chat-notifier.log', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler(stream=sys.stderr))
    logger.info('Starting chat notifier at {} UTC'.format(
        time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())))
    sys.excepthook = lambda type, value, traceback: unhandled_exception_hook(
        logger, type, value, traceback)

    cfg = configparser.ConfigParser()
    if not CONFIG_PATH.exists():
        logger.error(f'Config file ({CONFIG_PATH}) must be present.')
        return 2
    with CONFIG_PATH.open(encoding='utf-8') as f:
        cfg.read_file(f)
    if not check_config(cfg, logger):
        logger.error(f'Invalid config in {CONFIG_PATH}, refer to the included config.ini as an example.')  # noqa: E501
        return 2

    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        print('Usage: poe2-notifier.py [-h] [PoE2 directory override]')
        return 1
    install_dir = Path(cfg['Game']['POE2_DIRECTORY'])
    if len(sys.argv) > 1:
        install_dir = Path(sys.argv[1])

    notifier = create_notifier()
    always_play_sound = cfg.getboolean('Notifications',
                                       'ALWAYS_PLAY_NOTIFICATION_SOUND')
    poe_log_path = install_dir / Path('logs/Client.txt')
    if not install_dir.exists():
        logger.error(f'PoE2 installation directory ({CONFIG_PATH}::POE2_DIRECTORY) does not exist.')  # noqa: E501
        return 2
    if not poe_log_path.exists():
        # If the game has never been started before, this likely will not
        # exist.
        logger.info('Waiting for PoE2 to start...')
        logger.info(f'(if this hangs, double-check {CONFIG_PATH}::POE2_DIRECTORY.)')  # noqa: E501
        while not poe_log_path.exists():
            time.sleep(.25)
    logger.info('Opening chat...')
    # Since the seek can take a while, use the current file size since
    # seek(0, 2) might skip messages that are received after this program
    # starts running.
    initial_poe_log_size = poe_log_path.stat().st_size
    with poe_log_path.open(encoding='utf-8') as poe_log:
        poe_log.seek(initial_poe_log_size - 1, 0)
        # Skip possible incomplete line.
        if poe_log.read(1) != '\n':
            readline_blocking(poe_log)
        logger.info('Chat opened.')
        while True:
            entry = LogEntry(readline_blocking(poe_log))
            if (entry.type == 'chat' and
                    not is_filtered(entry.message, cfg['Filtering'])):
                print(entry.message)
                if (cfg.getboolean('Notifications', 'ENABLE_NOTIFICATIONS') and
                        is_not_outgoing_dm(entry.message)):
                    notifier.notify(entry.message, always_play_sound)
    return 0


if __name__ == '__main__':
    sys.exit(main())

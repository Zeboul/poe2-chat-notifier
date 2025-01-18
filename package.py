#!/usr/bin/env python3
from pathlib import Path
import platform
import shutil
import sys

import PyInstaller.__main__


ADDITIONAL_FILES = [
    'README.md',
    'config.ini',
    'LICENSE.txt',
]


def main() -> int:
    if len(sys.argv) != 2:
        print('Usage: package.py <version>')
        return 1
    release_version = sys.argv[1]

    DIST_DIR = Path('./dist')

    full_release_name = f'poe2-chat-notifier-{release_version}'
    pyinstaller_args = [
        str(Path('./src/poe2_chat_notifier/__main__.py')),
        '-n', 'poe2-chat-notifier',
        '-y',
    ]
    if platform.system() == 'Windows':
        pyinstaller_args.extend(['--collect-submodules', 'winrt.windows'])
    PyInstaller.__main__.run(pyinstaller_args)
    # --add-data puts them in a subdirectory, unfortunately
    for src in [Path(f) for f in ADDITIONAL_FILES]:
        shutil.copy(src, DIST_DIR / Path('poe2-chat-notifier') / src.name)
    shutil.make_archive(full_release_name, 'zip',
                        root_dir='dist/poe2-chat-notifier')


if __name__ == '__main__':
    sys.exit(main())

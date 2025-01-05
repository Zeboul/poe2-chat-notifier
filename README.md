Path of Exile 2 chat notifier tool.

When you receive a chat message, this tool will send a notification to you while
the game is minimized or you are tabbed-out, and by default will also make a
notification sound when you are in game. Chat messages will also be displayed in
a window outside of the game.

Common uses:
- Not missing trade messages.
- Viewing chat messages while the game is minimized.

This program will not get you banned. It does not send messages, change any game
state, or make any network communcations. It only reads from an event log file
(the `Client.txt` file).

## Configure and Run

### From Binaries

1. Download and extract the release zip file.
    - [https://github.com/Zeboul/poe2-chat-notifier/releases](https://github.com/Zeboul/poe2-chat-notifier/releases)
2. Edit the `config.ini` file to have the correct PoE2 installation directory
   (`POE2_DIRECTORY` option).
3. Double-click the `poe2-chat-notifier.exe` file. The first run might take
   longer since Windows may scan it for viruses.
    - If a "Windows protected your PC" window pops up, click "More info" and
      then "Run anyway".
    - A console window will stay open that displays a chat log. If it does not
      stay open, open the `poe2-chat-notifier.log` file to view error messages.

### From Source

These steps will download and install the program and a default `config.ini`
file. You may need to update the `POE_DIRECTORY` option in the `config.ini`
file before running the `poe2-chat-notifier` program.

```
pip3 install -U git+https://github.com/Zeboul/poe2-chat-notifier
curl -O --no-clobber https://raw.githubusercontent.com/Zeboul/poe2-chat-notifier/refs/heads/main/config.ini
poe2-chat-notifier
```

### Additional Configuration

The included `config.ini` configuration file explains each option. If the
configuration file is changed, the poe2-chat-notifier must be closed and
then run again for the changes to take effect.

## Known Issues and Limitations

- Messages you send in local/guild/global/trade chat can trigger notifications.
- Has only been tested on Windows 11.
- Notifications are only supported on Windows, on other operating systems chat
  messages will only be printed to the console.

## For Developers

```
git clone https://github.com/Zeboul/poe2-chat-notifier
cd poe2-chat-notifier
pip3 install -e .
```

To package a release:

```
python package.py RELEASE_VERSION
```

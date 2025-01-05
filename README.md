Path of Exile 2 chat notifier tool.

Release downloads: [https://github.com/Zeboul/poe2-chat-notifier/releases](https://github.com/Zeboul/poe2-chat-notifier/releases)

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

1. Extract the release zip file.
2. Edit the `config.ini` file to have the correct PoE2 installation directory
   (`POE2_DIRECTORY` option).
3. Double-click the `poe2-chat-notifier.exe` file. The first run might take
   longer since Windows may scan it for viruses.
    - A console window will stay open that displays a chat log. If it does not
      stay open, open the `poe2-chat-notifier.log` file to view error messages.

The included `config.ini` configuration file explains each option. If the
configuration file is changed, the poe2-chat-notifier must be closed and
then run again for the changes to take effect.

## Known Issues and Limitations

- Messages you send in local/guild/global/trade chat can trigger notifications.
- Has only been tested on Windows 11.
- Notifications are only supported on Windows, on other operating systems chat
  messages will only be printed to the console.

# Dependencies 
Websockets, discord.py

## Install in python

```shell
py -3 -m pip install -U discord.py websocket-client
```

# Instructions:
Run gosumemory (https://github.com/l3lackShark/gosumemory)

Run this discord bot script - python client.py


# Options located in client.py

PING_USERS: comma separated list of user ids to notify (can be empty)

BOT_CHANNEL: channel to notify

BOT_TOKEN: your discord bot token (from https://discord.com/developers/applications, your OAuth2 client secret)

SOCKET_ADDRESS: gosumemory socket (default is ws://localhost:24050/ws)

SR_THRESHOLD: only notify if map is higher than this sr

COMBO_THRESOLDS: comma separated list of map percentages to notify at

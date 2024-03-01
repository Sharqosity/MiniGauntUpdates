import websocket
import json
import discord
import threading
import asyncio
import time

PING_USERS = [95641408530026496, 159753928290992128]
BOT_CHANNEL = 405990872602247182
BOT_TOKEN = ''
SOCKET_ADDRESS = 'ws://localhost:24050/ws'
SR_THRESHOLD = 6.0
COMBO_THRESHOLDS = [0.25 , 0.7, 0.8, 0.85, 0.9, 0.95, 0.96, 0.97, 0.98, 0.99]

def reset_thresholds():
    global thresholdsHit
    thresholdsHit = [False] * len(COMBO_THRESHOLDS)

def on_message(wsapp, message):
    parsed = json.loads(message)
    playerState = parsed['menu']['state']
    if (playerState != 2):
        return
    
    sr = parsed['menu']['bm']['stats']['fullSR']
    if (sr < SR_THRESHOLD):
        return
    
    misses = parsed['gameplay']['hits']['0']
    sliderBreaks = parsed['gameplay']['hits']['sliderBreaks']
    if (misses > 0 or sliderBreaks > 0):
        return
    
    currentCombo = parsed['gameplay']['combo']['current']
    if(currentCombo == 0):
        reset_thresholds()

    maxCombo = parsed['menu']['bm']['stats']['maxCombo']
    playerName = parsed['gameplay']['name']
    mapName = parsed['menu']['bm']['metadata']['title']
    mods = parsed['menu']['mods']['str']
    modString = '' if mods == 'NM' else ' +' + mods
    for i, (threshold, hit) in enumerate(zip(COMBO_THRESHOLDS, thresholdsHit)):
        if (not hit and currentCombo / maxCombo > threshold):
            text = pingString + playerName + ' is FCing ' + mapName + modString + '!! Current combo: ' + str(currentCombo) + '/' + str(maxCombo)
            thresholdsHit[i] = True
            asyncio.run_coroutine_threadsafe(send(text), client.loop)
    
    
thresholdsHit = []
pingString = '<@' + '> <@'.join(map(str, PING_USERS)) + '>, ' if len(PING_USERS) > 0 else ''
reset_thresholds()
wsapp = websocket.WebSocketApp(SOCKET_ADDRESS, on_message=on_message)

intents = discord.Intents.default()
intents.message_content = True
channel = None
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    global channel
    channel = client.get_channel(BOT_CHANNEL)
    print('Logged in')

async def send(message):
    print(message)
    await channel.send(message)

socketThread = threading.Thread(target=wsapp.run_forever, args=())
discordThread = threading.Thread(target=client.run, args=(BOT_TOKEN,))

discordThread.start()
time.sleep(5)
print('Starting websocket')
socketThread.start()

while True:
    pass
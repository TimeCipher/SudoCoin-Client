import asyncio
import websockets
import time
import json
import base64
from threading import Thread

MultiThread = False
Mining = True

if MultiThread == True:
    AmountOfPasswords = int(input('Number of threads: '))

JsonAuthList = []

def AddAuth():
    Auth = input('Password: ')
    Auth64 = base64.b64encode(Auth.encode()).decode()
    JsonAuth = json.dumps(['auth', {'password': Auth64}])
    return JsonAuth

JsonAuthList.append(AddAuth())

async def mine(Pos):
    global JsonAuth
    #uri = "ws://localhost:8765"
    uri = 'ws://188.165.82.203:90'
    async with websockets.connect(uri) as websocket:

        await websocket.send(JsonAuthList[Pos])
        print(f"> {JsonAuthList[Pos]}")

        reply = json.loads(await websocket.recv())
        print(f'< {reply}')

        mineReq = json.dumps(['mine'])
        await websocket.send(mineReq)
        print(f"> {mineReq}")

        reply = json.loads(await websocket.recv())
        print(f'< {reply}')

ListPos = 0
while Mining == True: 
    if MultiThread == True:
        ListPos = ListPos + 1  
        Thread(target = asyncio.get_event_loop().run_until_complete(mine(ListPos))).start()
        if ListPos == AmountOfPasswords:
            ListPos = 0
            time.sleep(7)
    else:
        asyncio.get_event_loop().run_until_complete(mine(0))
        time.sleep(7)

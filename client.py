import asyncio
import websockets
import time
import json
import base64
from threading import Thread

uri = 'ws://188.165.82.203:90'
SOCKET = websockets.connect(uri)

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

async def AuthFunc(Pos):
    async with SOCKET as websocket:
        await websocket.send(JsonAuthList[Pos])
        print(f"> {JsonAuthList[Pos]}")

        reply = json.loads(await websocket.recv())
        print(f'< {reply}')

async def mine():
    async with SOCKET as websocket:

        mineReq = json.dumps(['mine'])
        await websocket.send(mineReq)
        print(f"> {mineReq}")

        reply = json.loads(await websocket.recv())
        print(f'< {reply}')

if MultiThread == False:
    asyncio.get_event_loop().run_until_complete(AuthFunc(0))

ListPos = 0
while Mining == True: 
    if MultiThread == True:
        Thread(target = asyncio.get_event_loop().run_until_complete(AuthFunc(ListPos))).start()
        ListPos = ListPos + 1  
        Thread(target = asyncio.get_event_loop().run_until_complete(mine())).start()
        if ListPos == AmountOfPasswords:
            ListPos = 0
            time.sleep(7)
    else:
        asyncio.get_event_loop().run_until_complete(mine())
        time.sleep(7)

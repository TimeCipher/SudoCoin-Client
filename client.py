import asyncio
import websockets
import time
import json
import base64

AuthList = ['auth']
Auth = input('Password: ')
Auth64 = base64.b64encode(Auth.encode())
AuthList.append(Auth64.decode())

JsonAuth = json.dumps(AuthList)

Mining = True

async def mine():
    global JsonAuth
    #uri = "ws://localhost:8765"
    uri = 'ws://188.165.82.203:90'
    async with websockets.connect(uri) as websocket:

        await websocket.send(JsonAuth)
        print(f"> {JsonAuth}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

'''
while Mining == True:   
    asyncio.get_event_loop().run_until_complete(mine())
    time.sleep(5)

'''
asyncio.get_event_loop().run_until_complete(mine())
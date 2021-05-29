import asyncio
import websockets
import time
import json
import base64
from threading import Thread

Mining = True
Transfer = False

AUTHORISED = False
PrintAuth = True
PrintAuth2 = False

Account = input('Password: ')
ExtraAcc = False
Account2 = None
ExtraAcc2 = False
Account3 = None

if ExtraAcc == True:
    Account2 = input('Second Password: ')
    if ExtraAcc2 == True:
        Account3 = input('Third Password: ')

async def AuthMine(Auth):
    global AUTHORISED
    global PrintAuth
    global PrintAuth2
    AUTHORISED = False
    uri = 'ws://188.165.82.203:90'
    async with websockets.connect(uri) as websocket:
        if AUTHORISED == False:
            Auth64 = base64.b64encode(Auth.encode()).decode()
            JsonAuth = json.dumps(['auth', {'password': Auth64}])

            await websocket.send(JsonAuth)
            reply = json.loads(await websocket.recv())

            if PrintAuth == True:
                print(f"> {JsonAuth}")
                print(f'< {reply}')
                PrintAuth = False

            AUTHORISED = True


        async def Mine():
            global PrintAuth2

            mineReq = json.dumps(["mine"])
            await websocket.send(mineReq)
            reply = json.loads(await websocket.recv())

            if PrintAuth2 == True:
                print(f"> {mineReq}")
                print(f'< {reply}')
        
        time.sleep(5.1)
        await Mine()
        time.sleep(5.1)
        await Mine()

async def AuthTransfer(Auth):
    uri = 'ws://188.165.82.203:90'
    async with websockets.connect(uri) as websocket:
        Auth64 = base64.b64encode(Auth.encode()).decode()
        JsonAuth = json.dumps(['auth', {'password': Auth64}])

        await websocket.send(JsonAuth)
        reply = json.loads(await websocket.recv())

        print(f"> {JsonAuth}")
        print(f'< {reply}')

        async def Tranfer():
            SendAmount = float(input('Amount to send: '))
            SendUser = int(input('User to send to: '))

            TransferReq = json.dumps(['transfer', {'amount': SendAmount, 'to': SendUser }])
            await websocket.send(TransferReq)
            print(f"> {TransferReq}")
   
        await Tranfer()

if Transfer == True:
    asyncio.get_event_loop().run_until_complete(AuthTransfer(Account))

while Mining == True:
    if ExtraAcc == True:
        Thread(target=asyncio.get_event_loop().run_until_complete(AuthMine(Account))).start()
        Thread(target=asyncio.get_event_loop().run_until_complete(AuthMine(Account2))).start()
        if ExtraAcc2 == True:
            Thread(target=asyncio.get_event_loop().run_until_complete(AuthMine(Account3))).start()
    else:     
        asyncio.get_event_loop().run_until_complete(AuthMine(Account))
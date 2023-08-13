import asyncio
import time
from backend.draft.RunDraft import rundraft_webapp

LOCK = False

async def listen():
    while True:
        with open("backend/events/data/messages.txt", "r") as f:
            line = f.readline()
        if line == "":
            time.sleep(.5)
        elif "RunDraft" in line.split():
            print("Removing instructions...")
            with open("backend/events/data/messages.txt", "w") as f2:
                f2.write("")
            print("Running...")
            values = line.split()
            rundraft_webapp(values[1], int(values[2]))
            

async def write(message_type, message_data):
    global LOCK
    if LOCK != True:
        LOCK = True
        with open("backend/events/data/messages.txt", "a") as f:
            message_data = [str(data) for data in message_data]
            string = message_type + " " + " ".join(message_data)
            f.write(string)
            print("SENT!")
        LOCK = False
        return
    await asyncio.sleep(1)
    asyncio.run(write(message_type, message_data))


if __name__ == "__main__":
    asyncio.run(listen())
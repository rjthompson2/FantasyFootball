import asyncio
import time
from multiprocessing import Process, Queue
from backend.draft.RunDraft import rundraft_webapp

LOCK = False
WORKERS = []

class Worker(Process):
    def __init__(self, queue):
        super(Worker, self).__init__()
        self.queue = queue

    def run(self, function, *args):
        function(args)


async def listen():
    global LOCK
    while True:
        lines = []
        
        while LOCK:
            await asyncio.sleep()

        with open("backend/events/data/messages.txt", "r") as f:
            lines.append(f.read())
        
        if lines != [] and lines != [""]:
            print(lines)
            LOCK = True
            print("Removing instructions...")
            with open("backend/events/data/messages.txt", "w") as f2:
                f2.write("")

            LOCK = False

            for line in lines:
                if "RunDraft" in line.split():
                    print("Running...")
                    values = line.split()
                    rundraft_webapp(values[1], int(values[2]))
            

async def write(message_type, message_data):
    global LOCK
    if LOCK != True:
        LOCK = True
        with open("backend/events/data/messages.txt", "a") as f:
            message_data = [str(data) for data in message_data]
            string = message_type + " " + " ".join(message_data) + "\n"
            f.write(string)
            print("SENT!")
        LOCK = False
        return
    await asyncio.sleep(1)
    asyncio.run(write(message_type, message_data))


if __name__ == "__main__":
    asyncio.run(listen())
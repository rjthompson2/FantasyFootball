import socket
import json
import re
from backend.data_collection.utils import get_season_year
from backend.data_collection.utils import clean_name_str
from backend.utils import find_in_data_folder
import pandas as pd

eliminated = []

def receiver():
    year = get_season_year()
    ip = "localhost"
    port = 8089
    buffer = 2000

    socket_server = socket.socket()
    socket_server.bind((ip, port))
    socket_server.listen()

    try:
        print("Server listening...")
        while True:
            connection, address = socket_server.accept()
            data = ""

            message = connection.recv(buffer).decode(encoding='utf-8')
            data += message
            while len(data) > 0 and data[-1] != "" and data[-1] != "}" and data[-1] != "\n":
                message = connection.recv(buffer).decode(encoding='utf-8')
                data += message
            data = re.findall("{.*", data)
            if data != "" and data != [] and data != None:
                data = json.loads(data[0])
                players = data["allDraftedPlayers"]
                path = find_in_data_folder(f"draft_order_{year}_copy.csv")
                df = pd.read_csv(path)
                for player in players:
                    if player not in eliminated and df['PLAYER'].isin([clean_name_str(player)]).any():
                        # Need a list of all player frist name and team abbreviated to convert to full name
                        df.drop(df[df['PLAYER'] == player].index, inplace=True)
                        eliminated.append(player)

                df.to_csv(
                    find_in_data_folder(f"draft_order_{year}_copy.csv"),
                    header=True,
                    index=False,
                )
        socket_server.close()
    except KeyboardInterrupt:
        socket_server.close()


if __name__ == "__main__":
    receiver()
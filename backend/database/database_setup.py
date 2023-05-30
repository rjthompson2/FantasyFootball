import psycopg2
from backend.database import database

cursor, connection = database.connect()
commands = (
    """
        CREATE TABLE players (
            player_id SERIAL PRIMARY KEY,
            player_name VARCHAR(225) NOT NULL,
            position VARCHAR(225) NOT NULL,
            team VARCHAR (225),
            is_playing BOOLEAN NOT NULL,
            date TIMESTAMP NOT NULL
        )
    """,
    """
        CREATE TABLE fpts (
            player_id INT PRIMARY KEY,
            date TIMESTAMP NOT NULL,
            projected_fpts FLOAT NOT NULL,
            ceiling FLOAT NOT NULL,
            floor FLOAT NOT NULL,
            std FLOAT NOT NULL,
            FOREIGN KEY (player_id)
            REFERENCES players (player_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        )
    """,
    """
        CREATE TABLE ecr (
            player_id INT PRIMARY KEY,
            date TIMESTAMP NOT NULL,
            ecr INT NOT NULL,
            FOREIGN KEY (player_id)
            REFERENCES players (player_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        )
    """,
    """
        CREATE TABLE vor (
            player_id INT PRIMARY KEY,
            date TIMESTAMP NOT NULL,
            vor FLOAT NOT NULL,
            value_rank INT NOT NULL,
            FOREIGN KEY (player_id)
            REFERENCES players (player_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        )
    """,
    """
        CREATE TABLE adp (
            player_id INT PRIMARY KEY,
            date TIMESTAMP NOT NULL,
            avg FLOAT NOT NULL,
            adp_rank INT NOT NULL,
            FOREIGN KEY (player_id)
            REFERENCES players (player_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        )
    """,
    """
        CREATE TABLE injury (
            player_id INT PRIMARY KEY,
            date TIMESTAMP NOT NULL,
            career_injuries INT NOT NULL,
            injury_liklihood FLOAT NOT NULL,
            proj_games_missed FLOAT NOT NULL,
            injury_per_game FLOAT NOT NULL,
            durability INT NOT NULL,
            FOREIGN KEY (player_id)
            REFERENCES players (player_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        )
    """,
    """
        CREATE TABLE weekly (
            player_id INT PRIMARY KEY,
            date TIMESTAMP NOT NULL,
            stat_name VARCHAR(225) NOT NULL,
            stat_value FLOAT NOT NULL,
            FOREIGN KEY (player_id)
            REFERENCES players (player_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        )
    """
    )

for command in commands:
    cursor.execute(command)

connection.commit()

database.close(cursor, connection)
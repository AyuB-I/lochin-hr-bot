import aiosqlite
import logging
from aiogram import types


class DBCommands:
    def __init__(self, filename):
        self.filename = filename
        self.connection = None

    async def get_connection(self):
        """  Getting connection or creating if not exists  """

        if self.connection is None:
            self.connection = await aiosqlite.connect(self.filename)
        return self.connection

    async def close_db(self):
        """  Closing connection to database  """

        if self.connection is not None:
            await self.connection.close()
            self.connection = None
            logging.info("DATABASE HAS DISCONNECTED!")

    async def create_table(self):
        """  Creating database tables with name 'users', 'form'  """

        connection = await self.get_connection()
        cursor = await connection.cursor()

        await cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE, 
        username VARCHAR, 
        full_name VARCHAR, 
        registration_date DATETIME NOT NULL DEFAULT ( (DATETIME('now')) )
        )""")
        await cursor.execute("""CREATE TABLE IF NOT EXISTS forms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    username VARCHAR,
                    full_name VARCHAR NOT NULL,
                    birthday DATETIME NOT NULL,
                    phone_number INTEGER NOT NULL,
                    profession VARCHAR NOT NULL,
                    address VARCHAR NOT NULL,
                    nation VARCHAR NOT NULL,
                    education VARCHAR NOT NULL,
                    marital_status VARCHAR NOT NULL,
                    business_trip VARCHAR NOT NULL,
                    military VARCHAR NOT NULL,
                    criminal VARCHAR NOT NULL,
                    driver_license VARCHAR NOT NULL,
                    personal_cal VARCHAR NOT NULL,
                    ru_lang VARCHAR NOT NULL,
                    eng_lang VARCHAR NOT NULL,
                    chi_lang VARCHAR NOT NULL,
                    other_lang VARCHAR NOT NULL, 
                    word_app VARCHAR NOT NULL,
                    excel_app VARCHAR NOT NULL,
                    onec_app VARCHAR NOT NULL,
                    other_app VARCHAR NOT NULL,
                    origin VARCHAR NOT NULL,
                    date DATETIME NOT NULL DEFAULT ( (DATETIME('now')) )
                    )""")
        await connection.commit()

    async def get_user(self, user_id):
        """  Getting user by id  """

        connection = await self.get_connection()
        cursor = await connection.cursor()
        await cursor.execute(sql="SELECT * FROM users WHERE user_id = ?", parameters=(user_id,))
        result = await cursor.fetchone()
        return result

    async def register_user(self):
        """  Registration user in database  """

        connection = await self.get_connection()
        cursor = await connection.cursor()
        current_user = types.User.get_current()
        user = await self.get_user(current_user.id)
        if user:  # Checking if the user has already registered
            return user

        query = await cursor.execute("""INSERT INTO users (user_id, username, full_name)
                                        VALUES (?, ?, ?)""",
                                     (current_user.id, current_user.username, current_user.full_name,))
        await connection.commit()
        return query

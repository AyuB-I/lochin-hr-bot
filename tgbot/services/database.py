import aiosqlite
import logging
import itertools
from aiogram import types


class DBCommands:
    def __init__(self, filename):
        self.filename = filename
        self.connection = None

    async def get_connection(self):
        """  Getting connection to database or creating if not exists  """

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
        """  Creating database tables with names 'users', 'form'  """

        connection = await self.get_connection()
        cursor = await connection.cursor()

        await cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY, 
        username VARCHAR, 
        full_name VARCHAR, 
        forms JSON DEFAULT ('[]'),
        registration_date DATETIME NOT NULL DEFAULT ( (DATETIME('now')) )
        )""")
        await cursor.execute("""CREATE TABLE IF NOT EXISTS forms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
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
                    personal_car VARCHAR NOT NULL,
                    ru_lang VARCHAR NOT NULL,
                    eng_lang VARCHAR NOT NULL,
                    chi_lang VARCHAR NOT NULL,
                    other_lang VARCHAR NOT NULL, 
                    word_app VARCHAR NOT NULL,
                    excel_app VARCHAR NOT NULL,
                    onec_app VARCHAR NOT NULL,
                    other_app VARCHAR NOT NULL,
                    origin VARCHAR NOT NULL,
                    photo_id TEXT NOT NULL,
                    date DATETIME NOT NULL DEFAULT ( (DATETIME('now')) ),
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE NO ACTION
                    )""")
        await connection.commit()

    async def get_user(self, user_id):
        """  Getting user by id from database  """

        connection = await self.get_connection()
        cursor = await connection.cursor()
        await cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
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

    async def add_form(self, full_name, birthday, phone_number, profession, address, nation, education, marital_status,
                       business_trip, military, criminal, driver_license, personal_car, ru_lang, eng_lang, chi_lang,
                       other_lang, word_app, excel_app, onec_app, other_app, origin, photo_id):
        """  Adding a new form to database  """

        connection = await self.get_connection()
        cursor = await connection.cursor()
        current_user = types.User.get_current()

        await cursor.execute("""INSERT INTO forms (user_id, username, full_name, birthday, phone_number, profession,
                             address, nation, education, marital_status, business_trip, military, criminal,
                             driver_license, personal_car, ru_lang, eng_lang, chi_lang, other_lang, word_app, excel_app,
                             onec_app, other_app, origin, photo_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                             ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                             (current_user.id, f"@{current_user.username}", full_name, birthday, phone_number,
                              profession, address, nation, education, marital_status, business_trip, military, criminal,
                              driver_license, personal_car, ru_lang, eng_lang, chi_lang, other_lang, word_app,
                              excel_app, onec_app, other_app, origin, photo_id))
        query = await cursor.execute("""SELECT id FROM forms WHERE user_id IN (SELECT user_id FROM users 
                                     WHERE user_id = ?)""", (current_user.id,))
        row_list = list(itertools.chain.from_iterable(await query.fetchall()))
        form_id = row_list[-1]
        logging.info(row_list)
        logging.info(form_id)

        await cursor.execute("UPDATE users SET forms = json_insert(forms, '$[#]', ?)", (form_id,))
        await connection.commit()

    async def get_all_forms(self):
        """  Getting all forms' ids and names from database and sending as a dict (id: name)  """

        connection = await self.get_connection()
        cursor = await connection.cursor()

        await cursor.execute("SELECT id FROM forms")
        ids = await cursor.fetchall()
        id_list = [i[0] for i in ids]
        await cursor.execute("SELECT full_name FROM forms")
        names = await cursor.fetchall()
        name_list = [n[0] for n in names]
        data_dict = dict(zip(id_list, name_list))
        return data_dict

    async def get_form(self, id):
        """  Getting a form from id  """

        connection = await self.get_connection()
        cursor = await connection.cursor()

        await cursor.execute("SELECT * FROM forms WHERE id = ?", (id,))
        data = await cursor.fetchone()
        form = {"id": data[0], "user_id": data[1], "username": data[2], "full_name": data[3], "birthday": data[4],
                "phone_number": data[5], "profession": data[6], "address": data[7], "nation": data[8],
                "education": data[9], "marital_status": data[10], "business_trip": data[11], "military": data[12],
                "criminal": data[13], "driver_license": data[14], "personal_car": data[15], "ru_lang": data[16],
                "eng_lang": data[17], "chi_lang": data[18], "other_lang": data[19], "word_app": data[20],
                "excel_app": data[21], "onec_app": data[22], "other_app": data[23], "origin": data[24],
                "photo_id": data[25], "date": data[26]}
        return form

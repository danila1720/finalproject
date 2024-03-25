import logging

import sqlite3

from strings import DB_NAME, DB_TABLE_USERS_NAME, LOGS_PATH

logging.basicConfig(filename=LOGS_PATH, level=logging.DEBUG, format="%(asctime)s %(message)s", filemode="a")


def create_db(database_name=DB_NAME):
    db_path = f'{database_name}'
    connection = sqlite3.connect(db_path)
    connection.close()

    logging.info(f"База данных успешно создана")


def execute_query(sql_query, data=None, db_path=f'{DB_NAME}'):
    logging.info(f"DATABASE: Execute query: {sql_query}")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    if data:
        cursor.execute(sql_query, data)
    else:
        cursor.execute(sql_query)

    connection.commit()
    connection.close()


def execute_selection_query(sql_query, data=None, db_path=f'{DB_NAME}'):
    logging.info(f"DATABASE: Execute query: {sql_query}")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    if data:
        cursor.execute(sql_query, data)
    else:
        cursor.execute(sql_query)
    rows = cursor.fetchall()
    connection.close()
    return rows


def create_table(table_name):
    sql_query = f'''CREATE TABLE IF NOT EXISTS {table_name} ''' \
                f'''(id INTEGER PRIMARY KEY, ''' \
                f'''user_id INTEGER, ''' \
                f'''person TEXT, ''' \
                f'''environment TEXT, ''' \
                f'''genre TEXT, ''' \
                f'''mode TEXT, ''' \
                f'''script TEXT,''' \
                f'''session INTEGER,''' \
                f'''content TEXT)'''
    execute_query(sql_query)


def insert_row(values):
    columns = '(user_id, person, environment, genre, mode, script, session, content)'
    sql_query = f'INSERT INTO {DB_TABLE_USERS_NAME} {columns} VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
    execute_query(sql_query, values)


def is_value_in_table(table_name, column_name, value):
    sql_query = f'SELECT * FROM {table_name} WHERE {column_name} = {value} LIMIT 1'
    rows = execute_selection_query(sql_query)
    return len(rows) > 0


def delete_user(user_id):
    if is_value_in_table(DB_TABLE_USERS_NAME, 'user_id', user_id):
        sql_query = f'DELETE FROM {DB_TABLE_USERS_NAME} WHERE user_id = ?'
        execute_query(sql_query, [user_id])


def update_row_value(user_id, column_name, new_value):
    if is_value_in_table(table_name=DB_TABLE_USERS_NAME, column_name='user_id', value=user_id):
        sql_query = f'UPDATE {DB_TABLE_USERS_NAME} SET {column_name} = "{new_value}" WHERE user_id = {user_id}'
        execute_query(sql_query)
    else:
        logging.info(f"DATABASE: Пользователь с id = {user_id} не найден")
        print("Такого пользователя нет :(")


def prepare_db(clean_if_exists=False):
    create_db()
    create_table(DB_TABLE_USERS_NAME)
    if clean_if_exists:
        clean_table(DB_TABLE_USERS_NAME)


def clean_table(table_name):
    execute_query(f'DELETE FROM {table_name}')


def get_data_for_user(user_id):
    if is_value_in_table(DB_TABLE_USERS_NAME, 'user_id', user_id):
        sql_query = f'SELECT user_id, person, environment, genre, mode, script ' \
                    f'FROM {DB_TABLE_USERS_NAME} where user_id = ? limit 1'
        row = execute_selection_query(sql_query, [user_id])[0]
        result = {'person': row[1], 'environment': row[2], 'genre': row[3], 'mode': row[4], 'script': row[5]}
        return result
    else:
        logging.info(f"DATABASE: Пользователь с id = {user_id} не найден")
        print("Такого пользователя нет :(")
        return {'person': "", 'environment': "", 'genre': "", 'script': ""}

import sqlalchemy
import psycopg2

user = 'myfinder'
password = 'network'

#  Создаем engine
db = f'postgresql://{user}:{password}@localhost:5432/vk_candidate'
engine = sqlalchemy.create_engine(db)
try:
    connection = engine.connect()
#  Устанавливаем соединение с БД
except Exception as error:
    print('Ошибка при работе с PostgreSQL. Возможен повтор данных', {error})


def insert_user(user_id: int):
    # Функция записывает данные пользователя в таблицу пользователей
    connection.execute(f"INSERT INTO vk_users (user_id) VALUES({user_id})")

def insert_candidate(owner_id: int, kandidat_info: dict):
    # Функция записывает кандидита в таблицу кандидатов, получает первичные ключи из таблиц пользователя
    # и кандидата, вносит промежуточную запись для связывания этих таблиц в таблицу vk_users_vk_candidate
    # :param owner_id:
    # :param kandidat_info:
    # :return:

    info = f"""INSERT INTO vk_candidate (candidate_id, first_name, last_name, bdate, city, relation, url_account, url_photo1, url_photo2, 
    url_photo3, bloked) 
    VALUES({candidate_info.get('candidate_id')}, '{candidate_info.get('first_name')}', '{candidate_info.get('last_name')}', 
    '{candidate_info.get('bdate')}','{candidate_info.get('city')}', '{candidate_info.get('relation')}', '{candidate_info.get('url_account')}', '{candidate_info.get('url_photo1')}', 
    '{candidate_info.get('url_photo2')}', '{candidate_info.get('url_photo3')}', '{candidate_info.get('bloсked')}');"""
    connection.execute(info)
    id_user = connection.execute(f"""SELECT id from vk_users WHERE user_id = {owner_id}""").fetchone()
    id_candidate = connection.execute(f"""SELECT id from vk_candidate WHERE candidate_id = {candidate_info.get('candidate_id')}""").fetchone()
    insert_vk_users_vk_candidate(*id_user, *id_candidate)


def insert_ban(any_id: int, bloked: str):
    # Функция записывает заблокированных кандидатов в таблицу кандидатов с отметкой блокировки
    # :param any_id:
    # :param bloked:
    # :return:

    connection.execute(f"""INSERT INTO vk_candidate (candidate_id, blocked) VALUES({any_id}, '{blocked}')""")


def insert_vk_users_vk_candidate(id_user: int, id_candidate: int):
    # Функция вносит промежуточную запись для связывания таблиц в таблицу vk_users_vk_candidate
    # :param id_user:
    # :param id_kandidat:
    # :return:

    connection.execute(f"""INSERT INTO vk_users_vk_candidate (id_user, id_candidate) VALUES({id_user}, {id_candidate})""")


def read_all(table_name: str, column: str) -> tuple:
    # Функция для отладки, чтение данных из таблицы
    # :param table_name:
    # :param column:
    #:return:
    return connection.execute(f"SELECT {column} FROM {table_name}").fetchall()


def get_candidate_id_for_user_id(user_id, candidate_id) -> tuple:
    # Функция проверяет на наличие записи кандидата для данного пользователя
    # :param user_id:
    # :param kandidat_id:
    # :return:

    sel = connection.execute(f"""SELECT candidate_id FROM vk_candidate
    JOIN vk_users_vk_candidate ON vk_candidate.id=vk_users_vk_candidate.id_candidate
    JOIN vk_users ON vk_users_vk_candidate.id_user = vk_users.id
    WHERE (vk_users.user_id = {user_id}) AND (vk_candidate.candidate_id = {candidate_id})""").fetchall()
    return(sel)


def if_user_inlist(user_id: int) -> tuple:
    # Проверка существования пользователя в таблице для избежания повторов его id vk
    # :param user_id:
    # :return:

    sel = connection.execute(f"""SELECT user_id FROM vk_users WHERE user_id = {user_id}""").fetchall()
    return sel


def if_blocked(candidate_id: int) -> tuple:
    # Проверка содержимого поля bloсked на заполение. Если не пустое - акканут заблокирован
    # :param user_id:
    # :return:
    con = connection.execute(f""" SELECT bloked FROM vk_candidate WHERE candidate_id = {candidate_id} """).fetchone()
    return con



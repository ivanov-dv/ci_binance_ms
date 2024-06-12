import logging
import psycopg2


def try_connect(func):
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            return data
        except Exception as _ex:
            logging.error(f"Ошибка БД. {func.__qualname__} {_ex}")
            return _ex
    return wrapper


class PostgresDB:
    def __init__(self, username, password, host, port, database, autocommit=True):
        self.connection = psycopg2.connect(
            user=username,
            password=password,
            host=host,
            port=port,
            database=database
        )
        self.connection.autocommit = autocommit
        self.cursor = self.connection.cursor()

    @try_connect
    def create_tables(self):
        with self.cursor as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users 
                (
                    id_telegram bigint NOT NULL,
                    name text,
                    surname text,
                    username text,
                    ban boolean DEFAULT FALSE,
                    date_registration date DEFAULT CURRENT_DATE,
                    date_update date DEFAULT CURRENT_DATE,
                    CONSTRAINT users_pkey PRIMARY KEY (id_telegram)
                );
                CREATE TABLE IF NOT EXISTS monitoring
                (
                    id bigint NOT NULL,
                    id_telegram bigint NOT NULL,
                    symbol text NOT NULL,
                    CONSTRAINT monitoring_pkey PRIMARY KEY (id)
                );
            ''')

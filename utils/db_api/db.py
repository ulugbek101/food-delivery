import pymysql


class Database:
    def __init__(self, db_name, db_password, db_user, db_port, db_host):
        self.db_name = db_name
        self.db_password = db_password
        self.db_user = db_user
        self.db_port = db_port
        self.db_host = db_host

    @property
    def db(self):
        return pymysql.connect(
            database=self.db_name,
            password=self.db_password,
            user=self.db_user,
            host=self.db_host,
            port=self.db_port,
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute(self,
                sql: str,
                params: tuple = None,
                commit: bool = False,
                fetchall: bool = False,
                fetchone: bool = False
                ):
        if not params:
            params = ()

        db = self.db
        cursor = db.cursor()
        cursor.execute(sql, params)
        data = None

        if commit:
            db.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        db.close()
        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f'{item} = %s' for item in parameters
        ])
        return sql, tuple(parameters.values())

    def create_users_table(self) -> None:
        """
        Creates Users table if not exists, user's telegram_id should be unique,
        otherwise it will not register user the second time in a database
        :return: None
        """

        sql = """
            CREATE TABLE IF NOT EXISTS users(
                id INT PRIMARY KEY AUTO_INCREMENT,
                fullname VARCHAR(200),
                phone_number VARCHAR(13),
                telegram_id VARCHAR(200) NOT NULL UNIQUE,
                language_code VARCHAR(2) NOT NULL DEFAULT 'uz',
                status VARCHAR(200) NOT NULL DEFAULT 'bronze',
                order_count INT DEFAULT 0    
            )
        """
        self.execute(sql, commit=True)

    def get_user_language(self, telegram_id: int) -> str:
        """
        Gets user's language code by telegram_id from users table
        :param telegram_id:
        :return: str
        """

        sql = """
            SELECT language_code FROM users WHERE telegram_id = %s
        """
        return self.execute(sql, (telegram_id,), fetchone=True).language_code

    def get_user(self, telegram_id: int) -> dict | None:
        """
        Returns user data from users table by telegram_id
        or None if user is not presented
        :param telegram_id:
        :return: dict | None
        """

        sql = """
            SELECT * FROM users WHERE telegram_id = %s
        """
        return self.execute(sql, (telegram_id,), fetchone=True) or None

    def register_user(self, telegram_id: int, fullname: str, language_code):
        """
        Registers user in a system
        :param telegram_id: int
        :param fullname: str
        :param language_code: str
        :return:
        """

        sql = """
            INSERT INTO users (telegram_id, fullname, language_code) VALUES (%s, %s, %s)
        """
        self.execute(sql, (telegram_id, fullname, language_code), commit=True)

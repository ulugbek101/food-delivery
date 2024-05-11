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
                ) -> list | dict | None:
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
                order_count INT DEFAULT 0,
                last_visited_place VARCHAR(20)    
            )
        """
        self.execute(sql)

    def create_categories_table(self) -> None:
        """
        Creates categories table if not exists
        :return: None
        """
        sql = """
            CREATE TABLE IF NOT EXISTS categories(
                id INT PRIMARY KEY AUTO_INCREMENT,
                name_uz VARCHAR(200) NOT NULL UNIQUE,
                name_ru VARCHAR(200) NOT NULL UNIQUE,
                name_en VARCHAR(200) NOT NULL UNIQUE,
                photo VARCHAR(200) NOT NULL,
                has_subcategory INT NOT NULL DEFAULT 0
            )
        """
        self.execute(sql)

    def create_subcategories_table(self) -> None:
        """
        Creates subcategories table if not exists
        :return: None
        """

        sql = """
            CREATE TABLE IF NOT EXISTS subcategories(
                id INT PRIMARY KEY AUTO_INCREMENT,
                category_id INT NOT NULL,
                name_uz VARCHAR(200) NOT NULL UNIQUE,
                name_ru VARCHAR(200) NOT NULL UNIQUE,
                name_en VARCHAR(200) NOT NULL UNIQUE,
                photo VARCHAR(200) NOT NULL
            )
        """
        self.execute(sql)

    def create_products_table(self) -> None:
        """
        Creates products table if not exists
        :return: None
        """

        sql = """
            CREATE TABLE IF NOT EXISTS products(
                id INT PRIMARY KEY AUTO_INCREMENT,
                category_id INT NOT NULL,
                subcategory_id INT DEFAULT NULL,
                name_uz VARCHAR(200) NOT NULL UNIQUE,
                name_ru VARCHAR(200) NOT NULL UNIQUE,
                name_en VARCHAR(200) NOT NULL UNIQUE,
                desc_uz VARCHAR(200),
                desc_ru VARCHAR(200),
                desc_en VARCHAR(200),
                price DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
                photo VARCHAR(200)
            )
        """
        self.execute(sql)

    def get_user_language(self, telegram_id: int) -> str:
        """
        Gets user's language code by telegram_id from users table
        :param telegram_id: user's telegram id
        :return: str
        """

        sql = """
            SELECT language_code FROM users WHERE telegram_id = %s
        """
        return self.execute(sql, (telegram_id,), fetchone=True)['language_code']

    def get_user(self, telegram_id: int) -> dict | None:
        """
        Returns user data from users table by telegram_id
        or None if user is not presented
        :param telegram_id: user's telegram id
        :return: user: dict[str: any] or None
        """

        sql = """
            SELECT * FROM users WHERE telegram_id = %s
        """
        return self.execute(sql, (telegram_id,), fetchone=True) or None

    def get_categories(self) -> list:
        """
        Gets all categories from categories table
        :return:
        """

        sql = """
            SELECT * FROM categories
        """
        return self.execute(sql, fetchall=True)

    def get_subcategories(self, category_id: int) -> list:
        """
        Returns subcategories list by category id
        :param category_id:
        :return: tuple
        """

        sql = """
            SELECT * FROM subcategories WHERE category_id = %s
        """
        return self.execute(sql, (category_id,), fetchall=True)

    def get_product(self, product_id: int) -> dict:
        """
        Returns product information by product id
        :param product_id:
        :return: dict
        """

        sql = """
            SELECT * FROM products WHERE id = %s
        """
        return self.execute(sql, (product_id,), fetchone=True)

    def register_user(self, telegram_id: int, fullname: str, language_code: str) -> None:
        """
        Registers user in a system
        :param telegram_id: user's telegram id
        :param fullname: user's fullname
        :param language_code: user's language code
        :return: None
        """

        sql = """
            INSERT INTO users (telegram_id, fullname, language_code) VALUES (%s, %s, %s)
        """
        self.execute(sql, (telegram_id, fullname, language_code), commit=True)

    def update_language_code(self, telegram_id: int, lang: str) -> None:
        """
        Updates user's language code by telegram_id in users table
        :param telegram_id: user's telegram id
        :param lang: new language
        :return: None
        """

        sql = f"""
            UPDATE users SET language_code = %s WHERE telegram_id = %s
        """
        self.execute(sql, (lang, telegram_id), commit=True)

    def update_last_step(self, telegram_id: int, place: str) -> None:
        """
        Updates last visited path/place of a user so that on Back button click user can return to previous menu
        :param telegram_id: user's telegram id
        :param place: Last visited place identifier
        :return: None
        """

        sql = """
            UPDATE users SET last_visited_place = %s WHERE telegram_id = %s
        """
        self.execute(sql, (place, telegram_id), commit=True)

    def update_phone_number(self, telegram_id: int, phone_number: str) -> None:
        """
        Updates user's phone number
        :param telegram_id: user's telegram id
        :param phone_number: user's phone number
        :return: None
        """

        sql = """
            UPDATE users SET phone_number = %s WHERE telegram_id = %s
        """
        self.execute(sql, (phone_number, telegram_id), commit=True)

    def update_fullname(self, telegram_id: int, fullname: str) -> None:
        """
        Updates user's fullname in users table
        :param telegram_id: user's telegram id
        :param fullname: user's fullname
        :return: None
        """

        sql = """
            UPDATE users SET fullname = %s WHERE telegram_id = %s
        """
        self.execute(sql, (fullname, telegram_id), commit=True)

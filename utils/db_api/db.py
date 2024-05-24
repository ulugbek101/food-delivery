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
                has_subcategory INT NOT NULL DEFAULT 0,
                category_id INT DEFAULT NULL,
                belongs_to VARCHAR(200) NOT NULL
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

    def create_locations_table(self):
        """
        Create user saved locations
        :return: None
        """

        sql = """
            CREATE TABLE IF NOT EXISTS locations(
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                coordinates VARCHAR(200) NOT NULL,
                full_address VARCHAR(100) NOT NULL,
                
                CONSTRAINT unique_full_address_for_user UNIQUE(user_id, full_address)
            )
        """
        self.execute(sql)

    def create_cart_table(self) -> None:
        """
        Creates cart table if not exists
        :return: None
        """

        sql = """
            CREATE TABLE IF NOT EXISTS cart(
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                total_price DECIMAL(12, 2) DEFAULT 0.00,
                
                CONSTRAINT unique_product_for_user UNIQUE(user_id, product_id)
            )
        """
        self.execute(sql)

    def add_to_cart(self, user_id: int, product_id: int, quantity: int) -> None:
        """
        Adds product to user's cart
        :param user_id: user's id
        :param product_id: product's id
        :param quantity: product's quantity
        :return: None
        """

        sql = """
            INSERT INTO cart (user_id, product_id, quantity) 
            VALUES (%s, %s, %s)
        """
        self.execute(sql, (user_id, product_id, quantity), commit=True)
        self.update_cart_products_total_price(user_id, product_id, quantity)

    def update_cart_products_total_price(self, user_id: int, product_id: int, quantity: int) -> None:
        """
        Updates total price of user's cart for a specific product's row
        :param user_id: user's id
        :param product_id: product's id
        :param quantity: product's quantity
        :return: None
        """

        product_price = self.get_product(product_id).get('price')
        total_price = int(product_price) * int(quantity)

        sql = """
            UPDATE cart SET total_price = %s WHERE user_id = %s AND product_id = %s    
        """
        self.execute(sql, (total_price, user_id, product_id), commit=True)

    def update_cart_product_quantity(self, user_id: int, product_id: int, new_quantity: int) -> None:
        """
        Updates product's quantity in user's cart
        :param user_id: user's id
        :param product_id: product id
        :param new_quantity: product's new quantity
        :return: None
        """

        sql = """
            UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s
        """
        self.execute(sql, (new_quantity, user_id, product_id), commit=True)
        self.update_cart_products_total_price(user_id, product_id, new_quantity)

    def get_user_locations(self, user_id: int):
        """
        Returns user's saved locations list
        :param user_id: user's id
        :return: list
        """

        sql = """
            SELECT * FROM locations WHERE user_id = %s
        """
        return self.execute(sql, (user_id,), fetchall=True)

    def get_user_location(self, user_id: int, full_address: str) -> tuple:
        """
        Returns user selected location from database by full address
        :param user_id: user's id
        :param full_address: full address name of a location
        :return: tuple
        """

        sql = """
            SELECT coordinates from locations WHERE user_id = %s AND full_address = %s
        """
        return self.execute(sql, (user_id, full_address), fetchone=True).get('coordinates')

    def get_product_quantity(self, product_id: int, user_id: int) -> int:
        """
        Returns product's quantity
        :param product_id: product's id
        :param user_id: user's id
        :return: int
        """

        sql = """
            SELECT quantity FROM cart WHERE user_id = %s AND product_id = %s
        """
        quantity = self.execute(sql, (user_id, product_id), fetchone=True)
        return quantity.get('quantity')

    def get_cart_product(self, user_id: int, product_id: int) -> dict | None:
        """
        Returns cart product from user's cart or None empty set instead if product is not presented in user's cart
        :param user_id:
        :param product_id:
        :return: dict | None
        """

        sql = """
            SELECT * FROM cart WHERE user_id = %s AND product_id = %s
        """
        product = self.execute(sql, (user_id, product_id), fetchone=True)
        return product if product else None

    def get_users_cart_products(self, user_id: int) -> list:
        """
        Returns user's cart products
        :param user_id: user's id
        :return: list
        """

        sql = """
            SELECT * FROM cart WHERE user_id = %s
        """
        return self.execute(sql, (user_id,), fetchall=True)

    def get_users_cart_total_price(self, user_id: int) -> float:
        """
        Returns user's cart's total price
        :param user_id: user's id
        :return: float
        """

        sql = """
            SELECT SUM(total_price) as total_price FROM cart WHERE user_id = %s
        """
        return self.execute(sql, (user_id,), fetchone=True).get('total_price')

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

    def get_categories(self, target: str) -> list:
        """
        Gets all categories from categories table
        :param: target, whether you want foods or other categories
        :return: list of categories
        """

        sql = """
            SELECT * FROM categories WHERE category_id IS NULL AND belongs_to = %s
        """
        return self.execute(sql, (target,), fetchall=True)

    def get_subcategories(self, category_id: int) -> list:
        """
        Returns subcategories list by category id
        :param category_id:
        :return: tuple
        """

        sql = """
            SELECT * FROM categories WHERE category_id = %s
        """
        return self.execute(sql, (category_id,), fetchall=True)

    def get_products(self, category_id: int) -> list:
        """
        Returns products list from products table
        :param category_id:
        :return: products list
        """

        sql = """
            SELECT * FROM products WHERE category_id = %s
        """
        return self.execute(sql, (category_id,), fetchall=True)

    def get_category(self, category_id: int) -> dict:
        """
        Returns category object by category object
        :param category_id:
        :return: dict
        """

        sql = """
            SELECT * FROM categories WHERE id = %s
        """
        return self.execute(sql, (category_id,), fetchone=True)

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

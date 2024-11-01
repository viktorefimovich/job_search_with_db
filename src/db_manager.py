from typing import Any, Dict, List

import psycopg2
from psycopg2 import sql


class DBManager:
    """
    Класс для работы с базой данных PostgreSQL.
    """

    def __init__(self, db_name: str, params: dict):
        """
        Инициализация подключения к базе данных PostgreSQL.
        """

        self.__db_name = db_name
        self.__params = params
        self.conn = psycopg2.connect(dbname="postgres", **self.__params)
        self.conn.autocommit = True

    def create_database(self, db_name: str) -> None:
        """
        Метод для создания базы данных.
        :param db_name: Название базы данных, которую нужно создать.
        """
        try:
            # Подключение к базе данных по умолчанию, чтобы создать новую БД
            conn = psycopg2.connect(dbname="postgres", **self.__params)

            conn.autocommit = True
            cur = self.conn.cursor()

            # Проверяем, существует ли база данных
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            if cur.fetchone() is None:
                # Если база данных не существует, создаем её
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                print(f"База данных {db_name} успешно создана.")
            else:
                print(f"База данных {db_name} уже существует.")

            cur.close()
            conn.close()

        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")

    def create_tables(self) -> None:
        """
        Создает таблицы для компаний и вакансий.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS companies (
                    company_id VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(255)
                )
            """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    company_id VARCHAR(255),
                    title VARCHAR(255),
                    salary INTEGER,
                    url TEXT,
                    FOREIGN KEY (company_id) REFERENCES companies (company_id)
                )
            """
            )
        print("Таблицы созданы.")

    def save_company_data(self, companies_data: List[Dict[str, Any]]) -> None:
        """
        Сохраняет данные о компаниях и их вакансиях в базу данных.

        :param companies_data: Список с данными о компаниях и их вакансиях.
        """
        with self.conn.cursor() as cur:
            for company in companies_data:
                cur.execute(
                    """
                    INSERT INTO companies (company_id, name)
                    VALUES (%s, %s)
                    ON CONFLICT (company_id) DO NOTHING
                """,
                    (company["company_id"], company["name"]),
                )

                for vacancy in company["vacancies"]:
                    cur.execute(
                        """
                        INSERT INTO vacancies (company_id, title, salary, url)
                        VALUES (%s, %s, %s, %s)
                    """,
                        (
                            company["company_id"],
                            vacancy["name"],
                            vacancy["salary"],
                            vacancy["url"],
                        ),
                    )
        print("Данные сохранены в БД.")

    def get_companies_and_vacancies_count(self) -> Any:
        """
        Получает список компаний и количество вакансий у каждой.

        :return: Список словарей с данными о компаниях и количестве вакансий.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.name, COUNT(vacancies.vacancy_id)
                FROM companies
                JOIN vacancies ON companies.company_id = vacancies.company_id
                GROUP BY companies.name
            """
            )
            return cur.fetchall()

    def get_all_vacancies(self) -> Any:
        """
        Получает список всех вакансий с названием компании, вакансии и зарплатой.

        :return: Список вакансий.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.company_id
            """
            )
            return cur.fetchall()

    def get_avg_salary(self) -> Any:
        """
        Получает среднюю зарплату по вакансиям.

        :return: Средняя зарплата.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL
            """
            )
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> Any:
        """
        Получает вакансии с зарплатой выше средней.

        :return: Список вакансий с зарплатой выше средней.
        """
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.name, vacancies.title, vacancies.salary
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.company_id
                WHERE vacancies.salary > %s
            """,
                (avg_salary,),
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> Any:
        """
        Получает вакансии, в названии которых содержится ключевое слово.

        :param keyword: Ключевое слово.
        :return: Список вакансий с ключевым словом.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.company_id
                WHERE vacancies.title ILIKE %s
            """,
                (f"%{keyword}%",),
            )
            return cur.fetchall()

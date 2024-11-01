from pathlib import Path

from src.config import config
from src.db_manager import DBManager
from src.hh_api import APIClient
from src.utils import read_json

ROOTPATH = Path(__file__).resolve().parent.parent


def main() -> None:
    db_params = config()
    db_name = "hh_vacancies"
    db_manager = DBManager(db_name, db_params)

    # Создаем базу данных
    db_manager.create_database(db_name)

    # Создаем таблицы в базе данных
    db_manager.create_tables()

    api_client = APIClient()
    companies_file = str(Path(ROOTPATH, "data/companies.json"))
    companies = read_json(companies_file)
    companies_list_id = [company["id"] for company in companies]
    companies_data = api_client.get_company_data(companies_list_id)
    db_manager.save_company_data(companies_data)

    while True:
        print("\nВыберите действие:")
        print("1. Посмотреть компании и количество вакансий")
        print("2. Посмотреть все вакансии")
        print("3. Средняя зарплата вакансий")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Вакансии с ключевым словом")
        print("0. Выход")

        choice = input("Введите номер действия: ")
        if choice == "1":
            print(db_manager.get_companies_and_vacancies_count())
        elif choice == "2":
            print(db_manager.get_all_vacancies())
        elif choice == "3":
            print(db_manager.get_avg_salary())
        elif choice == "4":
            print(db_manager.get_vacancies_with_higher_salary())
        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            print(db_manager.get_vacancies_with_keyword(keyword))
        elif choice == "0":
            break
        else:
            print("Некорректный ввод.")


if __name__ == "__main__":
    main()

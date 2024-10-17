import requests
from typing import List, Dict, Any


class HHAPIClient:
    """
    Класс для взаимодействия с API hh.ru.
    """

    BASE_URL = "https://api.hh.ru"

    def __init__(self, company_ids: List[str]):
        """
        Инициализация клиента API hh.ru.

        :param company_ids: Список ID компаний для получения данных.
        """
        self.company_ids = company_ids

    def get_company_vacancies(self, company_id: str) -> List[Dict[str, Any]]:
        """
        Получает вакансии для указанной компании.

        :param company_id: ID компании.
        :return: Список вакансий компании.
        """
        url = f"{self.BASE_URL}/vacancies"
        params = {'employer_id': company_id}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки
        return response.json()['items']

    def get_all_companies_data(self) -> List[Dict[str, Any]]:
        """
        Получает данные всех компаний и их вакансий.

        :return: Список с данными по компаниям и их вакансиям.
        """
        all_data = []
        for company_id in self.company_ids:
            vacancies = self.get_company_vacancies(company_id)
            all_data.append({
                'company_id': company_id,
                'vacancies': vacancies
            })
        return all_data

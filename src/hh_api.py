from typing import Any, Dict, List

import requests


class APIClient:
    """
    Класс для работы с API hh.ru.
    """

    BASE_URL = "https://api.hh.ru"

    def get_company_data(self, company_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Получает данные о компаниях и их вакансиях с API hh.ru.

        :param company_ids: Список ID компаний, от которых требуется получить вакансии.
        :return: Список словарей с информацией о каждой компании и её вакансиях.
        """
        companies_data = []
        for company_id in company_ids:
            company_url = f"{self.BASE_URL}/employers/{company_id}"
            vacancies_url = f"{self.BASE_URL}/vacancies?employer_id={company_id}"

            company_response = requests.get(company_url)
            if company_response.status_code == 200:
                company_info = company_response.json()
                company_name = company_info.get("name")

                vacancies_response = requests.get(vacancies_url)
                if vacancies_response.status_code == 200:
                    vacancies = vacancies_response.json().get("items", [])
                    vacancies_data = []

                    for vacancy in vacancies:
                        salary_info = vacancy.get("salary")
                        salary = (
                            salary_info.get("from") if salary_info else None
                        )  # Проверка, чтобы salary не было None

                        vacancies_data.append(
                            {
                                "name": vacancy["name"],
                                "salary": salary,
                                "url": vacancy["alternate_url"],
                            }
                        )

                    companies_data.append(
                        {
                            "company_id": company_id,
                            "name": company_name,
                            "vacancies": vacancies_data,
                        }
                    )
        return companies_data

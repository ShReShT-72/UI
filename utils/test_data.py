from faker import Faker
from typing import Dict


class CheckoutDataFactory:
    def __init__(self) -> None:
        self._faker = Faker()

    def generate_checkout_information(self) -> Dict[str, str]:
        return {
            "first_name": self._faker.first_name(),
            "last_name": self._faker.last_name(),
            "postal_code": self._faker.postcode(),
        }

import re
from typing import Tuple

import requests

from .base import BaseProcessor

PATTERN_WIN = re.compile(r"/(\w*)\?")


class ApiProcessor(BaseProcessor):
    """
    Processor based on API interaction.
    The idea is in pooling data for cars using API `/api/listings`.
    """

    def __init__(self, url: str, max_workers: int):
        self.URL_API = f'{url}/api/listings'
        self.MAX_WORKERS = max_workers

    def get_data_one(self, data_unit: str) -> Tuple[str, str, dict, list]:
        # data_unit is a link to the car
        # Get vin from link using regex
        vin = self.get_vin(data_unit)
        resp = requests.get(f'{self.URL_API}/{vin}')
        data = resp.json()

        # Strictly specified processing
        # Get name
        name = ' '.join([str(data.get(v)) for v in ('year', 'make', 'model')]).strip()

        # Get price
        price = f"${int(data.get('price')):,}"

        # Get options
        options = []
        for option in data.get('specs', {}).get('options', {}).get('equipment', {}).values():
            for group in option.get('optionGroups', []):
                for group_option in group.get('options', []):
                    options.append(group_option['name'])
        options = [o for o in options if o]

        # Get summary
        specs = data.get('specs', {})
        engine = specs.get('engine', {})
        gas = specs.get('gas', {})
        engine_hp = engine.get('value')
        engine_rpm = engine.get('rpm')
        engine_cylinders = gas.get('cylinders')
        engine_displacement = gas.get('displacement')
        fuel_economy = specs.get('fuelEconomy', {})
        fuel_economy_city = fuel_economy.get('city')
        fuel_economy_highway = fuel_economy.get('highway')
        fuel_economy_combined = fuel_economy.get('combined')
        summary = {
            'VIN': vin,
            'Trim': data.get('trim'),
            'Full style name': data.get('full_style_name'),
            'Mileage': data.get('mileage'),
            'Tire Mileage': data.get('tire_mileage'),
            'Transmission': specs.get('transmission', '').capitalize(),
            'Drive Type': specs.get('drivetrain'),
            'Engine': f"{engine_hp + ' HP' if engine_hp else ''} "
                      f"{engine_rpm + ' RPM' if engine_rpm else ''} "
                      f"{str(engine_cylinders) + ' cylinder' if engine_cylinders else ''} "
                      f"{str(engine_displacement) + 'L' if engine_displacement else ''}".strip(),
            'Fuel Economy': f"{str(fuel_economy_city) + ' MPG city' if fuel_economy_city else ''} "
                            f"{str(fuel_economy_highway) + ' MPG highway' if fuel_economy_highway else ''} "
                            f"{str(fuel_economy_combined) + ' MPG combined' if fuel_economy_combined else ''}",
            'Doors': specs.get('doors'),
            'Passengers': specs.get('passengerCapacity'),
            'Exterior': data.get('exterior_color_id')
        }
        summary = {k: v for k, v in summary.items() if v}

        return name, price, summary, options

    @staticmethod
    def get_vin(link: str) -> str:
        return PATTERN_WIN.search(link).group(1)

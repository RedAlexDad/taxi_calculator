
# Создаем приложение для расчета стоимости тарифа такси
# taxi_calculator.py

taxi_calculator_code = '''"""
Модуль для расчета стоимости тарифа такси.
Поддерживает различные типы тарифов и факторы, влияющие на цену.
"""

class TaxiCalculator:
    """
    Класс для расчета стоимости поездки такси.
    
    Поддерживаемые тарифы:
    - эконом: базовая цена 100 руб/км
    - комфорт: 150 руб/км
    - комфорт_плюс: 200 руб/км
    - бизнес: 300 руб/км
    """
    
    # Базовые ставки по типам тарифов (руб/км)
    TARIFF_RATES = {
        'эконом': 100,
        'комфорт': 150,
        'комфорт_плюс': 200,
        'бизнес': 300
    }
    
    # Минимальная стоимость поездки (руб)
    MIN_FARE = 50
    
    # Коэффициенты за влияние факторов
    TRAFFIC_MULTIPLIERS = {
        1: 1.0,      # Нет пробок
        2: 1.1,      # Легкие пробки
        3: 1.25,     # Средние пробки
        4: 1.5,      # Тяжелые пробки
        5: 2.0       # Очень тяжелые пробки
    }
    
    WEATHER_MULTIPLIERS = {
        1: 1.0,      # Хорошая погода
        2: 1.05,     # Облачно
        3: 1.15,     # Дождь/снег
        4: 1.3,      # Сильный дождь/метель
        5: 1.5       # Сильный шторм/ледяной дождь
    }
    
    OVERLOAD_MULTIPLIERS = {
        1: 1.0,      # Нет спроса
        2: 1.1,      # Нормальный спрос
        3: 1.25,     # Повышенный спрос
        4: 1.5,      # Высокий спрос
        5: 2.0       # Экстремальный спрос
    }
    
    def __init__(self):
        """Инициализация калькулятора."""
        pass
    
    def validate_distance(self, distance):
        """
        Проверяет корректность расстояния.
        
        Args:
            distance: Расстояние поездки в км
            
        Raises:
            ValueError: Если расстояние <= 0
            TypeError: Если расстояние не число
        """
        if not isinstance(distance, (int, float)):
            raise TypeError(f"Расстояние должно быть числом, получено: {type(distance)}")
        if distance <= 0:
            raise ValueError(f"Расстояние должно быть положительным, получено: {distance}")
    
    def validate_tariff(self, tariff):
        """
        Проверяет корректность типа тарифа.
        
        Args:
            tariff: Тип тарифа
            
        Raises:
            ValueError: Если тариф не поддерживается
        """
        if tariff not in self.TARIFF_RATES:
            raise ValueError(f"Неподдерживаемый тариф: {tariff}. "
                           f"Доступные: {list(self.TARIFF_RATES.keys())}")
    
    def validate_rating(self, rating, rating_type="traffic"):
        """
        Проверяет корректность рейтинга (1-5).
        
        Args:
            rating: Рейтинг от 1 до 5
            rating_type: Тип рейтинга (traffic, weather, overload)
            
        Raises:
            ValueError: Если рейтинг вне диапазона [1, 5]
            TypeError: Если рейтинг не целое число
        """
        if not isinstance(rating, int):
            raise TypeError(f"Рейтинг должен быть целым числом, получено: {type(rating)}")
        if not 1 <= rating <= 5:
            raise ValueError(f"Рейтинг {rating_type} должен быть от 1 до 5, получено: {rating}")
    
    def calculate_fare(self, distance, tariff, traffic_rating=1, 
                      weather_rating=1, overload_rating=1):
        """
        Рассчитывает стоимость поездки такси.
        
        Args:
            distance: Расстояние поездки в км
            tariff: Тип тарифа (эконом, комфорт, комфорт_плюс, бизнес)
            traffic_rating: Уровень пробок (1-5)
            weather_rating: Уровень непогоды (1-5)
            overload_rating: Уровень спроса/переполненности (1-5)
        
        Returns:
            float: Расчетная стоимость поездки в рублях
            
        Raises:
            ValueError: Если параметры некорректны
            TypeError: Если параметры неправильного типа
        """
        # Валидация параметров
        self.validate_distance(distance)
        self.validate_tariff(tariff)
        self.validate_rating(traffic_rating, "пробок")
        self.validate_rating(weather_rating, "непогоды")
        self.validate_rating(overload_rating, "спроса")
        
        # Расчет базовой стоимости
        base_rate = self.TARIFF_RATES[tariff]
        base_fare = distance * base_rate
        
        # Применение коэффициентов
        traffic_multiplier = self.TRAFFIC_MULTIPLIERS[traffic_rating]
        weather_multiplier = self.WEATHER_MULTIPLIERS[weather_rating]
        overload_multiplier = self.OVERLOAD_MULTIPLIERS[overload_rating]
        
        # Итоговая стоимость
        total_multiplier = traffic_multiplier * weather_multiplier * overload_multiplier
        fare = base_fare * total_multiplier
        
        # Применение минимальной стоимости
        fare = max(fare, self.MIN_FARE)
        
        # Округление до копеек
        fare = round(fare, 2)
        
        return fare
    
    def get_tariff_info(self):
        """
        Возвращает информацию о доступных тарифах.
        
        Returns:
            dict: Информация о тарифах
        """
        return {
            'тарифы': list(self.TARIFF_RATES.keys()),
            'ставки': self.TARIFF_RATES,
            'минимальная_стоимость': self.MIN_FARE
        }


def main():
    """Пример использования калькулятора."""
    calc = TaxiCalculator()
    
    # Пример 1: Эконом при нормальных условиях
    price = calc.calculate_fare(distance=10, tariff='эконом')
    print(f"Поездка 10 км (эконом): {price} руб")
    
    # Пример 2: Бизнес с пробками и дождем
    price = calc.calculate_fare(
        distance=15,
        tariff='бизнес',
        traffic_rating=4,
        weather_rating=3,
        overload_rating=2
    )
    print(f"Поездка 15 км (бизнес, пробки, дождь): {price} руб")


if __name__ == '__main__':
    main()
'''

print("✓ Создан модуль taxi_calculator.py")
print("\nСохраняем код для документации...")
print(taxi_calculator_code[:500] + "...")

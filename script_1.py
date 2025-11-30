
# Создаем Unit-тесты для taxi_calculator.py
test_code = '''"""
Unit-тесты для модуля расчета стоимости тарифа такси.
Используется фреймворк unittest.

Запуск тестов:
    python -m unittest test_taxi_calculator -v
    python -m unittest test_taxi_calculator --coverage
"""

import unittest
from taxi_calculator import TaxiCalculator


class TestTaxiCalculatorValidation(unittest.TestCase):
    """Тесты для проверки валидации входных параметров."""
    
    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом."""
        self.calc = TaxiCalculator()
    
    def test_validate_distance_positive(self):
        """Проверка: положительное расстояние должно быть корректным."""
        try:
            self.calc.validate_distance(10)
            self.calc.validate_distance(0.5)
        except ValueError:
            self.fail("Положительное расстояние вызвало исключение")
    
    def test_validate_distance_negative(self):
        """Проверка: отрицательное расстояние вызывает ValueError."""
        with self.assertRaises(ValueError):
            self.calc.validate_distance(-5)
    
    def test_validate_distance_zero(self):
        """Проверка: нулевое расстояние вызывает ValueError."""
        with self.assertRaises(ValueError):
            self.calc.validate_distance(0)
    
    def test_validate_distance_wrong_type(self):
        """Проверка: строка вместо числа вызывает TypeError."""
        with self.assertRaises(TypeError):
            self.calc.validate_distance("10 км")
    
    def test_validate_distance_none(self):
        """Проверка: None вызывает TypeError."""
        with self.assertRaises(TypeError):
            self.calc.validate_distance(None)
    
    def test_validate_tariff_valid(self):
        """Проверка: все поддерживаемые тарифы корректны."""
        valid_tariffs = ['эконом', 'комфорт', 'комфорт_плюс', 'бизнес']
        for tariff in valid_tariffs:
            try:
                self.calc.validate_tariff(tariff)
            except ValueError:
                self.fail(f"Валидный тариф '{tariff}' вызвал исключение")
    
    def test_validate_tariff_invalid(self):
        """Проверка: неподдерживаемый тариф вызывает ValueError."""
        with self.assertRaises(ValueError):
            self.calc.validate_tariff('премиум')
    
    def test_validate_rating_valid(self):
        """Проверка: рейтинги от 1 до 5 корректны."""
        for rating in range(1, 6):
            try:
                self.calc.validate_rating(rating)
            except ValueError:
                self.fail(f"Валидный рейтинг {rating} вызвал исключение")
    
    def test_validate_rating_too_low(self):
        """Проверка: рейтинг 0 вызывает ValueError."""
        with self.assertRaises(ValueError):
            self.calc.validate_rating(0)
    
    def test_validate_rating_too_high(self):
        """Проверка: рейтинг 6 вызывает ValueError."""
        with self.assertRaises(ValueError):
            self.calc.validate_rating(6)
    
    def test_validate_rating_not_integer(self):
        """Проверка: дробное число вызывает TypeError."""
        with self.assertRaises(TypeError):
            self.calc.validate_rating(3.5)


class TestTaxiCalculatorFareCalculation(unittest.TestCase):
    """Тесты для расчета стоимости поездки."""
    
    def setUp(self):
        """Подготовка к каждому тесту."""
        self.calc = TaxiCalculator()
    
    def test_simple_fare_econom(self):
        """Проверка: расчет базовой стоимости для эконома."""
        # 10 км * 100 руб/км = 1000 руб
        fare = self.calc.calculate_fare(distance=10, tariff='эконом')
        self.assertEqual(fare, 1000.0)
    
    def test_simple_fare_comfort(self):
        """Проверка: расчет базовой стоимости для комфорта."""
        # 10 км * 150 руб/км = 1500 руб
        fare = self.calc.calculate_fare(distance=10, tariff='комфорт')
        self.assertEqual(fare, 1500.0)
    
    def test_simple_fare_business(self):
        """Проверка: расчет базовой стоимости для бизнеса."""
        # 10 км * 300 руб/км = 3000 руб
        fare = self.calc.calculate_fare(distance=10, tariff='бизнес')
        self.assertEqual(fare, 3000.0)
    
    def test_minimum_fare(self):
        """Проверка: применение минимальной стоимости."""
        # Очень короткая поездка должна быть не менее 50 руб
        fare = self.calc.calculate_fare(distance=0.1, tariff='эконом')
        self.assertEqual(fare, 50.0)
    
    def test_fare_with_traffic(self):
        """Проверка: влияние пробок на стоимость."""
        # Базовая: 10 км * 100 = 1000
        # С пробками уровень 5: 1000 * 2.0 = 2000
        fare = self.calc.calculate_fare(
            distance=10,
            tariff='эконом',
            traffic_rating=5
        )
        self.assertEqual(fare, 2000.0)
    
    def test_fare_with_weather(self):
        """Проверка: влияние непогоды на стоимость."""
        # Базовая: 5 км * 150 = 750
        # С дождем уровень 3: 750 * 1.15 = 862.5
        fare = self.calc.calculate_fare(
            distance=5,
            tariff='комфорт',
            weather_rating=3
        )
        self.assertAlmostEqual(fare, 862.5, places=2)
    
    def test_fare_with_overload(self):
        """Проверка: влияние спроса на стоимость."""
        # Базовая: 8 км * 200 = 1600
        # С высоким спросом уровень 4: 1600 * 1.5 = 2400
        fare = self.calc.calculate_fare(
            distance=8,
            tariff='комфорт_плюс',
            overload_rating=4
        )
        self.assertEqual(fare, 2400.0)
    
    def test_fare_combined_multipliers(self):
        """Проверка: одновременное применение всех коэффициентов."""
        # Базовая: 10 км * 100 = 1000
        # Пробки уровень 4: * 1.5
        # Непогода уровень 3: * 1.15
        # Спрос уровень 2: * 1.1
        # Итого: 1000 * 1.5 * 1.15 * 1.1 = 1897.5
        fare = self.calc.calculate_fare(
            distance=10,
            tariff='эконом',
            traffic_rating=4,
            weather_rating=3,
            overload_rating=2
        )
        self.assertAlmostEqual(fare, 1897.5, places=2)
    
    def test_fare_float_distance(self):
        """Проверка: обработка дробных расстояний."""
        # 5.5 км * 100 = 550 руб
        fare = self.calc.calculate_fare(distance=5.5, tariff='эконом')
        self.assertEqual(fare, 550.0)
    
    def test_fare_precision(self):
        """Проверка: округление до копеек."""
        # Проверяем, что результат имеет максимум 2 знака после запятой
        fare = self.calc.calculate_fare(
            distance=3.33,
            tariff='комфорт',
            weather_rating=3
        )
        # fare должна быть округлена до сотых
        self.assertEqual(fare % 1, round(fare % 1, 2))


class TestTaxiCalculatorEdgeCases(unittest.TestCase):
    """Тесты для граничных случаев."""
    
    def setUp(self):
        """Подготовка к каждому тесту."""
        self.calc = TaxiCalculator()
    
    def test_very_long_distance(self):
        """Проверка: расчет для очень дальней поездки."""
        fare = self.calc.calculate_fare(distance=1000, tariff='бизнес')
        expected = 1000 * 300  # 1000 км * 300 руб/км = 300000
        self.assertEqual(fare, expected)
    
    def test_very_short_distance_below_minimum(self):
        """Проверка: применение минимума для очень короткой поездки."""
        fare = self.calc.calculate_fare(distance=0.001, tariff='бизнес')
        self.assertEqual(fare, 50.0)
    
    def test_all_ratings_at_minimum(self):
        """Проверка: все коэффициенты на минимуме (нет влияния)."""
        fare = self.calc.calculate_fare(
            distance=10,
            tariff='комфорт',
            traffic_rating=1,
            weather_rating=1,
            overload_rating=1
        )
        expected = 10 * 150  # 1500 руб
        self.assertEqual(fare, expected)
    
    def test_all_ratings_at_maximum(self):
        """Проверка: все коэффициенты на максимуме (худший сценарий)."""
        fare = self.calc.calculate_fare(
            distance=1,
            tariff='комфорт_плюс',
            traffic_rating=5,
            weather_rating=5,
            overload_rating=5
        )
        # 1 км * 200 * 2.0 * 1.5 * 2.0 = 1200 руб
        expected = 1 * 200 * 2.0 * 1.5 * 2.0
        self.assertEqual(fare, expected)


class TestTaxiCalculatorInfo(unittest.TestCase):
    """Тесты для методов получения информации."""
    
    def setUp(self):
        """Подготовка к каждому тесту."""
        self.calc = TaxiCalculator()
    
    def test_get_tariff_info(self):
        """Проверка: получение информации о тарифах."""
        info = self.calc.get_tariff_info()
        
        self.assertIn('тарифы', info)
        self.assertIn('ставки', info)
        self.assertIn('минимальная_стоимость', info)
        
        self.assertEqual(len(info['тарифы']), 4)
        self.assertEqual(info['минимальная_стоимость'], 50)
    
    def test_tariff_info_contains_all_rates(self):
        """Проверка: информация содержит все ставки."""
        info = self.calc.get_tariff_info()
        rates = info['ставки']
        
        self.assertEqual(rates['эконом'], 100)
        self.assertEqual(rates['комфорт'], 150)
        self.assertEqual(rates['комфорт_плюс'], 200)
        self.assertEqual(rates['бизнес'], 300)


class TestTaxiCalculatorIntegration(unittest.TestCase):
    """Интеграционные тесты для реальных сценариев."""
    
    def setUp(self):
        """Подготовка к каждому тесту."""
        self.calc = TaxiCalculator()
    
    def test_scenario_economy_good_weather(self):
        """Сценарий: экономная поездка в хорошую погоду."""
        # 7 км, эконом, без пробок, хорошая погода, нормальный спрос
        fare = self.calc.calculate_fare(
            distance=7,
            tariff='эконом',
            traffic_rating=1,
            weather_rating=1,
            overload_rating=2
        )
        # 7 * 100 * 1.0 * 1.0 * 1.1 = 770
        self.assertEqual(fare, 770.0)
    
    def test_scenario_business_bad_weather(self):
        """Сценарий: премиум-поездка в плохую погоду с пробками."""
        # 12 км, бизнес, пробки, шторм, высокий спрос
        fare = self.calc.calculate_fare(
            distance=12,
            tariff='бизнес',
            traffic_rating=4,
            weather_rating=5,
            overload_rating=4
        )
        # 12 * 300 * 1.5 * 1.5 * 1.5 = 12150
        expected = 12 * 300 * 1.5 * 1.5 * 1.5
        self.assertAlmostEqual(fare, expected, places=2)
    
    def test_scenario_comfort_plus_standard(self):
        """Сценарий: комфорт-плюс при стандартных условиях."""
        # 15 км, комфорт+, средние пробки, облачно, повышенный спрос
        fare = self.calc.calculate_fare(
            distance=15,
            tariff='комфорт_плюс',
            traffic_rating=3,
            weather_rating=2,
            overload_rating=3
        )
        # 15 * 200 * 1.25 * 1.05 * 1.25 = 4921.875
        expected = 15 * 200 * 1.25 * 1.05 * 1.25
        self.assertAlmostEqual(fare, expected, places=2)


if __name__ == '__main__':
    # Запуск всех тестов с подробным выводом
    unittest.main(verbosity=2)
'''

print("✓ Создан модуль test_taxi_calculator.py")
print("\nОсновные категории тестов:")
print("1. TestTaxiCalculatorValidation - 11 тестов валидации")
print("2. TestTaxiCalculatorFareCalculation - 10 тестов расчета")
print("3. TestTaxiCalculatorEdgeCases - 4 теста граничных случаев")
print("4. TestTaxiCalculatorInfo - 2 теста информации")
print("5. TestTaxiCalculatorIntegration - 3 интеграционных теста")
print("\nИтого: 30 Unit-тестов")

# Инструкции по созданию репозитория на GitHub

## Шаг 1: Подготовка локальной директории

```bash
# Создание директории проекта
mkdir taxi-calculator
cd taxi-calculator

# Инициализация Git репозитория
git init
git config user.name "Your Full Name"
git config user.email "your.email@example.com"
```

## Шаг 2: Добавление файлов проекта

Скопируйте в директорию следующие файлы:

```
taxi-calculator/
├── taxi_calculator.py           # Основной модуль
├── test_taxi_calculator.py      # Unit-тесты
├── README.md                    # Документация
├── requirements.txt             # Зависимости
└── .gitignore                   # Git игнор-правила
```

## Шаг 3: Первоначальный коммит

```bash
# Добавление всех файлов в staging area
git add .

# Проверка статуса
git status

# Создание первого коммита
git commit -m "Initial commit: Taxi calculator with unit tests and documentation"
```

## Шаг 4: Создание репозитория на GitHub

1. Откройте https://github.com/new
2. Заполните форму:
   - **Repository name**: `taxi-calculator`
   - **Description**: `Taxi fare calculator with comprehensive unit tests and 96% code coverage`
   - **Visibility**: Public (публичный репозиторий)
   - **Initialize this repository with**: не выбирайте (уже имеем локальный репо)
3. Нажмите кнопку **Create repository**

## Шаг 5: Подключение удаленного репозитория

После создания репозитория на GitHub вы увидите инструкции. Выполните:

```bash
# Переименование ветки (если нужно)
git branch -M main

# Добавление удаленного репозитория
git remote add origin https://github.com/YOUR_USERNAME/taxi-calculator.git

# Отправка кода на GitHub
git push -u origin main
```

**Замечание**: Замените `YOUR_USERNAME` на ваше имя пользователя GitHub.

## Шаг 6: Проверка репозитория

1. Перейдите на https://github.com/YOUR_USERNAME/taxi-calculator
2. Убедитесь, что все файлы загружены корректно
3. Проверьте наличие README.md в главном представлении

## Дополнительные команды Git

### Обновление кода на GitHub после изменений

```bash
# Просмотр статуса
git status

# Добавление изменений
git add .
# или конкретного файла:
git add taxi_calculator.py

# Коммит
git commit -m "Describe your changes here"

# Отправка на GitHub
git push origin main
```

### Просмотр истории коммитов

```bash
git log --oneline
git log --graph --oneline --all
```

### Клонирование репозитория

```bash
git clone https://github.com/YOUR_USERNAME/taxi-calculator.git
cd taxi-calculator
```

## Структура репозитория

После загрузки на GitHub репозиторий должен выглядеть так:

```
taxi-calculator/
├── taxi_calculator.py          # Основной модуль (215 строк)
├── test_taxi_calculator.py     # Unit-тесты (280 строк)
├── README.md                   # Подробная документация
├── requirements.txt            # Зависимости для разработки
└── .gitignore                  # Git игнор-правила
```

## Создание Issues и Pull Requests

### Создание Issue

1. На странице репозитория нажмите **Issues**
2. Нажмите **New issue**
3. Заполните название и описание проблемы
4. Нажмите **Submit new issue**

### Создание Pull Request

```bash
# Создание новой ветки для функции
git checkout -b feature/new-feature

# Внесение изменений...

# Коммит изменений
git add .
git commit -m "Add new feature"

# Отправка на GitHub
git push origin feature/new-feature
```

После этого на GitHub вы сможете создать Pull Request через веб-интерфейс.

## Защита основной ветки (main)

Для защиты от случайных изменений:

1. Перейдите в **Settings** репозитория
2. Выберите **Branches**
3. Добавьте правило защиты для ветки `main`:
   - Требовать pull request перед слиянием
   - Требовать одобрение рецензентов
   - Требовать статусные проверки перед слиянием

## Использование GitHub Actions для CI/CD

Создайте файл `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m unittest test_taxi_calculator -v
    
    - name: Run coverage
      run: |
        coverage run -m unittest test_taxi_calculator
        coverage report
```

После добавления этого файла и отправки на GitHub тесты будут запускаться автоматически при каждом push и pull request.

## Полезные ссылки

- [GitHub Documentation](https://docs.github.com)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Markdown Guide](https://guides.github.com/features/mastering-markdown/)
- [How to write a good Git commit message](https://chris.beams.io/posts/git-commit/)

## Распространенные проблемы

### "fatal: not a git repository"

**Решение**: Убедитесь, что вы находитесь в правильной директории и выполнили `git init`.

### "Permission denied (publickey)"

**Решение**: Настройте SSH ключи:
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Добавьте публичный ключ на GitHub в Settings > SSH and GPG keys
```

Или используйте HTTPS вместо SSH:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/taxi-calculator.git
```

### "Everything up-to-date"

Это означает, что нет новых изменений для отправки. Убедитесь, что вы сделали коммит:
```bash
git status  # Проверьте статус
git commit -m "Your message"  # Если изменения не закоммичены
```

---

**Дополнительная информация:**

После успешной загрузки на GitHub репозиторий готов к:
- Совместной разработке
- Отслеживанию проблем
- Управлению версиями
- Автоматизации тестирования (CI/CD)
- Документации и демонстрации проекта

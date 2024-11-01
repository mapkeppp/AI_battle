# Эволюционная симуляция боевых роботов

## Описание проекта
Проект представляет собой симуляцию сражения между двумя командами роботов с применением генетических алгоритмов для эволюции их поведения и характеристик. Каждая команда состоит из различных типов роботов, которые развиваются и адаптируются в процессе боев.

## Основные функции

### Типы роботов
- **MeleeRobot (ближний бой)**
  - Высокий урон в ближнем бою
  - Средняя скорость передвижения
  - Среднее здоровье
- **RangedRobot (дальний бой)**
  - Атака на расстоянии
  - Высокая скорость
  - Низкое здоровье
- **TankRobot (танк)**
  - Высокое здоровье
  - Низкая скорость
  - Средний урон
  - Защита союзников

### Генетическая эволюция
- **Характеристики роботов:**
  - Здоровье (health)
  - Скорость (speed)
  - Урон (damage)
  - Уровень агрессии (aggression)
- **Система эволюции:**
  - Мутации генов
  - Наследование характеристик
  - Адаптация к противнику

### Анализ данных
- **Логирование:**
  - Статистика боев
  - Эффективность роботов
  - Прогресс эволюции
- **Визуализация:**
  - Графики характеристик
  - Сравнение команд
  - Анализ эффективности стратегий

## Структура проекта
project/
├── main.py # Точка входа в программу
├── game_system/ # Игровая система
│ ├── game_manager.py # Управление игрой
│ ├── config.py # Конфигурация
│ └── csv_logger.py # Логирование
├── entities/ # Игровые объекты
│ ├── robot.py # Классы роботов
│ ├── base.py # Базы команд
│ ├── obstacle.py # Препятствия
│ ├── pathfinder.py # Поиск пути
│ └── projectile.py # Снаряды
├── genetic/ # Генетические алгоритмы
│ ├── chromosome.py # Гены
│ ├── fitness.py # Оценка приспособленности
│ ├── population.py # Управление популяцией
│ ├── visualizer.py # Визуализация данных
│ └── data_handler.py # Обработка данных
├── logs/ # Файлы логов
└── genetic_plots/ # Графики эволюции


## Установка

### Требования
- Python 3.8+
- pygame
- numpy
- pandas
- matplotlib
- seaborn

### Установка зависимостей
bash
pip install -r requirements.txt
### Запуск
bash
python main.py

## Визуализация данных

### Генерируемые графики
1. **Статистика поколений:**
   - Распределение характеристик
   - Корреляции между параметрами
   - Распределение агрессии
   - Соотношение здоровья к урону

2. **Сравнение команд:**
   - Эффективность типов роботов
   - Распределение характеристик
   - Статистика боев

3. **Прогресс эволюции:**
   - Изменение средних характеристик
   - Разброс параметров по поколениям

## Параметры генетического алгоритма
- Размер популяции: 10
- Уровень мутации: 0.1
- Размер турнира: 3
- Размер элиты: 1

## Метрики эффективности
- Количество убийств
- Нанесенный урон
- Урон по базе противника
- Время выживания
- Эффективность использования ресурсов

## Планы по развитию
1. **Улучшение ИИ:**
   - Внедрение нейронных сетей
   - Улучшение тактического поведения
   - Развитие командного взаимодействия

2. **Расширение функционала:**
   - Новые типы роботов
   - Дополнительные стратегии
   - Улучшенная визуализация

3. **Оптимизация:**
   - Параллельные вычисления
   - Улучшение производительности
   - Оптимизация памяти


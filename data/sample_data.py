def get_sample_data():
    """
    Получить примеры данных для тестирования
    
    Returns:
        dict: Примеры различных ниш
    """
    return {
        'good_niche': {
            'demand_ratio': 8.5,
            'revenue': 3500000,
            'price_ad_ratio': 35.0,
            'organic_percent': 70.0
        },
        'average_niche': {
            'demand_ratio': 5.2,
            'revenue': 2500000,
            'price_ad_ratio': 25.0,
            'organic_percent': 65.0
        },
        'poor_niche': {
            'demand_ratio': 2.1,
            'revenue': 800000,
            'price_ad_ratio': 12.0,
            'organic_percent': 30.0
        }
    }

def get_competitive_analysis_sample():
    """
    Примеры данных для конкурентного анализа
    
    Returns:
        dict: Данные о конкурентах
    """
    return {
        'names': ['Конкурент 1', 'Конкурент 2', 'Конкурент 3', 'Конкурент 4', 'Конкурент 5'],
        'prices': [1200, 1500, 900, 1800, 1100],
        'sales': [450, 320, 680, 210, 520],
        'market_share': [15, 12, 25, 8, 18],
        'ratings': [4.2, 4.5, 3.8, 4.7, 4.1]
    }

def get_historical_trends_sample():
    """
    Примеры исторических данных
    
    Returns:
        dict: Исторические тренды
    """
    import pandas as pd
    
    dates = pd.date_range('2024-01-01', '2024-12-31', freq='M')
    
    return {
        'dates': dates,
        'demand': [45, 48, 52, 55, 58, 62, 65, 68, 64, 60, 57, 59],
        'revenue': [65, 67, 70, 72, 75, 78, 80, 82, 78, 75, 73, 76],
        'ads': [35, 38, 42, 45, 48, 52, 55, 58, 54, 50, 47, 49],
        'organic': [70, 72, 68, 65, 62, 58, 55, 52, 56, 60, 63, 61]
    }

def get_niche_comparison_sample():
    """
    Примеры данных для сравнения ниш
    
    Returns:
        list: Данные нескольких ниш для сравнения
    """
    return [
        {
            'name': 'Маски для волос',
            'metrics': {
                'demand_ratio': 8.5,
                'revenue': 3500000,
                'price_ad_ratio': 35.0,
                'organic_percent': 70.0
            }
        },
        {
            'name': 'Кремы для лица',
            'metrics': {
                'demand_ratio': 6.2,
                'revenue': 4200000,
                'price_ad_ratio': 28.0,
                'organic_percent': 55.0
            }
        },
        {
            'name': 'Шампуни',
            'metrics': {
                'demand_ratio': 3.8,
                'revenue': 8500000,
                'price_ad_ratio': 15.0,
                'organic_percent': 40.0
            }
        },
        {
            'name': 'Сыворотки',
            'metrics': {
                'demand_ratio': 12.3,
                'revenue': 1800000,
                'price_ad_ratio': 45.0,
                'organic_percent': 85.0
            }
        }
    ]

def get_category_examples():
    """
    Примеры различных категорий товаров
    
    Returns:
        dict: Примеры по категориям
    """
    return {
        'beauty': {
            'name': 'Красота и здоровье',
            'examples': [
                'Маски для волос',
                'Кремы для лица', 
                'Сыворотки',
                'Тональные кремы',
                'Помады'
            ],
            'typical_metrics': {
                'demand_ratio': 6.5,
                'revenue': 2800000,
                'price_ad_ratio': 22.0,
                'organic_percent': 58.0
            }
        },
        'home': {
            'name': 'Дом и сад',
            'examples': [
                'Органайзеры',
                'Декоративные подушки',
                'Светильники',
                'Кашпо',
                'Текстиль'
            ],
            'typical_metrics': {
                'demand_ratio': 4.2,
                'revenue': 3200000,
                'price_ad_ratio': 18.0,
                'organic_percent': 65.0
            }
        },
        'electronics': {
            'name': 'Электроника',
            'examples': [
                'Наушники',
                'Зарядные устройства',
                'Кабели',
                'Чехлы для телефонов',
                'Аксессуары'
            ],
            'typical_metrics': {
                'demand_ratio': 3.8,
                'revenue': 5500000,
                'price_ad_ratio': 12.0,
                'organic_percent': 35.0
            }
        },
        'clothing': {
            'name': 'Одежда',
            'examples': [
                'Платья',
                'Футболки',
                'Джинсы',
                'Куртки',
                'Аксессуары'
            ],
            'typical_metrics': {
                'demand_ratio': 2.5,
                'revenue': 12000000,
                'price_ad_ratio': 8.0,
                'organic_percent': 25.0
            }
        }
    }

def get_seasonal_data_sample():
    """
    Примеры сезонных данных
    
    Returns:
        dict: Сезонные тренды по месяцам
    """
    return {
        'beauty_seasonal': {
            'months': ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
                      'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
            'demand': [85, 90, 95, 100, 105, 110, 115, 120, 110, 105, 95, 90],
            'description': 'Пик спроса летом (уход за кожей)'
        },
        'home_seasonal': {
            'months': ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
                      'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
            'demand': [120, 110, 100, 95, 90, 85, 80, 85, 90, 100, 110, 125],
            'description': 'Пик спроса зимой (обустройство дома)'
        },
        'electronics_seasonal': {
            'months': ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
                      'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
            'demand': [90, 85, 90, 95, 100, 105, 110, 115, 110, 105, 120, 130],
            'description': 'Пик спроса в конце года (подарки)'
        }
    }

def get_market_insights():
    """
    Примеры инсайтов рынка
    
    Returns:
        dict: Инсайты и рекомендации
    """
    return {
        'high_potential_niches': [
            {
                'name': 'Эко-косметика',
                'reason': 'Растущий тренд на экологичность',
                'demand_growth': '+45% за год',
                'competition': 'Низкая'
            },
            {
                'name': 'Товары для домашних животных',
                'reason': 'Увеличение числа владельцев питомцев',
                'demand_growth': '+32% за год',
                'competition': 'Средняя'
            },
            {
                'name': 'Умные устройства для дома',
                'reason': 'Цифровизация быта',
                'demand_growth': '+58% за год',
                'competition': 'Высокая'
            }
        ],
        'declining_niches': [
            {
                'name': 'DVD-диски',
                'reason': 'Переход на стриминговые сервисы',
                'demand_change': '-67% за год',
                'recommendation': 'Избегать'
            },
            {
                'name': 'Печатные книги (художественная литература)',
                'reason': 'Популярность электронных книг',
                'demand_change': '-23% за год',
                'recommendation': 'Осторожно'
            }
        ],
        'market_tips': [
            "Следите за трендами в социальных сетях",
            "Анализируйте сезонность спроса",
            "Изучайте отзывы покупателей конкурентов",
            "Обращайте внимание на новые технологии",
            "Учитывайте демографические изменения"
        ]
    }

def get_benchmark_data():
    """
    Бенчмарки для различных категорий
    
    Returns:
        dict: Средние показатели по отраслям
    """
    return {
        'benchmarks': {
            'beauty': {
                'avg_demand_ratio': 6.2,
                'avg_revenue': 2800000,
                'avg_price_ad_ratio': 22.0,
                'avg_organic_percent': 58.0,
                'top_performers_threshold': 75.0
            },
            'home': {
                'avg_demand_ratio': 4.5,
                'avg_revenue': 3200000,
                'avg_price_ad_ratio': 18.5,
                'avg_organic_percent': 62.0,
                'top_performers_threshold': 72.0
            },
            'electronics': {
                'avg_demand_ratio': 3.2,
                'avg_revenue': 5500000,
                'avg_price_ad_ratio': 12.8,
                'avg_organic_percent': 38.0,
                'top_performers_threshold': 65.0
            },
            'clothing': {
                'avg_demand_ratio': 2.8,
                'avg_revenue': 12000000,
                'avg_price_ad_ratio': 9.5,
                'avg_organic_percent': 28.0,
                'top_performers_threshold': 55.0
            }
        },
        'interpretation': {
            'demand_ratio': {
                'excellent': '> 8.0',
                'good': '5.0 - 8.0',
                'average': '2.0 - 5.0',
                'poor': '< 2.0'
            },
            'revenue': {
                'excellent': '> 5M',
                'good': '2M - 5M',
                'average': '500K - 2M',
                'poor': '< 500K'
            },
            'price_ad_ratio': {
                'excellent': '> 30',
                'good': '20 - 30',
                'average': '10 - 20',
                'poor': '< 10'
            },
            'organic_percent': {
                'excellent': '> 70%',
                'good': '50% - 70%',
                'average': '30% - 50%',
                'poor': '< 30%'
            }
        }
    }

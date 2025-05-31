"""
Модуль для расчета рейтинга товарных ниш
"""

class ProductRatingCalculator:
    """Калькулятор рейтинга товарных ниш"""
    
    def __init__(self):
        # Веса метрик по умолчанию (в процентах)
        self.weights = {
            'demand': 30,    # Соотношение запросов/товары
            'revenue': 25,   # Объем выручки
            'ads': 25,       # Эффективность рекламы
            'organic': 20    # Процент органики
        }
        
        # Пороговые значения по умолчанию
        self.thresholds = {
            'min_revenue': 1000000,  # Минимальная выручка (₽/мес)
            'min_demand_ratio': 1.0  # Минимальное соотношение запросов/товары
        }
    
    def update_weights(self, weights):
        """Обновить веса метрик"""
        self.weights.update(weights)
    
    def update_thresholds(self, thresholds):
        """Обновить пороговые значения"""
        self.thresholds.update(thresholds)
    
    def calculate_rating(self, metrics):
        """
        Рассчитать рейтинг товарной ниши
        
        Args:
            metrics (dict): Словарь с метриками
                - demand_ratio: соотношение запросов/товары
                - revenue: выручка категории (₽/мес)
                - price_ad_ratio: соотношение цена/ставка
                - organic_percent: процент органических позиций
        
        Returns:
            dict: Результат расчета с итоговым рейтингом и детализацией
        """
        
        # Нормализация метрик к шкале 0-100
        demand_score = self._calculate_demand_score(metrics['demand_ratio'])
        revenue_score = self._calculate_revenue_score(metrics['revenue'])
        ad_efficiency_score = self._calculate_ad_efficiency_score(metrics['price_ad_ratio'])
        organic_score = self._calculate_organic_score(metrics['organic_percent'])
        
        # Итоговый рейтинг с учетом весов
        final_rating = (
            demand_score * (self.weights['demand'] / 100) +
            revenue_score * (self.weights['revenue'] / 100) +
            ad_efficiency_score * (self.weights['ads'] / 100) +
            organic_score * (self.weights['organic'] / 100)
        )
        
        return {
            'final_rating': round(final_rating, 1),
            'breakdown': {
                'demand': round(demand_score, 1),
                'revenue': round(revenue_score, 1),
                'ad_efficiency': round(ad_efficiency_score, 1),
                'organic': round(organic_score, 1)
            },
            'weights_used': self.weights.copy(),
            'thresholds_used': self.thresholds.copy()
        }
    
    def _calculate_demand_score(self, demand_ratio):
        """Расчет оценки соотношения спроса и предложения"""
        if demand_ratio < self.thresholds['min_demand_ratio']:
            return 0
        
        # Логарифмическая шкала для больших значений
        import math
        score = min(demand_ratio * 15, 100)
        
        # Бонус за очень высокие значения
        if demand_ratio > 10:
            score = min(score * 1.2, 100)
        
        return score
    
    def _calculate_revenue_score(self, revenue):
        """Расчет оценки выручки категории"""
        if revenue < self.thresholds['min_revenue']:
            return 0
        
        # Логарифмическая шкала
        import math
        ratio = revenue / self.thresholds['min_revenue']
        score = min(math.log10(ratio) * 50 + 50, 100)
        
        return max(score, 0)
    
    def _calculate_ad_efficiency_score(self, price_ad_ratio):
        """Расчет оценки эффективности рекламы"""
        if price_ad_ratio <= 0:
            return 0
        
        # Чем выше соотношение цены к ставке, тем лучше
        score = min(price_ad_ratio * 3, 100)
        
        # Бонус за очень высокую эффективность
        if price_ad_ratio > 50:
            score = min(score * 1.1, 100)
        
        return score
    
    def _calculate_organic_score(self, organic_percent):
        """Расчет оценки процента органических позиций"""
        # Прямое соответствие процентам
        return min(max(organic_percent, 0), 100)
    
    def interpret_rating(self, rating):
        """
        Интерпретация рейтинга
        
        Args:
            rating (float): Рейтинг от 0 до 100
        
        Returns:
            tuple: (статус, описание)
        """
        if rating >= 80:
            return "🟢 Отличная ниша", "Низкая конкуренция, высокий потенциал"
        elif rating >= 60:
            return "🟡 Хорошая ниша", "Умеренная конкуренция, хороший потенциал"
        elif rating >= 40:
            return "🟠 Средняя ниша", "Высокая конкуренция, средний потенциал"
        else:
            return "🔴 Плохая ниша", "Очень высокая конкуренция, низкий потенциал"
    
    def get_recommendations(self, result):
        """
        Получить рекомендации на основе результатов анализа
        
        Args:
            result (dict): Результат расчета рейтинга
        
        Returns:
            list: Список рекомендаций
        """
        recommendations = []
        breakdown = result['breakdown']
        
        if breakdown['demand'] < 40:
            recommendations.append({
                'type': 'warning',
                'text': 'Низкое соотношение спроса к предложению. Рассмотрите более узкую нишу.',
                'action': 'Поищите менее насыщенные подкатегории или специализированные товары.'
            })
        
        if breakdown['revenue'] < 30:
            recommendations.append({
                'type': 'warning',
                'text': 'Низкая выручка категории. Проверьте сезонность или рассмотрите другую категорию.',
                'action': 'Изучите тренды продаж по месяцам и рассмотрите альтернативные категории.'
            })
        
        if breakdown['ad_efficiency'] < 40:
            recommendations.append({
                'type': 'warning',
                'text': 'Низкая эффективность рекламы. Высокие рекламные ставки относительно цены товара.',
                'action': 'Подготовьте больший рекламный бюджет или ищите способы снижения ставок.'
            })
        
        if breakdown['organic'] < 50:
            recommendations.append({
                'type': 'warning',
                'text': 'Мало органических позиций. Высокая конкуренция в рекламе.',
                'action': 'Сосредоточьтесь на SEO-оптимизации карточек и накоплении отзывов.'
            })
        
        # Позитивные рекомендации
        if result['final_rating'] >= 70:
            recommendations.append({
                'type': 'success',
                'text': 'Ниша выглядит привлекательно для входа!',
                'action': 'Переходите к детальному анализу конкурентов и планированию входа.'
            })
        elif result['final_rating'] >= 50:
            recommendations.append({
                'type': 'info',
                'text': 'Ниша имеет потенциал, но требует осторожного подхода.',
                'action': 'Подготовьте конкурентную стратегию и достаточный бюджет на продвижение.'
            })
        
        return recommendations
    
    def compare_niches(self, niches_data):
        """
        Сравнить несколько ниш
        
        Args:
            niches_data (list): Список словарей с данными ниш
        
        Returns:
            list: Отсортированный список ниш с рейтингами
        """
        results = []
        
        for niche in niches_data:
            rating_result = self.calculate_rating(niche['metrics'])
            results.append({
                'name': niche.get('name', 'Неизвестная ниша'),
                'rating': rating_result['final_rating'],
                'details': rating_result
            })
        
        # Сортировка по рейтингу (убывание)
        results.sort(key=lambda x: x['rating'], reverse=True)
        
        return results

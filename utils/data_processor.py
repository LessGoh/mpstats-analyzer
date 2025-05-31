import pandas as pd
import numpy as np
import io

class MPStatsDataProcessor:
    """Обработчик файлов MPStats"""
    
    def __init__(self):
        self.supported_files = {
            'niche_selection': ['выбор ниши', 'niche', 'ниша'],
            'seo_results': ['seo', 'результаты поиска', 'search results'],
            'brands_report': ['бренд', 'brand', 'отчет по брендам'],
            'sellers_report': ['продавец', 'seller', 'отчет по продавцам'],
            'products_report': ['товар', 'product', 'похожие товары']
        }
    
    def analyze_file(self, uploaded_file):
        """
        Анализ загруженного файла
        
        Args:
            uploaded_file: Файл, загруженный через Streamlit
        
        Returns:
            dict: Информация о файле
        """
        try:
            file_info = {
                'name': uploaded_file.name,
                'size': uploaded_file.size,
                'type': self._detect_file_type(uploaded_file.name),
                'rows': 0,
                'columns': 0,
                'preview': None,
                'error': None
            }
            
            # Чтение файла в зависимости от расширения
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.csv'):
                # Попробуем разные разделители
                content = uploaded_file.read().decode('utf-8')
                uploaded_file.seek(0)  # Сброс позиции
                
                separators = [';', ',', '\t']
                df = None
                
                for sep in separators:
                    try:
                        df = pd.read_csv(io.StringIO(content), sep=sep)
                        if df.shape[1] > 1:  # Если получили больше одной колонки
                            break
                    except:
                        continue
                
                if df is None or df.shape[1] == 1:
                    # Если не удалось определить разделитель, используем ;
                    df = pd.read_csv(io.StringIO(content), sep=';')
            else:
                raise ValueError(f"Неподдерживаемый формат файла: {uploaded_file.name}")
            
            # Заполнение информации о файле
            file_info['rows'] = len(df)
            file_info['columns'] = len(df.columns)
            file_info['preview'] = df.head(5)
            
            return file_info
            
        except Exception as e:
            file_info['error'] = str(e)
            return file_info
    
    def _detect_file_type(self, filename):
        """
        Определение типа файла по имени
        
        Args:
            filename (str): Имя файла
        
        Returns:
            str: Тип файла
        """
        filename_lower = filename.lower()
        
        for file_type, keywords in self.supported_files.items():
            for keyword in keywords:
                if keyword in filename_lower:
                    return file_type
        
        return 'unknown'
    
    def process_niche_selection_file(self, df):
        """
        Обработка файла "Выбор ниши"
        
        Args:
            df (pandas.DataFrame): Данные файла
        
        Returns:
            dict: Извлеченные метрики
        """
        try:
            metrics = {}
            
            # Поиск колонок с нужными данными
            for col in df.columns:
                col_lower = str(col).lower()
                
                if 'товар' in col_lower or 'product' in col_lower:
                    metrics['total_products'] = df[col].sum() if df[col].dtype in ['int64', 'float64'] else 0
                
                if 'выручка' in col_lower or 'revenue' in col_lower:
                    metrics['total_revenue'] = df[col].sum() if df[col].dtype in ['int64', 'float64'] else 0
                
                if 'продаж' in col_lower or 'sales' in col_lower:
                    metrics['total_sales'] = df[col].sum() if df[col].dtype in ['int64', 'float64'] else 0
            
            return metrics
            
        except Exception as e:
            raise ValueError(f"Ошибка обработки файла выбора ниши: {str(e)}")
    
    def process_seo_results_file(self, df):
        """
        Обработка файла SEO результатов
        
        Args:
            df (pandas.DataFrame): Данные файла
        
        Returns:
            dict: Извлеченные метрики
        """
        try:
            metrics = {}
            
            # Поиск данных о рекламных ставках
            ad_columns = [col for col in df.columns if 'ставка' in str(col).lower() or 'bid' in str(col).lower()]
            if ad_columns:
                ad_rates = df[ad_columns[0]].dropna()
                metrics['avg_ad_rate'] = ad_rates.mean() if len(ad_rates) > 0 else 0
                metrics['median_ad_rate'] = ad_rates.median() if len(ad_rates) > 0 else 0
            
            # Поиск данных о ценах
            price_columns = [col for col in df.columns if 'цена' in str(col).lower() or 'price' in str(col).lower()]
            if price_columns:
                prices = df[price_columns[0]].dropna()
                metrics['avg_price'] = prices.mean() if len(prices) > 0 else 0
                metrics['median_price'] = prices.median() if len(prices) > 0 else 0
            
            # Расчет соотношения цена/ставка
            if 'avg_price' in metrics and 'avg_ad_rate' in metrics and metrics['avg_ad_rate'] > 0:
                metrics['price_ad_ratio'] = metrics['avg_price'] / metrics['avg_ad_rate']
            
            # Поиск органических позиций
            organic_columns = [col for col in df.columns if 'без рекламы' in str(col).lower() or 'organic' in str(col).lower()]
            if organic_columns:
                organic_positions = df[organic_columns[0]].dropna()
                # Подсчет позиций в топ-100
                top_100_organic = len(organic_positions[organic_positions <= 100]) if len(organic_positions) > 0 else 0
                total_top_100 = len(df[df.index <= 100]) if len(df) > 0 else 1
                metrics['organic_percent'] = (top_100_organic / total_top_100) * 100
            
            return metrics
            
        except Exception as e:
            raise ValueError(f"Ошибка обработки SEO файла: {str(e)}")
    
    def process_brands_report_file(self, df):
        """
        Обработка отчета по брендам
        
        Args:
            df (pandas.DataFrame): Данные файла
        
        Returns:
            dict: Извлеченные метрики
        """
        try:
            metrics = {}
            
            # Анализ конкуренции по брендам
            if 'Brand' in df.columns or 'Бренд' in df.columns:
                brand_col = 'Brand' if 'Brand' in df.columns else 'Бренд'
                metrics['total_brands'] = len(df[brand_col].unique())
            
            # Анализ продаж по брендам
            sales_columns = [col for col in df.columns if 'sales' in str(col).lower() or 'продаж' in str(col).lower()]
            if sales_columns:
                total_sales = df[sales_columns[0]].sum() if df[sales_columns[0]].dtype in ['int64', 'float64'] else 0
                metrics['category_sales'] = total_sales
            
            # Анализ выручки по брендам
            revenue_columns = [col for col in df.columns if 'revenue' in str(col).lower() or 'выручка' in str(col).lower()]
            if revenue_columns:
                total_revenue = df[revenue_columns[0]].sum() if df[revenue_columns[0]].dtype in ['int64', 'float64'] else 0
                metrics['category_revenue'] = total_revenue
            
            return metrics
            
        except Exception as e:
            raise ValueError(f"Ошибка обработки отчета по брендам: {str(e)}")
    
    def extract_metrics_from_files(self, file_data_list):
        """
        Извлечение метрик из нескольких файлов
        
        Args:
            file_data_list (list): Список с данными файлов
        
        Returns:
            dict: Объединенные метрики для расчета рейтинга
        """
        combined_metrics = {
            'demand_ratio': 0,
            'revenue': 0,
            'price_ad_ratio': 0,
            'organic_percent': 0
        }
        
        try:
            for file_data in file_data_list:
                file_type = file_data.get('type')
                df = file_data.get('dataframe')
                
                if df is None:
                    continue
                
                if file_type == 'niche_selection':
                    niche_metrics = self.process_niche_selection_file(df)
                    
                    # Примерный расчет соотношения спроса к предложению
                    # В реальности нужны данные о поисковых запросах
                    if 'total_products' in niche_metrics and niche_metrics['total_products'] > 0:
                        # Используем выручку как прокси для спроса
                        demand_proxy = niche_metrics.get('total_revenue', 0) / 1000000  # Нормализация
                        combined_metrics['demand_ratio'] = demand_proxy / niche_metrics['total_products'] * 1000
                    
                    combined_metrics['revenue'] = niche_metrics.get('total_revenue', 0)
                
                elif file_type == 'seo_results':
                    seo_metrics = self.process_seo_results_file(df)
                    combined_metrics['price_ad_ratio'] = seo_metrics.get('price_ad_ratio', 0)
                    combined_metrics['organic_percent'] = seo_metrics.get('organic_percent', 0)
                
                elif file_type == 'brands_report':
                    brands_metrics = self.process_brands_report_file(df)
                    if combined_metrics['revenue'] == 0:  # Если не было данных из файла ниш
                        combined_metrics['revenue'] = brands_metrics.get('category_revenue', 0)
            
            return combined_metrics
            
        except Exception as e:
            raise ValueError(f"Ошибка извлечения метрик: {str(e)}")
    
    def validate_metrics(self, metrics):
        """
        Валидация извлеченных метрик
        
        Args:
            metrics (dict): Метрики для валидации
        
        Returns:
            tuple: (bool, list) - (валидны ли метрики, список ошибок)
        """
        errors = []
        
        required_fields = ['demand_ratio', 'revenue', 'price_ad_ratio', 'organic_percent']
        
        for field in required_fields:
            if field not in metrics:
                errors.append(f"Отсутствует поле: {field}")
            elif not isinstance(metrics[field], (int, float)):
                errors.append(f"Неверный тип данных для {field}")
            elif metrics[field] < 0:
                errors.append(f"Отрицательное значение для {field}")
        
        # Специфичные проверки
        if 'organic_percent' in metrics and metrics['organic_percent'] > 100:
            errors.append("Процент органики не может быть больше 100%")
        
        return len(errors) == 0, errors
    
    def get_file_processing_tips(self, file_type):
        """
        Получение советов по подготовке файлов
        
        Args:
            file_type (str): Тип файла
        
        Returns:
            list: Список советов
        """
        tips = {
            'niche_selection': [
                "Убедитесь, что файл содержит данные о количестве товаров в категории",
                "Проверьте наличие данных о выручке категории",
                "Данные должны быть за последний месяц для актуальности"
            ],
            'seo_results': [
                "Файл должен содержать информацию о рекламных ставках",
                "Убедитесь в наличии данных о ценах товаров",
                "Проверьте данные об органических позициях (без рекламы)"
            ],
            'brands_report': [
                "Файл должен содержать данные по всем брендам в категории",
                "Проверьте наличие информации о продажах и выручке",
                "Убедитесь в актуальности данных"
            ],
            'unknown': [
                "Переименуйте файл, включив ключевые слова: 'ниша', 'SEO', 'бренд'",
                "Убедитесь, что файл в формате .xlsx или .csv",
                "Проверьте структуру данных в файле"
            ]
        }
        
        return tips.get(file_type, tips['unknown'])

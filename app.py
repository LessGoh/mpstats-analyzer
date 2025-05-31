import streamlit as st
import pandas as pd
import numpy as np
from utils.calculator import ProductRatingCalculator
from utils.data_processor import MPStatsDataProcessor
from utils.visualizations import create_radar_chart, create_metrics_bar_chart
from data.sample_data import get_sample_data

# Конфигурация страницы
st.set_page_config(
    page_title="Анализатор ниш MPStats",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Инициализация калькулятора
@st.cache_resource
def init_calculator():
    return ProductRatingCalculator()

@st.cache_resource
def init_data_processor():
    return MPStatsDataProcessor()

def main():
    """Основная функция приложения"""
    
    # Заголовок приложения
    st.title("📊 Анализатор ниш MPStats")
    st.markdown("**Инструмент для оценки потенциала товарных ниш на маркетплейсах**")
    
    # Инициализация классов
    calculator = init_calculator()
    data_processor = init_data_processor()
    
    # Боковая панель с настройками
    setup_sidebar(calculator)
    
    # Основной контент
    tab1, tab2, tab3 = st.tabs(["🔍 Анализ ниши", "📁 Загрузка файлов", "ℹ️ Инструкция"])
    
    with tab1:
        manual_analysis_tab(calculator)
    
    with tab2:
        file_upload_tab(data_processor, calculator)
    
    with tab3:
        instructions_tab()

def setup_sidebar(calculator):
    """Настройка боковой панели"""
    st.sidebar.header("⚙️ Настройки анализа")
    
    # Веса для метрик
    st.sidebar.subheader("Веса метрик (%)")
    weights = {}
    weights['demand'] = st.sidebar.slider("Соотношение запросов/товары", 0, 100, 30)
    weights['revenue'] = st.sidebar.slider("Объем выручки", 0, 100, 25)
    weights['ads'] = st.sidebar.slider("Эффективность рекламы", 0, 100, 25)
    weights['organic'] = st.sidebar.slider("Процент органики", 0, 100, 20)
    
    # Проверка суммы весов
    total_weight = sum(weights.values())
    if total_weight != 100:
        st.sidebar.warning(f"⚠️ Сумма весов: {total_weight}%. Рекомендуется 100%")
    
    # Обновление весов в калькуляторе
    calculator.update_weights(weights)
    
    # Пороговые значения
    st.sidebar.subheader("Пороговые значения")
    thresholds = {}
    thresholds['min_revenue'] = st.sidebar.number_input(
        "Мин. выручка категории (₽/мес)", 
        value=1000000, 
        step=100000,
        format="%d"
    )
    thresholds['min_demand_ratio'] = st.sidebar.number_input(
        "Мин. соотношение запросов/товары", 
        value=1.0, 
        step=0.1,
        format="%.1f"
    )
    
    calculator.update_thresholds(thresholds)
    
    # Информация о версии
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Версия:** MVP 1.0")
    st.sidebar.markdown("**Автор:** AI Assistant")

def manual_analysis_tab(calculator):
    """Вкладка ручного анализа"""
    st.header("🔧 Ручной ввод метрик")
    
    col1, col2 = st.columns(2)
    
    with col1:
        demand_ratio = st.number_input(
            "Соотношение запросов/товары", 
            value=5.2, 
            step=0.1,
            help="Количество поисковых запросов на один товар в категории"
        )
        revenue = st.number_input(
            "Выручка категории (₽/мес)", 
            value=2500000, 
            step=100000,
            format="%d",
            help="Общая выручка категории за месяц"
        )
    
    with col2:
        price_ad_ratio = st.number_input(
            "Соотношение цена/ставка", 
            value=25.0, 
            step=0.5,
            help="Отношение средней цены товара к средней рекламной ставке"
        )
        organic_percent = st.number_input(
            "Процент органики (%)", 
            value=65.0, 
            step=1.0, 
            max_value=100.0,
            help="Процент позиций без рекламы в топ-100"
        )
    
    # Кнопки действий
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        analyze_button = st.button("🔍 Анализировать", type="primary")
    
    with col2:
        sample_button = st.button("📋 Загрузить пример")
    
    # Загрузка примера данных
    if sample_button:
        sample_data = get_sample_data()
        st.session_state.update(sample_data)
        st.rerun()
    
    # Анализ данных
    if analyze_button:
        metrics = {
            'demand_ratio': demand_ratio,
            'revenue': revenue,
            'price_ad_ratio': price_ad_ratio,
            'organic_percent': organic_percent
        }
        
        display_analysis_results(calculator, metrics)

def display_analysis_results(calculator, metrics):
    """Отображение результатов анализа"""
    result = calculator.calculate_rating(metrics)
    
    st.header("📈 Результаты анализа")
    
    # Основной рейтинг
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        rating_status, rating_desc = calculator.interpret_rating(result['final_rating'])
        st.metric(
            label="🎯 Итоговый рейтинг ниши",
            value=f"{result['final_rating']}/100",
            help="Чем выше рейтинг, тем лучше ниша для входа"
        )
        st.info(f"{rating_status}: {rating_desc}")
    
    # Детализация по метрикам
    display_metrics_breakdown(result, metrics)
    
    # Визуализации
    display_visualizations(result)
    
    # Рекомендации
    display_recommendations(result)

def display_metrics_breakdown(result, metrics):
    """Отображение детализации по метрикам"""
    st.subheader("📊 Детализация по метрикам")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Спрос/Предложение",
            f"{result['breakdown']['demand']}/100",
            help=f"Входное значение: {metrics['demand_ratio']}"
        )
    
    with col2:
        st.metric(
            "Выручка категории",
            f"{result['breakdown']['revenue']}/100",
            help=f"Входное значение: {metrics['revenue']:,} ₽"
        )
    
    with col3:
        st.metric(
            "Эффективность рекламы",
            f"{result['breakdown']['ad_efficiency']}/100",
            help=f"Входное значение: {metrics['price_ad_ratio']}"
        )
    
    with col4:
        st.metric(
            "Процент органики",
            f"{result['breakdown']['organic']}/100",
            help=f"Входное значение: {metrics['organic_percent']}%"
        )

def display_visualizations(result):
    """Отображение визуализаций"""
    st.subheader("📈 Визуализация")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Радарная диаграмма
        radar_fig = create_radar_chart(result['breakdown'])
        st.plotly_chart(radar_fig, use_container_width=True)
    
    with col2:
        # Столбчатая диаграмма
        bar_fig = create_metrics_bar_chart(result)
        st.plotly_chart(bar_fig, use_container_width=True)

def display_recommendations(result):
    """Отображение рекомендаций"""
    st.subheader("💡 Рекомендации")
    
    recommendations = []
    
    if result['breakdown']['demand'] < 40:
        recommendations.append("⚠️ Низкое соотношение спроса к предложению. Рассмотрите более узкую нишу.")
    
    if result['breakdown']['revenue'] < 30:
        recommendations.append("⚠️ Низкая выручка категории. Проверьте сезонность или рассмотрите другую категорию.")
    
    if result['breakdown']['ad_efficiency'] < 40:
        recommendations.append("⚠️ Низкая эффективность рекламы. Высокие рекламные ставки относительно цены товара.")
    
    if result['breakdown']['organic'] < 50:
        recommendations.append("⚠️ Мало органических позиций. Высокая конкуренция в рекламе.")
    
    if not recommendations:
        recommendations.append("✅ Ниша выглядит привлекательно для входа!")
    
    for rec in recommendations:
        st.write(rec)

def file_upload_tab(data_processor, calculator):
    """Вкладка загрузки файлов"""
    st.header("📁 Загрузка и обработка файлов MPStats")
    
    uploaded_files = st.file_uploader(
        "Выберите отчеты MPStats",
        accept_multiple_files=True,
        type=['xlsx', 'csv'],
        help="Поддерживаются файлы: Выбор ниши, SEO результаты, Отчет по брендам"
    )
    
    if uploaded_files:
        st.subheader("📄 Загруженные файлы")
        
        for file in uploaded_files:
            with st.expander(f"📄 {file.name}"):
                try:
                    # Попытка обработки файла
                    file_info = data_processor.analyze_file(file)
                    st.write(f"**Тип файла:** {file_info['type']}")
                    st.write(f"**Строк:** {file_info['rows']}")
                    st.write(f"**Столбцов:** {file_info['columns']}")
                    
                    if file_info['preview']:
                        st.write("**Превью данных:**")
                        st.dataframe(file_info['preview'])
                
                except Exception as e:
                    st.error(f"Ошибка обработки файла: {str(e)}")
        
        # Кнопка анализа
        if st.button("🔍 Анализировать загруженные файлы"):
            st.info("🚧 Автоматический анализ файлов будет реализован в следующей версии")

def instructions_tab():
    """Вкладка с инструкциями"""
    st.header("ℹ️ Инструкция по использованию")
    
    st.markdown("""
    ## 📋 Поддерживаемые файлы MPStats:
    
    1. **WB Выбор ниши** - для анализа объема выручки и количества товаров
    2. **SEO Результаты поиска** - для анализа рекламных ставок и органических позиций
    3. **Отчет по брендам** - для дополнительной аналитики по конкурентам
    
    ## 🎯 Метрики анализа:
    
    ### 1. Соотношение запросов/товары (по умолчанию 30%)
    - Показывает насыщенность ниши
    - Высокое значение = много запросов на мало товаров = хорошая возможность
    
    ### 2. Объем выручки категории (по умолчанию 25%)
    - Фильтр по минимальной выручке (по умолчанию 1M ₽/мес)
    - Показывает жизнеспособность и размер ниши
    
    ### 3. Эффективность рекламы (по умолчанию 25%)
    - Соотношение цены товара к рекламной ставке
    - Высокое значение = низкие рекламные затраты относительно цены
    
    ### 4. Процент органики (по умолчанию 20%)
    - Доля позиций без рекламы в топ-100
    - Высокое значение = проще войти в нишу без больших рекламных бюджетов
    
    ## 🎚️ Шкала рейтингов:
    
    - **80-100**: 🟢 Отличная ниша - низкая конкуренция, высокий потенциал
    - **60-79**: 🟡 Хорошая ниша - умеренная конкуренция, хороший потенциал
    - **40-59**: 🟠 Средняя ниша - высокая конкуренция, средний потенциал
    - **0-39**: 🔴 Плохая ниша - очень высокая конкуренция, низкий потенциал
    
    ## 🚀 Как использовать:
    
    1. **Настройте веса метрик** в боковой панели согласно вашим приоритетам
    2. **Введите данные вручную** на вкладке "Анализ ниши" или загрузите файлы
    3. **Получите рейтинг** с детализацией и рекомендациями
    4. **Используйте рекомендации** для принятия решения о входе в нишу
    
    ## 💡 Советы:
    
    - Тестируйте разные комбинации весов для ваших целей
    - Сравнивайте несколько ниш перед принятием решения
    - Учитывайте сезонность и тренды рынка
    - Проверяйте данные на актуальность
    """)

if __name__ == "__main__":
    main()

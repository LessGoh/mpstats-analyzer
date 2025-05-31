import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def create_radar_chart(breakdown):
    """
    Создание радарной диаграммы метрик
    
    Args:
        breakdown (dict): Детализация метрик
    
    Returns:
        plotly.graph_objects.Figure: Радарная диаграмма
    """
    categories = [
        'Спрос/Предложение',
        'Выручка категории', 
        'Эффективность рекламы',
        'Процент органики'
    ]
    
    values = [
        breakdown['demand'],
        breakdown['revenue'],
        breakdown['ad_efficiency'],
        breakdown['organic']
    ]
    
    # Замыкаем диаграмму
    values_closed = values + [values[0]]
    categories_closed = categories + [categories[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        name='Метрики ниши',
        line_color='rgb(32, 201, 151)',
        fillcolor='rgba(32, 201, 151, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
                gridcolor='rgba(128, 128, 128, 0.3)'
            ),
            angularaxis=dict(
                tickfont=dict(size=11)
            )
        ),
        showlegend=False,
        title=dict(
            text="Радарная диаграмма метрик",
            x=0.5,
            font=dict(size=14)
        ),
        height=400
    )
    
    return fig

def create_metrics_bar_chart(result):
    """
    Создание столбчатой диаграммы метрик с весами
    
    Args:
        result (dict): Результат расчета рейтинга
    
    Returns:
        plotly.graph_objects.Figure: Столбчатая диаграмма
    """
    breakdown = result['breakdown']
    weights = result['weights_used']
    
    categories = [
        'Спрос/Предложение',
        'Выручка категории',
        'Эффективность рекламы', 
        'Процент органики'
    ]
    
    values = [
        breakdown['demand'],
        breakdown['revenue'],
        breakdown['ad_efficiency'],
        breakdown['organic']
    ]
    
    weight_values = [
        weights['demand'],
        weights['revenue'],
        weights['ads'],
        weights['organic']
    ]
    
    # Взвешенные значения
    weighted_values = [
        values[i] * weight_values[i] / 100 for i in range(len(values))
    ]
    
    # Создание DataFrame для удобства
    df = pd.DataFrame({
        'Метрика': categories,
        'Оценка': values,
        'Вес (%)': weight_values,
        'Взвешенная оценка': weighted_values
    })
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Оценки метрик', 'Вклад в итоговый рейтинг'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Первый график - оценки метрик
    fig.add_trace(
        go.Bar(
            x=df['Метрика'],
            y=df['Оценка'],
            name='Оценка',
            marker_color='lightblue',
            text=df['Оценка'].round(1),
            textposition='outside'
        ),
        row=1, col=1
    )
    
    # Второй график - взвешенные оценки
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    fig.add_trace(
        go.Bar(
            x=df['Метрика'],
            y=df['Взвешенная оценка'],
            name='Взвешенная оценка',
            marker_color=colors,
            text=df['Взвешенная оценка'].round(1),
            textposition='outside'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=400,
        title_text="Анализ метрик и их вклад в рейтинг",
        showlegend=False
    )
    
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(title_text="Оценка (0-100)", row=1, col=1)
    fig.update_yaxes(title_text="Взвешенная оценка", row=1, col=2)
    
    return fig

def create_comparison_chart(comparison_data):
    """
    Создание диаграммы сравнения ниш
    
    Args:
        comparison_data (list): Список данных для сравнения ниш
    
    Returns:
        plotly.graph_objects.Figure: Диаграмма сравнения
    """
    if not comparison_data:
        return go.Figure()
    
    names = [item['name'] for item in comparison_data]
    ratings = [item['rating'] for item in comparison_data]
    
    # Цвета в зависимости от рейтинга
    colors = []
    for rating in ratings:
        if rating >= 80:
            colors.append('#28a745')  # Зеленый
        elif rating >= 60:
            colors.append('#ffc107')  # Желтый
        elif rating >= 40:
            colors.append('#fd7e14')  # Оранжевый
        else:
            colors.append('#dc3545')  # Красный
    
    fig = go.Figure(data=[
        go.Bar(
            x=names,
            y=ratings,
            marker_color=colors,
            text=ratings,
            textposition='outside',
            texttemplate='%{text:.1f}'
        )
    ])
    
    fig.update_layout(
        title="Сравнение рейтингов ниш",
        xaxis_title="Ниши",
        yaxis_title="Рейтинг",
        yaxis=dict(range=[0, 100]),
        height=400
    )
    
    return fig

def create_trend_chart(historical_data):
    """
    Создание графика трендов по времени
    
    Args:
        historical_data (dict): Исторические данные
    
    Returns:
        plotly.graph_objects.Figure: График трендов
    """
    if not historical_data or 'dates' not in historical_data:
        return go.Figure()
    
    fig = go.Figure()
    
    # Добавляем линии для каждой метрики
    metrics = ['demand', 'revenue', 'ads', 'organic']
    metric_names = ['Спрос/Предложение', 'Выручка', 'Реклама', 'Органика']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    for i, metric in enumerate(metrics):
        if metric in historical_data:
            fig.add_trace(go.Scatter(
                x=historical_data['dates'],
                y=historical_data[metric],
                mode='lines+markers',
                name=metric_names[i],
                line=dict(color=colors[i], width=2),
                marker=dict(size=6)
            ))
    
    fig.update_layout(
        title="Тренды метрик по времени",
        xaxis_title="Дата",
        yaxis_title="Значение метрики",
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_distribution_chart(data, metric_name):
    """
    Создание диаграммы распределения значений
    
    Args:
        data (list): Данные для анализа распределения
        metric_name (str): Название метрики
    
    Returns:
        plotly.graph_objects.Figure: Гистограмма распределения
    """
    if not data:
        return go.Figure()
    
    fig = go.Figure(data=[
        go.Histogram(
            x=data,
            nbinsx=20,
            marker_color='lightblue',
            opacity=0.7
        )
    ])
    
    fig.update_layout(
        title=f"Распределение: {metric_name}",
        xaxis_title=metric_name,
        yaxis_title="Частота",
        height=300
    )
    
    return fig

def create_competitive_analysis_chart(competitive_data):
    """
    Создание диаграммы конкурентного анализа
    
    Args:
        competitive_data (dict): Данные о конкурентах
    
    Returns:
        plotly.graph_objects.Figure: Пузырьковая диаграмма
    """
    if not competitive_data:
        return go.Figure()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=competitive_data.get('prices', []),
        y=competitive_data.get('sales', []),
        mode='markers',
        marker=dict(
            size=competitive_data.get('market_share', []),
            color=competitive_data.get('ratings', []),
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Рейтинг"),
            sizemode='diameter',
            sizeref=2.*max(competitive_data.get('market_share', [1]))/40,
            sizemin=4
        ),
        text=competitive_data.get('names', []),
        hovertemplate='<b>%{text}</b><br>' +
                      'Цена: %{x}<br>' +
                      'Продажи: %{y}<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Конкурентный анализ",
        xaxis_title="Цена",
        yaxis_title="Продажи",
        height=500
    )
    
    return fig

def create_rating_gauge(rating):
    """
    Создание шкалы-индикатора рейтинга
    
    Args:
        rating (float): Значение рейтинга
    
    Returns:
        plotly.graph_objects.Figure: Шкала-индикатор
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=rating,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Рейтинг ниши"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "lightgray"},
                {'range': [40, 60], 'color': "yellow"},
                {'range': [60, 80], 'color': "lightgreen"},
                {'range': [80, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    
    return fig

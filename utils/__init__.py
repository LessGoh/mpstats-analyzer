from .calculator import ProductRatingCalculator
from .data_processor import MPStatsDataProcessor
from .visualizations import (
    create_radar_chart,
    create_metrics_bar_chart,
    create_comparison_chart,
    create_rating_gauge
)

__all__ = [
    'ProductRatingCalculator',
    'MPStatsDataProcessor',
    'create_radar_chart',
    'create_metrics_bar_chart',
    'create_comparison_chart',
    'create_rating_gauge'
]

__version__ = '1.0.0'
__author__ = 'AI Assistant'
__description__ = 'Инструменты для анализа товарных ниш MPStats'

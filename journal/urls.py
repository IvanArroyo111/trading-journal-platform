from django.urls import path
from . import views

urlpatterns = [
    # Trade calendar view
    path('calendar/', views.trade_calendar, name='trade-calendar'),

    # Add a new trade
    path('trades/add/', views.add_trade, name='add-trade'),

    # Trade detail, edit, and delete views
    path('trades/<int:trade_id>/', views.trade_detail, name='trade-detail'),
    path('trades/<int:trade_id>/edit/', views.edit_trade, name='edit-trade'),
    path('trades/<int:trade_id>/delete/', views.delete_trade, name='delete-trade'),

    # Reports and analytics
    path('reports/', views.trade_reports, name='trade-reports'),

    # Save journal entry for a trade
    path('trade/<int:trade_id>/save-journal/', views.save_journal_entry, name='save-journal-entry'),

    # Trade log (all trades)
    path('trades/', views.trade_log, name='trade-log'),
]
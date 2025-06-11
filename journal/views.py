from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trade
from .forms import TradeForm
from django.db.models import Avg, Sum, F, ExpressionWrapper, FloatField
from datetime import timedelta
from django.utils.timezone import now
from collections import defaultdict
import calendar
from django.views.decorators.http import require_POST

# ───────────────────────────────────────
# Trade Calendar View
# ───────────────────────────────────────
@login_required
def trade_calendar(request):
    user_trades = Trade.objects.filter(user=request.user).order_by('-date')
    # Annotate each trade with calculated pnl
    trades = Trade.objects.filter(user=request.user).annotate(
        pnl=ExpressionWrapper(
            (F('exit_price') - F('entry_price')) * F('position_size'),
            output_field=FloatField()
        )
    )
    # Aggregate PnL per date for calendar
    daily_pnl = (
        trades
        .values('date')
        .annotate(total_pnl=Sum('pnl'))
        .order_by('date')
    )
    return render(request, "journal/trade_calendar.html", {
        "user_trades": user_trades,
        "daily_pnl": daily_pnl,
    })

# ───────────────────────────────────────
# Trade Journal Views (Add / Edit / Delete)
# ───────────────────────────────────────
@login_required
def add_trade(request):
    if request.method == "POST":
        form = TradeForm(request.POST, request.FILES)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.user = request.user
            trade.save()
            return redirect('dashboard-home')
    else:
        form = TradeForm()
    return render(request, "journal/add_trade.html", {"form": form})

@login_required
def edit_trade(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id, user=request.user)
    if request.method == "POST":
        form = TradeForm(request.POST, request.FILES, instance=trade)
        if form.is_valid():
            form.save()
            return redirect("trade-log")
    else:
        form = TradeForm(instance=trade)
    # Provide screenshot URL if available
    screenshot_url = trade.screenshot.url if trade.screenshot else None
    return render(request, "journal/edit_trade.html", {"form": form, "trade": trade, "screenshot_url": screenshot_url})

@login_required
def delete_trade(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id, user=request.user)
    if request.method == "POST":
        trade.delete()
        return redirect('trade-log')
    return render(request, "journal/delete_confirm.html", {"trade": trade})

# ───────────────────────────────────────
# Trade Details View
# ───────────────────────────────────────
@login_required
def trade_detail(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id, user=request.user)
    tags = [tag.strip() for tag in trade.tags.split(',')] if trade.tags else []
    return render(request, "journal/trade_detail.html", {"trade": trade, "tags": tags})

# ───────────────────────────────────────
# Trade Log View (All Trades)
# ───────────────────────────────────────
@login_required
def trade_log(request):
    trades = Trade.objects.filter(user=request.user).annotate(
        annotated_pnl=ExpressionWrapper(
            (F('exit_price') - F('entry_price')) * F('position_size'),
            output_field=FloatField()
        )
    ).order_by('-date')
    return render(request, "journal/trade_log.html", {"trades": trades})

# ───────────────────────────────────────
# Save Journal Entry View
# ───────────────────────────────────────
@login_required
@require_POST
def save_journal_entry(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id, user=request.user)
    trade.journal_entry = request.POST.get('journal_entry', '')
    trade.save()
    return redirect('trade-detail', trade_id=trade.id)

# ───────────────────────────────────────
# Trade Reports & Analytics View
# ───────────────────────────────────────
@login_required
def trade_reports(request):
    # Date Range Filter
    range_param = request.GET.get('range', '30')
    if range_param == 'all':
        trades = Trade.objects.filter(user=request.user)
        days = 'all'
    else:
        days = int(range_param)
        start_date = now().date() - timedelta(days=days)
        trades = Trade.objects.filter(user=request.user, date__gte=start_date)

    # Key Metrics
    total_pnl = sum((t.exit_price - t.entry_price) * t.position_size for t in trades)
    total_trades = trades.count()
    wins = sum(1 for t in trades if (t.exit_price - t.entry_price) > 0)
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    avg_rr = (
        sum((getattr(t, 'rr', 0) or 0) for t in trades if hasattr(t, 'rr'))
        / total_trades if total_trades > 0 else 0
    )

    # Equity Curve
    sorted_trades = trades.order_by('date')
    equity_dates = []
    equity_values = []
    cumulative_total = 0
    for trade in sorted_trades:
        pnl = (trade.exit_price - trade.entry_price) * trade.position_size
        cumulative_total += float(pnl)
        equity_dates.append(trade.date.strftime('%Y-%m-%d'))
        equity_values.append(round(cumulative_total, 2))

    # Win Rate by Weekday
    weekday_wins = defaultdict(int)
    weekday_total = defaultdict(int)
    for trade in trades:
        day = trade.date.weekday()  # 0 = Monday
        pnl = (trade.exit_price - trade.entry_price) * trade.position_size
        weekday_total[day] += 1
        if pnl > 0:
            weekday_wins[day] += 1
    weekday_labels = [calendar.day_name[i] for i in range(7)]
    weekday_win_rates = [
        round((weekday_wins[i] / weekday_total[i]) * 100, 2) if weekday_total[i] > 0 else 0
        for i in range(7)
    ]

    # PnL by Setup (Pie Chart)
    pnl_by_setup = defaultdict(float)
    for trade in trades:
        setup = trade.setup or "Unknown"
        pnl = (trade.exit_price - trade.entry_price) * trade.position_size
        pnl_by_setup[setup] += float(pnl)
    setup_labels = list(pnl_by_setup.keys())
    setup_values = [round(pnl_by_setup[setup], 2) for setup in setup_labels]

    # Best vs Worst Day
    daily_pnl = defaultdict(float)
    for trade in trades:
        pnl = (trade.exit_price - trade.entry_price) * trade.position_size
        daily_pnl[trade.date] += float(pnl)
    if daily_pnl:
        best_day = max(daily_pnl.items(), key=lambda x: x[1])
        worst_day = min(daily_pnl.items(), key=lambda x: x[1])
    else:
        best_day = worst_day = (None, 0.0)

    # Context for template
    context = {
        "trades": trades,
        "total_pnl": total_pnl,
        "total_trades": total_trades,
        "win_rate": win_rate,
        "avg_rr": avg_rr,
        "range": days,
        "equity_dates": equity_dates,
        "equity_values": equity_values,
        "weekday_labels": weekday_labels,
        "weekday_win_rates": weekday_win_rates,
        "setup_labels": setup_labels,
        "setup_values": setup_values,
        "best_day": {"date": best_day[0], "pnl": round(best_day[1], 2)},
        "worst_day": {"date": worst_day[0], "pnl": round(worst_day[1], 2)},
        "quick_ranges": [30, 60, 90],
    }
    return render(request, 'journal/trade_reports.html', context)
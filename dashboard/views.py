# ───────────────────────────────────────
# Imports
# ───────────────────────────────────────

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from journal.models import Trade  # Import Trade model

# ───────────────────────────────────────
# Dashboard Home View (Post-login landing)
# ───────────────────────────────────────

@login_required
def dashboard_home(request):
    # Get today's date (used to filter current month)
    today = date.today()

    # Get the "days" filter from URL query parameters
    days = request.GET.get('days')

    # Compares trades to the previous month
    compare = request.GET.get('compare')

    # Comparison mode: calculate stats for this and last month
    if compare == "1":
        # Calculate last month and year
        if today.month == 1:
            last_month_year = today.year - 1
            last_month = 12
        else:
            last_month_year = today.year
            last_month = today.month - 1

        # This month trades
        this_month_trades = Trade.objects.filter(
            user=request.user,
            date__year=today.year,
            date__month=today.month
        )

        # Last month trades
        last_month_trades = Trade.objects.filter(
            user=request.user,
            date__year=last_month_year,
            date__month=last_month
        )
    
        # Calculate stats for THIS MONTH
        this_total_pnl = sum(trade.pnl for trade in this_month_trades)
        this_trades_taken = len(this_month_trades)
        this_winners = [trade for trade in this_month_trades if trade.pnl > 0]
        this_win_rate = (len(this_winners) / this_trades_taken) * 100 if this_trades_taken > 0 else 0

        # Average R:R for this month
        this_rr_sum = sum((trade.rr if hasattr(trade, 'rr') and trade.rr is not None else 0) for trade in this_month_trades)
        this_avg_rr = this_rr_sum / this_trades_taken if this_trades_taken > 0 else None

        # Calculate stats for LAST MONTH
        last_total_pnl = sum(trade.pnl for trade in last_month_trades)
        last_trades_taken = len(last_month_trades)
        last_winners = [trade for trade in last_month_trades if trade.pnl > 0]
        last_win_rate = (len(last_winners) / last_trades_taken) * 100 if last_trades_taken > 0 else 0

        last_rr_sum = sum((trade.rr if hasattr(trade, 'rr') and trade.rr is not None else 0) for trade in last_month_trades)
        last_avg_rr = last_rr_sum / last_trades_taken if last_trades_taken > 0 else None

    # Filter trades by "days" parameter or default to current month
    if days:
        if days == "all":
            user_trades = Trade.objects.filter(
                user=request.user
            )
        else:
            try:
                days_int = int(days)
                start_date = today - timedelta(days=days_int)
                user_trades = Trade.objects.filter(
                    user=request.user,
                    date__gte=start_date
                )
            except ValueError:
                # If 'days' is not a valid number, fallback to this month
                user_trades = Trade.objects.filter(
                    user=request.user,
                    date__year=today.year,
                    date__month=today.month
                )
    else:
        # No days param = default to current month
        user_trades = Trade.objects.filter(
            user=request.user,
            date__year=today.year,
            date__month=today.month
        )

    # Total PnL = sum of each trade's pnl
    total_pnl = sum(trade.pnl for trade in user_trades)

    # Winning trades = trades where pnl > 0
    winners = [trade for trade in user_trades if trade.pnl > 0]

    # Win Rate = (# winners / total trades) × 100
    if user_trades:
        win_rate = (len(winners) / len(user_trades)) * 100
    else:
        win_rate = 0

    # Amount of total trades taken
    trades_taken = len(user_trades)

    # Average R:R for all trades
    rr_sum = sum((trade.rr if hasattr(trade, 'rr') and trade.rr is not None else 0) for trade in user_trades)
    avg_rr = rr_sum / trades_taken if trades_taken > 0 else None

    # Trades sorted by their individual dates (for equity curve)
    sorted_trades = user_trades.order_by('date')

    # Prepare equity curve data
    cumulative_total = 0
    dates = []
    equity_curve = []

    for trade in sorted_trades:
        cumulative_total += trade.pnl
        dates.append(trade.date.strftime("%Y-%m-%d"))
        equity_curve.append(round(cumulative_total, 2))

    # Tracks the last 5 trades taken
    recent_trades = Trade.objects.filter(user=request.user).order_by('-date')[:5]

    # Render template with values passed into context
    return render(request, "dashboard/dashboard_home.html", {
        "total_pnl": total_pnl,
        "win_rate": win_rate,
        "trades_taken": trades_taken,
        "avg_rr": avg_rr,
        "equity_dates": dates,
        "equity_values": equity_curve,
        "recent_trades": recent_trades,

        # Pass comparison stats (even if blank unless compare mode)
        "compare": compare,
        "this_total_pnl": locals().get("this_total_pnl"),
        "this_win_rate": locals().get("this_win_rate"),
        "this_avg_rr": locals().get("this_avg_rr"),
        "this_trades_taken": locals().get("this_trades_taken"),
        "last_total_pnl": locals().get("last_total_pnl"),
        "last_win_rate": locals().get("last_win_rate"),
        "last_avg_rr": locals().get("last_avg_rr"),
        "last_trades_taken": locals().get("last_trades_taken"),
    })

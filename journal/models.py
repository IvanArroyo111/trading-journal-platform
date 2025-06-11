from django.db import models
from django.contrib.auth.models import User

class Trade(models.Model):
    # Link to the user who owns the trade
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Trade basics
    ticker = models.CharField(max_length=10)
    date = models.DateField()

    # Trade execution details
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    exit_price = models.DecimalField(max_digits=10, decimal_places=2)
    position_size = models.IntegerField()

    # Risk management fields
    stop_loss = models.DecimalField(max_digits=10, decimal_places=2)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Strategy and notes
    setup = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=100, blank=True)  # e.g. "fear,mistake,breakout"

    # Optional screenshot of the trade
    screenshot = models.ImageField(upload_to='trade_screenshots/', blank=True, null=True)

    # Optional journal entry for the trade
    journal_entry = models.TextField(blank=True, null=True)

    # Timestamp when the trade is created
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def pnl(self):
        """
        Calculate profit or loss for the trade.
        Returns:
            Decimal: The PnL value (exit - entry) * position size.
        """
        return (self.exit_price - self.entry_price) * self.position_size

    @property
    def rr(self):
        """
        Calculate risk/reward ratio for the trade.
        Returns:
            float or None: Reward/risk ratio, or None if not computable.
        """
        # Defensive: handle None and division by zero
        if self.entry_price is None or self.stop_loss is None or self.target_price is None:
            return None
        risk = float(self.entry_price) - float(self.stop_loss)
        reward = float(self.target_price) - float(self.entry_price)
        if risk == 0:
            return None
        return reward / risk


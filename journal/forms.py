from django import forms
from .models import Trade

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = [
            'ticker', 'date', 'entry_price', 'exit_price',
            'position_size', 'stop_loss', 'target_price',
            'setup', 'notes', 'tags', 'screenshot'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

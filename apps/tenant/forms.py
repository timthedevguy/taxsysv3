from django.forms import ModelForm, Select, TextInput, CheckboxInput
from .models import Setting


class SettingForm(ModelForm):
    class Meta:
        model = Setting
        exclude = ['tenant']
        widgets = {
            'start_date': TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'mineral_tax_rate': TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'goo_tax_rate': TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'source': Select(attrs={'class': 'form-control'}),
            'source_type': Select(attrs={'class': 'form-control'}),
            'source_stat': Select(attrs={'class': 'form-control'}),
            'source_modifier': TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'ice_refine_rate': TextInput(attrs={'class': 'form-control', 'type': 'float'}),
            'ore_refine_rate': TextInput(attrs={'class': 'form-control', 'type': 'float'}),
            'moon_refine_rate': TextInput(attrs={'class': 'form-control', 'type': 'float'}),
            'late_fees_enabled': CheckboxInput(attrs={'class': 'custom-control-input'}),
            'late_fee_threshold': TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'late_fee_day': Select(attrs={'class': 'form-control'}),
            'late_fee_charge': TextInput(attrs={'class': 'form-control', 'type': 'number'}),
        }

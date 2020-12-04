from django import forms


class AddCorporationForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput)
    corporation_id = forms.IntegerField(required=True, widget=forms.TextInput)
    ceo_name = forms.CharField(required=True,widget=forms.TextInput)
    ceo_id = forms.IntegerField(required=True, widget=forms.TextInput)

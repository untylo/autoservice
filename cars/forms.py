from django import forms
from .models import *

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']
class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = ['name']

from django import forms
from .models import Client, Car

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'address', 'phone']

class CarForm(forms.ModelForm):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=True, label="Бренд")
    model = forms.ModelChoiceField(queryset=CarModel.objects.none(), required=True, label="Модель")

    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'vin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['model'].queryset = CarModel.objects.filter(brand_id=brand_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['model'].queryset = self.instance.brand.models.order_by('name')
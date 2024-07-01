from django import forms
from .models import Product,BranchStock

class BranchStockForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        label="Producto",
        widget=forms.Select(attrs={'class': 'product-select'})
    )
    stock = forms.IntegerField(
        label="Stock",
        min_value=0,
        widget=forms.NumberInput(attrs={'id': 'id_stock'})
    )

    class Meta:
        model = BranchStock
        fields = ['product', 'stock']

    def __init__(self, *args, **kwargs):
        branch = kwargs.pop('branch', None)
        super().__init__(*args, **kwargs)
        self.branch = branch
        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))
                self.fields['product'].queryset = Product.objects.filter(id=product_id)
            except (ValueError, TypeError):
                pass  # en caso de que el ID no sea válido
    
    def clean_product(self):
        product = self.cleaned_data.get('product')
        if not product:
            raise forms.ValidationError("Seleccione un producto válido.")
        return product

    def save(self, commit=True):
        product = self.cleaned_data.get('product')
        stock = self.cleaned_data.get('stock')
        instance, created = BranchStock.objects.get_or_create(
            product=product, 
            branch=self.branch,
            defaults={'stock': stock}
        )
        if not created:
            instance.stock = stock
            if commit:
                instance.save()
        return instance

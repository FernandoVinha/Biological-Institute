from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['amount', 'currency']
        # Inclua outros campos que você deseja que o usuário preencha no formulário

    # Aqui você pode adicionar métodos de validação personalizados se necessário
    # Por exemplo:
    # def clean_amount(self):
    #     amount = self.cleaned_data.get('amount')
    #     # Adicione aqui a lógica de validação para o 'amount'
    #     return amount

# Outros formulários que você precisar podem ser adicionados aqui

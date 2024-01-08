from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import InvoiceForm
from .models import Invoice
from django.conf import settings
from lnd import *

@login_required
def create_invoice_view(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            print(invoice.user)

            # Gera a fatura LND e define os campos lightning_address e r_hash
            try:
                print("Chamando create_lnd_invoice")
                lnd_invoice = create_lnd_invoice(settings.LND_API_URL, settings.LND_API_PORT, memo=f"{invoice.currency.code} - Valor: {invoice.amount}")
                print("Invoice LND criada:", lnd_invoice)
                invoice.lightning_address = lnd_invoice.get('payment_request')
                invoice.r_hash = lnd_invoice.get('r_hash')
            except Exception as e:
                print(f"Erro ao criar fatura LND: {e}")
                # Pode ser útil para depuração
                raise e
            invoice.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm()  # Um formulário vazio
    
    return render(request, 'invoice/create_invoice.html', {'form': form})

# Adicione outras views relacionadas à Invoice conforme necessário


@login_required
def invoice_list_view(request):
    user = request.user
    invoices = Invoice.objects.filter(user=user)  # Obter todas as invoices do usuário
    return render(request, 'invoice/invoice_list.html', {'invoices': invoices})

from django.urls import path
from . import views

urlpatterns = [
    # ... outras URLs do seu aplicativo ...

    # URL para a criação de uma nova invoice
    path('create-invoice/', views.create_invoice_view, name='create_invoice'),
    path('invoices/', views.invoice_list_view, name='invoice_list'),

    # ... outras URLs que você possa ter ...
]

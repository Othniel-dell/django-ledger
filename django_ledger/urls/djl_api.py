from django.urls import path

from django_ledger import views

urlpatterns = [
    path('entity/<slug:entity_slug>/data/pnl/',
         views.PnLAPIView.as_view(),
         name='entity-json-pnl'),
    path('entity/<slug:entity_slug>/data/net-payables/',
         views.PayableNetAPIView.as_view(),
         name='entity-json-net-payables'),
    path('entity/<slug:entity_slug>/data/net-receivables/',
         views.ReceivableNetAPIView.as_view(),
         name='entity-json-net-receivables'),
    path('unit/<slug:entity_slug>/<slug:unit_slug>/data/pnl/',
         views.PnLAPIView.as_view(),
         name='unit-json-pnl'),
    path('unit/<slug:entity_slug>/<slug:unit_slug>/data/net-payables/',
         views.PayableNetAPIView.as_view(),
         name='unit-json-net-payables'),
    path('unit/<slug:entity_slug>/<slug:unit_slug>/data/net-receivables/',
         views.ReceivableNetAPIView.as_view(),
         name='unit-json-net-receivables'),
]
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
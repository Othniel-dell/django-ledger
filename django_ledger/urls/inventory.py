from django.urls import path

from django_ledger import views

urlpatterns = [
    path('<slug:entity_slug>/list/',
         views.InventoryListView.as_view(),
         name='inventory-list'),
    path('<slug:entity_slug>/recount/',
         views.InventoryRecountView.as_view(),
         name='inventory-recount'),
]
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
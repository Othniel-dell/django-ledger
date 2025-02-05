from django.urls import path
from django_ledger import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('<slug:entity_slug>/list/', views.VendorModelListView.as_view(), name='vendor-list'),
    path('<slug:entity_slug>/create/', views.VendorModelCreateView.as_view(), name='vendor-create'),
    path('<slug:entity_slug>/update/<uuid:vendor_pk>/', views.VendorModelUpdateView.as_view(), name='vendor-update'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
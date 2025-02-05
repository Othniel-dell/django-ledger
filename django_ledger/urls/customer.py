from django.urls import path
from django_ledger import views

urlpatterns = [
    path('<slug:entity_slug>/list/', views.CustomerModelListView.as_view(), name='customer-list'),
    path('<slug:entity_slug>/create/', views.CustomerModelCreateView.as_view(), name='customer-create'),
    path('<slug:entity_slug>/update/<uuid:customer_pk>/',
         views.CustomerModelUpdateView.as_view(),
         name='customer-update'),
]
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
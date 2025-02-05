from django.urls import path

from django_ledger import views

urlpatterns = [
    path('my-dashboard/', views.DashboardView.as_view(), name='home'),
]
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
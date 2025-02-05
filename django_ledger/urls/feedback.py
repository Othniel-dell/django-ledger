from django.urls import path
from django_ledger.views.feedback import BugReportView, RequestNewFeatureView

urlpatterns = [
    path('bug-report/', BugReportView.as_view(), name='bug-report'),
    path('new-feature/', RequestNewFeatureView.as_view(), name='new-feature')
]
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.urls import path
from django_ledger import views

urlpatterns = [
    path('<slug:entity_slug>/list/current/',
         views.LedgerModelListView.as_view(show_current=True),
         name='ledger-list'),
    path('<slug:entity_slug>/list/visible/',
         views.LedgerModelListView.as_view(show_visible=True),
         name='ledger-list-visible'),
    path('<slug:entity_slug>/list/all/',
         views.LedgerModelListView.as_view(show_all=True),
         name='ledger-list-all'),
    path('<slug:entity_slug>/list/year/<int:year>/',
         views.LedgerModelYearListView.as_view(),
         name='ledger-list-year'),
    path('<slug:entity_slug>/list/month/<int:year>/<int:month>',
         views.LedgerModelMonthListView.as_view(),
         name='ledger-list-month'),
    path('<slug:entity_slug>/create/',
         views.LedgerModelCreateView.as_view(),
         name='ledger-create'),
    path('<slug:entity_slug>/detail/<uuid:ledger_pk>/',
         views.LedgerModelUpdateView.as_view(),
         name='ledger-detail'),
    path('<slug:entity_slug>/update/<uuid:ledger_pk>/',
         views.LedgerModelUpdateView.as_view(),
         name='ledger-update'),
    path('<slug:entity_slug>/delete/<uuid:ledger_pk>/',
         views.LedgerModelDeleteView.as_view(),
         name='ledger-delete'),

    # ACTIONS...
    path('<slug:entity_slug>/action/<uuid:ledger_pk>/post/',
         views.LedgerModelModelActionView.as_view(action_name='post'),
         name='ledger-action-post'),
    path('<slug:entity_slug>/action/<uuid:ledger_pk>/post-journal-entries/',
         views.LedgerModelModelActionView.as_view(action_name='post_journal_entries'),
         name='ledger-action-post-journal-entries'),
    path('<slug:entity_slug>/action/<uuid:ledger_pk>/unpost/',
         views.LedgerModelModelActionView.as_view(action_name='unpost'),
         name='ledger-action-unpost'),
    path('<slug:entity_slug>/action/<uuid:ledger_pk>/lock/',
         views.LedgerModelModelActionView.as_view(action_name='lock'),
         name='ledger-action-lock'),
    path('<slug:entity_slug>/action/<uuid:ledger_pk>/lock-journal-entries/',
         views.LedgerModelModelActionView.as_view(action_name='lock_journal_entries'),
         name='ledger-action-lock-journal-entries'),
    path('<slug:entity_slug>/action/<uuid:ledger_pk>/unlock/',
         views.LedgerModelModelActionView.as_view(action_name='unlock'),
         name='ledger-action-unlock'),

    path('<slug:entity_slug>/action/<uuid:ledger_pk>/hide/',
         views.LedgerModelModelActionView.as_view(action_name='hide'),
         name='ledger-action-hide'),
    path('<slug:entity_slug>/action/<uuid:ledger_pk>/unhide/',
         views.LedgerModelModelActionView.as_view(action_name='unhide'),
         name='ledger-action-unhide'),

]
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
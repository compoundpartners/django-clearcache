from django.urls import path
from .views import ClearCacheAdminView

urlpatterns = [
    path('clear_cache/', ClearCacheAdminView.as_view(), name="clearcache_admin"),
]

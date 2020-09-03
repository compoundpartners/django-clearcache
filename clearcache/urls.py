from django.conf.urls import url
from .views import ClearCacheAdminView

urlpatterns = [
    url(r'clearcache/$', ClearCacheAdminView.as_view(), name="clearcache_admin"),
]

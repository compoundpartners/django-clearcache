from django.conf.urls import url
from .views import ClearCacheAdminView, PurgeCFCache

urlpatterns = [
    url(r'clearcache/cf_cache/$', PurgeCFCache.as_view(), name="clearcache_cf_cache_admin"),
    url(r'clearcache/$', ClearCacheAdminView.as_view(), name="clearcache_admin"),
]

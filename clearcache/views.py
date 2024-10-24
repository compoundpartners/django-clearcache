from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from clearcache.forms import ClearCacheForm, PurgeCFCacheForm
from clearcache.utils import clear_cache


class ClearCacheAdminView(UserPassesTestMixin, FormView):
    form_class = ClearCacheForm
    template_name = "clearcache/admin/clearcache_form.html"

    success_url = reverse_lazy('clearcache_admin')

    def test_func(self):
        # Only super user can clear caches via admin.
        return self.request.user.is_superuser

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, args, kwargs)
        return response

    def form_valid(self, form):
        try:
            cache_name = form.cleaned_data['cache_name']
            clear_cache(cache_name)
            messages.success(self.request, f"Successfully cleared '{form.cleaned_data['cache_name']}' cache")
        except Exception as err:
            messages.error(self.request, f"Couldn't clear cache, something went wrong. Received error: {err}")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clear cache'
        return context


class PurgeCFCache(ClearCacheAdminView):
    form_class = PurgeCFCacheForm
    template_name = "clearcache/admin/clearcache_form.html"

    success_url = reverse_lazy('clearcache_cf_cache_admin')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Purge CF Cache'
        return context

    def form_valid(self, form):
        try:
            urls = form.cleaned_data['urls']
            purge_everything = form.cleaned_data['purge_everything']
            from js_cloudflare.models import purge_cache, purge_all_cache, get_base_url
            base_url = get_base_url()
            urls = [base_url + url.strip() if url.startswith('/') else url.strip() for url in urls.split('\n')]
            if purge_everything:
                if purge_all_cache():
                    messages.success(self.request, "Successfully purged all CF cache")
                else:
                    messages.error(self.request, "Couldn't purged CF cache, something went wrong")
            else:
                if purge_cache(urls):
                    messages.success(self.request, "Successfully purged CF cache")
                else:
                    messages.error(self.request, "Couldn't purged CF cache, something went wrong")
        except ImportError:
            messages.error(self.request, "Couldn't purged CF cache, import error (js_cloudflare)")
        except Exception as err:
            messages.error(self.request, f"Couldn't purged CF cache, something went wrong. Received error: {err}")
        return HttpResponseRedirect(self.success_url)

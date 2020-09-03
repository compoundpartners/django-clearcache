from aldryn_client import forms

class Form(forms.BaseForm):
    def to_settings(self, data, settings):

        settings['INSTALLED_APPS'].insert(
            min(
                settings['INSTALLED_APPS'].index('django.contrib.admin'),
                settings['INSTALLED_APPS'].index('djangocms_admin_style')
            ),
            'clearcache',
        )
        settings['ADDON_URLS'].insert(0, 'clearcache.urls')
        return settings

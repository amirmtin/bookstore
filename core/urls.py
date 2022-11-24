from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf.urls.static import static
from azbankgateways.urls import az_bank_gateways_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("favicon.ico/", RedirectView.as_view(url=staticfiles_storage.url("icon/favicon.svg")),),
    path('account/', include('account.urls', namespace='account')),
    path('', include('store.urls', namespace='store')),
    path('api/', include('store.api.urls', namespace='api')),
    path('bankgateways/', az_bank_gateways_urls()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

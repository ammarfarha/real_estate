from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('main_app.urls', namespace='main')),
    path('users/', include('accounts.urls', namespace='accounts')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('accounts/', include('allauth.urls')),
    path('martor/', include('martor.urls')),
)

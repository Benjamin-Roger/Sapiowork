from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images import urls as wagtailimages_urls


from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language


from search import views as search_views

from .settings import base

from django.conf.urls.static import static

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'^i18n/', include('django.conf.urls.i18n')),
    

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]





urlpatterns += i18n_patterns(
    url(r'', include(wagtail_urls)),
    url(r'^search/$', search_views.search, name='search'),

)


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

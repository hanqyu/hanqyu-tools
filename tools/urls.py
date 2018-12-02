from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

urlpatterns = [
    url(r'^$', views.show_photo, name='Photo'),
    url(r'^$', views.download, name='download'),
    url(r'^download', views.download),
    url(r'^download/[\w_-]\.[\w]$', views.download),
    url(r'^app/download/[\w_-]\.[\w]$', views.download),
    url(r'^media/[\w_-]\.[\w]$', views.download),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

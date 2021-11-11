from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html')
    ),
    path(
        'api/v1/auth/',
        include(
            'authentication.urls',
            namespace='authentication'
        )
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

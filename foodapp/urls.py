from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("blog/", TemplateView.as_view(template_name="blog/index.html")),
    path("create-recipe/", TemplateView.as_view(template_name="create-recipe/index.html")),
    path("", include("base.urls")),
    path("", include("accounts.urls")),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

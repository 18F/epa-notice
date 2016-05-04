from django.conf.urls import include, url
from django.views.generic import TemplateView

from regcore import urls as regcore_urls
from regulations import urls as regsite_urls


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='regulations/nc-homepage.html')),
    url(r'^api/', include(regcore_urls))
] + regsite_urls.urlpatterns

from django.conf import settings
from django.conf.urls import include, url
from django.http import HttpResponse
# from django.views.generic import TemplateView

from regcore import urls as regcore_urls
from regulations import urls as regsite_urls
from regulations.views.notice_home import NoticeHomeView

urlpatterns = [
    url(r'^$', NoticeHomeView.as_view(
        template_name='regulations/nc-homepage.html')),
    url(r'^api/', include(regcore_urls))
] + regsite_urls.urlpatterns

if settings.DISABLE_ROBOTS and settings.DISABLE_ROBOTS.lower() == "true":
    urlpatterns.append(url(r"^robots.txt",
                           lambda r: HttpResponse(
                               "User-agent: *\nDisallow: /",
                               content_type="text/plain")))

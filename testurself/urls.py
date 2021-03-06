"""testurself URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from tests.views import base,signup,index,signin,mission,contact
from tests.views import logout,edit_sec,save_paper,edit_basic,parteners,profile,result_r,rank,dashboard,paper_p,generate_result,instruct_p,finish_t

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^base/$', base),
    url(r'^$', index),
    url(r'^signup/$', signup),
    url(r'^signin/$', signin),
    url(r'^logout/$', logout),
    url(r'^dashboard/$', dashboard),
    url(r'^(.+)/paper/(.+)/$', paper_p),
    url(r'^(.+)/inst/(.+)/$', instruct_p),
    url(r'^generate_result/$', generate_result),
    url(r'^edit_basic/$', edit_basic),
    url(r'^edit_sec/$', edit_sec),
    url(r'^finish_t/(.+)/$', finish_t),
    url(r'^mission/$', mission),
    url(r'^contact/$', contact),
    url(r'^profile/$', profile),
    url(r'^parteners/$', parteners),
    url(r'^result/(.+)/$', result_r),
    url(r'^save_paper/(.+)/$', save_paper),
    url(r'^rank/(.+)/$', rank),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT, })
]
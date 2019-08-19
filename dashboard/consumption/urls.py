from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.SummaryView.as_view(), name='top'),
    url(
        r'^summary/$',
        views.SummaryView.as_view(),
        name='summary',
    ),
    url(
        r'^detail/(?P<user_id>\d+)/$',
        views.DetailView.as_view(),
        name='detail',
    ),
]

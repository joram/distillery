from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    # browsing
    url(r'^still/(?P<still_id>\d+)/$', 'common.views.distillery.distillery', name='distillery'),
    url(r'^$', 'common.views.home.home', name='index'),
    url(r'^stills$', 'common.views.distilleries.distilleries', name='distilleries'),
    url(r'^recipes$', 'common.views.recipes.recipes', name='recipes'),
    url(r'^still/(?P<still_id>\d+)/run/(?P<run_id>\d+)$', 'common.views.distillery.run'),


    # AJAX endpoints
    url(r'^ajax/still/(?P<still_id>\d+)/sensor/(?P<sensor_id>\d+)/$', 'common.views.sensor.recent_data'),
    url(r'^ajax/still/(?P<still_id>\d+)/allsensors/$', 'common.views.sensor.recent_data_all_sensors'),

    # API endpoints
    url(r'^api/sensor/(?P<sensor_id>\d+)/run/(?P<run_id>\d+)$', 'api.views.sensor.sensor_data'),
    url(r'^api/sensor/(?P<sensor_id>\d+)$', 'api.views.sensor.sensor_data'),
    url(r'^api/run/(?P<run_id>\d+)$', 'api.views.sensor.sensor_data'),

    # static and admin stuffs
    url(r'^admin/', include(admin.site.urls)),
   # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

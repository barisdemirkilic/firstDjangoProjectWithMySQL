from django.urls import path

from . import views

app_name = "adapp"

urlpatterns = \
[
    path('', views.IndexView.as_view(), name="index"),
    path('addSqlData/', views.addSqlData, name="addSqlData"),
    path('analyseByCity/', views.analyseByCity, name="analyseByCity"),
    path('clearTables/', views.clearTables, name="clearTables"),
    path('sqldatabase/', views.SqlDatabaseView.as_view(), name="sqldatabase"),
]

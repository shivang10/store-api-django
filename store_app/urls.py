from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.get_data, name='test')

]

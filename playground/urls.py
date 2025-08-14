from django.urls import path
from . import views


# URLConfiguration for the playground app
urlpatterns = [
    path('hello/', views.say_hello, name='say_hello'),
]

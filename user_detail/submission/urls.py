from django.urls import path
from . import views 

urlpatterns = [
    path('', views.submit_view, name='submit'),
    path("all/", views.submissions_list, name="submissions_list"),

]
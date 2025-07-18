from django.urls import path
from user_management_app.views import *
from . import views


urlpatterns = [

    path('SkillsList/', views.SkillAPIView.as_view())


]

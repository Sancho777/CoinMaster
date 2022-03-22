from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('sobre', views.aboutPage, name='about'),
    path('indicador', views.indicatorPage, name='indicator'),

    path('account/create/', views.signupView, name='signup'),
    path('account/signin/', views.signinView, name='signin'),
    path('account/signout/', views.signoutView, name='signout'),

]

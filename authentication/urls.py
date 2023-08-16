from authentication import views
from django.urls import path

urlpatterns = [
    path('', views.signIn,name="login"),
    path('signup', views.signUp,name="signup"),
    path('home', views.home,name="home"),
    path('logout', views.signout,name="logout"),

]
from django.contrib import admin 
from django.urls import path 
from journal import views

urlpatterns = [ 
path('',views.index,name="home"),
path('entries/',views.entries,name="entries"),
path('mygallery/',views.mygallery,name="mygallery"),   
path('reviews/',views.reviews,name="reviews"), 
path('signout/',views.signout,name="signout"), 
path('myentries/',views.myentries,name="myentries"),
path('myprofile/',views.myprofile,name="myprofile"),
path('changepassword/',views.changepassword,name="changepassword"),
path('myfavourites/',views.myfavourites,name="fav"),
path('usersignup/',views.user_signup,name="usersignup"),
path('userlogin/',views.user_login,name="userlogin"),
path('deleteentry/<str:dailytime>/',views.deleteentry,name="deleteentry"),
path('myentries/updateentry/<str:dailytime>/',views.updateentry,name="updateentry"),
path('deletegallery/<str:caption>/',views.deletegallery,name="deletegallery"),
path('deletemyaccount/<str:username>/', views.deletemyaccount, name='deletemyaccount')
]

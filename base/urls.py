from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('preflop/<str:pk>/', views.preflop, name="preflop"),
    path('flop/<str:pk>/', views.flop, name="flop"),
    path('turn/<str:pk>/', views.turn, name="turn"),
    path('river/<str:pk>/', views.river, name="river"),
    path('reveal_hand/<str:pk>/', views.reveal_hand, name="reveal_hand"),
    path('fold/<str:pk>/', views.fold, name="fold"),
    
    
    
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]

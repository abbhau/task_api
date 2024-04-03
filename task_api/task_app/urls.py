from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserCreateRetrieve.as_view()),
    path('verf-user/<str:token>/', views.verify_user, name='verf_token'),
    path('login/', views.UserLoginview.as_view()),
    path('logout/', views.UserLogOutView.as_view()),
    path('update/user/<int:pk>/', views.UserUpdateAPI.as_view()),
    path('retrieve/user/<int:pk>/', views.UserRetrieveAPI.as_view()),
    path('listcreate/task/', views.TaskCreateRetrieve.as_view()),
    path('developer/task/', views.TaskForDevelopers.as_view())
]

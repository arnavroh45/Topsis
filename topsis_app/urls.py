from django.urls import path
from . import views

urlpatterns = [
    path('topsis', views.topsis_view, name='topsis_view'),
    path('login', views.loginUser, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('history', views.user_history_view, name='history'),
    path('analysis/<int:id>/', views.view_analysis, name='view_analysis'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_picture, name='upload_picture'),
    path('picture/<int:pk>/', views.picture_detail, name='picture_detail'),
    path('picture/<int:pk>/delete/', views.delete_picture, name='delete_picture'),
    path('recently_uploaded/', views.recently_uploaded, name='recently_uploaded'),
]

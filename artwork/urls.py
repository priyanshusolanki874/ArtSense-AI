from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
    path('upload/', views.upload_artwork, name='upload'),
    path('gallery/', views.gallery, name='gallery'),
    path('artwork/<int:pk>/', views.artwork_detail, name='artwork_detail'),
    path('analyze/<int:pk>/', views.analyze, name='analyze'),
    path('delete/<int:pk>/', views.delete_artwork, name='delete_artwork'),
    path('edit/<int:pk>/', views.edit_artwork, name='edit_artwork'),
]
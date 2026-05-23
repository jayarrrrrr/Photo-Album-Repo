from django.urls import path
from . import views

app_name = 'albums'

urlpatterns = [
    path('albums/', views.AlbumListView.as_view(), name='list'),
    path('albums/create/', views.AlbumCreateView.as_view(), name='create'),
    path('albums/<int:pk>/', views.AlbumDetailView.as_view(), name='detail'),
    path('albums/<int:pk>/edit/', views.AlbumUpdateView.as_view(), name='edit'),
    path('albums/<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='delete'),
    path('albums/<int:album_pk>/photos/add/', views.PhotoCreateView.as_view(), name='photo_add'),
    path('accounts/register/', views.SignUpView.as_view(), name='register'),
    path('photos/<int:pk>/edit/', views.PhotoUpdateView.as_view(), name='photo_edit'),
    path('photos/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo_delete'),
]

from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name = 'index'),
    path('search/', views.search_results,name='search_results'),
    path('user/', views.profile, name='profile'),
    path('comments/<image_id>', views.comments,name='comments'),
    path('like/',views.like_post, name='like_post'),
    path('profile/', views.profile, name='profile'),
    # path('user/<int:id>', views.user_profile, name='user.profile'),
    path('user_profile/<user_id>', views.user_profile,name='user_profile'),
]
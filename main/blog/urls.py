from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path("", HomeViews.as_view(), name="home"),
    path("category/<int:category_id>/", PostByCategory.as_view(), name="category"),
    path("post/<int:pk>/", ViewPost.as_view(), name="views_post"),
    path("post/add-post/", CreatePost.as_view(), name="add_post"),
    path("post/update/<int:pk>/", UpdatePost.as_view(), name="update_post"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('user-posts/', UserPostListView.as_view(), name='user_posts'),
    path('delete_comment/<int:comment_id>/', ViewPost.delete_comment, name='delete_comment'),
    path('signup/', signup, name='signup'),
    path('help/', help, name='help'),
    path('confidence/', confidence, name='confidence'),
    path('doc/', doc, name='doc'),
    path('rules/', rules, name='rules'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
]
from django.conf.urls import url
from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-listing", views.new_listing, name ="new-listing"),
    path("listing/<int:pk>", views.make_bid, name="make-bid"),
    path("makebid", views.bid_manager, name="bid-manager"),
    path("comment-manager", views.comment_manager, name="comment-manager"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('mylistings', views.mylistings,name="mylistings"),
    path('category/<str:category_name>/', views.category),
    
]

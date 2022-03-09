from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("<int:list_id>", views.listing, name="listing"),
    path("category", views.categoryList, name="category"),
    path("<int:list_id>/addBid", views.addBid, name="addBid"),
    path("<int:list_id>/acceptBid", views.acceptBid, name="acceptBid"),
    path("<int:list_id>/addComment", views.addComment, name="addComment"),
    path("<int:list_id>/watchlist", views.watchlist, name="watchlist"),
    path("showWatchlist/<int:user_id>", views.showWatchlist, name="showWatchlist"),
    path("showCategorylist/<str:category>", views.showCategorylist, name="showCategorylist"),
]


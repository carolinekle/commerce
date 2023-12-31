from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing_page, name="listing_page"),
    path("add_watcher/<int:listing_id>", views.add_watcher, name="add_watcher"),
    path("watchlist-page", views.watchlist_page, name ="watchlist_page"),
    path("categories", views.categories_page, name="categories_page"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction")
]

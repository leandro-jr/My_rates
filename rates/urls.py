from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

# router = DefaultRouter()
# router.register("", views.MoviesRatesViewSet)

urlpatterns =[
    path("", views.index, name="index"),
    path("<int:movie_id>", views.movie_details, name="movie_details"),
    path("movie_added/", views.movie_added, name="movie_added"),
    path("<str:movie_id>", views.chosen_movie, name="chosen_movie"),
    path("favicon.png", RedirectView.as_view(url=staticfiles_storage.url("favicon.png")))
]

urlpatterns += staticfiles_urlpatterns()

# urlpatterns =[
#     path("", views.index, name="index"),
#     path("<int:movie_id>", views.movie_details, name="movie_details"),
#     path("movie_added/", views.movie_added, name="movie_added"),
#     path("movies/", views.MoviesRatesViewSet.as_view()),
#     path("movies/<int:movie_id>/", views.MoviesRatesDetail.as_view()),
#     # path("movies/", include(router.urls)),
#     #path("movies/SearchMovie/<str:search_movie>", views.MoviesRatesSearch),
#     path("<str:movie_id>", views.chosen_movie, name="chosen_movie"),
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# router = DefaultRouter()
# router.register("", views.MoviesRatesViewSet)

urlpatterns =[
    path("", views.index, name="index"),
    path("<int:movie_id>", views.movie_details, name="movie_details"),
    path("movie_added/", views.movie_added, name="movie_added"),
    path("<str:movie_id>", views.chosen_movie, name="chosen_movie"),
]

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
from django.urls import path

from . import views

urlpatterns =[
    path("", views.movies_ranking, name="movies_ranking"),
    path("<int:movie_id>", views.movie_details, name="movie_details"),
]
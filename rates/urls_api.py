from django.urls import path
from . import views

urlpatterns =[
    path("", views.api, name="api"),
    path("movies/", views.MoviesRatesViewSet.as_view()),
    path("movies/<int:movie_id>/", views.MoviesRatesDetail.as_view()),
    path("movies/<str:movie_title>/", views.MoviesRatesSearch.as_view()),
]
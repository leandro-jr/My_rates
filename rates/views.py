from django.shortcuts import render
from .models import MoviesRates, MoviesData, MoviesRatesRanking, MoviesRatesWorstRanking
from .forms import SubmitForm, SubmitRate, SubmitSearchMovie, SubmitRanking, SubmitRankingYear, SubmitRankingWorstYear
import requests
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MoviesRatesSerializer, MoviesDataSerializer
from datetime import datetime
from django.conf import settings


# Create your views here.
def index(request):
    """
    Main page. Lists all movies already watched and form to add new movies
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        # Search for new movie to be added to the site using API and display possible matches
        form = SubmitForm(request.POST)
        if form.is_valid():
            movie = form.cleaned_data["movie"]
            api_url = f"https://imdb-api.com/en/API/SearchMovie/{settings.IMDB_KEY}/{movie}"

            response = requests.get(api_url)
            possible_movies = response.json()
            # print(response.json())
            """{'searchType': 'Movie', 'expression': 'inception 2010', 'results': [
                {'id': 'tt1375666', 'resultType': 'Title',
                 'image': 'https://imdb-api.com/images/original/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_Ratio0.6800_AL_.jpg',
                 'title': 'Inception', 'description': '(2010)'}, {'id': 'tt1790736', 'resultType': 'Title',
                                                                  'image': 'https://imdb-api.com/images/original/MV5BMjE0NGIwM2EtZjQxZi00ZTE5LWExN2MtNDBlMjY1ZmZkYjU3XkEyXkFqcGdeQXVyNjMwNzk3Mjk@._V1_Ratio0.6800_AL_.jpg',
                                                                  'title': 'Inception: Motion Comics',
                                                                  'description': '(2010 Video)'},
                {'id': 'tt5295990', 'resultType': 'Title',
                 'image': 'https://imdb-api.com/images/original/MV5BZGFjOTRiYjgtYjEzMS00ZjQ2LTkzY2YtOGQ0NDI2NTVjOGFmXkEyXkFqcGdeQXVyNDQ5MDYzMTk@._V1_Ratio0.6800_AL_.jpg',
                 'title': 'Inception: Jump Right Into the Action', 'description': '(2010 Video)'},
                {'id': 'tt1686778', 'resultType': 'Title',
                 'image': 'https://imdb-api.com/images/original/nopicture.jpg',
                 'title': 'Inception: 4Movie Premiere Special', 'description': '(2010 TV Movie)'},
                {'id': 'tt12960252', 'resultType': 'Title',
                 'image': 'https://imdb-api.com/images/original/nopicture.jpg', 'title': 'Inception Premiere',
                 'description': '(2010)'}], 'errorMessage': ''}"""
            return render(request, "rates/choose_movie.html", {"possible_movies": possible_movies})

        # Search movies on the site
        form_search_movie = SubmitSearchMovie(request.POST)
        if form_search_movie.is_valid():
            movie_search = form_search_movie.cleaned_data["movie_search"]
            movies = MoviesRates.objects.filter(filme__icontains=movie_search)

            context = {
                "movies": movies,
                "count_list": range(1, movies.count() + 1),
                "form": SubmitForm(),
                "form_search_movie": SubmitSearchMovie()
            }
            return render(request, "rates/index.html", context)

    else:
        movies = MoviesRates.objects.all()
        context = {
            "movies": movies,
            "count_list": range(1, movies.count() + 1),
            "form": SubmitForm(),
            "form_search_movie": SubmitSearchMovie()
        }
        return render(request, "rates/index.html", context)


def movie_details(request, movie_id):
    """
    Displays details of the movie
    :param movie_id: int that id the movies on MoviesRate table
    :return: movie_details.html page
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    movie_rate = MoviesRates.objects.get(pk=movie_id)
    movie_data = MoviesData.objects.filter(pk=movie_rate).last()
    return render(request, "rates/movie_details.html", {
        "movie_rate": movie_rate, "movie_data": movie_data
    })


def chosen_movie(request, movie_id):
    """
    When the user wants to add a new movie, he/she enters it on index form. The matches are displayed at
    rates/choose_movie.html. The movie id of the chosen movie is used to collect the movie details using the API and then
    saved on MoviesData table
    :param movie_id: str with movie id used on imdb-api.com
    :return: rates/chosen_movie_data.html
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    api_url = f"https://imdb-api.com/en/API/Title/{settings.IMDB_KEY}/{movie_id}"

    response = requests.get(api_url)
    movie_data = response.json()
    m = MoviesRates(filme=movie_data["title"], nota=0.0, data="25/07/1980")
    m.save()
    last_movie_id = MoviesRates.objects.all().last().id
    movie = MoviesData(id=MoviesRates.objects.get(id=last_movie_id), tconst=movie_data["id"], title=movie_data["title"],
                       year=movie_data["year"], image=movie_data["image"], runtime=movie_data["runtimeMins"],
                       plot=movie_data["plot"], directors=movie_data["directors"], stars=movie_data["stars"],
                       imDbRating=movie_data["imDbRating"])
    movie.save()

    # add to MoviesData
    return render(request, "rates/chosen_movie_data.html", {
        "movie_data": movie_data, "form": SubmitRate()
    })

def movie_added(request):
    """
    Once the user selected the movie to be added, he/she can add a rate and the date the movies was watched. This will
    be saved on MoviesRates table
    :return:
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        form = SubmitRate(request.POST)
        if form.is_valid():
            rate = float(form.cleaned_data["rate"])
            date = form.cleaned_data["date"]
            last_movie = MoviesRates.objects.all().last()
            m = MoviesRates(id=last_movie.id, filme=last_movie.filme, nota=rate, data=date)
            m.save()
            return render(request, "rates/movie_added/movie_added.html", {
                "rate": rate, "date": date
            })


# Ranking
def save_in_ranking(kind_of_rank, year, form):
    """
    From the form it is extracted the movie id of the 10 best/worst movies. This will be used to find the movie in
    MoviesRate table. With the movie found, it is added/upadted on MoviesRatesRanking/MoviesRatesWorstRanking
    :param kind_of_rank: str 'best' if is best movies rank and 'worst' to worst movies rank
    :param year: str with year to be used on the rank
    :param form: form_best_year or form_worst_year info provided by the forms
    """
    if form.is_valid():
        filmes = []
        for i in range(1, 11):
            movie_id = form.cleaned_data[f"movie_choice_{i}"]
            filme = MoviesRates.objects.get(id=movie_id)
            filmes.append(filme)

            # verify if movie is already in ranking and update
            if kind_of_rank == "best":
                movie_in_ranking = MoviesRatesRanking.objects.filter(filme=filme).first()
            elif kind_of_rank == "worst":
                movie_in_ranking = MoviesRatesWorstRanking.objects.filter(filme=filme).first()

            # movie is been updated or added on different year (rewatched)
            if movie_in_ranking is not None:
                if movie_in_ranking.ano == year:
                    if kind_of_rank == "best":
                        movie = MoviesRatesRanking(id=movie_in_ranking.id, position=i, filme=filme, ano=year)
                    elif kind_of_rank == "worst":
                        movie = MoviesRatesWorstRanking(id=movie_in_ranking.id, position=i, filme=filme, ano=year)
                    movie.save()
                else:
                    if kind_of_rank == "best":
                        movie = MoviesRatesRanking(position=i, filme=filme, ano=year)
                    elif kind_of_rank == "worst":
                        movie = MoviesRatesWorstRanking(position=i, filme=filme, ano=year)
                    movie.save()

            # movie is been added to rank for the first time
            else:
                if kind_of_rank == "best":
                    movie = MoviesRatesRanking(position=i, filme=filme, ano=year)
                elif kind_of_rank == "worst":
                    movie = MoviesRatesWorstRanking(position=i, filme=filme, ano=year)
                movie.save()

        # remove duplicated position from ranking after update
        if kind_of_rank == "best":
            MoviesRatesRanking.objects.filter(ano=year).exclude(filme__in=filmes).delete()
        elif kind_of_rank == "worst":
            MoviesRatesWorstRanking.objects.filter(ano=year).exclude(filme__in=filmes).delete()


def movies_ranking(request):
    """
    The /ranking page displays the movies' ranking per year. It has 4 different section. On the top it can be chosen the
     year to be used on the ranking. Secondly there is section where it is possible to create/update the best and worst
     movies' ranking. These information will be saved on MoviesRatesRanking and MoviesRatesWorstRanking tables and
     displayed on the third section. Lastly it displays the movies by month
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    today = datetime.today()
    current_year = today.year
    # Display ranking according to year
    if request.method == "POST":
        if "form_year" in request.POST:
            form = SubmitRanking(request.POST)
            if form.is_valid():
                year = form.cleaned_data["year_choice"]

        # Top 10 per year
        elif "form_best_ranking" in request.POST:
            year = request.POST.get('year')
            form_best_year = SubmitRankingYear(year, request.POST)
            save_in_ranking("best", year, form_best_year)

        # Botton 10 per year
        elif "form_worst_ranking" in request.POST:
            year = request.POST.get('year')
            form_worst_year = SubmitRankingWorstYear(year, request.POST)
            save_in_ranking("worst", year, form_worst_year)

    # when acessed by get, the current year will be used
    elif request.method == "GET":
        year = str(current_year)

    # create dict with months as keys and MoviesRates content as values
    movies = {}
    year_two_digits = year[2:]
    if int(year) < current_year:
        month = 12
    else:
        month = today.month
    for m in range(1, month + 1):
        if m < 10:
            m = str(m)
            movies[m] = (MoviesRates.objects.filter(data__icontains=year).filter(data__startswith=m) |
                         MoviesRates.objects.filter(data__icontains=year).filter(data__startswith='0' + m) |
                         MoviesRates.objects.filter(data__icontains=year_two_digits).filter(data__startswith=m) |
                         MoviesRates.objects.filter(data__icontains=year_two_digits).filter(data__startswith='0' + m)
                         ).order_by("-nota")
        else:
            m = str(m)
            movies[m] = (MoviesRates.objects.filter(data__icontains=year).filter(data__startswith=m) |
                         MoviesRates.objects.filter(data__endswith=year_two_digits).filter(data__startswith=m)).order_by(
                "-nota")

    # count the movies watched on a year
    movies_count = 0
    for query in movies.values():
        movies_count += len(query)

    # best and worst movies to be displayed
    ranking_best_movies = MoviesRatesRanking.objects.all().filter(ano=year).order_by("position")
    ranking_worst_movies = MoviesRatesWorstRanking.objects.all().filter(ano=year).order_by("position")

    return render(request, "rates/ranking.html", {
        "year": year,
        "movies": movies,
        "movies_count": movies_count,
        "form": SubmitRanking(),
        "form_best_year": SubmitRankingYear(year),
        "form_worst_year": SubmitRankingWorstYear(year),
        "ranking_best_movies": ranking_best_movies,
        "ranking_worst_movies": ranking_worst_movies,
    })


# REST API
def api(request):
    """
    :return: render page showing how to use the API
    """
    return render(request, "rates/api.html")


class MoviesRatesViewSet(APIView):
    """
    Return the serialized data from MoviesRates
    """
    def get(self, request, format=None):
        movies = MoviesRates.objects.all()
        # convert info from database to json
        serializer = MoviesRatesSerializer(movies, many=True)
        return Response(serializer.data)


class MoviesRatesDetail(APIView):
    """
    With the movie id(int), movie data is accessed from MovieRates and MovieData tables. These data are then serialized
    to json format
    """
    def get_object(self, movie_id):
        try:
            return MoviesRates.objects.get(pk=movie_id)
        except MoviesRates.DoesNotExist:
            raise Http404

    def get(self, request, movie_id, format=None):
        movie_rate = self.get_object(movie_id)
        serializer_rate = MoviesRatesSerializer(movie_rate)
        movie_data = MoviesData.objects.filter(pk=movie_rate).last()
        serializer_data = MoviesDataSerializer(movie_data)
        return Response(
            {
                'basic': serializer_rate.data,
                'details': serializer_data.data
            }
        )


class MoviesRatesSearch(APIView):
    """
    Search for the movie_title on MoviesRates table and serialize the results
    """
    def get(self, request, movie_title, format=None):
        movies = MoviesRates.objects.filter(filme__icontains=movie_title)
        serializer = MoviesRatesSerializer(movies, many=True)
        return Response(serializer.data)


class MoviesDataViewSet(viewsets.ModelViewSet):
    serializer_class = MoviesDataSerializer
    queryset = MoviesData.objects.all()

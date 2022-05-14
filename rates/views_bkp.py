from django.shortcuts import render
from .models import MoviesRates, MoviesData, MoviesRatesRanking, MoviesRatesWorstRanking
from .forms import SubmitForm, SubmitRate, SubmitSearchMovie, SubmitRanking, SubmitRankingYear, SubmitRankingWorstYear
import requests
from django.http import Http404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MoviesRatesSerializer, MoviesDataSerializer
from datetime import datetime


# Create your views here.
def index(request):
    if request.method == "POST":
        form = SubmitForm(request.POST)
        if form.is_valid():
            movie = form.cleaned_data["movie"]
            imdb_key = "k_k9is2iw9"
            api_url = f"https://imdb-api.com/en/API/SearchMovie/{imdb_key}/{movie}"

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
            # print(response.status_code)  # 200
            # print(response.headers["Content-Type"])  # application/json; charset=utf-8
            return render(request, "rates/choose_movie.html", {"possible_movies": possible_movies})

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
            # return render(request, "rates/choose_movie.html", {"movie": movie})
        # context = {"form": SubmitForm(request.POST)}
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
    movie_rate = MoviesRates.objects.get(pk=movie_id)
    movie_data = MoviesData.objects.filter(pk=movie_rate).last()
    return render(request, "rates/movie_details.html", {
        "movie_rate": movie_rate, "movie_data": movie_data
    })


def chosen_movie(request, movie_id):
    # if request.method == "POST":
    #     form = SubmitForm(request.POST)
    #     if form.is_valid():
    #         rate = form.cleaned_data["rate"]
    #         date = form.cleaned_data["date"]
    #         print(rate, date)
    # else:
    imdb_key = "k_k9is2iw9"
    api_url = f"https://imdb-api.com/en/API/Title/{imdb_key}/{movie_id}"

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
    if request.method == "POST":
        form = SubmitRate(request.POST)
        if form.is_valid():
            rate = float(form.cleaned_data["rate"])
            date = form.cleaned_data["date"]
            last_movie = MoviesRates.objects.all().last()
            m = MoviesRates(id=last_movie.id, filme=last_movie.filme, nota=rate, data=date)
            m.save()
            # MoviesRates.objects.all().last().update(nota=rate, data=date)
            return render(request, "rates/movie_added/movie_added.html", {
                "rate": rate, "date": date
            })



# Ranking

def fill_ranking():
    movies = {}
    if int(year) < current_year:
        month = 12
    else:
        month = last_update.month
    for m in range(1, month + 1):
        if m < 10:
            m = str(m)
            movies[m] = (MoviesRates.objects.filter(data__icontains=year).filter(data__startswith=m) |
                         MoviesRates.objects.filter(data__icontains=year).filter(
                             data__startswith='0' + m)).order_by("-nota")
        else:
            m = str(m)
            movies[m] = MoviesRates.objects.filter(data__icontains=year).filter(data__startswith=m).order_by(
                "-nota")

    ranking_best_movies = MoviesRatesRanking.objects.all().filter(ano=year)
    ranking_worst_movies = MoviesRatesWorstRanking.objects.all().filter(ano=year)

    return render(request, "rates/ranking.html", {
        "year": year,
        "movies": movies,
        "form": SubmitRanking(),
        "form_best_year": SubmitRankingYear(year),
        "form_worst_year": SubmitRankingWorstYear(year),
        "ranking_best_movies": ranking_best_movies,
        "ranking_worst_movies": ranking_worst_movies,
    })

def movies_ranking(request):
    # Display ranking according to year
    if request.method == "POST":
        last_update = datetime.today()
        current_year = last_update.year

        if "form_year" in request.POST:
            form = SubmitRanking(request.POST)
            if form.is_valid():
                year = form.cleaned_data["year_choice"]


                # current_year = datetime.today().year
                movies = {}
                if int(year) < current_year:
                    month = 12
                else:
                    month = last_update.month
                for m in range(1, month + 1):
                    if m < 10:
                        m = str(m)
                        movies[m] = (MoviesRates.objects.filter(data__icontains=year).filter(data__startswith=m) |
                                     MoviesRates.objects.filter(data__icontains=year).filter(
                                         data__startswith='0' + m)).order_by("-nota")
                    else:
                        m = str(m)
                        movies[m] = MoviesRates.objects.filter(data__icontains=year).filter(data__startswith=m).order_by(
                            "-nota")

                ranking_best_movies = MoviesRatesRanking.objects.all().filter(ano=year)
                ranking_worst_movies = MoviesRatesWorstRanking.objects.all().filter(ano=year)

                return render(request, "rates/ranking.html", {
                    "year": year,
                    "movies": movies,
                    "form": SubmitRanking(),
                    "form_best_year": SubmitRankingYear(year),
                    "form_worst_year": SubmitRankingWorstYear(year),
                    "ranking_best_movies": ranking_best_movies,
                    "ranking_worst_movies": ranking_worst_movies,
                })

        # Top 10 per year
        elif "form_best_ranking" in request.POST:
            year = request.POST.get('year')
            form_best_year = SubmitRankingYear(year, request.POST)
            if form_best_year.is_valid():
                # last_update = datetime.today()
                # current_year = last_update.year
                if int(year) < current_year:
                    month = 12
                else:
                    month = last_update.month
                movies = {}
                for m in range(1, month + 1):
                    if m < 10:
                        m = str(m)
                        movies[m] = (MoviesRates.objects.filter(data__icontains=year).filter(data__startswith=m) |
                                     MoviesRates.objects.filter(data__icontains=year).filter(
                                         data__startswith='0' + m)).order_by("-nota")
                    else:
                        m = str(m)
                        movies[m] = MoviesRates.objects.filter(data__icontains=year).filter(data__startswith=m).order_by(
                            "-nota")
                print("Step 4")
                for i in range(1, 11):
                    movie_id = form_best_year.cleaned_data[f"movie_choice_{i}"]
                    filme = MoviesRates.objects.get(id=movie_id)
                    movie = MoviesRatesRanking(position=i, filme=filme, ano=year)
                    movie.save()
                print("Step 5")
                ranking_best_movies = MoviesRatesRanking.objects.all().filter(ano=year)
                ranking_worst_movies = MoviesRatesWorstRanking.objects.all().filter(ano=year)
                print("Step 6")
                return render(request, "rates/ranking.html", {
                    "year": year,
                    "movies": movies,
                    "form": SubmitRanking(),
                    "form_best_year": SubmitRankingYear(year),
                    "form_worst_year": SubmitRankingWorstYear(year),
                    "ranking_best_movies": ranking_best_movies,
                    "ranking_worst_movies": ranking_worst_movies,
                    "last_update": last_update
                })

        # Botton 10 per year
        elif "form_worst_ranking" in request.POST:
            year = request.POST.get('year')
            form_worst_year = SubmitRankingWorstYear(year, request.POST)
            if form_worst_year.is_valid():
                last_update = datetime.today()
                current_year = last_update.year
                if int(year) < current_year:
                    month = 12
                else:
                    month = last_update.month
                movies = {}
                for m in range(1, month + 1):
                    if m < 10:
                        m = str(m)
                        movies[m] = (MoviesRates.objects.filter(data__icontains=year).filter(data__startswith=m) |
                                     MoviesRates.objects.filter(data__icontains=year).filter(
                                         data__startswith='0' + m)).order_by("-nota")
                    else:
                        m = str(m)
                        movies[m] = MoviesRates.objects.filter(data__icontains=year).filter(
                            data__startswith=m).order_by(
                            "-nota")
                for i in range(1, 11):
                    movie_id = form_worst_year.cleaned_data[f"movie_choice_{i}"]
                    filme = MoviesRates.objects.get(id=movie_id)
                    movie = MoviesRatesWorstRanking(position=i, filme=filme, ano=year)
                    movie.save()

                ranking_best_movies = MoviesRatesRanking.objects.all().filter(ano=year)
                ranking_worst_movies = MoviesRatesWorstRanking.objects.all().filter(ano=year)

                return render(request, "rates/ranking.html", {
                    "year": year,
                    "movies": movies,
                    "form": SubmitRanking(),
                    "form_best_year": SubmitRankingYear(year),
                    "form_worst_year": SubmitRankingWorstYear(year),
                    "ranking_best_movies": ranking_best_movies,
                    "ranking_worst_movies": ranking_worst_movies,
                    "last_update": last_update
                })


    # Initial ranking set to current year
    elif request.method == "GET":
        year = str(datetime.today().year)
        month = datetime.today().month
        movies = {}
        for m in range(1, month + 1):
            if m < 10:
                m = str(m)
                movies[m] = (MoviesRates.objects.filter(data__icontains=year).filter(data__startswith=m) |
                          MoviesRates.objects.filter(data__icontains=year).filter(data__startswith='0' + m)).order_by("-nota")
            else:
                m = str(m)
                movies[m] = MoviesRates.objects.filter(data__icontains=year).filter(data__startswith=m).order_by("-nota")

        ranking_best_movies = MoviesRatesRanking.objects.all().filter(ano=year)
        ranking_worst_movies = MoviesRatesWorstRanking.objects.all().filter(ano=year)

        return render(request, "rates/ranking.html", {
            "year": year,
            "movies": movies,
            "form": SubmitRanking(),
            "form_best_year": SubmitRankingYear(year),
            "form_worst_year": SubmitRankingWorstYear(year),
            "ranking_best_movies": ranking_best_movies,
            "ranking_worst_movies": ranking_worst_movies
        })


# REST API
class MoviesRatesViewSet(APIView):
    def get(self, request, format=None):
        movies = MoviesRates.objects.all()
        serializer = MoviesRatesSerializer(movies, many=True)
        return Response(serializer.data)

# class MoviesRatesViewSet(viewsets.ModelViewSet):
#     serializer_class = MoviesRatesSerializer
#     queryset = MoviesRates.objects.all()

class MoviesRatesDetail(APIView):
    def get_object(self, movie_id):
        try:
            return MoviesRates.objects.get(pk=movie_id)
        except MoviesRates.DoesNotExist:
            raise Http404
        # except MoviesData.DoesNotExist:
        #     raise Http404

    def get(self, request, movie_id, format=None):
        movie_rate = self.get_object(movie_id)
        serializer_rate = MoviesRatesSerializer(movie_rate)
        movie_data = MoviesData.objects.filter(pk=movie_rate).last()
        print(movie_data)
        serializer_data = MoviesDataSerializer(movie_data)
        print(serializer_data.data)
        return Response(
            {
                'basic': serializer_rate.data,
                'details': serializer_data.data
            }
        )


class MoviesRatesSearch(APIView):
    def get(self, request, movie_title, format=None):
        movies = MoviesRates.objects.filter(filme__icontains=movie_title)
        print(movies)
        serializer = MoviesRatesSerializer(movies, many=True)
        print(serializer.data)
        return Response(serializer.data)


class MoviesDataViewSet(viewsets.ModelViewSet):
    serializer_class = MoviesDataSerializer
    queryset = MoviesData.objects.all()


# def MoviesRatesSearch(search_movie):
#     serializer = MoviesRatesSerializer
#     movies = MoviesRates.objects.filter(filme__icontains=search_movie)
#     queryset = MoviesRates.objects.
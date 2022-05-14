from django import forms
from datetime import datetime
from .models import MoviesRates


class SubmitForm(forms.Form):
    movie = forms.CharField(label='Movie Name')


class SubmitSearchMovie(forms.Form):
    movie_search = forms.CharField(label='Movie Name')


class SubmitRate(forms.Form):
    rate = forms.DecimalField(label='Rate from 0 to 5', max_value=5, min_value=0)
    date = forms.CharField(label='When the movie was watched')


class SubmitRanking(forms.Form):
    choices = []
    for year in range(datetime.today().year, 2013, -1):
        choices.append((year, year))
    year_choice = forms.ChoiceField(label='Choose Year', choices=choices)


class SubmitRankingYear(forms.Form):
    def __init__(self, year, *args, **kargs):
        super().__init__(*args, **kargs)

        year_two_digits = year[2:]
        movies = (MoviesRates.objects.filter(data__icontains=year) |
                  MoviesRates.objects.filter(data__endswith=year_two_digits)).order_by("-nota")

        choices = []
        for movie in movies:
            choices.append((movie.id, f"{movie.filme}, {movie.nota}, watched: {movie.data}"))
        self.fields['year'].initial = year
        self.fields['movie_choice_1'].choices = choices
        self.fields['movie_choice_2'].choices = choices
        self.fields['movie_choice_3'].choices = choices
        self.fields['movie_choice_4'].choices = choices
        self.fields['movie_choice_5'].choices = choices
        self.fields['movie_choice_6'].choices = choices
        self.fields['movie_choice_7'].choices = choices
        self.fields['movie_choice_8'].choices = choices
        self.fields['movie_choice_9'].choices = choices
        self.fields['movie_choice_10'].choices = choices

    year = forms.CharField(label='Year')
    movie_choice_1 = forms.ChoiceField(label='1')
    movie_choice_2 = forms.ChoiceField(label='2')
    movie_choice_3 = forms.ChoiceField(label='3')
    movie_choice_4 = forms.ChoiceField(label='4')
    movie_choice_5 = forms.ChoiceField(label='5')
    movie_choice_6 = forms.ChoiceField(label='6')
    movie_choice_7 = forms.ChoiceField(label='7')
    movie_choice_8 = forms.ChoiceField(label='8')
    movie_choice_9 = forms.ChoiceField(label='9')
    movie_choice_10 = forms.ChoiceField(label='10')


class SubmitRankingWorstYear(forms.Form):
    def __init__(self, year, *args, **kargs):
        super().__init__(*args, **kargs)
        year_two_digits = year[2:]
        movies = (MoviesRates.objects.filter(data__icontains=year) |
                  MoviesRates.objects.filter(data__endswith=year_two_digits)).order_by("nota")
        choices = []
        for movie in movies:
            choices.append((movie.id, f"{movie.filme}, {movie.nota}, watched: {movie.data}"))
        self.fields['year'].initial = year
        self.fields['movie_choice_1'].choices = choices
        self.fields['movie_choice_2'].choices = choices
        self.fields['movie_choice_3'].choices = choices
        self.fields['movie_choice_4'].choices = choices
        self.fields['movie_choice_5'].choices = choices
        self.fields['movie_choice_6'].choices = choices
        self.fields['movie_choice_7'].choices = choices
        self.fields['movie_choice_8'].choices = choices
        self.fields['movie_choice_9'].choices = choices
        self.fields['movie_choice_10'].choices = choices

    year = forms.CharField(label='Year')
    movie_choice_1 = forms.ChoiceField(label='1')
    movie_choice_2 = forms.ChoiceField(label='2')
    movie_choice_3 = forms.ChoiceField(label='3')
    movie_choice_4 = forms.ChoiceField(label='4')
    movie_choice_5 = forms.ChoiceField(label='5')
    movie_choice_6 = forms.ChoiceField(label='6')
    movie_choice_7 = forms.ChoiceField(label='7')
    movie_choice_8 = forms.ChoiceField(label='8')
    movie_choice_9 = forms.ChoiceField(label='9')
    movie_choice_10 = forms.ChoiceField(label='10')
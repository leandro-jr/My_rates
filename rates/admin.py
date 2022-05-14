from django.contrib import admin

from .models import MoviesRates, MoviesData, MoviesRatesRanking, MoviesRatesWorstRanking

# Register your models here.
admin.site.register(MoviesRates)
admin.site.register(MoviesData)
admin.site.register(MoviesRatesRanking)
admin.site.register(MoviesRatesWorstRanking)
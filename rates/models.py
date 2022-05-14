from django.db import models


# Create your models here.
class MoviesRates(models.Model):
    filme = models.CharField(max_length=256)
    nota = models.FloatField()
    data = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.id}: {self.filme}, nota: {self.nota}"


class MoviesData(models.Model):
    id = models.ForeignKey(MoviesRates, on_delete=models.CASCADE, related_name="movies_rates", primary_key=True)
    tconst = models.CharField(max_length=16)
    title = models.CharField(max_length=256)
    year = models.CharField(max_length=4)
    image = models.URLField()
    runtime = models.CharField(max_length=3)
    plot = models.TextField()
    directors = models.CharField(max_length=128)
    stars = models.CharField(max_length=256)
    imDbRating = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.id}: {self.title}, {self.year}"


class MoviesRatesRanking(models.Model):
    position = models.SmallIntegerField()
    filme = models.ForeignKey(MoviesRates, on_delete=models.PROTECT, related_name="movies_ranking", primary_key=False)
    ano = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.position}: {self.filme}, {self.ano}"


class MoviesRatesWorstRanking(models.Model):
    position = models.SmallIntegerField()
    filme = models.ForeignKey(MoviesRates, on_delete=models.PROTECT, related_name="movies_worst_ranking", primary_key=False)
    ano = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.position}: {self.filme}, {self.ano}"


# class TitleBasics(models.Model):
#     tconst = models.CharField(max_length=16, primary_key=True)
#     primaryTitle = models.CharField(max_length=256)
#     originalTitle = models.CharField(max_length=256)
#     year = models.SmallIntegerField()
#     runtime = models.SmallIntegerField()
#     genres = models.CharField(max_length=512)
#
#     def __str__(self):
#         return f"{self.tconst}: {self.primaryTitle}, year: {self.year}, {self.runtime}min"
#
#
# class Names(models.Model):
#     nconst = models.CharField(max_length=16, primary_key=True)
#     primaryName = models.CharField(max_length=256)
#     birthYear = models.CharField(max_length=4)
#     deathYear = models.CharField(max_length=4)
#     primaryProfession = models.CharField(max_length=256)
#     knownForTitles = models.CharField(max_length=256)
#
#     def __str__(self):
#         return f"{self.nconst}: {self.primaryName}, {self.primaryProfession}"
#
#
# class TitlePrincipals(models.Model):
#     tconst = models.ForeignKey(TitleBasics, on_delete=models.CASCADE, related_name="titles_principals")
#     ordering = models.SmallIntegerField()
#     nconst = models.ForeignKey(Names, on_delete=models.CASCADE, related_name="names_principals")
#     category = models.CharField(max_length=64)
#     job = models.CharField(max_length=64)
#     characters = models.CharField(max_length=256)
#
#     def __str__(self):
#         return f"{self.tconst}: {self.ordering}, {self.nconst}"

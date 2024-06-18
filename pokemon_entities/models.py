from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='pokemon', blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     if self.title and not self.image.name:
    #         self.image.name = f'{self.title}.png'
    #     super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.title}'
class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return f'{self.lat}, {self.lon}'

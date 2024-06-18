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
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE) # или on_delete=models.PROTECT
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(blank=True, null=True)
    disappeared_at = models.DateTimeField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True, default=0, verbose_name='Уровень')
    health = models.IntegerField(blank=True, null=True, default=0, verbose_name='Здоровье')
    strength = models.IntegerField(blank=True, null=True, default=0, verbose_name='Атака')
    defence = models.IntegerField(blank=True, null=True, default=0, verbose_name='Защита')
    stamina = models.IntegerField(blank=True, null=True, default=0, verbose_name='Выносливость')
    def __str__(self):
        return f'{self.pokemon} {self.lat}, {self.lon} {self.appeared_at} - {self.disappeared_at}'

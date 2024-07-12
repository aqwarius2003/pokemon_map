from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name='Название на русском')
    title_en = models.CharField(max_length=200,
                                blank=True,
                                verbose_name='Название на английском')
    title_jp = models.CharField(max_length=200,
                                blank=True,
                                verbose_name='Название на японском')
    image = models.ImageField(upload_to='pokemon', blank=True, null=True, verbose_name='Картинка покемона')
    description = models.TextField(blank=True,
                                   verbose_name='Описание')
    previous_evolution = models.ForeignKey('self',
                                           null=True,
                                           blank=True,
                                           on_delete=models.SET_NULL,
                                           related_name='next_evolutions',
                                           verbose_name='Из кого превратился')


    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)  # или on_delete=models.PROTECT
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Время появления')
    disappeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Время исчезновения')
    level = models.IntegerField(blank=True, null=True, default=0, verbose_name='Уровень')
    health = models.IntegerField(blank=True, null=True, default=0, verbose_name='Здоровье')
    strength = models.IntegerField(blank=True, null=True, default=0, verbose_name='Атака')
    defence = models.IntegerField(blank=True, null=True, default=0, verbose_name='Защита')
    stamina = models.IntegerField(blank=True, null=True, default=0, verbose_name='Выносливость')

    def __str__(self):
        return f'{self.pokemon.title} {self.lat}, {self.lon} {self.appeared_at} - {self.disappeared_at}'

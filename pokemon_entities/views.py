import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity
import logging


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)
logger = logging.getLogger(__name__)

def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    try:
        icon = folium.features.CustomIcon(
            image_url,
            icon_size=(50, 50),
        )
        folium.Marker(
            [lat, lon],
            # Warning! `tooltip` attribute is disabled intentionally
            # to fix strange folium cyrillic encoding bug
            icon=icon,
        ).add_to(folium_map)
    except Exception as e:
        logger.error(f"Ошибка в добавлении покемона: {e}")


def show_all_pokemons(request):
    # with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
    #     pokemons = json.load(database)['pokemons']
    try:
        pokemons = Pokemon.objects.all()
        pokemon_entities = PokemonEntity.objects.all()

        folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

        #проверка путей
        for pokemon_entity in pokemon_entities:
            print(pokemon_entity.pokemon.image)

        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map,
                pokemon_entity.lat, pokemon_entity.lon,
                pokemon_entity.pokemon.image.url if pokemon_entity.pokemon.image else None
            )

        pokemons_on_page = []
        for pokemon in pokemons:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': pokemon.image.url if pokemon.image else None,
                'title_ru': pokemon.title,
            })

        return render(request, 'mainpage.html', context={
            'map': folium_map._repr_html_(),
            'pokemons': pokemons_on_page,
        })
    except Exception as e:
        logger.error(f"Ошибка в show_all_pokemons: {e}")
        raise # Поднимаем ошибку, чтобы Django могла обработать её



def show_pokemon(request, pokemon_id):
    try:
        with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
            pokemons = json.load(database)['pokemons']

        for pokemon in pokemons:
            if pokemon['pokemon_id'] == int(pokemon_id):
                requested_pokemon = pokemon
                break
        else:
            return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

        folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
        for pokemon_entity in requested_pokemon['entities']:
            add_pokemon(
                folium_map, pokemon_entity['lat'],
                pokemon_entity['lon'],
                pokemon['img_url']
            )

        return render(request, 'pokemon.html', context={
            'map': folium_map._repr_html_(), 'pokemon': pokemon
        })
    except Exception as e:
        logger.error(f"Ошибка в show_pokemon: {e}")
        raise  # Поднимаем ошибку, чтобы Django могла обработать её


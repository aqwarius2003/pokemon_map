from django.conf import settings
import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity
import logging
from django.utils.timezone import localtime

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)
logger = logging.getLogger(__name__)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    try:
        if image_url:
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
        logger.error(f"Ошибка в добавлении покемона в функции add_pokemon: {e}")


def get_full_image_url(pokemon, request):
    return request.build_absolute_uri(pokemon.image.url) \
        if pokemon.image \
        else request.build_absolute_uri(DEFAULT_IMAGE_URL)


def show_all_pokemons(request):
    try:
        current_time = localtime()

        pokemons = Pokemon.objects.all()
        pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=current_time, disappeared_at__gte=current_time)

        folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

        for pokemon_entity in pokemon_entities:
            # image_url = None
            add_pokemon(
                folium_map,
                pokemon_entity.lat, pokemon_entity.lon,
                get_full_image_url(pokemon_entity.pokemon, request)
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
        raise  # Поднимаем ошибку, чтобы Django могла обработать её


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon)

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            get_full_image_url(pokemon_entity.pokemon, request)
        )

    pokemon = {
        'pokemon_id': requested_pokemon.id,
        'img_url': get_full_image_url(requested_pokemon, request),
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })



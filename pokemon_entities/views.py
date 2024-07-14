import folium

from django.shortcuts import render
from django.shortcuts import get_object_or_404

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
    return (
        request.build_absolute_uri(pokemon.image.url)
        if pokemon.image
        else request.build_absolute_uri(DEFAULT_IMAGE_URL)
    )


def show_all_pokemons(request):
    try:
        folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
        current_time = localtime()

        pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=current_time, disappeared_at__gte=current_time)

        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map,
                pokemon_entity.lat, pokemon_entity.lon,
                get_full_image_url(pokemon_entity.pokemon, request)
            )

        pokemons = Pokemon.objects.all()
        pokemons_on_page = []
        for pokemon in pokemons:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': get_full_image_url(pokemon, request),
                'title_ru': pokemon.title,
            })

        return render(request, 'mainpage.html', context={
            'map': folium_map._repr_html_(),
            'pokemons': pokemons_on_page,
        })
    except Exception as e:
        logger.error(f"Ошибка в show_all_pokemons: {e}")
        raise


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)

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

    previous_evolution_pokemon = requested_pokemon.previous_evolution
    if previous_evolution_pokemon:
        pokemon['previous_evolution'] = {
            'pokemon_id': previous_evolution_pokemon.id,
            'img_url': get_full_image_url(previous_evolution_pokemon, request),
            'title_ru': previous_evolution_pokemon.title,
        }

    next_evolution_pokemon = requested_pokemon.next_evolutions.first()
    if next_evolution_pokemon:
        pokemon['next_evolution'] = {
            'pokemon_id': next_evolution_pokemon.id,
            'img_url': get_full_image_url(next_evolution_pokemon, request),
            'title_ru': next_evolution_pokemon.title,
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })

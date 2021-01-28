import json

from flask_login import UserMixin
from pip._vendor import requests

from lib.Gamer.DataMapper import DataMapper
from lib.utils import Singleton


class Pokemon(metaclass=Singleton):
    """
    Class used to load data from PokeAPI
    """
    __pokemon_cache = {}

    @classmethod
    def get_pokemon(cls, name):
        if name not in cls.__pokemon_cache:
            with requests.Session() as req:
                cls.__pokemon_cache[name] = json.loads(req.get(f"https://pokeapi.co/api/v2/pokemon/{name}"
                                                               ).content.decode("utf-8"))
        return cls.__pokemon_cache[name]

    @classmethod
    def get_list_pokemons(cls, pok_names):
        pokemons_data = []

        for pokemon in pok_names:
            pokemons_data.append(cls.get_pokemon(pokemon))

        return pokemons_data


class GamerObject(UserMixin):
    def __init__(self, id, name, login, password, pokemon=(), pokemon_data=None):
        self.id = id
        self.name = name
        self.login = login
        self.password = password
        self.pokemon = pokemon
        self.pokemon_data = pokemon_data

    def get_dict(self):
        return {"id": self.id,
                "name": self.name,
                "login": self.login,
                "password": self.password,
                "pokemon": self.pokemon,
                "pokemon_data": self.pokemon_data}

    @staticmethod
    def _get_gamer_pokemons(gamer):
        return Pokemon.get_list_pokemons(gamer['pokemon'])

    @staticmethod
    def from_tuple(gamer_data):
        """Create Gamer object from a given tuple"""
        print(gamer_data)
        return GamerObject(gamer_data[0], gamer_data[1], gamer_data[2], gamer_data[3],
                           gamer_data[4], Pokemon.get_list_pokemons(gamer_data[4]))


class Gamer(metaclass=Singleton):

    def __init__(self):
        self.__data_mapper = DataMapper()

    def _get_gamer(self, query, params):
        """
        Gets gamer from database
        :return: GamerObject or [] if gamer isn't found
        """
        gamer_data = self.__data_mapper.query(query, params)
        if gamer_data:
            gamer_data = GamerObject.from_tuple(gamer_data[0])

        return gamer_data

    def get_by_id(self, gamer_id):
        return self._get_gamer("select_gamer_by_id", gamer_id)

    def get_by_login(self, login):
        return self._get_gamer("select_gamer_by_login", login)

    def get_all_gamers(self):
        raw_gamers = self.__data_mapper.query("select_all_gamers")
        gamers_list = []
        for gamer in raw_gamers:
            gamers_list.append(GamerObject.from_tuple(gamer).get_dict())
        return gamers_list

    def create_gamer(self, gamer_data, last_row_id=False):
        login = gamer_data["login"]

        if self.get_by_login(login):
            return "Given login already exists", 400

        parsed_gamer_data = [gamer_data['name'], login, gamer_data["password"]]

        new_gamer_id = self.__data_mapper.query("insert_new_gamer", (*parsed_gamer_data,), last_row_id=last_row_id)

        if last_row_id:
            return new_gamer_id

    def update_gamer_pokemon(self, gamer_data):
        gamer_login = gamer_data['login']
        gamer_new_pokemon = '{' + gamer_data['pokemon'] + '}'

        self.__data_mapper.query("update_gamer_pokemon", (gamer_new_pokemon, gamer_login))

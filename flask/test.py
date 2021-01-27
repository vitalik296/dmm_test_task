from unittest.mock import MagicMock

import requests

from lib.Gamer.Gamer import Pokemon, Gamer

session = requests.Session()


class TestClient:
    login = "test_1"

    def test_register_gamer(self):
        clients_len = len(Gamer().get_all_gamers())

        session.post("http://localhost:5000/api/gamer", json={"login": self.login,
                                                              "name": "test",
                                                              "password": "password"},
                     headers={"Content-Type": "application/json; charset=UTF-8"})
        assert clients_len + 1 == len(Gamer().get_all_gamers())

    def test_gamer_pokemons_update(self):
        pokemon_count = len(Gamer().get_by_login(self.login).pokemon)

        session.put("http://localhost:5000/api/gamer", json={"login": self.login,
                                                             "pokemon": "ditto"},
                    headers={"Content-Type": "application/json; charset=UTF-8"})

        assert pokemon_count + 1 == len(Gamer().get_by_login(self.login).pokemon)

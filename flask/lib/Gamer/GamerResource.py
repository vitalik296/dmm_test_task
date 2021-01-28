"""
Gamer resource(Flask restfull)
"""

from flask import request
from flask_restful import Resource

from lib.Gamer.Gamer import Gamer


class GamerResource(Resource):
    def __init__(self):
        self._gamer = Gamer()

    def get(self, gamer=None):
        """
        Handler for GET HTTP method
        :param gamer: identifier of a given gamer(if None returns all existing gamers)
        """
        if gamer:
            try:
                gamer = int(gamer)
                gamer = self._gamer.get_by_id(gamer)
            except ValueError:
                gamer = self._gamer.get_by_login(gamer)

            if not gamer:
                return "Gamer does not found", 404
        else:
            gamer = self._gamer.get_all_gamers()

        return gamer.get_dict(), 200

    def post(self):
        """
        Handler for POST HTTP method
        Create new Gamer
        """
        data = request.json
        last_row_id = data.get("last_row_id", None)
        if last_row_id:
            return self._gamer.create_gamer(data), 200
        else:
            self._gamer.create_gamer(data), 200
            return "OK", 200

    def put(self):
        """
        Handler got PUT HTTP method
        Update gamer pokemon list
        """
        data = request.json
        self._gamer.update_gamer_pokemon(data)
        return "OK", 200

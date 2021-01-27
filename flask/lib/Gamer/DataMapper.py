from configparser import ConfigParser

import psycopg2

from lib.utils import Singleton

CF = ConfigParser()
CF.read("etc/config.ini")


class DataMapper(metaclass=Singleton):
    def __init__(self, **kwargs):
        self._queries = {"insert_new_gamer": """INSERT INTO 
                                                    public.Gamer(name, login, password)
                                                 VALUES
                                                    (%s, %s, %s)
                                                 RETURNING
                                                    id;
                                              """,
                         "select_gamer_by_id": """SELECT
                                                        id, name, login, password, pokemon
                                                   FROM
                                                        public.Gamer
                                                   WHERE
                                                        id=%s;
                                                """,
                         "select_all_gamers": """SELECT
                                                    id, name, login, password, pokemon
                                                 FROM
                                                    public.Gamer;
                                              """,
                         "select_gamer_by_login": """SELECT
                                                        id, name, login, password, pokemon
                                                      FROM
                                                        public.Gamer
                                                      WHERE
                                                        login=%s;
                                                   """,
                         "is_exists": """SELECT EXISTS(
                                              SELECT
                                                *
                                              FROM
                                                information_schema.tables 
                                              WHERE
                                                table_name='gamer');
                                      """,
                         "update_gamer_pokemon": """UPDATE
                                                        public.Gamer
                                                     SET
                                                        pokemon=pokemon||%s
                                                     WHERE
                                                        login=%s;
                                                  """
                         }

        try:
            self.database = kwargs['database'] if kwargs.get('database') else CF.get("Database", "database")
            self.user = kwargs['user'] if kwargs.get('user') else CF.get("Database", "user")
            self.host = kwargs['host'] if kwargs.get('host') else CF.get("Database", "host")
            self.port = kwargs['port'] if kwargs.get('port') else CF.get("Database", "port")
            self.password = kwargs['password'] if kwargs.get('password') else CF.get("Database", "password")
        except Exception as ex:
            raise RuntimeError('Cannot connect to DB: {}'.format(ex))

        self.__is_exists()

    def _connect(self):
        return psycopg2.connect(database=self.database, user=self.user, host=self.host, password=self.password,
                                port=self.port)

    def __is_exists(self):
        if not self.query('is_exists')[0][0]:
            self._load_from_schema()

    def _load_from_schema(self, path_name=CF.get("Database", "schema")):
        db = self._connect()
        cursor = db.cursor()
        cursor.execute(open(path_name, "r").read())
        db.commit()
        cursor.close()
        db.close()

    def _dbh(self, query, params=None, last_row_id=False):
        if query in self._queries:
            db = self._connect()
            cursor = db.cursor()
            try:
                if params:
                    cursor.execute(self._queries[query], params)
                else:
                    cursor.execute(self._queries[query])
                db.commit()
            except Exception as ex:
                print('dbh: {} <sql:{}, param:{}>'.format(ex, query, params))
                db.rollback()
                raise ex
            try:
                result = cursor.fetchall()
                lastrowid = cursor.lastrowid
                cursor.close()
                db.close()
                if last_row_id:
                    return result, lastrowid
                return result
            except Exception as ex:
                print(ex)
        else:
            raise Exception("Unknown query")

    def query(self, query, params=None, last_row_id=False):
        if (params is not None) and (not isinstance(params, tuple)):
            params = (params,)
        return self._dbh(query, params, last_row_id=last_row_id)

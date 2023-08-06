from fast_sql_manager.abstractions.sqlite import SQLite
from fast_sql_manager.interfaces.db_config_interface import DBConfigInterface
import sqlite3


class DataBaseConfig(DBConfigInterface):
  """ 
  Inicialização da classe de conexão
  ao banco
  """

  def __init__(self, db_path: str, db_name: str = 'sqlite'):
    self._db_path = db_path
    self.name = db_name


  def get_connection(self):
    mydb = sqlite3.connect(database=self._db_path, check_same_thread=False)
    return mydb


class SQLiteRepository(SQLite):
  def __init__(self, db_path: str):
    super().__init__(db_config=DataBaseConfig(db_path))

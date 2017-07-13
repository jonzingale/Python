from sqlite3 import dbapi2 as sqlite
from pdb import set_trace as st
# This module extends functionality for sqlite3.

ROW_QUERY = 'select ROWID from %s'
TABLE_QUERY = "SELECT name FROM sqlite_master WHERE type='table'"

class sql_ext:
  def __init__(self, dbname):
    self.con = sqlite.connect(dbname)
    self.cur = self.con.cursor()

  def __del__(self):
    self.con.close()

  def qqs(self, query): # String -> [Row]
    resp = self.con.execute(query).fetchall()
    return(resp)

  def qq(self, query): # String -> Row
    resp = self.con.execute(query).fetchone()
    return(resp)

  def row_q(self, tablename): # :: String -> [RowId]
    resp = self.qqs(ROW_QUERY % tablename)
    return([row[0] for row in resp])

  def maketable(self, tablename, *colnames):
    colnames = '(%s)' % ','.join(str(v) for v in colnames)
    self.con.execute('create table %s%s' % (tablename, colnames))

  def droptables(self):
    tables = self.get_tablenames()
    for table in tables:
      self.con.execute(f"drop table {table}")
    self.con.commit()

  def get_tablenames(self): # :: [Table]
    tables = self.qqs(TABLE_QUERY)
    return([table[0] for table in tables])

  def showtablesrows(self):
    tables = self.get_tablenames()
    for table in tables:
      rows = self.con.execute(f"select * from {table}")
      print(f"{table}")
      for row in rows: print(row)
      print('\n')

import rebrick
import json
import sqlite3


# conn = sqlite3.connect('lego.db')
# # print "Opened database successfully";
# cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
# for row in cursor:
#    print(f'ID = {row[0]}')
# #    print "NAME = ", row[1]
# #    print "ADDRESS = ", row[2]
# #    print "SALARY = ", row[3], "\n"

class LegoDBHelper():
   
   def __init__(self) -> None:

      self.API_KEY = "9ae6321fbe86b420e884560f124ce1bd"
      self.piece_id = 98138
      # init rebrick module for general reading
      rebrick.init(self.API_KEY)
      self.conn = conn = sqlite3.connect('lego.db')
      self.conn.row_factory = sqlite3.Row
      # self.cursor = conn.cursor()
      self.create_table()

      pass

   def create_table(self):
      all_tables = self.conn.execute('''SELECT name FROM sqlite_master WHERE type='table' and name='BRICK';''').fetchall()
      if len(all_tables) > 0:
         return
      else:
         self.conn.execute('''CREATE TABLE BRICK
            (ID INTEGER PRIMARY KEY AUTOINCREMENT   NOT  NULL,
            REBRICK_ID      INT                 NOT NULL,
            PIECE_ID        INT                 NOT NULL,
            NAME            TEXT                NOT NULL,
            HEX_CD          CHAR(6)             NOT NULL,
            BRICK_OWL_ID    INT,
            BRICK_LINK_ID   INT,

            LEGO_ID         INT);''')
   

   def retrieve_color_info(self, color_id):
      response = rebrick.lego.get_color(color_id)
      return json.loads(response.read())
   
   def add_row(self, piece, piece_id):
      color_id = piece['color_id']
      color_info = self.retrieve_color_info(color_id)
      print(color_info)
      hex_cd = color_info['rgb']
      name = piece['color_name'] 
      external_ids = color_info['external_ids']
      owl_id = external_ids['BrickOwl']['ext_ids'][0] ##THIS IS A COLOR ID NOT A FUCKING PIECE ID, USELESS INFO FOR THIS SAME WITH NEXT ONE
      link_id = external_ids['BrickLink']['ext_ids'][0]
      # lego_id = external_ids['LEGO']['ext_ids'][0] #old way, maybe a color id on lego site
      if len(piece['elements']) == 0:
         lego_id = 0
      else:
         lego_id = piece['elements'][len(piece['elements'])-1]
      rebrick_id = color_info['id']
      self.conn.execute('INSERT INTO BRICK (REBRICK_ID, PIECE_ID, NAME, HEX_CD, BRICK_OWL_ID, BRICK_LINK_ID, LEGO_ID) VALUES(?, ?, ?, ?, ?, ?, ?)', (rebrick_id, piece_id, name, hex_cd, owl_id, link_id, lego_id))
      pass

   def commit_to_db(self):
      self.conn.commit()
   
   def close_db(self):
      self.conn.close()

   def get_by_piece_id(self, piece_id: int):
      result = self.conn.execute('SELECT * FROM BRICK WHERE PIECE_ID=?', (piece_id,))
      # result = self.conn.execute('SELECT * FROM BRICK WHERE PIECE_ID=? AND NAME NOT LIKE "Trans%"', (piece_id,))
      # print(result.fetchall())
      return result.fetchall()
      pass

   def get_hex_cds_by_id(self, piece_id: int):
      result = self.conn.execute('SELECT HEX_CD FROM BRICK WHERE PIECE_ID=?', (piece_id,))
      print(result.fetchall())
      return result.fetchall()









# conn.execute('''CREATE TABLE COMPANY
#          (ID INT PRIMARY KEY     NOT NULL,
#          NAME           TEXT    NOT NULL,
#          AGE            INT     NOT NULL,
#          ADDRESS        CHAR(50),
#          SALARY         REAL);''')

# conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (1, 'Paul', 32, 'California', 20000.00 )");

# conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");

# conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");

# conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");

# conn.commit()
# print "Records created successfully";
# conn.close()







if __name__ == "__main__":
   

   API_KEY = "9ae6321fbe86b420e884560f124ce1bd"
   # piece_id = 98138 # 98138 is flat dots
   # piece_id = 85861 # 85861 us dots that can still connect with hole?
   piece_id = 6141 # 85861 us dots that can still connect

   # # init rebrick module for general reading
   rebrick.init(API_KEY)

   # # get set info
   response = rebrick.lego.get_set(6608)
   response = rebrick.lego.get_part_colors(piece_id)
   result = json.loads(response.read())

   current_results = []
   # # # #print out elements
   # for res in result['results']:
   #    print(res['elements'])
   count = 0
   found_count = 0
   for res in result['results']:
      count += 1
      print(count)
      res_response = json.loads(rebrick.lego.get_part_color(part_id=piece_id, color_id=res['color_id']).read())
      if res_response['year_to'] >= 2023:
         found_count += 1 
         current_results.append(res)
   
   print(current_results)
   print(found_count)

   # # #print instance of results
   # print(result['results'][0])

   # # # #create helper
   lego_db_helper = LegoDBHelper()

   for piece in current_results:
      lego_db_helper.add_row(piece, piece_id)

   lego_db_helper.commit_to_db()


   lego_db_helper.close_db()

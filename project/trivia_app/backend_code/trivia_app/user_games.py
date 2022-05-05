import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="josh17rog",
  database="project",
  autocommit=True
)
mycursor = mydb.cursor()



class user_games:
    """<user objects"""

    def __init__(self,**kwargs):
        if len(kwargs)==2:
            self.game_id=kwargs["game_id"]
            self.username=kwargs["username"]
            
        elif "username" not in kwargs:
            self.game_id=kwargs["game_id"]
        else:
            self.username=kwargs["username"]

    """<user objects"""

    """<main functions"""
    
    def GetUserArrayGames(self):#getting all id of games by username
        sql_query = "Select game_id from user_games where username=%s"
        value_sql = (self.username,)
        mycursor.execute(sql_query, value_sql)
        arr =  mycursor.fetchall()
        return arr


    def Register_Game(self,id):#register new game
        sql_query = "INSERT INTO user_games (game_id, username) VALUES (%s, %s)"
        value_sql = (id, self.username)
        mycursor.execute(sql_query, value_sql)

    def CreateNewGameId(self):#getting the last game and then returning the id+1
        mycursor.execute("SELECT * FROM user_games WHERE game_id=(SELECT max(game_id) FROM user_games)")
        arara = mycursor.fetchall()
        if arara==[]:
            return 0
        return arara[0][0]+1
    
    def GetUsernameByGameId(self):#getting the username of player that played that game
        sql_query = "SELECT username FROM user_games WHERE game_id=%s"
        value_sql = (self.game_id,)
        mycursor.execute(sql_query, value_sql)
        arara=mycursor.fetchall()
        if arara==[]:
            return 0
        return arara[0][0]



    """main functions>"""

    """<Admin Fuctions"""
    def DeleteAllUserGamesByName(self):#deleting all games of a user
        sql_query="DELETE FROM user_games WHERE username=%s"
        value_sql = (self.username,)
        mycursor.execute(sql_query, value_sql)

    

    """Admin Function>"""
    def ShowGamesTable():#getting all user_games table - to show admins
        mycursor.execute("Select * from user_games")
        return mycursor.fetchall()
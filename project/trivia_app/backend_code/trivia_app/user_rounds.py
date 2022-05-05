import mysql.connector
from .user_games import user_games

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="josh17rog",
  database="project",
  autocommit=True
)

mycursor = mydb.cursor()

class user_rounds(user_games):
    def __init__(self,**kwargs):
        if len(kwargs)==1 and 'question_id' not in kwargs:
            user_games.__init__(self,username=kwargs["username"])
        elif len(kwargs)==1 and 'question_id' not in kwargs:
            self.question_id=kwargs["question_id"]
        else:   
            self.question_id = kwargs["question_id"]
            self.answer= kwargs["answer"]
            if 'username' and 'game_id' in kwargs:
                user_games.__init__(self,game_id=kwargs["game_id"],username=kwargs["username"])
            elif 'username' in kwargs and 'game_id' not in kwargs:
                user_games.__init__(self,game_id=kwargs["game_id"])
         
         







    """<user objects"""

    """<main functions"""
    
    def RegisterUserRound(self):#register new round in data base
        sql_query = "INSERT INTO user_rounds (game_id, question_id, answer) VALUES (%s, %s, %s)"
        value_sql = (self.game_id,self.question_id,self.answer)
        mycursor.execute(sql_query, value_sql)
        mydb.commit()

    







    """main functions>"""

    """<admin functions"""
    def DeleteAllUserRounds(self):#deleting all user rounds by game id
      for item in self.GetUserArrayGames():
        sql_query="DELETE FROM user_rounds WHERE game_id=%s"
        value_sql = (item[0],)
        mycursor.execute(sql_query, value_sql)


    """admin functions>"""

    def ShowRoundsTable():#show table id of rounds - to admin only
        mycursor.execute("Select * from user_rounds")
        return mycursor.fetchall()

    def ReturnUserInfoRounds(self):#going through each round of specific game id and then return it by game_id,number_of_rounds,points_earned
        arara = []
        for item in self.GetUserArrayGames():
            sql_query="Select COUNT(question_id) from user_rounds where game_id=%s"
            value_sql = (item[0],)
            mycursor.execute(sql_query, value_sql)
            value = mycursor.fetchall()
            points=value[0][0]-1
            if points < 0:
                points = 0
            arara.append([item[0],value[0][0]-1,points])
        return arara

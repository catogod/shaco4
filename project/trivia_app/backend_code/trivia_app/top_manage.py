import mysql.connector
import shutil,os

from trivia_app.backend_code.trivia_app.style_item import style_item
from trivia_app.backend_code.trivia_app.user_games import user_games
from trivia_app.backend_code.trivia_app.user_manage import user_manage

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="josh17rog",
  database="project",
  autocommit=True
)
mycursor = mydb.cursor()

class top_manage:

    def __init__(self):
        pass

    def SortByPoints(self):#sorting user by thier points
       mycursor.execute("SELECT username,points,image_id FROM user ORDER BY points DESC LIMIT 10")#GIVES ME ALL ALTHOUGH THE PICTURE
       arara = mycursor.fetchall()
       arara= [list(i) for i in arara]#making it change able
       st=style_item()
       for i in arara:
           i[2]=st.GetItemCharcteristicById(i[2])[3]#changing to the image itself - not sure if works
       return arara#the top 10

    def SortByGames(self):#sorting users by they amount of games
       mycursor.execute("SELECT username,COUNT(username) AS Duplicates FROM user_games GROUP BY username ORDER BY Duplicates DESC LIMIT 10")#GIVES ME ALL ALTHOUGH THE PICTURE
       arara_of_games = mycursor.fetchall()#the array of usernames and games >>> # problem with someting
       arara_of_games= [list(i) for i in arara_of_games]#making it changeable
       st=style_item()
       for i in arara_of_games:
           um = user_manage(username=i[0])#the user
           i.append(um.GetImage_IdOfUserFromData())#appending the image id
           i[2]=st.GetItemCharcteristicById(i[2])[3]#changing to the image itself - not sure if works
       return arara_of_games#the top 10

    
    def SortByRoundsMost(self):#sorting users by they strike of rounds
       mycursor.execute("SELECT game_id,count(game_id)AS Duplicates FROM user_rounds GROUP BY game_id ORDER BY Duplicates DESC LIMIT 10")#GIVES ME ALL ALTHOUGH THE PICTURE
       arara_of_games = mycursor.fetchall()#the array of usernames and games >>>
       arara_of_games= [list(i) for i in arara_of_games]#making it changeable
       st=style_item()
       for i in arara_of_games:
           ug=user_games(game_id=i[0])#putting the id of the game
           um = user_manage(username=ug.GetUsernameByGameId())#the user
           i[0]=um.username#changing the game id to username
           i.append(um.GetImage_IdOfUserFromData())#appending the image id
           i[2]=st.GetItemCharcteristicById(i[2])[3]
       return arara_of_games#the top 10

    def SortByMostStyles(self):#sorting users by their amount of styles
       mycursor.execute("SELECT username,COUNT(username) AS Duplicates FROM user_items GROUP BY username ORDER BY Duplicates DESC LIMIT 10")#GIVES ME ALL ALTHOUGH THE PICTURE
       arara = mycursor.fetchall()
       arara= [list(i) for i in arara]#making it change able
       st=style_item()
       for i in arara:
           um = user_manage(username=i[0])#the user
           i.append(um.GetImage_IdOfUserFromData())#appending the image id
           i[2]=st.GetItemCharcteristicById(i[2])[3]#changing to the image itself - not sure if works
       return arara#the top 10

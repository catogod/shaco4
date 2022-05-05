import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="josh17rog",
    database="project",
    autocommit=True
)

mycursor = mydb.cursor()

#dont forget to do  mydb.commit()


class user_manage:
    """<user objects"""

    def __init__(self, **kwargs):
        if len(kwargs)==3:
            self.username = kwargs["username"]
            self.password = kwargs["password"]
            self.email = kwargs["email"]
            self.points = 0
        elif len(kwargs)==2:
            self.username = kwargs["username"]
            self.password = kwargs["password"]        
        elif 'username' in kwargs:
            self.username=kwargs["username"]
        elif 'email' in kwargs:
            self.email = kwargs["email"]
        else:
            pass


    """user objects>"""


    """<main functions"""

    #check if table is empty

    def if_table_is_empty(self):#check if user table is empty
        mycursor.execute("SELECT COUNT(*) FROM user")
        arr = mycursor.fetchall()#the rows of table
        if arr[0][0] == 0:
            return True
        return False

    def check_if_user_exit(self,username):#checl if user exist by username
        if self.if_table_is_empty() == False:
           sql_query = "Select * from user where username=%s"
           value_sql = (username,)
           mycursor.execute(sql_query, value_sql)
           if len(mycursor.fetchall()) != 0:
            return True
        return False

    def check_user(self, username, password):#check if user exist by username and password
        if self.if_table_is_empty() == False:
          sql_query = "Select * from user where username=%s and password=%s"
          value_sql = (username,password)
          mycursor.execute(sql_query, value_sql)
          if len(mycursor.fetchall()) != 0:
            return True
        return False

    def Register(self):#register a new user
        username = self.username
        password = self.password
        email = self.email
        if self.check_if_user_exit(username) == True:
            return False        
        sql_query = "INSERT INTO user (username, password, email, points, color_id, image_id) VALUES (%s, %s, %s, %s, %s, %s)"
        #aaa should get the none.png and black
        value_sql = (username, password, email, 0, 1, 1)
        mycursor.execute(sql_query, value_sql)
        return True
    
    def Login(self):#login and then return the username for session
        username=self.username
        password=self.password
        if self.check_user(username, password) == True:
            return username # the session - security sucks but no one pay me for the work so, gg es bot jungle diff(seesion cant accept classes because of something and you need do some manipulation to put the class and i dont want work on this - this site is shit )
        return None

    def AddOnePointToUser(self):#adding one point to user
        sql_query = "UPDATE user SET points=%s where username=%s"
        value_sql = (self.GetPointsFromData()+1,self.username)
        mycursor.execute(sql_query, value_sql)

    def BuyItem(self,cost):#taking from user the price of product
        user_money=self.GetPointsFromData()
        if user_money>=cost:
            sql_query = "UPDATE user SET points=%s where username=%s"
            value_sql = (user_money-cost,self.username)
            mycursor.execute(sql_query, value_sql)
            return True
        return False



    """main functions>"""

    """<change email/password"""

    def ChangeEmail(self, new_email):#change user email
        self.email=new_email
        if self.CheckIfEmailExitsInData()==False:
            sql_query = "UPDATE user SET email=%s where username=%s"
            value_sql = (new_email, self.username)
            mycursor.execute(sql_query, value_sql)
            return True
        return False


    def ChangePassword(self, new_password):#change user passowrd
        sql_query = "UPDATE user SET password=%s where username=%s"
        value_sql = (new_password, self.username)
        mycursor.execute(sql_query, value_sql)


    """change email/password>"""


    def ReturnUserMoney(self,username,Rmoney):#return user money after deleting style
        sql_query = "UPDATE user SET points=%s where username=%s"
        value_sql = (int(Rmoney),username)
        mycursor.execute(sql_query, value_sql)

    def CheckIfEmailExitsInData(self):#check if email exist in data base
        sql_query = "Select email from user where email=%s"
        value_sql = (self.email,)
        mycursor.execute(sql_query, value_sql)
        arr = mycursor.fetchall()
        if arr == []:
            return False
        return True

    def UpdateUserPoints(self,points):
        sql_query = "UPDATE user SET points=%s where username=%s"
        value_sql = (points,self.username)
        mycursor.execute(sql_query, value_sql)


    """<Return from data base"""

    #id,username,password,email,points,games_played
    def GetUsernameFromData(self):#usless
        sql_query = "Select username from user where username=%s"
        value_sql = (self.username,)
        mycursor.execute(sql_query, value_sql)
        arr = mycursor.fetchall()
        result = arr[0][0]
        return result  # return username

    def GetPasswordFromData(self):#get password from data base
        sql_query = "Select password from user where username=%s"
        value_sql = (self.username,)
        mycursor.execute(sql_query, value_sql)
        arr = mycursor.fetchall()
        result = arr[0][0]
        return result  # return password

    def GetEmailFromData(self):#get email from data base
        sql_query = "Select email from user where username=%s"
        value_sql = (self.username,)
        mycursor.execute(sql_query, value_sql)
        arr =  mycursor.fetchall()
        result = arr[0][0]
        return result  # return email

    def GetGamesPlayedFromData(self):#get count of user games from data base
        sql_query = "SELECT COUNT(*) from user_games where username=%s"
        value_sql = (self.username,)
        mycursor.execute(sql_query, value_sql)
        arr =  mycursor.fetchall()
        result = arr[0][0]
        return result  # return games played

    def GetPointsFromData(self):# get points of user from data base
        sql_query = "Select points from user where username=%s"
        value_sql = (self.username,)
        mycursor.execute(sql_query, value_sql)
        arr =  mycursor.fetchall()
        result = arr[0][0]
        return result  # return points

    def GetColor_IdOfUserFromData(self):#get id of color of user from data base
        sql_query = "Select color_id from user where username=%s "
        value_sql = (self.username,)
        mycursor.execute(sql_query, value_sql)
        result = mycursor.fetchall()
        return result[0][0]#id of user color
    
    def GetImage_IdOfUserFromData(self):#get id of image of user from data base
        sql_query = "Select image_id from user where username=%s "
        value_sql = (self.username,)
        mycursor.execute(sql_query, value_sql)
        result = mycursor.fetchall()
        return result[0][0]#id of user image
    

    """Return from data base>"""

    """almost h api"""

    def ReturnUserByEmailForAPI(self):#return username by email
        sql_query = "Select * from user where email=%s"
        value_sql = (self.email,)
        mycursor.execute(sql_query, value_sql)
        arara=mycursor.fetchall()
        if arara!=[]:
            return arara[0]#all user data
        return False

    


    """<Admin Functions"""
    def DeleteUserByName(self):#deleting user by username
        sql_query="DELETE FROM user WHERE username=%s"
        value_sql = (self.username,)
        if self.check_if_user_exit(self.username)== True:
            mycursor.execute(sql_query, value_sql)
            return True
        return False
    #later

    def SpecificNoObjectUserMoney(self,username):#get points of user from data base
        sql_query = "Select points from user where username=%s"
        value_sql = (username,)
        mycursor.execute(sql_query, value_sql)
        arr =  mycursor.fetchall()
        result = arr[0][0]
        return result  # return points

    """Admin Function>"""
#yasuo mains irl
   #table show
    def ShowUsersTable():#show table of user - to admins
        mycursor.execute("Select * from user")
        return mycursor.fetchall()



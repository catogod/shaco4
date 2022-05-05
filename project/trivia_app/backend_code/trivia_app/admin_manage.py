from tabnanny import check
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

class admin_manage:
    """<user objects"""

    def __init__(self,**kwargs):#
        if len(kwargs)==2:
          self.username = kwargs["username"]
          self.password = kwargs["password"]
        elif len(kwargs)==1:
            self.username = kwargs["username"]
        pass

    """user objects>"""


    """<main functions"""

    #check if table is empty

    def if_table_is_empty(self):#checks if the table is empty
        mycursor.execute("SELECT COUNT(*) FROM admin_layer2")
        arr = mycursor.fetchall()#the rows of table
        if arr[0][0] == 0:
            return True
        return False

    def check_if_admin_exit(self):#check if admin exist - by name
        if self.if_table_is_empty() == False:
           sql_query = "Select * from admin_layer2 where username=%s"
           value_sql = (self.username,)
           mycursor.execute(sql_query, value_sql)
           if len(mycursor.fetchall()) != 0:
            return True
        return False

    def check_admin(self):#check if admin exist - by name and password
        if self.if_table_is_empty() == False:
          sql_query = "Select * from admin_layer2 where username=%s and password=%s"
          value_sql = (self.username, self.password)
          mycursor.execute(sql_query, value_sql)
          if len(mycursor.fetchall()) != 0:
            return True
        return False

    def Register(self):#register new admin to data base
        if self.check_if_admin_exit() == True:
            return False        
        sql_query = "INSERT INTO admin_layer2 (username, password) VALUES (%s, %s)"
        value_sql = (self.username, self.password)
        mycursor.execute(sql_query, value_sql)
        mydb.commit()
        return True
    
    
    def Login(self):#function that returns admin username if he logins
        if self.check_admin() == True:
            return self.username # the session - security sucks but no one pay me for the work so, gg es bot jungle diff(seesion cant accept classes because of something and you need do some manipulation to put the class and i dont want work on this - this site is shit )
        return None

    def AdminTable(self):
        mycursor.execute("SELECT * from admin_layer2")
        return mycursor.fetchall()
    
    def Delete_Admin_By_Name(self):
        if self.check_admin()==True:
            sql_query = "DELETE FROM admin_layer2 WHERE username=%s"
            value_sql = (self.username,)
            mycursor.execute(sql_query, value_sql)
            return True
        return False


    """main functions>"""


    """<Admin Functions"""
    """Admin Function>"""


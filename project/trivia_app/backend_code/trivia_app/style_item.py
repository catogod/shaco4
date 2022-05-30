import mysql.connector
import shutil,os

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="josh17rog",
  database="project",
  autocommit=True
)
mycursor = mydb.cursor()

class style_item:
  """<user objects"""

  def __init__(self,**kwargs):#
    if len(kwargs)==6:
      self.item_id=kwargs["item_id"]
      self.name=kwargs["name"]
      self.cost=kwargs["cost"]
      self.url=kwargs["url"]
      self.description=kwargs["description"]
      self.type1=kwargs["type1"]
    elif len(kwargs)==5:
      self.item_id=GetNewItemID()
      self.name=kwargs["name"]
      self.cost=kwargs["cost"]
      self.url=kwargs["url"]
      self.description=kwargs["description"]
      self.type1=kwargs["type1"]
    elif len(kwargs)==1:
      self.item_id=kwargs["item_id"]
    else:
      pass
    
  """user objects>"""

  """<main functions"""
  #insert new item(color and photo) - insert into bubble, if table exist , basic and image  
  def _Check_If_No_Items(self):#check if style table exist in data
    mycursor.execute("SELECT COUNT(*) FROM style_item")
    arr = mycursor.fetchall()#the rows of table
    if arr[0][0] == 0:
      return True
    return False

  def InsertNewStyleItem(self):#registering new style to data base
    if self.type1 == "image":
      self.url=str(self.item_id)+"."+CutTheExtension(self.url)
    sql_query = "INSERT INTO style_item (item_id, name, cost, url, description, type) VALUES (%s, %s, %s, %s, %s, %s)"
    value_sql = (self.item_id, self.name, self.cost, self.url, self.description, self.type1)
    mycursor.execute(sql_query, value_sql)
    if self.type1== "image":
      return self.url
    return None
    
  def GetItemCharcteristicById(self,item_id):#getting item charcteristic of item by his id
      sql_query = "SELECT * FROM style_item where item_id=%s"
      value_sql = (item_id,)
      mycursor.execute(sql_query, value_sql)
      arara = mycursor.fetchall()
      if arara!=[]:
       return list(arara[0])#return the only item
      return False

  def CutProductArray(self,arara,i):#cutting a list that sql data base give to me 
    return arara[0][i]

  def DeleteStyleByIdAndReturnIt(self):#delting the style by id and then return it char's - for future needs
    arara_of_style=self.GetItemCharcteristicById(self.item_id)
    if arara_of_style==False:
      return False
    if CheckIfItABasicStyle(arara_of_style[3])==False:#checking if it not basic style
      if arara_of_style!=False:
        sql_query = "DELETE FROM style_item WHERE item_id=%s"
        value_sql = (self.item_id,)
        mycursor.execute(sql_query, value_sql)
        #deleting it from static folder if image
        if arara_of_style[5]=="image":
          os.remove("trivia_app/static/trivia_app/"+arara_of_style[3])#the url of image in folder
        return arara_of_style#returning the cost of product
    return False


  def If_Table_exist(self):#check if the style data base is exist
     mycursor.execute("SELECT COUNT(*) FROM style_item")
     arr = mycursor.fetchall()#the rows of table
     if arr[0][0] == 0:
          return True
     return False
  

    
  """main functions>"""

  
  """<Admin Function"""



  def Add_Basic_Color(self):# adding basic color to data (only one time)
    if CheckForBasicStyles("color")==False:
      sql_query = "INSERT INTO style_item (item_id, name, cost, url, description, type) VALUES (%s, %s, %s, %s, %s, %s)"
      value_sql = (GetNewItemID(), "Black", 0, "black", "A basic black color, can't be removed","color")
      mycursor.execute(sql_query, value_sql)

  def Add_Basic_Image(self):# adding basic color to data and code folder (only one time)
    if CheckForBasicStyles("image")==False:
      sql_query = "INSERT INTO style_item (item_id, name, cost, url, description, type) VALUES (%s, %s, %s, %s, %s, %s)"
      value_sql = (GetNewItemID(), "None", 0,"None.png", "A basic image, can't be removed", "image")
      mycursor.execute(sql_query, value_sql)
      shutil.copy("static/Basic_image/None.png","trivia_app/static/trivia_app/None.png")

        


  def ReturnAllStyleItems():#getting all the styles and putting into array with images and urls
     mycursor.execute("SELECT * FROM style_item")
     arara = mycursor.fetchall()
     arara= [list(i) for i in arara]
     return arara

  """Admin Function>"""


def GetNewItemID():#auto increments and getting new id - by one more
    sql_query = ("SELECT * FROM style_item WHERE item_id=(SELECT max(item_id) FROM style_item)")
    mycursor.execute(sql_query)
    arara = mycursor.fetchall()
    if arara==[]:
      return 1
    return arara[0][0]+1

def CutTheExtension(filename):#get us the file type like jpg,png etc
  return filename.split(".",1)[1]

def CheckForBasicStyles(types):#checks if the one or two of the basic style exist in data
  if types=="image":
    sql_query = "Select * from style_item where url=%s"
    value_sql = ("None.png",)
    mycursor.execute(sql_query, value_sql)
    if mycursor.fetchall()!=[]:
      return True
    return False
  if types=="color":
    sql_query = "Select * from style_item where url=%s"
    value_sql = ("black",)
    mycursor.execute(sql_query, value_sql)
    if mycursor.fetchall()!=[]:
      return True
    return False

def CheckIfItABasicStyle(url):
  if url=="None.png" or url=="black":
    return True
  return False









































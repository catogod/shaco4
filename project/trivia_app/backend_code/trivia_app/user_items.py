import mysql.connector

from .style_item import style_item
from .user_manage import user_manage

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="josh17rog",
  database="project",
  autocommit=True
)
mycursor = mydb.cursor()

class user_items:
#wtf i need this class - it usless - but the paper say that you need it - usless -usless - usless --> enjoy my code checker
  """<user objects"""

  def __init__(self,**kwargs):
     if len(kwargs)==2:
      self.user=user_manage(username=kwargs["username"])
      self.style_item=style_item(item_id=kwargs["item_id"])
     elif 'username' in kwargs:
       self.style_item=style_item()
       self.user=user_manage(username=kwargs["username"])
     elif 'style_item_deleted' in kwargs:
       self.style_item=style_item(item_id=kwargs["style_item_deleted"][0]   ,name=kwargs["style_item_deleted"][1],cost=kwargs["style_item_deleted"][2],url=kwargs["style_item_deleted"][3],description=kwargs["style_item_deleted"][4],type1=kwargs["style_item_deleted"][5])
       self.user=user_manage()
     else:
       self.style_item=style_item()
       self.user=user_manage()
      


  """user objects>"""

  """<main functions"""
  def BuyItem(self):#function of buying a new item - interaction 
    arara_check = self.style_item.GetItemCharcteristicById(self.style_item.item_id)#array of items or False
    if arara_check!=False and CheckIfUserHaveThisStyle(self.style_item.item_id,self.user.username)==False:#if the item is exist and if the user dont have this item
     # user_check = self.user.BuyItem(arara_check[0][2])#False or true, arara_check[2] is cost
      #need to add item
      if self.user.BuyItem(arara_check[2])==True:
        sql_query = "INSERT INTO user_items (username,item_id) VALUES (%s, %s)"
        value_sql = (self.user.username,self.style_item.item_id)
        mycursor.execute(sql_query, value_sql)
        return True
    return False


  def ChangeUserStyleById(self,type):#the problem that there is not check out for this item
    the_item=self.style_item.GetItemCharcteristicById(self.style_item.item_id)#the item or false(no item)
    if the_item!=False and the_item[5]==type:
      if CheckIfUserHaveThisStyle(self.style_item.item_id, self.user.username)==True:
        sql_query = "UPDATE user SET color_id=%s where username=%s"#basic for color
        if type=="image":
          sql_query = "UPDATE user SET image_id=%s where username=%s"#if its not color
        value_sql = (self.style_item.item_id, self.user.username)
        mycursor.execute(sql_query, value_sql)
        return True
    return False


  def AddBasicStyleToUser(self,url):#adding to data base the specific style
    itemid=GetItem_idByUrl(url)
    if CheckIfUserHaveThisStyle(itemid[0],self.user.username)==False:
      sql_query = "INSERT INTO user_items (username,item_id) VALUES (%s, %s)"
      value_sql = (self.user.username,itemid[0])
      mycursor.execute(sql_query, value_sql)
      self.style_item.item_id=itemid[0]#changing
    return False


  def GetUserSelectedStyles(self):#return the array with 2 users selected styles
    image = self.user.GetImage_IdOfUserFromData()#image id
    color =self.user.GetColor_IdOfUserFromData()#color id
    image=self.style_item.GetItemCharcteristicById(image)#override to array - image 
    color=self.style_item.GetItemCharcteristicById(color)#override to array - color
    #[('fsfs')]
    arr = [color[3],image[3]]#array of url of color and then image
    return arr


  def GetAllUserStylesAsFullData(self):#getting all user styles and then return it
    user_styles_id=GetAllUserStylesId(self.user.username)
    data=list()
    for item in user_styles_id:
      the_add=self.style_item.GetItemCharcteristicById(item[0])
      data.append(the_add)
    data = [list(i) for i in data]
    return data

  def AdminMoneyToUsersAfterDeleteStyle(self):#return the money back to users after deleting specific style
    for id_user in self.GetAllUsersByIdOfProduct():#id_user is username
      self.user.ReturnUserMoney(id_user[0], self.user.SpecificNoObjectUserMoney(id_user[0])+self.style_item.cost)
  
  def DeleteAllUserStyleById(self):#deleting the user item by id
    sql_query = "DELETE FROM user_items WHERE item_id=%s"
    value_sql = (self.style_item.item_id,)
    mycursor.execute(sql_query, value_sql)

  def GetAllUsersByIdOfProduct(self):#getting the username by item id
    sql_query = "Select username from user_items where item_id=%s"
    value_sql = (self.style_item.item_id,)
    mycursor.execute(sql_query, value_sql)
    arara=mycursor.fetchall()
    return arara#getting array of usernames

  def DeleteUserInUserItems(self):#deleting the item by username
    sql_query="DELETE FROM user_items WHERE username=%s"
    value_sql = (self.user.username,)
    mycursor.execute(sql_query, value_sql)

    



  """main functions>"""


def CheckIfUserHaveThisStyle(item_id,username): #checking if user have this specific item
    sql_query = "Select * from user_items where username=%s and item_id=%s"
    value_sql = (username,item_id)
    mycursor.execute(sql_query, value_sql)
    boolian=mycursor.fetchall()
    if(boolian!=[]):
      return True
    return False

def GetAllUserStylesId(username):#selecting item id by username
    sql_query = "Select item_id from user_items where username=%s"
    value_sql = (username,)
    mycursor.execute(sql_query, value_sql)
    arara=mycursor.fetchall()
    return arara#getting

def GetItem_idByUrl(url):#returning the item id by url(the css)
  sql_query = "Select item_id from style_item where url=%s"
  value_sql = (url,)
  mycursor.execute(sql_query, value_sql)
  arara=mycursor.fetchall()
  return arara[0]




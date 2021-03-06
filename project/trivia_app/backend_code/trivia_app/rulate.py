import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="josh17rog",
  database="project#2",
  autocommit=True
)
mycursor = mydb.cursor()

class rulate_manage:
    def __init__(self,**kwargs):
        if len(kwargs)==2:
          self.name = kwargs["product_name"]
          self.amount = kwargs["amount"]
        elif len(kwargs)==1:
          self.name = kwargs["product_name"]
        else:
            pass


    #should add if no item no login, add the checker for the product,and add a null 50 / 50 as the items
    
    def RegisterItem(self):#register new product
      if self.name=="none":
        return False
      if self.AddItemToExisting() == False:
        sql_query = "INSERT INTO prize_pool (product_name,amount) VALUES (%s,%s)"
        value_sql = (self.name, self.amount)
        mycursor.execute(sql_query, value_sql)
        return True

    def ChangeAmount(self):#change amount of specific product
      sql_query = "UPDATE prize_pool SET amount=%s where product_name=%s"
      value_sql = (self.amount,self.name)
      mycursor.execute(sql_query, value_sql)
      AutoDelteItem()#auto data base clear
    

    def JoinWheel(self):#getting all avliable products
      mycursor.execute("Select * from prize_pool")
      arara=[]
      items =  mycursor.fetchall()
      for item in items:
        arara.append(item[0])
        arara.append("none")
      DeleteOneItemForShortPeriod(items)#if 2 user will join at same time and get the same item of amount=1, chances are low
      return [arara,items]

    def UserWin(self,items,product_win):#same as where he losses
      DelOneFromItemInArray(product_win,items)#array changer
      AddTheItemsToPreviusBeforeDelExceptThatOne(items)#the data changer
      AutoDelteItem()#auto data base clear

    def CheckIfUserCanUseRulate(self,user_money):
      points=int(user_money)-GetThePointsThatNeedToJoinWheel()
      if points>=0:#problems with 0 and false
        return [True,points]
      return [False,points]

    def RulateTable(self):
      mycursor.execute("Select * from prize_pool")
      return mycursor.fetchall()

    def if_table_is_empty(self):
        mycursor.execute("SELECT COUNT(*) FROM prize_pool")
        arr = mycursor.fetchall()#the rows of table
        if arr[0][0] == 0:
            return True
        return False

    
    def AddItemToExisting(self):
      if self.if_table_is_empty() == False:
        sql_query = "Select * from prize_pool where product_name=%s"
        value_sql = (self.name,)
        mycursor.execute(sql_query, value_sql)
        if len(mycursor.fetchall()) != 0:
          item=mycursor.fetchall()[0]
          sql_query = "UPDATE prize_pool SET amount=%s where product_name=%s"
          value_sql = (self.name,int(self.amount+item[1]))
          mycursor.execute(sql_query, value_sql)
          return True
      return False

          





def DeleteOneItemForShortPeriod(list_item):
  for item in list_item:
    sql_query="UPDATE prize_pool set amount=%s WHERE product_name=%s "
    value_sql = (int(item[1]-1),item[0])
    mycursor.execute(sql_query, value_sql)

def AddTheItemsToPreviusBeforeDelExceptThatOne(list_item):# in data(a,1) --> the array (a,2)
  for item in list_item:
    sql_query="UPDATE prize_pool SET amount=%s WHERE product_name=%s and amount<%s"
    value_sql = (int(item[1]),item[0],item[1])
    mycursor.execute(sql_query, value_sql)

  

def AutoDelteItem():#auto delete the item when admin register
    mycursor.execute("Select * from prize_pool")
    list_of_items = mycursor.fetchall()
    for item in list_of_items:
        if item[1]<=0:
            sql_query="DELETE FROM prize_pool WHERE product_name=%s"
            value_sql = (item[0],)
            mycursor.execute(sql_query, value_sql)

def GetThePointsThatNeedToJoinWheel():#kinds sus
  mycursor.execute("Select points_for_rulate from main_admin where key_1=1")
  points = mycursor.fetchall()
  return points[0][0]

def DelOneFromItemInArray(product_name,array):
  for item in array:
    if item[0]==product_name.lstrip(' '):
      item[1]=item[1]-1







    
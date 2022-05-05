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


    
    
    def RegisterItem(self):#register new product
      sql_query = "INSERT INTO prize_pool (product_name,amount) VALUES (%s,%s)"
      value_sql = (self.name, self.amount)
      mycursor.execute(sql_query, value_sql)

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
        arara.append(item[1])
      DeleteOneItemForShortPeriod(items)#if 2 user will join at same time and get the same item of amount=1, chances are low
      return [arara,items]

    def UserWin(self,items):
      AddTheItemsToPreviusBeforeDelExceptThatOne(items)#the data changer
      AutoDelteItem()#auto data base clear

    def CheckIfUserCanUseRulate(self,user_money):
      if user_money>=GetThePointsThatNeedToJoinWheel():
        return user_money-GetThePointsThatNeedToJoinWheel()
      return False

    def RulateTable(self):
      mycursor.execute("Select * from prize_pool")
      return mycursor.fetchall()



def DeleteOneItemForShortPeriod(list_item):
  for item in list_item:
    sql_query="UPDATE prize_pool set amount=%s WHERE product_name=%s "
    value_sql = (item[2]-1,item[1])
    mycursor.execute(sql_query, value_sql)

def AddTheItemsToPreviusBeforeDelExceptThatOne(list_item):# in data(a,1) --> the array (a,2)
  for item in list_item:
    sql_query="UPDATE prize_pool SET amount=%s WHERE product_name=%s and amount<%s"
    value_sql = (item[2],item[1],item[2])
    mycursor.execute(sql_query, value_sql)

  

def AutoDelteItem():#auto delete the item when admin register
    mycursor.execute("Select * from prize_pool")
    list_of_items = mycursor.fetchall()
    for item in list_of_items:
        if item[2]<=0:
            sql_query="DELETE FROM prize_pool WHERE product_name=%s"
            value_sql = (item[1],)
            mycursor.execute(sql_query, value_sql)

def GetThePointsThatNeedToJoinWheel():
  mycursor.execute("Select points_for_rulate from main_admin where key_1=1")
  points = mycursor.fetchall()
  return points[0][0]



    
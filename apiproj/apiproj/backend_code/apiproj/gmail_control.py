import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="josh17rog",
    database="project#2",
    autocommit=True
)

mycursor = mydb.cursor()

#dont forget to do  mydb.commit()
class gmail_control:

    def __init__(self,**kwargs):
        if len(kwargs)==4:
            self.admin_username=kwargs["admin_username"]
            self.user_email=kwargs["user_email"]
            self.email_text=kwargs["email_text"]
            self.system_email=kwargs["system_email"]
        elif len(kwargs)==3:
            self.user_email=kwargs["user_email"]
            self.email_text=kwargs["email_text"]
            self.system_email=kwargs["system_email"]
            self.admin_username=None
        else:
            pass
    
    def Send_email_info_to_data(self):
        sql_query = "INSERT INTO gmail_send (admin_username, user_email, email_text, system_email) VALUES (%s, %s,%s,%s)"
        value_sql = (self.admin_username, self.user_email, self.email_text,self.system_email)
        mycursor.execute(sql_query, value_sql)
    


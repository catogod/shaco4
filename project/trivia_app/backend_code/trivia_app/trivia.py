import mysql.connector
from random import randint



#you cant delete trivia question

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="josh17rog",
  database="project",
  autocommit=True
)
mycursor = mydb.cursor()

class trivia():
    """<user objects"""

    def __init__(self,**kwargs):
      if len(kwargs) == 6:
        self.correct_answer = kwargs["correct_answer"] #the numbers 1,2,3,4 when using admin add question
        self.question  =kwargs["question"]
        self.answer1 = kwargs["answer1"]
        self.answer2 = kwargs["answer2"]
        self.answer3 = kwargs["answer3"]
        self.answer4 = kwargs["answer4"]
        self.question_id = GetNewTriviaID()  
      elif len(kwargs) == 1:
        self.question_id=kwargs["question_id"]
      else:
        pass

    """<user objects"""

    """<main functions"""

    def CreateQuestion(self):#creating question - admin only function
      if self.correct_answer=='1':
        self.correct_answer=self.answer1
      elif self.correct_answer=='2':
        self.correct_answer=self.answer2
      elif self.correct_answer=='3':
        self.correct_answer=self.answer3
      elif self.correct_answer=='4':
        self.correct_answer=self.answer4
      sql_query = "INSERT INTO trivia (question_id,correct_answer,question,answer1,answer2,answer3,answer4) VALUES (%s, %s, %s, %s, %s, %s, %s)"
      value_sql = (self.question_id,self.correct_answer,self.question,self.answer1,self.answer2,self.answer3,self.answer4)
      mycursor.execute(sql_query, value_sql)

    def GetRandomQuestion(self):#getting random question from data base
      mycursor.execute("SELECT * FROM trivia ORDER BY RAND() LIMIT 1")
      arara = mycursor.fetchall()
      return arara
    
    def GetQuestionAnswerById(self,id):#getting answer by id of question
      sql_query = "Select correct_answer from trivia where question_id=%s"
      value_sql = (id,)
      mycursor.execute(sql_query, value_sql)
      arr = mycursor.fetchall()
      if arr==[]:
        return False
      return arr[0][0]

    def CompareAnswers(self,id,user_answer_id):#comparing the answer of user and the answer from data
      if user_answer_id == self.GetQuestionAnswerById(id):
        return True
      return False


    def Delete_question_by_id(self):#deleting question by id - admin only function
      if self.GetQuestionAnswerById(self.question_id)!=False:#checking if the question is exiting by answer or other thing dont lethal
        sql_query="DELETE FROM trivia WHERE question_id=%s"
        value_sql = (self.question_id,)
        mycursor.execute(sql_query, value_sql)
        return True
      return False

 

    
    def ShowTriviaTable():#getting all trivia table - to show admins
      mycursor.execute("Select * from trivia")
      return mycursor.fetchall()
    
    """main functions>"""

    """<cutting"""
    def GetSpecificValueFromArara(self,arara,i):#cutting the list that sql returns - for my needs
      return arara[0][i]
    """cutting>"""

def GetNewTriviaID():#incrementing by one the last trivia id
      sql_query = ("SELECT * FROM trivia WHERE question_id=(SELECT max(question_id) FROM trivia)")
      mycursor.execute(sql_query)
      arara = mycursor.fetchall()
      if arara==[]:
        return 1
      return arara[0][0]+1

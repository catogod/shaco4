from pickle import TRUE
from django.shortcuts import redirect, render
from django.http import Http404
from django.views.decorators.cache import cache_control
import requests

from trivia_app.backend_code.trivia_app.admin_manage import admin_manage
from trivia_app.backend_code.trivia_app.rulate import rulate_manage
from trivia_app.backend_code.trivia_app.main_admin import main_admin

# Create your views here.
#not saving in session user because of it
from .backend_code.trivia_app.user_manage import user_manage
from .backend_code.trivia_app.trivia import trivia
from .backend_code.trivia_app.user_games import user_games
from .backend_code.trivia_app.user_rounds import user_rounds
from.backend_code.trivia_app.style_item import style_item
from.backend_code.trivia_app.user_items import user_items
from.backend_code.trivia_app.top_manage import top_manage


from django.db.models import Avg,Count

def Main_login(request):#no url
       #the basic color for data base at start of the program
       styleItems=style_item()
       styleItems.Add_Basic_Color()
       styleItems.Add_Basic_Image()
       return redirect("/RegisterNDLogin")


#django cant store objects in seesion at easy way so fuck off
# ---- when you use arrows you to navigate back session.pop() -------
#you should not delete any data 
# https://stackoverflow.com/questions/9877263/time-delayed-redirect/16541769 - to timer

def Error_404_view(request,str):
    return render(request,"404.html")

#log out view
def Log_out(request):
    if 'user' in request.session:
      request.session.pop("user")
      return redirect("/")
    if 'admin' in request.session:
      request.session.pop("admin")
      return redirect("/")
    if 'main_admin' in request.session:
      request.session.pop("main_admin")
      return redirect("/")
    return redirect("/")


#view of register and login
def RegisterNDLogin(request):
    if request.method =="POST":
        #register method post
       if 'registerbutton' in  request.POST:
        text_register="Wrong username/password or username already taken"#the sended value 
        User = user_manage(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"])
        if User.CheckIfEmailExitsInData()==False:#there is no user with that email
            if User.Register()== True:#add 
                text_register="Registered scucesfuly"
                #adding basic style_items - hardcoded
                styleItems=user_items(username=request.POST["username"])
                styleItems.AddBasicStyleToUser("None.png")#adding image
                styleItems.ChangeUserStyleById("image")
                styleItems.AddBasicStyleToUser("blue")#adding color
                styleItems.ChangeUserStyleById("color")
        else:
            text_register="User with this email already exists"       
        return render(request,"trivia_app/login.html",{"text_return":text_register})

          #login method post
       if 'loginbutton' in request.POST:
          User = user_manage(username=request.POST["username"],password=request.POST["password"])
          request.session['user'] = User.Login()#starting session with username
          if request.session['user'] != None:
            return redirect("/menu")
          else:
            request.session.pop('user')  
            return render(request,"trivia_app/login.html",{
           "text_return":"Wrong username or password",
            })
       if 'api_button' in request.POST:#the api
           user=user_manage(email=request.POST["email_api"])
           text_api="There is no user with this email"
           user=user.ReturnUserByEmailForAPI()#override to user info
           if user!=False:
                requests.post("http://127.0.0.1:3000/forgot_password/",data={"email_address":user[3],"username":user[1],"password":user[2]})#sending the email to send the user password to email
                text_api="check your email to get the password(check in spam)"
           return render(request,"trivia_app/login.html",{
           "text_api":text_api,})
       if 'admin_go' in request.POST:
            return redirect("/admin_RNL")

    if request.method=="GET":
        return render(request,"trivia_app/login.html")
    return render(request,"trivia_app/login.html")#the 500 return

#view of menu
def Menu_handele(request):
    if 'user' in request.session:
        if request.method == "GET":
            userItems =user_items(username=request.session['user'])
            userItems=userItems.GetUserSelectedStyles()#override to user styles get the user selcted styles
            return render(request, "trivia_app/menu.html",{
             "username_session":request.session['user'],
             "text_color":userItems[0],
             "img":"static/trivia_app/"+userItems[1],      
           })
    return redirect("/")

#all views of users
def User_handele(request):
    if 'user' in request.session:#should add the user color and image to preview - next time
      All_user_items=user_items(username=request.session['user']).GetAllUserStylesAsFullData()#all the items that avliable to user
      round_object=user_rounds(username=request.session['user']).ReturnUserInfoRounds()#the data of user games
      user__Items=user_items(username=request.session['user']).GetUserSelectedStyles()#user existed items
      #post
      if request.method=="POST":
        #change style
        if 'user_change_style_post' in request.POST:
           userItems=user_items(username=request.session['user'],item_id=request.POST["item_id_send"])#user and the item id
           change_item_return="you dont have this style"
           if userItems.ChangeUserStyleById(request.POST["hidden_style_choosed"]) == True:#function that change the user specific style by id return true if style change
               change_item_return="style changed succsesfuly, wait unitll the data update it!"
               user__Items=user_items(username=request.session['user']).GetUserSelectedStyles()#change the style
           return render(request,"trivia_app/user_info.html",{
              "username_info":request.session['user'],"password_info":userItems.user.GetPasswordFromData(),
              "email_info":userItems.user.GetEmailFromData(),"points_info":userItems.user.GetPointsFromData(),
              "games_played_info":userItems.user.GetGamesPlayedFromData(),"color_info":userItems.user.GetColor_IdOfUserFromData(),
              "image_info":userItems.user.GetImage_IdOfUserFromData(),"change_item":change_item_return,"style_arara":All_user_items,
              "round_arara":round_object,"text_color":user__Items[0],"img":"static/trivia_app/"+user__Items[1] })
        #change password
        elif 'user_change_password_post' in request.POST:
            User=user_manage(username=request.session['user'])
            User.ChangePassword(request.POST["password_send"])
            return render(request,"trivia_app/user_info.html",{
              "username_info":request.session['user'],
              "password_info":User.GetPasswordFromData(),
              "email_info":User.GetEmailFromData(),
              "points_info":User.GetPointsFromData(),
              "games_played_info":User.GetGamesPlayedFromData(),
              "text_password":"password changed succsesfuly",
              "style_arara":All_user_items,"color_info":User.GetColor_IdOfUserFromData(),
              "image_info":User.GetImage_IdOfUserFromData(),"round_arara":round_object,"text_color":user__Items[0],"img":"static/trivia_app/"+user__Items[1]})
        #change email
        elif 'user_change_email_post' in request.POST:
            User=user_manage(username=request.session['user'])
            text_email="This Email already exist in data"
            if User.ChangeEmail(request.POST["email_send"]) == True:
                text_email="Email changed successfully"
            return render(request,"trivia_app/user_info.html",{
            "username_info":request.session['user'],"password_info":User.GetPasswordFromData(),"email_info":User.GetEmailFromData(),
            "points_info":User.GetPointsFromData(),"games_played_info":User.GetGamesPlayedFromData(),"change_item":text_email,
            "style_arara":All_user_items,"color_info":User.GetColor_IdOfUserFromData(),
              "image_info":User.GetImage_IdOfUserFromData(),"round_arara":round_object,"text_color":user__Items[0],"img":"static/trivia_app/"+user__Items[1],})
      #get
      if request.method == "GET":
          User=user_manage(username=request.session['user'])
          return render(request,"trivia_app/user_info.html",{
              "username_info":request.session['user'],
              "password_info":User.GetPasswordFromData(),
              "email_info":User.GetEmailFromData(),
              "points_info":User.GetPointsFromData(),
              "games_played_info":User.GetGamesPlayedFromData(),
              "style_arara":All_user_items,"color_info":User.GetColor_IdOfUserFromData(),
              "image_info":User.GetImage_IdOfUserFromData(),"round_arara":round_object,"text_color":user__Items[0],"img":"static/trivia_app/"+user__Items[1],
          })
    return redirect("/")

#all trivia views
def Trivia_handele(request):
    if 'user' in request.session:
        #post
        if request.method=="POST":#i will delete the vriables after i arrive to api and css
            Trivia_object=trivia()
            if Trivia_object.CompareAnswers(request.POST["hid_q_id"],request.POST["hid_answer"])==True:
                round_object=user_rounds(question_id=request.POST["hid_q_id"],answer=request.POST["hid_answer"],
                username=request.session['user'],game_id=request.POST["hid_game_id"])#new round object with username and game_id
                round_object.RegisterUserRound()#only for it the inheritance lol XDDDDDDDDD
                arara = Trivia_object.GetRandomQuestion()
                userItems =user_items(username=request.session['user'])
                userItems=userItems.GetUserSelectedStyles()
                user_add_point = user_manage(username=request.session['user'])
                user_add_point.AddOnePointToUser()
                return render(request,"trivia_app/trivia_game.html",{"text_question":Trivia_object.GetSpecificValueFromArara(arara,2),
                 "text_answer_1":Trivia_object.GetSpecificValueFromArara(arara,3),
                 "text_answer_2":Trivia_object.GetSpecificValueFromArara(arara,4),
                 "text_answer_3":Trivia_object.GetSpecificValueFromArara(arara,5),
                 "text_answer_4":Trivia_object.GetSpecificValueFromArara(arara,6),
                 "text_end_round":"Press the button to view the result",
                 "hid_question_id":Trivia_object.GetSpecificValueFromArara(arara,0),#getting a new random question
                 "hid_game_id":request.POST["hid_game_id"],
                 "text_color":userItems[0],
                 "img_user":"static/trivia_app/"+userItems[1],   })
            else:
                round_object=user_rounds(question_id=request.POST["hid_q_id"],answer=request.POST["hid_answer"],
                username=request.session['user'],game_id=request.POST["hid_game_id"])#new round object with username and game_id
                round_object.RegisterUserRound()#register user round but dont give points
                userItems =user_items(username=request.session['user'])
                userItems=userItems.GetUserSelectedStyles()#override to user styles get the user selcted styles
                return render(request,"trivia_app/menu.html",{
                 "all_return":"wrong answer, check your game history for more info - id of game : " + request.POST["hid_game_id"],
                 "username_session":request.session['user'],"text_color":userItems[0],"img":"static/trivia_app/"+userItems[1],})
        #get
        if request.method=="GET":
            #so first get in - need to game id, username, and all rounds
            round_object=user_rounds(username=request.session['user'])#creating round object that inherate from games
            game_id=round_object.CreateNewGameId()#using this object to create new game id
            round_object.Register_Game(game_id)#register the id in data base with the username
            Trivia_object=trivia()
            arara=Trivia_object.GetRandomQuestion()#getting the question and all it attributes by random
            userItems =user_items(username=request.session['user'])
            userItems=userItems.GetUserSelectedStyles()
            return render(request,"trivia_app/trivia_game.html",{
             "text_question":Trivia_object.GetSpecificValueFromArara(arara,2),
             "text_answer_1":Trivia_object.GetSpecificValueFromArara(arara,3),
             "text_answer_2":Trivia_object.GetSpecificValueFromArara(arara,4),
             "text_answer_3":Trivia_object.GetSpecificValueFromArara(arara,5),
             "text_answer_4":Trivia_object.GetSpecificValueFromArara(arara,6),
             "text_end_round":"Press the button to view the result",
             "hid_question_id":Trivia_object.GetSpecificValueFromArara(arara,0),
             "hid_game_id":game_id,
             "text_color":userItems[0],
             "img_user":"static/trivia_app/"+userItems[1],})
    return redirect("/log_out")

#all admins views
def admin_handele(request):
   if 'admin' in request.session:
       if request.method=="POST":
           #add trivia question
           if 'button_add_trivia_text' in request.POST:
               Trivia_object=trivia(correct_answer=request.POST["hid_answer"],question=request.POST["question"],
               answer1=request.POST["answer1"],answer2=request.POST["answer2"],answer3=request.POST["answer3"],answer4=request.POST["answer4"])
               Trivia_object.CreateQuestion()
               return render(request,"trivia_app/admin.html",{"return_answer":"question saved successfuly","user_show":user_manage.ShowUsersTable(),
               "style_show":style_item.ReturnAllStyleItems(),"games_show":user_games.ShowGamesTable(),"rounds_show":user_rounds.ShowRoundsTable(),"trivia_show":trivia.ShowTriviaTable()})
            #delete trivia question
           if 'button_delete_question' in request.POST:
               trivia_q=trivia(question_id=request.POST["question_delete"])
               return_answer="there is not question like this"
               if trivia_q.Delete_question_by_id()==True:
                   return_answer="question deleted successfully"
               return render(request,"trivia_app/admin.html",{"return_answer":return_answer,"user_show":user_manage.ShowUsersTable(),
               "style_show":style_item.ReturnAllStyleItems(),"games_show":user_games.ShowGamesTable(),"rounds_show":user_rounds.ShowRoundsTable(),"trivia_show":trivia.ShowTriviaTable()})
               #######################################################
            #add style item
           if 'button_add_style' in request.POST:
               url=request.POST["url"]
               if request.POST["url"]=="":
                  url=request.FILES["image_send"]
                  url=url.name
               style=style_item(name=request.POST["name"],cost=request.POST["cost"],url=url,description=request.POST["description"],type1=request.POST["hid_type"])
               url=style.InsertNewStyleItem()# none is color else is image
               if url!=None:
                  filename=request.FILES["image_send"]#the file 
                  with open("trivia_app/static/trivia_app/"+url, "wb+") as dest:#put file into folder images chuck by chunk(rewrite)
                    for chunk in filename.chunks():
                       dest.write(chunk)
               return render(request,"trivia_app/admin.html",{"return_answer":"item saved successfuly","user_show":user_manage.ShowUsersTable(),
               "style_show":style_item.ReturnAllStyleItems(),"games_show":user_games.ShowGamesTable(),"rounds_show":user_rounds.ShowRoundsTable(),"trivia_show":trivia.ShowTriviaTable()})
            #delete style item
           if 'button_delete_style' in request.POST:
               style_it=style_item(item_id=request.POST["style_delete"])
               return_answer="There is not item with this id, or you can't delete basic style"
               style_item_deleted=style_it.DeleteStyleByIdAndReturnIt()#the deleted item
               if style_item_deleted!=False :
                   userItems=user_items(style_item_deleted=style_item_deleted)
                   userItems.AdminMoneyToUsersAfterDeleteStyle()#giving the money
                   userItems.DeleteAllUserStyleById()#deleting all info from data base
                   return_answer="Deleted successfully"
               return render(request,"trivia_app/admin.html",{"return_answer":return_answer,"user_show":user_manage.ShowUsersTable(),
               "style_show":style_item.ReturnAllStyleItems(),"games_show":user_games.ShowGamesTable(),"rounds_show":user_rounds.ShowRoundsTable(),"trivia_show":trivia.ShowTriviaTable()})
               ####################################################
            #user delete
           if 'button_delete_user' in request.POST:
               user=user_manage(username=request.POST["username_find"])
               return_answer="username not exiting in data base"
               if user.DeleteUserByName()==True:#deletin the user
                   round_object=user_rounds(username=request.POST["username_find"])
                   round_object.DeleteAllUserRounds()#get a array of game_id of users and then delete al rounds of this id_games
                   round_object.DeleteAllUserGamesByName()#deleting all users game
                   user_items(username=request.POST["username_find"]).DeleteUserInUserItems()
                   return_answer="All the data about the user deleted succesfully"
               return render(request,"trivia_app/admin.html",{"return_answer":return_answer,"user_show":user_manage.ShowUsersTable(),
               "style_show":style_item.ReturnAllStyleItems(),"games_show":user_games.ShowGamesTable(),"rounds_show":user_rounds.ShowRoundsTable(),"trivia_show":trivia.ShowTriviaTable()})
            #admin send register code to email
           if 'button_add_admin' in request.POST:
               return_answer="There is no email like this in the data"
               user=user_manage(email=request.POST["email_address"])
               if user.ReturnUserByEmailForAPI()!=False:#check if email like this is in data
                   admin=admin_manage()#for the admin code
                   requests.post("http://127.0.0.1:3000/invite_user_to_become_admin/",data={"admin_username":request.session['admin'],
                   "email_address":request.POST["email_address"],"admin_code":admin.Admin_register_code})#sending the request to the other server
                   return_answer="The data sended successfuly to email"
               return render(request,"trivia_app/admin.html",{"return_answer":return_answer,"user_show":user_manage.ShowUsersTable(),
               "style_show":style_item.ReturnAllStyleItems(),"games_show":user_games.ShowGamesTable(),"rounds_show":user_rounds.ShowRoundsTable(),"trivia_show":trivia.ShowTriviaTable()})
        #basic get request
       return render(request,"trivia_app/admin.html",{
           "user_show":user_manage.ShowUsersTable(),"style_show":style_item.ReturnAllStyleItems(),"games_show":user_games.ShowGamesTable(),
           "rounds_show":user_rounds.ShowRoundsTable(),"trivia_show":trivia.ShowTriviaTable()
       })#basic get request     
   return redirect("/")#if not session
        
#all shop views
def shop_handele(request):
    if 'user' in request.session:
        if request.method =="GET":
          arara=style_item.ReturnAllStyleItems()
          user_item=user_items(username=request.session['user']).GetUserSelectedStyles()
          return render(request,"trivia_app/shop.html",{
          "style_arara":arara,
          "text_color":user_item[0]}) 
        if request.method == "POST" and 'buy_item_button' in request.POST:
            arara=style_item.ReturnAllStyleItems()
            user_item=user_items(username=request.session['user']).GetUserSelectedStyles()#user existed items
            userItems=user_items(username=request.session['user'],item_id=request.POST['item_id'])#the item that user bought - no subscriptable
            Shop_Return_Buy="The item unavilibale or you dont have enough points or you already have this item"
            if userItems.BuyItem() == True:#checks if user can buy it
                Shop_Return_Buy="The item added to your catalog, check it in user info"#change the reutrn
            return render(request,"trivia_app/shop.html",{"style_arara":arara,"text_color":user_item[0],
                "Shop_Return_Buy":Shop_Return_Buy})       
    return redirect("/")

#all admin_login views
def admin_RNL_handele(request):
    #post request
    if request.method=="POST":
        #register method post
        if 'registerbutton' in  request.POST:
            text_register="wrong username/password or wrong code"#the sended value 
            admin = admin_manage(username=request.POST["username"],password=request.POST["password"],code=request.POST["code"])
            if admin.Register() == True:#add 
                text_register="Registered scucesfuly"
            return render(request,"trivia_app/admin_login.html",{"text_return":text_register})

          #login method post
        if 'loginbutton' in request.POST:
            admin = admin_manage(username=request.POST["username"],password=request.POST["password"])
            request.session['admin'] = admin.Login()#starting session with username
            if request.session['admin'] != None:
                return redirect("/admin")
            else:
                request.session.pop('admin')  
            return render(request,"trivia_app/admin_login.html",{
            "text_return":"wrong username or password",})
          #redirect to user page
        if 'user_go' in request.POST:
            return redirect("/RegisterNDLogin")
        if 'main_admin_go' in request.POST:
            return redirect("/main_admin_login")
    #get request
    if request.method == "GET":
        return render(request,"trivia_app/admin_login.html")
    return render(request,"trivia_app/admin_login.html")#the 500 return

def Top_page_handele(request):
    if 'user' in request.session:
        if request.method=="GET":
            tp= top_manage()
            user_item=user_items(username=request.session['user']).GetUserSelectedStyles()
            return render(request,"trivia_app/top_page.html",
            {"user_color":"arara need color","arara_points":tp.SortByPoints(),"arara_games":tp.SortByGames()
            ,"arara_rounds":tp.SortByRoundsMost(),"arara_styles":tp.SortByMostStyles(),"text_color":user_item[0]})
    return redirect("/")

#all rulate views
def rulate(request):#should add user colors
    if 'user' in request.session:
        userItems =user_items(username=request.session['user']).GetUserSelectedStyles()#user styles

        if request.method=="GET":#the 0 array is only name the 1 is the items
            user_m=user_manage(username=request.session['user'])
            rr=rulate_manage()
            remain_points=rr.CheckIfUserCanUseRulate(user_m.GetPointsFromData())#false or user points after paying for rulate
            if remain_points !=False:
                user_m.UpdateUserPoints(remain_points)#taking the points from user
                rr=rr.JoinWheel()#parsing the value to the 2 arrays - each time user realod it takes the items so...
                request.session['items_array'] = rr[1]
                return render(request,"trivia_app/rulate.html",{"option_wheel":rr[0],"all_items":rr[1],
                "all_return":"From your blance were taken ","text_color":userItems[0],      
                })

        
            return render(request,"trivia_app/menu.html",{
                 "all_return":"Sorry but you are dont have enough points to use rulate",#maybe to do from top 10 of each
                 "username_session":request.session['user'],"text_color":userItems[0],"img":"static/trivia_app/"+userItems[1],})

        if request.method=="POST":
            rr=rulate_manage()
            rr.UserWin(request.session["items_array"])#data changer
            request.session.pop("items_array")
            location="Country: "+request.POST["country"]+", "+"City: "+request.POST["city"]+", "+"street: "+request.POST["street"]+", "+"Home Number: "+request.POST["home"]+", "+"Appartment number: "+request.POST["appartment"]
            user_email=user_manage(username=request.session['user']).GetEmailFromData()
            requests.post("http://127.0.0.1:3000/Send_user_his_win_info_in_rulate/",data={"email_address":user_email,"product":request.POST["product"],"user_location":location})
            return render(request,"trivia_app/menu.html",{"all_return":"The product you won will arrive soon to you, check your email for more information","text_color":userItems[0],"username_session":request.session['user'],})     
        
    return redirect("/")


def Main_admin_login(request):
    if request.method=="GET":
        return render(request,"trivia_app/main_admin_login.html")
    if request.method=="POST":
        if 'login_p' in request.POST:
            return redirect("/")
            
        r=rulate_manage()
        admin=admin_manage()
        Main_admin=main_admin()

        M_admin=main_admin(code=request.POST["code"])
        if M_admin.if_table_is_empty()==True:#first login
            request.session['main_admin']="Confirmed"
            return render(request,"trivia_app/main_admin.html",{"notice":"Notice you should register a code for this tables access,code for normal admins and the value of using the rulate","rulateT":r.RulateTable(),"adminT":admin.AdminTable,"GmailT":Main_admin.GetGmails(),"codeT":M_admin.GetTableCodes()})

        if M_admin.CompareCodes()==True:#normal logins
            request.session['main_admin']="Confirmed"
            return render(request,"trivia_app/main_admin.html",{"rulateT":r.RulateTable(),"adminT":admin.AdminTable,"GmailT":Main_admin.GetGmails(),"codeT":M_admin.GetTableCodes()})
        return render(request,"trivia_app/main_admin_login.html",{"return":"Wrong Code"})


def Main_admin(request):
    if "main_admin" in request.session:
        r=rulate_manage()
        admin=admin_manage()
        M_admin=main_admin()

        if request.method=="GET":           
            return render(request,"trivia_app/main_admin.html",{"rulateT":r.RulateTable(),"adminT":admin.AdminTable,"GmailT":M_admin.GetGmails(),"codeT":M_admin.GetTableCodes()})

        if request.method=="POST":
            #delete admin
            if 'button_delete_admin' in request.POST:
               ad=admin_manage(username=request.POST["username_find"])
               text="There is not admin with this username"
               if ad.Delete_Admin_By_Name() == True:
                   text="Admin deleted"
               return render(request,"trivia_app/main_admin.html",{"return_answer":text,"rulateT":r.RulateTable(),"adminT":admin.AdminTable,"GmailT":M_admin.GetGmails(),"codeT":M_admin.GetTableCodes()})
            if 'button_insert_prize' in request.POST:
                rulate=rulate_manage(product_name=request.POST["name_insert"],amount=request.POST["amount_insert"])
                text="the item added to the data"
                rulate.RegisterItem()
                return render(request,"trivia_app/main_admin.html",{"return_answer":text,"rulateT":r.RulateTable(),"adminT":admin.AdminTable,"GmailT":M_admin.GetGmails(),"codeT":M_admin.GetTableCodes()})
            if 'button_insert_values' in request.POST:
                m_ad=main_admin(code=request.POST["main_code_insert"],inv_code=request.POST["admin_inv_code_insert"],rulate_p=request.POST["rulate_points_insert"])
                text="you cant insert new values, update it!"
                if m_ad.InsertCode()==True:
                    text="Insert successfuly"
                return render(request,"trivia_app/main_admin.html",{"return_answer":text,"rulateT":r.RulateTable(),"adminT":admin.AdminTable,"GmailT":M_admin.GetGmails(),"codeT":M_admin.GetTableCodes()})
            if 'button_update_value_code' in request.POST:
                text="Update failed, no code regisetered"
                M_admin=main_admin(code=request.POST["update"])
                if M_admin.UpdateCode()==True:
                    text="Main admin code Updated"
                return render(request,"trivia_app/main_admin.html",{"return_answer":text,"rulateT":r.RulateTable(),"adminT":admin.AdminTable,"GmailT":M_admin.GetGmails(),"codeT":M_admin.GetTableCodes()})
            if 'button_update_value_inv_code' in request.POST:
                text="Update failed, no code regisetered"
                M_admin=main_admin(inv_code=request.POST["update"])
                if M_admin.UpdateInvCode()==True:
                    text="Main admin invation code Updated"
                return render(request,"trivia_app/main_admin.html",{"return_answer":text,"rulateT":r.RulateTable(),"adminT":admin.AdminTable,"GmailT":M_admin.GetGmails(),"codeT":M_admin.GetTableCodes()})
            if 'button_update_value_rulate' in request.POST:
                text="Update failed, no code regisetered"
                M_admin=main_admin(rulate_p=request.POST["update"])
                if M_admin.UpdateRulatePoints()==True:
                    text="Base points for rulate Updated"
                return render(request,"trivia_app/main_admin.html",{"return_answer":text,"rulateT":r.RulateTable(),"adminT":admin.AdminTable,"GmailT":M_admin.GetGmails(),"codeT":M_admin.GetTableCodes()})          
    return redirect("/")
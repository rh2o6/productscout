from flask import Blueprint, render_template, request, json,session,redirect,url_for
import itemsearching
views = Blueprint(__name__, "views")
import config
@views.route("/")
def home():

    isloggedin = session.get('isloggedin')
    name = session.get('name')
    print(name)
    print(isloggedin)

    return render_template("homepage.html",islog=isloggedin,username=name)

@views.route("/button-click",methods=["POST"])
def button_click():
    searchitem = request.form["itemtofind"]
    print("Item to look for:",searchitem)
    session['item'] = searchitem
    if searchitem:
        findings = itemsearching.run_search(searchitem)

    for store in findings:
        print(store)

    results_dict = {}
    for store in findings:
        results_dict[store] = {
        'Results': itemsearching.convert_items_to_dict(findings[store]['Results'])
    }
        
    session['results'] = results_dict
    #print(session.get('results'))


    return render_template("results.html",results_dict=results_dict,searchitem=searchitem)

@views.route('/filter',methods=['POST'])
def resultsfilter():
    store = request.form.get('store')
    filteroption = request.form.get('filter')
    sorted = itemsearching.resultsorting(store,session.get('results'),filteroption)
    for store in sorted:
        print(store)
    session['results'] = sorted

    return render_template("results.html",results_dict=sorted,searchitem=session.get('item'))
    

@views.route("/about")
def aboutpage():
    return render_template("about.html")

@views.route("/contact")
def contactpage():
    return render_template("contact.html")

@views.route("/wishlist")
def wishlist():
    import redissetup
    name = session['name']
    userstr = redissetup.r.hget("users",session.get('email'))
    userdict = json.loads(userstr)
    wishlist = userdict["Wishlist"]
    print("LOADEDWISHLIST\n",wishlist)




    return render_template("wishlist.html",username=name,userlist=wishlist)
@views.route("/signup")
def bugspage():
    
    return render_template("signup.html")

@views.route("/signup",methods=['POST'])
def onsignup():
    import redissetup
    usremail = request.form.get('email')
    usrname = request.form.get('name')
    usrpass = request.form.get('password')
    usrpass = config.passhashing(usrpass)
    usrpass_str = usrpass.decode('utf-8') 
    datatosend = {"Email":usremail,
                  "Password":usrpass_str,
                  "Name":usrname,
                  "Wishlist":[]}
    
    signuperror = False
    
    if redissetup.r.hget('users', usremail) is not None:
        signuperror = True
    else:
     # If email doesn't exist, convert the data to JSON and save it
        datatosend_json = json.dumps(datatosend)
        redissetup.r.hset('users', usremail, datatosend_json)
        print("Account created successfully")



    return render_template("signup.html",signuperror=signuperror)

@views.route("/login")
def login():
    return render_template("login.html")

@views.route("/login", methods = ['POST'])
def onlogin():
    import redissetup
    import bcrypt
    usremail = request.form.get('email')
    usrpass = request.form.get('password')
    print(usremail,usrpass)
    userinfo = redissetup.r.hget('users',usremail)
    userinfo = json.loads(userinfo)
    usrpass = usrpass.encode("utf-8")
    hashedpass = userinfo['Password']
    hashedpass = hashedpass.encode("utf-8")
    loginerror = False
    if (redissetup.r.hget('users',usremail) is None):
        loginerror = True

    elif (bcrypt.checkpw(password=usrpass,hashed_password=hashedpass)):
        session['isloggedin'] = True
        session['name'] = userinfo['Name']
        session['email'] = usremail
        print("Login Success!")
        return redirect(url_for('views.home'))
        

    elif not(bcrypt.checkpw(password=usrpass,hashed_password=hashedpass)):
        loginerror = True

    

    return render_template("login.html",loginerror=loginerror)

@views.route("/logout")
def onlogout():
    import redissetup
    session.clear()
    redissetup.r.delete("your_prefix")
    return render_template("logout.html")

@views.route("/addwishlist",methods=["POST"])
def addwishlist():
    from flask import request,jsonify
    import redissetup
    import json



    if not session.get('isloggedin'):
        return jsonify({'success': False, 'message': 'User not logged in'}), 403 

    else:       
        data = request.get_json()
        item_title = data.get('title')
        item_price = data.get('price')
        item_img = data.get('img')
        item_link = data.get('link')
        item_dict = {'Title':item_title,'Price':item_price, 'Image':item_img,"Link":item_link}
        print(item_dict)



    # Example logic to save the item details (e.g., database or session)
        if item_title and item_price and item_img and item_link:
        # Save the liked item (title, price, img, link) to the database or session
            print("Succesfully liked item")

            if session.get('email') is not None:
                oldwishlist = redissetup.r.hget("users",session.get('email'))
                userinfo = json.loads(oldwishlist)
                oldwishlist = userinfo["Wishlist"]
                print("Old Wishlist",oldwishlist)
                oldwishlist.append(item_dict)
                print(oldwishlist)
                userinfo["Wishlist"] = oldwishlist
                userinfo = json.dumps(userinfo)
                redissetup.r.hset(name ='users',value=userinfo,key=session.get('email'))
                return jsonify({'success': True, 'message': 'Succesfully added item to wishlist!'})

            else:
                print("Cannot get email")


    
        else:
            return jsonify({'success': False, 'message': 'Incomplete item data'})
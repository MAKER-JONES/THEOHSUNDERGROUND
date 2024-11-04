
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, current_user,  logout_user
from datetime import date, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from wtf_fields import *
from passlib.hash import pbkdf2_sha256
from flask_whooshee import  Whooshee

app = Flask(__name__)


app.secret_key = 'secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=4)
#session = sqlite3.connect('data.db', check_same_thread=False)
app.config['WHOOSHEE_DIR'] = '/tmp/whoosheers'
db = SQLAlchemy(app)
whooshee = Whooshee(app)
#migrate=Migrate(app,db) #Initializing migrate.
#manager = Manager(app)
#manager.add_command('db',MigrateCommand)

login = LoginManager(app)
login.init_app(app)
@login.user_loader
def load_user(id):
    return User.query.get(id)
class Req(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=True)
    reason = db.Column(db.Text, nullable=False)

    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=True)
    reason = db.Column(db.Text, nullable=False)
    admin = db.Column(db.Boolean, default = False, nullable=False)
@whooshee.register_model('title')
class articles(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, nullable = False)
    date = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable = False)
    articleHTML = db.Column(db.Text, nullable = False)
    category = db.Column(db.String, nullable = False)
    thumbnail = db.Column(db.Text, nullable = False)
    views = db.Column(db.Integer, default=0, nullable = False )
    reported = db.Column(db.Boolean, default = False, nullable=False)
    post_type = db.Column(db.String, default='article', nullable=False)
    username = db.Column(db.String, nullable=False)
class banned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=True)
    reason = db.Column(db.Text, nullable=False)
    admin = db.Column(db.Boolean, default = False, nullable=False)
    ban_reason = db.Column(db.Text, nullable = False)
    banned_by = db.Column(db.String, nullable = False)
class top_article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, nullable = False)


admin = 'adminUsername'
adminName = 'AdminName'
@app.route('/start')
def start():
    
    isAdmin = User.query.filter_by(username = admin).first()
    if isAdmin is None:
        admin_passowrd = 'AdminPassword'
        hashed_admin = pbkdf2_sha256.hash(admin_passowrd)
        adminadd = User(email = 'AdminEmail', password=hashed_admin, username= admin, name = adminName, phone='AdminNumber', reason = 'Knowledge is power', admin = True)
        db.session.add(adminadd)
        db.session.commit()
    adminObject = User.query.filter_by(username = admin).limit(5).first()
    if adminObject.admin == False:
        adminObject.admin = True
        db.session.commit()
    return redirect('/login')

@app.route('/home')
def index():
    trending = articles.query.filter_by(date = date.today()).order_by(articles.views.desc()).limit(5)
    
    topId = top_article.query.first()
    topArt = articles.query.filter_by(id = topId.article_id).first()
    school_news = articles.query.filter_by(category = "School-related").order_by(articles.id.desc()).limit(4)
    
    if current_user.is_authenticated:
        lgtitle = 'Logout'
    else:
        lgtitle = ''
    return render_template('home.html', lgtitle=lgtitle, topArt = topArt, trending = trending, news = school_news)
@app.route('/write', methods=['POST', 'GET'])
def write():
    if current_user.is_authenticated:
        if request.method == 'POST':
            article = request.form['post_article']
            article_title = request.form['title']
            author = current_user.name
            category = request.form['Category']
            thumbnail = request.form['dataurl']
            
            today = date.today()

            
            #print('the article ' + article_title + ' was submited ' + str(today) + ' by ' + author + ' with the category of ' + category + ' The html is this: \n' + article)
            article_info = articles(author = author, date = str(today), title=article_title, articleHTML = article, category= category, thumbnail=thumbnail, username=current_user.username)
            db.session.add(article_info)
            db.session.commit()
            return redirect('/dashboard')
        return render_template('write.html')
    

    return render_template('deny.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    #db.session.close_all()
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        
        email = reg_form.email.data
        password = reg_form.password.data
        username = reg_form.username.data
        name = reg_form.name.data
        phone = reg_form.phone.data
        reason = reg_form.why.data

        hashed_pswd = pbkdf2_sha256.hash(password)
        
        user = Req(email = email, password=hashed_pswd, username=username, phone=phone, reason=reason, name=name)

        db.session.add(user)
        db.session.commit()
        db.session.close()
        return redirect('/home')
    else:
        if current_user.is_authenticated:
            return render_template('register.html', lgtitle = 'Logout', form=reg_form)
        return render_template('register.html', form=reg_form)
        

@app.route('/login', methods=['GET', 'POST'])
def loginpg():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)

        return redirect('/home')

    
    if not current_user.is_authenticated:
        return render_template('login.html', form = login_form)

    else:
        return render_template('login.html', form=login_form, lgtitle = 'Logout')
@app.route('/logout')
def logout():
    logout_user()

    return redirect('/home')

@app.route('/backdoor/requests', methods=['GET', 'POST'])
def back():
    if not current_user.is_authenticated:
        return redirect('/home')
    if current_user.admin == True:
        all_posts = Req.query.all()
    

        if request.method == 'POST':
            #print('post')
            post_email = request.form['email']
            post_username = request.form['username']
            post_name = request.form['name']
            post_phone = request.form['phone']
            post_reason = request.form['reason']
            accept_or_deny = request.form['ad']
            post_id = request.form['id']
            person = Req.query.filter_by(id=post_id).first()
            if accept_or_deny == 'accept':
                #print('accepted ' + post_name + ' ' + post_id)
            
                person_accepted = User(email = post_email, password=person.password, username=post_username, phone=post_phone, reason=post_reason, name=post_name)
                db.session.add(person_accepted)
                db.session.delete(person)
                db.session.commit()
            if accept_or_deny == 'deny':
            
                #print('denied ' + post_name + ' ' + post_id)
                db.session.delete(person)
                db.session.commit()
            return redirect('/backdoor/home')

        return render_template('acceptusers.html', requests = all_posts)
    else:
        return redirect('/home')

@app.route('/search/<string:type>/<string:textInputs>/<int:page>')

def searches(type, textInputs, page):
    textInput = textInputs.replace('%20', ' ')
    if current_user.is_authenticated:
        lgtitle = 'Logout'
    else:
        lgtitle = ''
    if type == 'title':
        all_posts = articles.query.filter_by(title=textInput).order_by(articles.id.desc()).paginate(per_page=10, page=page, error_out = True)
        return render_template('search2.html', data = all_posts, type=type, textInput = textInput, lgtitle = lgtitle)
    if type == 'author':
        all_posts = articles.query.filter_by(author=textInput).order_by(articles.id.desc()).paginate(per_page=10, page=page, error_out = True)
        return render_template('search2.html', data = all_posts, type=type, textInput = textInput, lgtitle = lgtitle)
    if type == 'category':
        all_posts = articles.query.filter_by(category=textInput).order_by(articles.id.desc()).paginate(per_page=10, page=page, error_out = True)
        return render_template('search2.html', data = all_posts, type=type, textInput = textInput, lgtitle = lgtitle)
@app.route('/search', methods=['POST', 'GET'])
def searchp():
    if current_user.is_authenticated:
        ltitle = 'Logout'
    else:
        ltitle = ''
    if request.method == 'POST':
        typeSearch = request.form['typeSearch']
        #pagenum = request.form['pagenum']
        input = request.form['text_search']
        if typeSearch == 'Category':
            
            
            category = request.form['category']
            input = category
            return redirect('/search/category/' + input + '/1')
            all_posts = articles.query.filter_by(category=category).order_by(articles.id.desc()).paginate(per_page=10, page=int(pagenum), error_out = True)
            
            print(all_posts)
            return render_template('search2.html', data = all_posts, lgtitle=ltitle, cat = category, action = '/search' )
        if typeSearch == 'Title':
            return redirect('/search/title/' + input + '/1')
            all_posts = articles.query.filter_by(title = input).all()
            
            return render_template('search.html', data = all_posts, lgtitle=ltitle )
        if typeSearch == 'Author':
            return redirect('/search/author/' + input + '/1')
            all_posts = articles.query.filter_by(author = input).all()
            
            return render_template('search.html', data = all_posts, lgtitle=ltitle )

        #print('Client searched by ' + typeSearch)
        return typeSearch
    return render_template('search.html', lgtitle = ltitle)




@app.route('/dashboard', methods=['GET', 'POST'])
def dash():
    
    if current_user.is_authenticated:
        if request.method == 'POST':
            articleID = request.form['id']
            article = articles.query.filter_by(id=articleID).first()
            db.session.delete(article)
            db.session.commit()

            
        userArt = articles.query.filter_by(username = current_user.username).all()
        return render_template('dash.html', articles = userArt )
    
    return render_template('deny.html')
@app.route('/article/<int:id>', methods=['GET', 'POST'])
def artView(id):
    if current_user.is_authenticated:
        lgtitle = 'Logout'
    else:
        lgtitle = ''
    
    article = articles.query.filter_by(id = id).first()
    article.views = article.views + 1
    db.session.commit()
    if article:
        if current_user.is_authenticated:
            if current_user.admin == True:
                
                deletHTML = '<form  id="delform" style="align-self: center;"><input type="text" name="type" value="del" hidden><input id="deleteId" type="text" name="delete"  hidden> <input type="submit" value="delete" style="color: white; background-color: black; border-style: solid; border-color: goldenrod; width:160px; outline: none; width: 250px; padding: 12px; border-width: 1px;"></form>'
                if request.method == 'POST':
                    type = request.form['type']
                    #print(type)
                    if type == 'del':
                        if article.username == admin:
                            return redirect('/home')
                        else:
                            artID = id
                            article = articles.query.filter_by(id = artID).first()
                            db.session.delete(article)
                            db.session.commit()
                    elif type == 'top':
                        topArt = id
                        isTop = top_article.query.first()
                        if isTop:
                            db.session.delete(isTop)
                            db.session.commit()
                        newTop = top_article(article_id = topArt)
                        db.session.add(newTop)
                        db.session.commit()
                    elif type == 'report':
                        artID = id
                        isReported = articles.query.filter_by(id = artID).first()
                        if not isReported.reported == True:
                            isReported.reported = True
                            db.session.commit()  
                    return redirect('/home')
                    
                return render_template('articleViewer.html', article = article,lgtitle=lgtitle, delete = deletHTML,  video="video", topart = '<form  id="topform" style="align-self: center;"><input type="text" name="type" value="top" hidden><input id="topId" type="text" name="topid"  hidden> <input type="submit" value="Make top article" style="color: white; background-color: black; border-style: solid; border-color: goldenrod; width:160px; outline: none; width: 250px; padding: 12px; border-width: 1px;"></form>')
        if request.method == 'POST':
            artID = id
            isReported = articles.query.filter_by(id = artID).first()
            
            if  not isReported.reported == True:
                isReported.reported = True
                db.session.commit()
            
            return redirect('/home')
        
        return render_template('articleViewer.html', article = article, lgtitle=lgtitle, video="video")
    else:
        return redirect('/home')
    
@app.route('/backdoor/home')
def backhome():
    if current_user.is_authenticated and current_user.admin == True:
        return render_template('backdoor-home.html')
    else:
        return redirect('/home')
@app.route('/backdoor/users', methods=['POST', 'GET'])
def backusers():
    if not current_user.is_authenticated:
        return redirect('/home')
    if current_user.admin == True:
        all_users = User.query.all()
        return render_template('backdoor-users.html', users = all_users)
    else:
        return redirect('/home')
@app.route('/backdoor/users/<string:userInfo>', methods=['POST', 'GET'])
def Uinfo(userInfo):
    user = User.query.filter_by(username = userInfo).first()
    art = articles.query.filter_by(username = user.username).all()
    if not current_user.is_authenticated:
        return redirect('/home')
    if current_user.admin == True:
        if current_user.username == admin:
            if request.method == 'POST':
            
            
            
                if userInfo == admin and current_user.username != admin:
                    return redirect('/backdoor/users')
                elif current_user.username == admin:
                    if request.method == 'POST':
                        type = request.form['type']
                    
                        #print('type is ' + type)
                        if type == 'AdminPerm':
                            adminName = request.form['username']
                            decision = request.form['decision']
                            if decision == 'Take admin permission':
                                user.admin = False
                                db.session.commit()
                            elif decision == 'Enable admin permission':
                                user.admin = True
                                db.session.commit()
                            return redirect('/backdoor/home')
                        else:
                            #print('ban')
                            ban_reason = request.form['reason']
                            banned_person = banned(email = user.email, password=user.password, username=user.username, name=user.name, phone=user.phone, reason=user.reason, admin=user.admin, ban_reason=ban_reason, banned_by = current_user.name)
                            db.session.add(banned_person)
                            db.session.delete(user)
                            db.session.commit()
                            return redirect('/backdoor/home')
            return render_template('user-info.html', user=user,lgtitle='Logout', articles = art, adminform = '<form action="/backdoor/users" style="align-self: center; width: 200px;" id="adform"><input type="text" name="type" value="AdminPerm"hidden><input type="text" name="username"  id="banname" hidden><input type="submit" value=""  name="decision" id="make/takeadmin" style="color: goldenrod; align-self: center; margin-bottom: 20px; font-size: normal; background-color:black; width: 100%;"></form>')
        else:
            if request.method == 'POST':
                    
                ban_reason = request.form['reason']
                banned_person = banned(email = user.email, password=user.password, username=user.username, name=user.name, phone=user.phone, reason=user.reason, admin=user.admin, ban_reason=ban_reason, banned_by = current_user.name)
                db.session.add(banned_person)
                db.session.delete(user)
                db.session.commit()
                return redirect('/backdoor/home')
            return render_template('user-info.html', user=user, articles = art, lgtitle='Logout')
    return redirect('/home')
@app.route('/backdoor/banned', methods=['GET', 'POST'])  
def banUsers():
    banned_users = banned.query.all()
    if not current_user.is_authenticated:
        return redirect('/home')
    if current_user.admin == True:
        if request.method == 'POST':
            uname = request.form['username']
            user = banned.query.filter_by(username = uname).first()
            unban = User(email=user.email, password = user.password, username  = user.username, name=user.name, phone=user.phone, reason=user.reason, admin=user.admin)
            db.session.add(unban)
            db.session.delete(user)
            db.session.commit()
            return redirect('/backdoor/home')
        return render_template('banned.html', user = banned_users)
    else:
        return redirect('/home')
@app.route('/video', methods=['GET', 'POST'])
def vid():
    if not current_user.is_authenticated:
        return redirect('/home')
    else:
        if request.method == 'POST':
            title = request.form['title']
            thumbnail = request.form['thumbnailSRC']
            category = request.form['Category']
            video = request.form['video_blob']
            author = current_user.name
            type = 'video'

            today = date.today()
            article_info = articles(author = author, date = str(today), title=title, articleHTML = video, category= category, thumbnail=thumbnail, post_type = type, username=current_user.username)
            db.session.add(article_info)
            db.session.commit()
            return redirect('/dashboard')
        return render_template('video.html')

@app.route('/info')
def info():
    if not current_user.is_authenticated:
        return redirect('/home')
    else:
        return render_template('info.html', user=current_user ,lgtitle='Logout')
@app.route('/backdoor/reported', methods=['POST', 'GET'])
def repo():
    if not current_user.is_authenticated:
        return redirect('/home')
    if current_user.admin == True:

        reported = articles.query.filter_by(reported = True).all()
        if request.method == 'POST':
            artID = request.form['artID']
            article = articles.query.filter_by(id=artID).first()
            article.reported = False
            db.session.commit()
            return redirect('/backdoor/reported')
        return render_template('reported.html', reported = reported)
    else:
        return redirect('/home')

if __name__ == "__main__":
    #manager.run()
    app.run(debug=True, host='0.0.0.0', port='3000')
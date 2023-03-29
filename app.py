from flask import Flask,render_template,redirect,flash,url_for,session, abort,request
from models import connect_db,User,Feedback,hash_function,hash_function_check
from forms import RegisterForm,LoginForm,FeedbackForm,EditUserForm,EditPasswordForm
from variables import SECRET_KEY,SQLALCHEMY_DATABASE_URI,SQLALCHEMY_TRACK_MODIFICATIONS,SQLALCHEMY_ECHO,DEBUG_TB_INTERCEPT_REDIRECT,TESTING,DEBUG_TB_HOSTS,database,dont_show_debug_toolbar
from secrets_key import flask_secret_key
from session_variables import session_username,session_fullname,session_is_admin
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config[SECRET_KEY] = flask_secret_key
app.config[SQLALCHEMY_DATABASE_URI] = database
app.config[SQLALCHEMY_TRACK_MODIFICATIONS] = False
app.config[SQLALCHEMY_ECHO] = True
app.config[DEBUG_TB_INTERCEPT_REDIRECT] = False
app.config[TESTING] = True
app.config[DEBUG_TB_HOSTS] = dont_show_debug_toolbar
connect_db(app)
toolbar = DebugToolbarExtension(app)
  

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(401)
def access_denied(e):
    return render_template('401.html'), 401

def clear_session():
     if session_username in session:
        session.pop(session_username)
     if session_fullname in session:
        session.pop(session_fullname)
     if session_is_admin in session:
        session.pop(session_is_admin)

@app.route('/')
def root():
    if session_username in session:
      return redirect(url_for('feedback_all'))
    return redirect(url_for('login'))

@app.route('/register', methods=["GET", "POST"])
def register():
    """ Sign up view. """


    if session_username in session:
      return redirect(url_for('show_user',username=session.get(session_username)))

    form=RegisterForm()
    if form.validate_on_submit():
         firstname = form.first_name.data
         lastname = form.last_name.data
         username = form.username.data
         email = form.email.data
         password = form.password.data
         new_user =  User.register(firstname, lastname, username.casefold(), email, password)
         
         if User.get_users().filter(User.username == username.casefold()).count() > 0:
             form.username.errors = ["This username already exists. Please enter a new username!"]
             if User.get_users().filter(User.email == email).count() > 0:
                   form.email.errors = ["This email address already exists. Please enter another one!"]
             return render_template('authentication/register.html',form=form)
         User.add_users(new_user)
         if new_user.id:
             session[session_username] = new_user.username
             session[session_fullname] = new_user.full_name
             session[session_is_admin] = new_user.is_admin
             flash('Registration succeeded!','success')
             return redirect(url_for('feedback_all'))
         
    return render_template('authentication/register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    """ login view. """
    if session_username in session:
      return redirect(url_for('feedback_all'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.login(username = username.casefold(), password = password)
        if user:
           session[session_username] = user.username
           session[session_fullname] = user.full_name
           session[session_is_admin] = user.is_admin
           return redirect(url_for('feedback_all'))
        else:
            form.username.errors = ["Bad username or password"]

    return render_template('authentication/login.html',form=form)

@app.route('/logout',methods=['POST'])
def logout():
    clear_session()
    return redirect(url_for('login'))
   
############################# User section ###########################################
@app.route('/users/<username>',methods=['GET', 'POST'])
def show_user(username):
    """ User detail view. """

    if session_username not in session:
        flash('Please log in first!','info')
        return redirect(url_for('login'))
    if session_username in session and ((username != session.get(session_username)) and (session.get('is_admin') == False)):
         abort(401)
    user = User.get_users().filter(User.username == username).first()
    if user is None:
        abort(404)

    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        if Feedback.add_feedback(username, title, content):
              return redirect(url_for('show_user',username = username))
        
    return render_template('users/show.html',user=user,form=form)

@app.route('/users/<username>/edit',methods=['GET', 'POST'])
def edit_user(username):
    """ User detail edit view. """

    if session_username not in session:
        flash('Please log in first!','info')
        return redirect(url_for('login'))
    if session_username in session and ((username != session.get(session_username)) and (session.get('is_admin') == False)):
         abort(401)
    
    user = User.get_users().filter(User.username == username).first()

    if user is None:
        abort(404)

    form = EditUserForm(obj=user)
    if form.validate_on_submit():
         firstname = form.first_name.data
         lastname = form.last_name.data
         email = form.email.data
         is_admin = form.is_admin.data
         
         user_final = User.update_users(user.id, firstname,lastname,email,is_admin)
         if user_final:
             if session.get(session_username) == username:
                session[session_fullname] = user_final.full_name
                session[session_is_admin] = user_final.is_admin
             flash('Profile updated successfully!','success')
             return redirect(url_for('show_user',username = username))

    
    return render_template('users/edit.html',form=form,username=username)

@app.route('/users/<username>/password/edit',methods=['GET', 'POST'])
def edit_password(username):
    """ User password edit view. """

    if session_username not in session:
        flash('Please log in first!','info')
        return redirect(url_for('login'))
    if session_username in session and (username != session.get(session_username) and not  session.get('is_admin')):
         abort(401)
    
    user = User.get_users().filter(User.username == username).first()

    if user is None:
        abort(404)

    form = EditPasswordForm()
    if form.validate_on_submit():
         
         password_old = form.password_old.data
         password_new = form.password_new.data
         password_new_confirm = form.password_new_confirm.data

         if hash_function_check(user.password, password_old):
             if password_new == password_new_confirm:
                 is_save = User.update_password(user.id, hash_function(password_new_confirm))
                 if is_save:
                    flash('Password updated successfully!','success')
                    return redirect(url_for('show_user',username = session.get('username')))
             else:
                  form.password_new_confirm.errors = ['Your new password is incorrect!']
         else:
             form.password_old.errors = ['Your current password is invalid!']
        
    return render_template('users/pass-edit.html',form = form,username=username)

@app.route('/users/<username>/delete',methods=['POST'])
def delete_user(username):
    """ User deleting . """

    if session_username not in session:
        flash('Please log in first!','info')
        return redirect(url_for('login'))
    
    user = User.get_users().filter(User.username == username).first()
    if user is None:
        abort(404)
    if session_username in session and (username != session.get(session_username) and not  session.get('is_admin')):
         abort(401)
    
    if User.delete_users(user.id):
           if user.username == session.get('username'):
              flash('User deleted successfully!','success')
              clear_session()
              return redirect(url_for('login'))
           else:
                flash('User deleted successfully!','success')
                return redirect(url_for('users_all'))
    
@app.route('/users')
def users_all():
    if session_username not in session:
        flash('Please log in first!','info')
        return redirect(url_for('login'))
    
    if session_username in session  and (session.get('is_admin') == False):
         abort(401)

    users = User.get_users().order_by(User.last_name,User.first_name).all()
                
    return render_template('users/list.html',users=users)


############################# Feedback section ###########################################
@app.route('/feedback',methods=['GET', 'POST'])
def feedback_all():
    """ All feedback and feedback post form """

    if session_username not in session:
        flash('Please log in first!','info')
        return redirect(url_for('login'))

    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        if Feedback.add_feedback(session.get(session_username), title, content):
              return redirect(url_for('feedback_all'))
            
    feedbacks = Feedback.get_feedbacks().order_by(Feedback.created_at.desc()).all()
    return render_template('feedbacks/index.html',form=form,feedbacks=feedbacks)

@app.route('/feedback/<int:feedback_id>/update',methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    """ Edit feedback """
    if session_username not in session:
        flash('Please log in first!','info')
        return redirect(url_for('login'))
    
    feedback = Feedback.get_feedback_by_id(feedback_id)
    if session_username in session and (feedback.username != session.get(session_username) and not  session.get('is_admin')):
         abort(401)
    form = FeedbackForm(obj=feedback)
    return_page_code=request.args.get('back')
    
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        if Feedback.update_feedback(feedback.id, feedback.title, feedback.content):
           flash(f"Feedback '{feedback.title}' has been updated successfully!",'success')
           if return_page_code == 'feed':
              return redirect(url_for('feedback_all'))
           elif return_page_code == 'profile':
              return redirect(url_for('show_user',username = session.get('username')))

    return render_template('feedbacks/edit.html',form=form,feedbacks_id=feedback.id,date_published=feedback.friendly_date,return_page_code=return_page_code)

@app.route('/feedback/<int:feedback_id>/delete',methods=['POST'])
def delete_feedback(feedback_id):
    """ Delete feedback """
    if session_username not in session:
        flash('Please log in first!','info')
        return redirect(url_for('login'))
    
    feedback = Feedback.get_feedback_by_id(feedback_id)
    if feedback is None:
        abort(404)
    if session_username in session and (feedback.username != session.get(session_username) and not  session.get('is_admin')):
         abort(401)
    return_page_code=request.args.get('back')

    if Feedback.delete_feedback(feedback.id):
           flash('Feedback deleted successfully!','success')
           if return_page_code == 'feed':
              return redirect(url_for('feedback_all'))
           elif return_page_code == 'profile':
              return redirect(url_for('show_user',username = session.get('username')))



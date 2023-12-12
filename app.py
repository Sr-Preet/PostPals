from flask import Flask,redirect,url_for,request,render_template,session
from datetime import datetime
import sqlite3
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home_page():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Fetch data from the blogs table
    cursor.execute('SELECT * FROM blogs ORDER BY id DESC')
    blogs_data = cursor.fetchall()
    conn.close()
    return render_template('index.html',data=blogs_data) 
  

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        fname=request.form['fname']
        lname=request.form['lname']
        contact=request.form['contact']
        email=request.form['email']
        password=request.form['password']

        # if lname=='' or fname=='':
        #     return render_template('register.html',data={'success': False, 'message': 'Please Fill all the fields'}) 

        # if not email or '@' not in email:
        #     return render_template('register.html',data={'success': False, 'message': 'Invalid email address'}) 

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO USERS (email,fname,lname,contact,password)
                VALUES (?, ?, ?, ?, ?)
            ''', (email, fname, lname, contact, password))
            conn.commit()
            conn.close()

            return render_template('register.html',data={'success': True})     

        except Exception as e:
            conn.close()
            return render_template('register.html', data={'success': False})

    return render_template('register.html',data={'success': None}) 

def is_valid_login(email, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the email exists in the database
    cursor.execute('SELECT * FROM USERS WHERE email = ?', (email,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data and user_data[4] == password:
        # Email and password match
        return True

    # Email or password is incorrect
    return False



@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        if is_valid_login(email, password):
            session['logged_email'] = email
            return redirect(url_for('user_dashboard'))
        else:
            return render_template('login.html', data={'success': False, 'message': 'Invalid email or password'})
    else:
        if 'logged_email' in session:
            return redirect(url_for('user_dashboard'))
        else:
            return render_template('login.html',data={'success': None, 'message': 'Nothing'})         



    



@app.route('/user_dashboard',methods=['POST','GET'])
def user_dashboard():
    if request.method=='POST':
        return ''
    else:
        if 'logged_email' in session:
            logged_email = session['logged_email']
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Fetch data from the blogs table
            cursor.execute('SELECT * FROM users where email=? ',(logged_email,))
            user_detail = cursor.fetchone()

            cursor.execute('SELECT COUNT(*) FROM blogs WHERE email=?', (logged_email,))
            count_result = cursor.fetchone()
            print(count_result[0])
            return render_template('user_dashboard.html',name={'fname':user_detail[1],'lname':user_detail[2],'count':count_result[0]})
        else:
            return redirect(url_for('login'))



@app.route('/add_new_blog',methods=['POST','GET'])
def user_add_blog():
    
    if request.method=='POST':
        blog_heading=request.form['bh']
        blog_info=request.form['bi']
        category = request.form['selectedOption'] 
        logged_email = session['logged_email']
        
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('database.db')
    
        # Connect to the database again
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM USERS WHERE email = ?', (logged_email,))
        user_data = cursor.fetchone()
        uname = user_data[1]+" "+user_data[2]
    

        cursor.execute('INSERT INTO blogs (name,info,category,email,uname,dateTime) VALUES (?,?,?,?,?,?)', (blog_heading,blog_info,category,logged_email,uname,formatted_datetime))


        conn.commit()
        conn.close()
        return redirect(url_for('user_view_blog'))



@app.route('/latest_blog/', defaults={'category': None})
@app.route('/latest_blog/<category>')
def latest_blog(category):
    if category==None:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Fetch data from the blogs table
        cursor.execute('SELECT * FROM blogs ORDER BY id DESC')
        blogs_data = cursor.fetchall()
        conn.close()
        return render_template('latest_blogs.html',data=blogs_data,category=None) 
    else:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Fetch data from the blogs table
        cursor.execute('SELECT * FROM blogs where category=? ORDER BY id DESC',(category,))
        blogs_data = cursor.fetchall()
        conn.close()
        return render_template('latest_blogs.html',data=blogs_data,category=category)

  

@app.route('/logout')
def logout():
    session.pop('logged_email')
    return redirect(url_for('login'))
  


@app.route('/user_view_blog')
def user_view_blog():
    if 'logged_email' in session:
        logged_email = session['logged_email']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Fetch data from the blogs table
        cursor.execute('SELECT * FROM blogs where email=?  ORDER BY id DESC',(logged_email,))
        blogs_data = cursor.fetchall()

        conn.close()

        return render_template('user_view_blogs.html',data=blogs_data) 
  
    else:
        return redirect(url_for('login'))



@app.route('/delete/<int:id>')
def delete(id):
        conn = sqlite3.connect('database.db')
        print(f"Deleting blog with id: {id}")
        conn.execute('Delete FROM blogs where id=?',(id,))
        conn.commit() 
        conn.close()
        print(f"Deleting blog succesfuly")
        return redirect(url_for('user_view_blog'))


@app.route('/search',methods=['POST','GET'])
def search_blog():
    print("I am running")
    if request.method=='POST':
        search=request.form['search']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM blogs WHERE name LIKE ? OR info LIKE ?', ('%' + search + '%', '%' + search + '%'))
        search_results = cursor.fetchall()

        return render_template('Search_blogs.html',data=search_results) 
    
    else:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Fetch data from the blogs table
        cursor.execute('SELECT * FROM blogs ORDER BY id DESC')
        blogs_data = cursor.fetchall()
        conn.close()
        return render_template('Search_blogs.html',data=blogs_data) 

 

if __name__=="__main__":
    app.run()

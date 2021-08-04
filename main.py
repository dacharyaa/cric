from flask import Flask, render_template, request, jsonify, url_for
import mysql.connector as connection

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST']) # To render Homepage
def home_page():
    return render_template('index.html')

@app.route('/select', methods=['POST'])  # This will be called from UI
def math_operation():
    result= []
    if (request.method=='POST'):
        operation=request.form['operation']

        if(operation=='select'):
            mydb = connection.connect(host="localhost", database='student', user="root", passwd="mysql", use_pure=True)

            cursor = mydb.cursor()
            qry = 'select * from cric '

            cursor.execute(qry)
            result = cursor.fetchall()
            print('Records fetched ...', cursor.rowcount)


        return render_template('results.html',result=result)


# This route is for Update our Players
@app.route('/update/<id>/', methods=['GET', 'POST'])
def update(id):
    print(int(id))
    mydb = connection.connect(host="localhost", database='student', user="root", passwd="mysql", use_pure=True)
    cursor = mydb.cursor()
    qry = 'select first_name,last_name from cric where idd= {}'.format(int(id))
    print(qry)

    cursor.execute(qry)
    row= cursor.fetchone()
    print(row[0],row[1])
    return render_template('updatedelete.html', idd= id,first_name=row[0],last_name=row[1])

@app.route('/edit', methods=['POST'])  # This will be called from UI
def edit():
    print('edit---------')
    if (request.method=='POST'):
        idd = int(request.form['id1'])
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        print('idd -->>>',idd)
        print('Name -->>>', first_name ,last_name)
        mydb = connection.connect(host="localhost", database='student', user="root", passwd="mysql", use_pure=True)
        cursor = mydb.cursor()
        str= "update cric set first_name= '{}',last_name= '{}' where idd= {}".format(first_name,last_name,idd)
        print(str)
        cursor.execute(str)
        mydb.commit()
    return render_template('index.html')

@app.route('/insert', methods=['GET','POST'])  # insert a player to DB
def insert():
    print('insert a player---------')
    return render_template('insert_record.html')
@app.route('/insert_record', methods=['POST'])  # This will be called from UI
def insert_record():
    print('insert_record---------')
    if (request.method=='POST'):
        idd1 = int(request.form['id1'])
        first_name1 = request.form['first_name']
        last_name1 = request.form['last_name']
        print('idd -->>>',idd1)
        print('Name -->>>', first_name1 ,last_name1)
        mydb = connection.connect(host="localhost", database='student', user="root", passwd="mysql", use_pure=True)
        cursor = mydb.cursor()
        str = "insert into cric (idd,first_name,last_name) values({},'{}','{}')".format(idd1,first_name1, last_name1)
        print(str)
        cursor.execute(str)
        mydb.commit()
        return render_template('index.html')

# This route is for Delete our Players
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    print(id)
    mydb = connection.connect(host="localhost", database='student', user="root", passwd="mysql", use_pure=True)
    cursor = mydb.cursor()
    qry = 'delete from cric where idd= {}'.format(int(id))
    print(qry)

    cursor.execute(qry)
    mydb.commit()
    result='Record ID {} Data Deleted'.format(int(id))

    return render_template('delete.html',result=result)



if __name__ == '__main__':
    app.run()

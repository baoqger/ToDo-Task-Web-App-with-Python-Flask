from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker 
from database_setup import Base, ToDoTask
import time, datetime

def time_consume(total_time):
	hour = int(total_time // 3600)
	total_time = total_time%3600
	min = int(total_time // 60)
	total_time = total_time % 60
	sec = int(total_time)
	#print hour
	#print min
	#print sec
	return str(hour) + "hour" + str(min) + "mins" + str(sec) + "secs"


app = Flask(__name__)

engine = create_engine('sqlite:///todotask_new5.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/todotask')
def index():
	items = session.query(ToDoTask).order_by(ToDoTask.priority)
	return render_template('index.html', items = items)
	
@app.route('/todotask/new', methods = ['GET','POST'])
def newTask():
	if request.method == 'POST':
		newItem = ToDoTask(content = request.form['content'], priority = request.form['priority'], status = 'Created')
		session.add(newItem)
		session.commit()
		flash_message = "Task" + str(newItem.id) + " is added."
		flash(flash_message)
		return redirect(url_for('index'))
	else:
		return render_template('newtask.html')

@app.route('/todotask/<int:task_id>/edit', methods = ['GET','POST'])
def editTask(task_id):
	editeditem = session.query(ToDoTask).filter_by(id = task_id).one()
	if request.method == 'POST':
		editeditem.content = request.form['content']
		editeditem.priority = request.form['priority']
		session.add(editeditem)
		session.commit()
		flash_message = "Task" + str(task_id) + " is edited."
		flash(flash_message)
		return redirect(url_for('index'))
	else:
		return render_template('edittask.html', item = editeditem)

@app.route('/todotask/<int:task_id>/delete', methods = ['GET','POST'])
def deleteTask(task_id):
	deletedItem = session.query(ToDoTask).filter_by(id = task_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash_message = "Task" + str(task_id) + " is deleted."
		flash(flash_message)
		return redirect(url_for('index'))
	else:
		return render_template('deletetask.html', item = deletedItem)

@app.route('/todotask/<int:task_id>/done', methods = ['GET','POST'])
def doneTask(task_id):
	doneItem = session.query(ToDoTask).filter_by(id = task_id).one()
	if request.method == 'POST':
		
		time_cost =  time.time() - doneItem.create_time
		print time_cost
		str_time_cost = time_consume(time_cost)
		doneItem.status = 'Done'
		doneItem.used_time = str_time_cost
		#print str_time_cost
		session.add(doneItem)
		session.commit()
		flash_message = "Task" + str(task_id) + " is done."
		flash(flash_message)
		return redirect(url_for('index'))
	else:
		return render_template('donetask.html', item = doneItem)

@app.route('/todotask/update', methods = ['GET'])
def updateTask():
	current_time = time.time()
	items = session.query(ToDoTask).order_by(ToDoTask.priority)
	str_time_pass_list = []
	for each_item in items:
		item_status = each_item.status
		if item_status == "Created":
			each_create_time = each_item.create_time
			each_pass_time = current_time - each_create_time
			str_time_pass_list.append([item_status,time_consume(each_pass_time)])
		else:
			each_pass_time = each_item.used_time
			str_time_pass_list.append([item_status,each_item.used_time])
	print str_time_pass_list
	return jsonify(result =str_time_pass_list)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
import pymysql
import settings
import docker_interface


def get_db(config):
	host = config['host']
	port = config['port']
	user = config['user']
	password = config['password']
	dbname = config['dbname']
	db = pymysql.connect(host=host, port=port, user=user, password=password, db=dbname)
	return db


def update_task_status(status, task_id):
	db = get_db(settings.db)
	cursor = db.cursor()
	sql = "UPDATE task SET task_status=%s WHERE id=%s"
	try:
		cursor.execute(sql, (status, task_id))
		db.commit()
	except Exception as e:
		db.rollback()
		print(e)
	finally:
		db.close()


def check_task_status(task_id):
	db = get_db(settings.db)
	cursor = db.cursor()
	sql = "SELECT task_status FROM task WHERE id=%s"
	try:
		cursor.execute(sql, (task_id))
		task_status = cursor.fetchone()
		print('The task_status of task ' + str(task_id) + ' is ' + str(task_status[0]))
		return task_status[0]
	except Exception as e:
		print(e)
	finally:
		db.close()


def get_all_not_finished_tasks():
	tasks = []
	db = get_db(settings.db)
	cursor = db.cursor()
	sql = 'SELECT id FROM task WHERE task_status<>0'
	cursor.execute(sql)
	for task in cursor.fetchall():
		tasks.append(task[0])
	print('all_not_finished_tasks: ' + str(tasks))
	return tasks


def get_all_finished_tasks():
	tasks = []
	db = get_db(settings.db)
	cursor = db.cursor()
	sql = 'SELECT id FROM task WHERE task_status=0'
	cursor.execute(sql)
	for task in cursor.fetchall():
		tasks.append(task[0])
	print('all_finished_tasks: ' + str(tasks))
	return tasks


def change_executor_status():
	db = get_db(settings.db)
	cursor = db.cursor()
	sql = 'update executor set status = 0 where exec_ip = %s'
	try:
		cursor.execute(sql, (docker_interface.config['self']['ip']))
		db.commit()
	except Exception as e:
		print(e)
	finally:
		db.close()


if __name__ == '__main__':
	# update_task_status(0, 1)
	check_task_status(2)
	get_all_not_finished_tasks()
	get_all_finished_tasks()

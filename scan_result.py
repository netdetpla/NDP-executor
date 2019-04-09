import threading
import os
import settings
import db_manager
import codecs
from kafka_test import Kafka_producer
import json
import time


def scan_result():
	print('scan_result_thread starts')
	path = settings.watch_dir
	while True:
		tasks = db_manager.get_all_finished_tasks()
		for task_id in tasks:
			send_result(task_id)
		time.sleep(5)


def send_result(task_id):
	print('sending result...')

	if not os.path.exists(settings.watch_dir + os.sep + task_id + os.sep + 'result'):
		print('no result dir')
		db_manager.update_task_status(-3, task_id)
		return

	resultList = os.listdir(settings.watch_dir + os.sep + str(task_id) + os.sep + 'result')
	for result in resultList:
		if result.split('.')[-1] == 'result':
			f = codecs.open(settings.watch_dir + os.sep + str(task_id) + os.sep + 'result' + os.sep + result, 'r',
							'utf-8')
			try:
				result = f.read()
				result = {'task_id': task_id, 'md5': '', 'resultline': result}
				producer = Kafka_producer(settings.kafka_ip, settings.kafka_port, settings.result_topic_name)
				producer.sendjsondata(json.dumps(result).encode())
				print(result)
			except Exception as e:
				print('in send_result: ' + str(e))
			finally:
				f.close()
	print('send result complete.')
	db_manager.update_task_status(-2, task_id)
	return


if __name__ == '__main__':
	scan_result()

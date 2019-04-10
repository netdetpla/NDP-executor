import threading
import os
import settings
import db_manager
import codecs
from kafka_test import Kafka_producer
import json
import time
import docker_interface


def scan_result():
	print('scan_result_thread starts')
	path = settings.watch_dir
	while True:
		tasks = db_manager.get_all_finished_tasks()
		for task_id in tasks:
			pass
			# send_result(task_id)
		time.sleep(5)


def send_result(container_name):
	task_id = container_name[4:]
	print('sending result...')

	if not os.path.exists(settings.watch_dir + os.sep + container_name + os.sep + 'result'):
		print('no result dir')
		db_manager.update_task_status(-1, container_name)
		return

	resultList = os.listdir(settings.watch_dir + os.sep + str(container_name) + os.sep + 'result')
	for result in resultList:
		if result.split('.')[-1] == 'result':
			f = codecs.open(settings.watch_dir + os.sep + str(container_name) + os.sep + 'result' + os.sep + result, 'r',
							'utf-8')
			try:
				result = f.read()
				result = {'task_id': task_id, 'md5': '', 'resultline': result}
				print("result: " + str(result))
				producer = Kafka_producer(settings.kafka_ip, settings.kafka_port, settings.result_topic_name)
				producer.sendjsondata(json.dumps(result).encode('utf-8'))
				docker_interface.delete_container(container_name)
			except Exception as e:
				print('in send_result: ' + str(e))
			finally:
				f.close()
	print('send result complete.')
	db_manager.update_task_status(20030, task_id)
	return


if __name__ == '__main__':
	scan_result()

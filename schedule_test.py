import datetime
import json
import socket
from pykafka import KafkaClient


def send_task_test():
	data = {
		"id": "1",
		"task_tag": "task",
		"image_name": "ubuntu",
		"tag": "1.0.0",
		"config": {

		},
		"param": {
			"time": datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		}
	}
	data_json = json.dumps(data)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1', 9996))
	s.send(data_json.encode())


def accept_result(port, kafkaHost, kafkatopic):
	pass


if __name__ == '__main__':
	send_task_test()
	accept_result()

# def taskResultLink(port,db,machineManager,taskManager,kafkaHost,kafkatopic):#通过kafka接收镜像任务执行的结果文件中的记录
#     print('taskResultLink start')
#     client = KafkaClient(hosts=kafkaHost)#链接kafka
#
#     print client.topics
#
#     topic = client.topics[bytes(kafkatopic)]
#     consumer = topic.get_simple_consumer(consumer_group='taskResultLink', auto_commit_enable=True, auto_commit_interval_ms=1,
#                                          consumer_id='taskResultLink')
#     for message in consumer:
#         if message is not None:
#             time.sleep(7)
#             taskResultUpdate(message.value,db,machineManager,taskManager)
#         else:
#             print('Waiting for new message...')
#             time.sleep(10)
# def taskResultUpdate(message,db,machineManager,taskManager):
#     print ('Accept new message')
#     try:
#         db.ping(True)
#     except (AttributeError, MySQLdb.OperationalError):
#         db.close()
#         db=getSQLConnecter(machineManager.conf)
#     if (is_json(message)==False):#检查jason格式
#         return
#     resultjson = json.loads(message)
#     mysqlUpdateResult(db,resultjson,taskManager)

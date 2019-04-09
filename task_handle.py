import socket
import json
import os
import threading
import datetime
import docker_interface
import scan_result

with open("config.json", 'r') as f:
	config = json.load(f)

scheduling_ips = config["scheduling"]["ip"]
task_port = config["scheduling"]["task-port"]
self_port = config["self"]["port"]
containers = []


def server_for_task():
	print('task_handle_thread starts')
	sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sockfd.bind(('', self_port))
	sockfd.listen(5)

	while True:
		client_sock, client_addr = sockfd.accept()
		if client_addr[0] not in scheduling_ips:
			client_sock.close()
		else:
			recv_json = ""
			while True:
				buf = client_sock.recv(1024).decode()
				if buf:
					recv_json += buf
				else:
					break
			client_sock.close()
			print("receive json: " + recv_json)
			recv_dict = json.loads(recv_json)

			# 接受json后的处理
			if recv_dict['task_tag'] == 'task':
				parse_task_thread = threading.Thread(target=parse_task, args=(recv_dict, client_addr[0],))
				parse_task_thread.start()
			# parse_task_thread.join()
			elif recv_dict['task_tag'] == 'delete':
				target_container = recv_dict['taskid']
				docker_interface.delete_container(target_container)

			print("waitting for next connection...")


# reply暂缺
def parse_task(task_config, scheduling_ip):
	print("parsing task config")
	print("creating sub_task environment")

	reply = {}
	try:
		reply['task_id'] = task_config['id']
		reply['result_status'] = 0
		reply['desc'] = 'success'

		mid_name = task_config['id'] # + '_' + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
		dirs = '/tmp/' + mid_name
		os.makedirs(dirs + '/conf')
		with open(dirs + '/conf/config.json', 'w') as f:
			content = task_config['param']
			content = json.dumps(content)
			f.write(content)
		with open(dirs + '/conf/id', 'w') as f:
			f.write(mid_name)
		id = docker_interface.create_container(
			task_config['image_name'],
			dirs,
			mid_name,
			task_config['config']
		)
		# 若创建容器成功
		if id:
			check_container_status_thread = threading.Thread(target=docker_interface.check_container_status, args=(mid_name, task_config['id']))
			check_container_status_thread.setName(mid_name)
			check_container_status_thread.start()
		else:
			reply['result_status'] = -1
			reply['desc'] = 'failure'
	except Exception as e:
		print(e)
		reply['result_status'] = -1
		reply['desc'] = 'failure'
	finally:
		send_dresult(scheduling_ip, task_port, reply)


def send_dresult(scheduling_ip, task_port, reply):
	sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sockfd.connect((scheduling_ip, task_port))
	print(json.dumps(reply))
	sockfd.send(json.dumps(reply).encode('utf-8'))
	sockfd.close()


if __name__ == '__main__':
	server_for_task()

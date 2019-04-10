import threading
import os
import sys
import signal
import task_handle
import scan_result


class Watcher:
	def __init__(self):
		self.child = os.fork();
		if self.child == 0:
			return
		else:
			self.watch()

	def watch(self):
		try:
			os.wait()
		except KeyboardInterrupt:
			print("all servers on task machine exit.")
			self.kill()
		sys.exit()

	def kill(self):
		try:
			os.kill(self.child, signal.SIGKILL)
		except OSError:
			print("os error!")


Watcher()

task_handle_thread = threading.Thread(target=task_handle.server_for_task)
task_handle_thread.start()
# scan_result_thread = threading.Thread(target=scan_result.scan_result)
# scan_result_thread.start()
# task_handle_thread.join()

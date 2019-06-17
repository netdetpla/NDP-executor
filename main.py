import threading
import os
import sys
import signal
import task_handle
import scan_result
import time


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


def rm_exited_container():
    while True:
        # 每过一段时间清理已存在的container
        time.sleep(10)
        print("rm exited container")
        os.system("docker rm $(docker ps -q -f status=exited)")


Watcher()

task_handle_thread = threading.Thread(target=task_handle.server_for_task)
task_handle_thread.start()

rm_exited_container_thread = threading.Thread(target=rm_exited_container)
rm_exited_container_thread.start()
# scan_result_thread = threading.Thread(target=scan_result.scan_result)
# scan_result_thread.start()
# task_handle_thread.join()

# coding=utf-8

import docker
import json
import os
import time
import db_manager
import scan_result
import settings

with open('config.json', 'r') as f:
    config = json.load(f)

repo_url = config['center-repo']['ip'] + ':' + str(config['center-repo']['port']) + '/'

docker_client = docker.from_env(version='1.24', timeout=600)


def pull_image(image_name):
    print('pulling image: ' + image_name)
    print(image_name)
    docker_client.images.pull(repo_url + image_name)
    os.system('docker tag ' + repo_url + image_name + ' ' + image_name)
    print('pulled image: ' + image_name)


def delete_container(container_name):
    docker_client.containers.get(container_name).remove(force=True)


# 创建容器的配置暂缺
def create_container(image_name, project_path, container_name, container_config):
    print(docker_client.images.list(name=image_name))
    if not docker_client.images.list(name=image_name):
        print("pulling")
        pull_image(image_name)
    print('creating container: ' + container_name)
    return docker_client.containers.run(
        image_name,
        detach=True,
        volumes={project_path: {'bind': settings.watch_dir, 'mode': 'rw'}},
        name=container_name,
        command=''
    ).id


# 检查容器状态，暂缺写日志
def check_container_status(container_name, task_id, image_name):
    while True:
        result = {}
        container = docker_client.containers.get(container_name)
        if container:
            status = container.attrs['State']
            result['status'] = status['Status']
            result['dead'] = status['Dead']
            result['paused'] = status['Paused']
            result['running'] = status['Running']
            result['restarting'] = status['Restarting']
            result['error'] = status['Error']
            result['exitcode'] = status['ExitCode']

            if result['status'] == 'running':
                db_manager.update_task_status(20020, task_id)
                print(str(container_name) + ': container_status is ' + str(result))
                time.sleep(5)
            elif result['status'] == 'exited':
                if result['exitcode'] == 0:
                    db_manager.update_task_status(20030, task_id)
                    print(str(container_name) + ': container_status is ' + str(result))
                    scan_result.send_result(container_name, image_name)
                    break
                else:
                    db_manager.update_task_status(result['exitcode'], task_id)
                    print(str(container_name) + ': container_status is ' + str(result))
                    break
            else:
                db_manager.update_task_status(result['exitcode'], task_id)
                print(str(container_name) + ': container_status is ' + str(result))
                break
        else:
            # container不存在
            break


if __name__ == '__main__':
    create_container("scanweb:2", "/tmp/task6", "test", "")
# check_container_status('d4427', 1)
# {
# 	"Status": "exited",
# 	"Pid": 0,
# 	"OOMKilled": False,
# 	'Dead': False,
# 	'Paused': False,
# 	'Running': False,
# 	'FinishedAt': '2019-04-03T06:26:30.112207381Z',
# 	'Restarting': False,
# 	'Error': '',
# 	'StartedAt': '2019-04-02T12:56:30.156265524Z',
# 	'ExitCode': 0
# }
# test = {
# 	"Platform": "linux",
# 	"State": {
# 		"Status": "running",
# 		"Pid": 2867,
# 		"OOMKilled": False,
# 		"Dead": False,
# 		"Paused": False,
# 		"Running": True,
# 		"FinishedAt": "2019-04-09T07:07:55.853558508Z",
# 		"Restarting": False,
# 		"Error": "",
# 		"StartedAt": "2019-04-09T07:13:39.098284243Z",
# 		"ExitCode": 0
# 	},
# 	"Config": {
# 		"Tty": False,
# 		"Cmd": ["/etc/docker/registry/config.yml"],
# 		"Volumes": {
# 			"/var/lib/registry": {}
# 		},
# 		"Domainname": "",
# 		"WorkingDir": "",
# 		"Image": "registry:2",
# 		"Hostname": "d4427edafbf4",
# 		"StdinOnce": False,
# 		"ArgsEscaped": True,
# 		"Labels": {},
# 		"AttachStdin": False,
# 		"User": "",
# 		"Env": ["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"],
# 		"ExposedPorts": {
# 			"5000/tcp": {}
# 		},
# 		"OnBuild": None,
# 		"AttachStderr": False,
# 		"Entrypoint": ["/entrypoint.sh"],
# 		"AttachStdout": False,
# 		"OpenStdin": False
# 	},
# 	"ResolvConfPath": "/var/lib/docker/containers/d4427edafbf48c3e34aa24a2a60b13805f629e62fb5ad108959746186e481118/resolv.conf",
# 	"HostsPath": "/var/lib/docker/containers/d4427edafbf48c3e34aa24a2a60b13805f629e62fb5ad108959746186e481118/hosts",
# 	"Args": ["/etc/docker/registry/config.yml"], "Driver": "overlay2", "Path": "/entrypoint.sh",
# 	"HostnamePath": "/var/lib/docker/containers/d4427edafbf48c3e34aa24a2a60b13805f629e62fb5ad108959746186e481118/hostname",
# 	"RestartCount": 0, "Name": "/registry", "Created": "2019-02-20T06:22:54.576612986Z", "ExecIDs": None,
# 	"GraphDriver": {
# 		"Data": {
# 			"MergedDir": "/var/lib/docker/overlay2/46b75bb372374cf7fb3f2f8befad15d2b2be9d8fafef50dda824af2129cc27d4/merged",
# 			"WorkDir": "/var/lib/docker/overlay2/46b75bb372374cf7fb3f2f8befad15d2b2be9d8fafef50dda824af2129cc27d4/work",
# 			"LowerDir": "/var/lib/docker/overlay2/46b75bb372374cf7fb3f2f8befad15d2b2be9d8fafef50dda824af2129cc27d4-init/diff:/var/lib/docker/overlay2/d9441895b4aab88fd4782322ff7de11efa16c07b29af4862c90cef15df62c5fb/diff:/var/lib/docker/overlay2/023bda1b92efa5556f97323a007cd3abbeb3edf02e52a52d0bae9dd0d67587a9/diff:/var/lib/docker/overlay2/884f2886405e9dc0b7c5d744727b87c6681b0d2bc033f1abfc3e6bbd2d1023ef/diff:/var/lib/docker/overlay2/33227e04cf4deb0dd43ac0847e1c135044d07e5a31ef18f4f5c8f6cf024413db/diff:/var/lib/docker/overlay2/34bd5af2803d62bc1e729a0496b9984bb3153bf39668efd997b18ebe6d57187d/diff",
# 			"UpperDir": "/var/lib/docker/overlay2/46b75bb372374cf7fb3f2f8befad15d2b2be9d8fafef50dda824af2129cc27d4/diff"
# 		},
# 		"Name": "overlay2"
# 	}, "Mounts": [{
# 		"RW": True,
# 		"Propagation": "rprivate",
# 		"Destination": "/var/lib/registry",
# 		"Source": "/var/data",
# 		"Mode": "",
# 		"Type": "bind"
# 	}], "ProcessLabel": "", "NetworkSettings": {
# 		"Bridge": "",
# 		"Networks": {
# 			"bridge": {
# 				"NetworkID": "650e104d38c29adf77a5397524e1471f2b36f4eafc0fa6613a1b6d07e6616800",
# 				"MacAddress": "02:42:ac:11:00:02",
# 				"GlobalIPv6PrefixLen": 0,
# 				"Links": None,
# 				"GlobalIPv6Address": "",
# 				"IPv6Gateway": "",
# 				"DriverOpts": None,
# 				"IPAMConfig": None,
# 				"EndpointID": "2e8c67bf6ae458fccfaa00aa040b44f0c3f8b8b2bca80a872e2e01166635c7bf",
# 				"IPPrefixLen": 16,
# 				"IPAddress": "172.17.0.2",
# 				"Gateway": "172.17.0.1",
# 				"Aliases": None
# 			}
# 		},
# 		"SecondaryIPv6Addresses": None,
# 		"LinkLocalIPv6Address": "",
# 		"HairpinMode": False,
# 		"IPv6Gateway": "",
# 		"SecondaryIPAddresses": None,
# 		"SandboxID": "4ee3c325b25374bfb2d47d3c757e27e9537b50453a433b326b099859928787d9",
# 		"MacAddress": "02:42:ac:11:00:02",
# 		"GlobalIPv6Address": "",
# 		"Gateway": "172.17.0.1",
# 		"LinkLocalIPv6PrefixLen": 0,
# 		"EndpointID": "2e8c67bf6ae458fccfaa00aa040b44f0c3f8b8b2bca80a872e2e01166635c7bf",
# 		"SandboxKey": "/var/run/docker/netns/4ee3c325b253",
# 		"GlobalIPv6PrefixLen": 0,
# 		"IPPrefixLen": 16,
# 		"IPAddress": "172.17.0.2",
# 		"Ports": {
# 			"5000/tcp": [{
# 				"HostPort": "5000",
# 				"HostIp": "0.0.0.0"
# 			}]
# 		}
# 	}, "AppArmorProfile": "docker-default",
# 	"Image": "sha256:2e2f252f3c88679f1207d87d57c07af6819a1a17e22573bcef32804122d2f305",
# 	"LogPath": "/var/lib/docker/containers/d4427edafbf48c3e34aa24a2a60b13805f629e62fb5ad108959746186e481118/d4427edafbf48c3e34aa24a2a60b13805f629e62fb5ad108959746186e481118-json.log",
# 	"HostConfig": {
# 		"CpuPeriod": 0,
# 		"MemorySwappiness": None,
# 		"ContainerIDFile": "",
# 		"KernelMemory": 0,
# 		"Memory": 0,
# 		"CpuQuota": 0,
# 		"UsernsMode": "",
# 		"AutoRemove": False,
# 		"BlkioDeviceReadIOps": None,
# 		"Dns": [],
# 		"ExtraHosts": None,
# 		"PidsLimit": 0,
# 		"DnsSearch": [],
# 		"Privileged": False,
# 		"IOMaximumIOps": 0,
# 		"CpuPercent": 0,
# 		"NanoCpus": 0,
# 		"Ulimits": None,
# 		"CpusetCpus": "",
# 		"DiskQuota": 0,
# 		"CgroupParent": "",
# 		"BlkioWeight": 0,
# 		"MemorySwap": 0,
# 		"RestartPolicy": {
# 			"MaximumRetryCount": 0,
# 			"Name": "always"
# 		},
# 		"OomScoreAdj": 0,
# 		"BlkioDeviceReadBps": None,
# 		"VolumeDriver": "",
# 		"ReadonlyRootfs": False,
# 		"CpuShares": 0,
# 		"PublishAllPorts": False,
# 		"MemoryReservation": 0,
# 		"BlkioWeightDevice": [],
# 		"ConsoleSize": [0, 0],
# 		"NetworkMode": "default",
# 		"BlkioDeviceWriteBps": None,
# 		"Isolation": "",
# 		"GroupAdd": None,
# 		"ReadonlyPaths": ["/proc/asound", "/proc/bus", "/proc/fs", "/proc/irq", "/proc/sys", "/proc/sysrq-trigger"],
# 		"CpuRealtimeRuntime": 0,
# 		"Devices": [],
# 		"BlkioDeviceWriteIOps": None,
# 		"Binds": ["/var/data:/var/lib/registry"],
# 		"CpusetMems": "",
# 		"Cgroup": "",
# 		"UTSMode": "",
# 		"PidMode": "",
# 		"Runtime": "runc",
# 		"VolumesFrom": None,
# 		"CapDrop": None,
# 		"DnsOptions": [],
# 		"ShmSize": 67108864,
# 		"Links": None,
# 		"CpuRealtimePeriod": 0,
# 		"IpcMode": "shareable",
# 		"MaskedPaths": ["/proc/acpi", "/proc/kcore", "/proc/keys", "/proc/latency_stats", "/proc/timer_list",
# 						"/proc/timer_stats", "/proc/sched_debug", "/proc/scsi", "/sys/firmware"],
# 		"PortBindings": {
# 			"5000/tcp": [{
# 				"HostPort": "5000",
# 				"HostIp": ""
# 			}]
# 		},
# 		"SecurityOpt": None,
# 		"CapAdd": None,
# 		"CpuCount": 0,
# 		"DeviceCgroupRules": None,
# 		"OomKillDisable": False,
# 		"LogConfig": {
# 			"Config": {},
# 			"Type": "json-file"
# 		},
# 		"IOMaximumBandwidth": 0
# 	}, "Id": "d4427edafbf48c3e34aa24a2a60b13805f629e62fb5ad108959746186e481118", "MountLabel": ""
# }
# print(test)
# print(type(test))
# print(json.dumps(test))

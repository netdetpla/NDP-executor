import os
status_topic_name = 'statusnew'
result_topic_name = 'resultnew'
log_topic_name='newrunlog'
kafka_ip = '192.168.120.11'
kafka_port = 9092
watch_dir = '/tmp'
maximum_interval_time = 3600*4
check_interval_time = 10
kafkalist=["192.168.120.10:9092", "192.168.120.11:9092", "192.168.120.12:9092"]
log_topics={"dnsau":"domainTaskStatus","dnsns":"domainTaskStatus","dnssecure":"domainTaskStatus","scandns":"scanDnsTaskStatus","scanweb":"scanWebTaskStatus","info_shell":"bugTaskStatus","scanservice":"scanServiceTaskFile","scanvul":"scanVulTaskStatus","socketvul":"socketVulTaskStatus","httpvul":"httpVulTaskStatus"}
result_topics={"dnsau":"domainTaskFile","dnsns":"nsTaskFile","dnssecure":"domainTaskFile","scandns":"scanDnsTaskFile","scanweb":"scanWebTaskFile","info_shell":"bugTaskFile","scanservice":"scanServiceTaskFile","scanvul":"scanVulTaskFile","socketvul":"socketVulTaskFile","httpvul":"httpVulTaskFile","ecdsystem":"ecdsystemTaskFile"}
status_topics='statusnew'
db = {"host": "192.168.120.10", "port": 3306, "user": "root", "password": "password", "dbname": "ndp"}

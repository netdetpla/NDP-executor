import os
status_topic_name = 'statusnew'
result_topic_name = 'resultnew'
log_topic_name='newrunlog'
kafka_ip = '127.0.0.1'
kafka_port = 9092
watch_dir = '/tmp'
maximum_interval_time = 3600*4
check_interval_time = 10
kafkalist=["127.0.0.1:9092"]
log_topics={"dnsau":"domainTaskStatus","dnsns":"domainTaskStatus","dnssecure":"domainTaskStatus","scandns":"scanDnsTaskStatus","scanweb":"scanWebTaskStatus","info_shell":"bugTaskStatus","scanservice":"scanportTaskStatus","scanvul":"scanVulTaskStatus","socketvul":"socketVulTaskStatus","httpvul":"httpVulTaskStatus"}
result_topics={"dnsau":"domainTaskFile","dnsns":"domainTaskFile","dnssecure":"domainTaskFile","scandns":"scanDnsTaskFile","scanweb":"scanWebTaskFile","info_shell":"bugTaskFile","scanservice":"scanportTaskFile","scanvul":"scanVulTaskFile","socketvul":"socketVulTaskFile","httpvul":"httpVulTaskFile"}
status_topics='statusnew'
db = {"host": "127.0.0.1", "port": 3306, "user": "root", "password": "123456", "dbname": "ndp"}

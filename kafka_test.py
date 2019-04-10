#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError

import settings


class Kafka_producer():

	def __init__(self, kafkahost, kafkaport, kafkatopic):
		self.kafkaHost = kafkahost
		self.kafkaPort = kafkaport
		self.kafkatopic = kafkatopic
		self.producer = KafkaProducer(bootstrap_servers=settings.kafkalist)

	def sendjsondata(self, params):
		try:
			print('try-------------------')
			producer = self.producer
			producer.send(self.kafkatopic, params.encode('utf-8'))
			producer.flush()
		except KafkaError as e:
			print(e)

	def close(self):
		self.producer.close()


class Kafka_consumer():

	def __init__(self, kafkahost, kafkaport, kafkatopic, groupid):
		self.kafkaHost = kafkahost
		self.kafkaPort = kafkaport
		self.kafkatopic = kafkatopic
		self.groupid = groupid
		self.consumer = KafkaConsumer(self.kafkatopic, group_id=self.groupid,
									  bootstrap_servers='{kafka_host}:{kafka_port}'.format(
										  kafka_host=self.kafkaHost,
										  kafka_port=self.kafkaPort))

	def consume_data(self):
		try:
			for message in self.consumer:
				# print json.loads(message.value)
				yield message
		except KeyboardInterrupt as e:
			print(e)

	def close(self):
		self.consumer.close()

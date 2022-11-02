import json
import MySQLdb as mdb
from kafka import KafkaConsumer
from threading import Thread
from loguru import logger
import pymysql.cursors


class KafkaEventThread(Thread):
    def __init__(self, topic_event):
        """
        :param topic_event: topic_name like 'conn_topic'
        """
        super().__init__()
        self.topic = topic_event
        self.table_name_mul = 'multi'
        self.table_name_seanson = 'seasonal'
        self.consumer = KafkaConsumer(self.topic, value_deserializer=lambda m: json.loads(m.decode('ascii')),
                                      bootstrap_servers=['localhost:9092'], group_id='cloud-group',
                                      enable_auto_commit=False)
        self.conn = mdb.connect('192.168.0.133', 'root', 'toor', 'busines_data')
        # 如果使用事务引擎，可以设置自动提交事务，或者在每次操作完成后手动提交事务conn.commit()
        self.conn.autocommit(1)  # conn.autocommit(True)

    def run(self):
        """
        if kafka have any new data,it will be put into mysql
        :return: null
        """
        with self.conn:
            for message in self.consumer:
                item = message.value
                print("%s,:%d,:%d,:value=%s" % (message.topic, message.partition, message.offset, message.value))
                print("value=%s" % (item))
                sql_season = "INSERT INTO `"+self.table_name_seanson+"`(`data`) VALUES ("+str(item['data_season']) + ")"
                # print(sql_season)
                sql_mul = "INSERT INTO `" + self.table_name_mul + "`(`data1`,`data2`,`data3`,`data4`) VALUES (" \
                          + str(item['data_mul'][0]) + ',' + str(item['data_mul'][1]) + ',' + str(item['data_mul'][2])+\
                          ',' + str(item['data_mul'][3]) + ") "
                # print(sql_mul)
                with self.conn.cursor() as cursor:
                    try:
                        cursor.execute(sql_mul)
                        cursor.execute(sql_season)
                    except Exception as ex:
                        logger.error(str(ex))
                        self.conn.rollback()
                        self.conn.close()


if __name__ == '__main__':
    kafka_thread = KafkaEventThread('business_topic')
    kafka_thread.start()
# event_list = ['conn_topic', 'x509_topic', 'http_topic', 'stats_topic', 'known_services_topic', 'known_hosts_topic',
#               'packet_filter_topic', 'ssl_topic', 'software_topic', 'files_topic', 'reporter_topic',
#               'capture_loss_topic', 'notice_topic', 'loaded_scripts_topic', 'ssh_topic']

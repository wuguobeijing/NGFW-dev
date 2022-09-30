import datetime
import json
import os
import socket
import tarfile
import time
from time import sleep

import autogluon.core as ag
import pandas as pd
import pyarrow.parquet as pq
import tqdm
from autogluon.tabular import TabularPredictor, TabularDataset
from kafka import KafkaConsumer, KafkaProducer
from loguru import logger


# import pyodbc
# model_host = 'k'


def received():
    # 设置服务器的ip和 port
    # 服务器信息
    sever_host = '192.168.0.133'
    sever_port = 1234
    # 传输数据间隔符
    SEPARATOR = 'sep'

    # 文件缓冲区
    Buffersize = 4096 * 10
    s = socket.socket()
    s.bind((sever_host, sever_port))

    # 设置监听数
    s.listen(128)
    print(f'服务器监听{sever_host}:{sever_port}')

    # 接收客户端连接
    client_socket, address = s.accept()
    # 打印客户端ip
    print(f'客户端{address}连接')

    # 接收客户端信息
    received = client_socket.recv(Buffersize).decode()
    filename, file_size = received.split(SEPARATOR)
    # 获取文件的名字,大小
    filename = os.path.basename(filename)
    file_size = int(file_size)

    # 文件接收处理
    progress = tqdm.tqdm(range(file_size), f'接收{filename}', unit='B', unit_divisor=1024, unit_scale=True)

    with open(filename, 'wb') as f:
        for _ in progress:

            # 从客户端读取数据
            bytes_read = client_socket.recv(Buffersize)
            # 如果没有数据传输内容
            if not bytes_read:
                break
            # 读取写入
            f.write(bytes_read)
            # 更新进度条
            progress.update(len(bytes_read))

    # 关闭资源
    client_socket.close()
    s.close()
    sleep(3)
    path = '/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/Anomaly-Detection-IoT23/data.parquet'
    df1 = read_pyarrow(path)
    df1.to_csv(
        '/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/Anomaly-Detection-IoT23/Models/Data/self_data1.csv',
        sep=',', index=False)


def read_pyarrow(path):
    return pq.read_table(path).to_pandas()


def train_auto_gl():
    gbm_options = {  # specifies non-default hyperparameter values for lightGBM gradient boosted trees
        'num_boost_round': 100,  # number of boosting rounds (controls training time of GBM models)
        'num_leaves': ag.space.Int(lower=26, upper=66, default=36),
        # number of leaves in trees (integer hyperparameter)
        'learning_rate': ag.space.Real(lower=5e-3, upper=0.2, default=0.05, log=True),
        'feature_fraction': ag.space.Real(lower=0.75, upper=1.0, default=1.0),
        'min_data_in_leaf': ag.space.Int(lower=2, upper=60, default=20)
    }
    XT_options = {}
    hyperparameters = {  # hyperparameters of each model type
        # 'XGB': XGB_option_best
        # 'RF':RF_option,
        # 'XT' : XT_options,
        'GBM': gbm_options,
        #  'CAT' : CAT_option_best,
        # 'NN_TORCH': nn_options,  # NOTE: comment this line out if you get errors on Mac OSX

    }  # When these keys are missing from hyperparameters dict, no models of that type are trained

    time_limit = 2 * 60  # train various models for ~2 min
    num_trials = 6  # try at most 5 different hyperparameter configurations for each type of model
    search_strategy = 'auto'  # to tune hyperparameters using random search routine with a local scheduler

    hyperparameter_tune_kwargs = {  # HPO is not performed unless hyperparameter_tune_kwargs is specified
        'num_trials': num_trials,
        'scheduler': 'local',
        'searcher': search_strategy,
    }
    file_path = "/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/Data/self_data1.csv"
    df = pd.read_csv(file_path)
    del df['module_labels']
    train_data = TabularDataset(df)
    save_path = '/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/auto_gl' \
                '/edge_model/binary'
    label = 'label'
    predictor = TabularPredictor(label=label, eval_metric='roc_auc', path=save_path)
    predictor.fit(train_data, num_bag_folds=5, num_bag_sets=1, num_stack_levels=0,
                  time_limit=time_limit, presets='optimize_for_deployment', hyperparameters=hyperparameters,
                  hyperparameter_tune_kwargs=hyperparameter_tune_kwargs, verbosity=4,
                  ag_args_fit={'num_gpus': 1},
                  )
    logger.info("binary:\n" + predictor.fit_summary())


def train_auto_gl_mul():
    gbm_options = {  # specifies non-default hyperparameter values for lightGBM gradient boosted trees
        'num_boost_round': 100,  # number of boosting rounds (controls training time of GBM models)
        'num_leaves': ag.space.Int(lower=26, upper=66, default=36),
        # number of leaves in trees (integer hyperparameter)
        'learning_rate': ag.space.Real(lower=5e-3, upper=0.2, default=0.05, log=True),
        'feature_fraction': ag.space.Real(lower=0.75, upper=1.0, default=1.0),
        'min_data_in_leaf': ag.space.Int(lower=2, upper=60, default=20)
    }
    XT_options = {}
    hyperparameters = {  # hyperparameters of each model type
        # 'XGB': XGB_option_best
        # 'RF':RF_option,
        # 'XT' : XT_options,
        'GBM': gbm_options,
        #  'CAT' : CAT_option_best,
        # 'NN_TORCH': nn_options,  # NOTE: comment this line out if you get errors on Mac OSX

    }  # When these keys are missing from hyperparameters dict, no models of that type are trained

    time_limit = 2 * 60  # train various models for ~2 min
    num_trials = 6  # try at most 5 different hyperparameter configurations for each type of model
    search_strategy = 'auto'  # to tune hyperparameters using random search routine with a local scheduler

    hyperparameter_tune_kwargs = {  # HPO is not performed unless hyperparameter_tune_kwargs is specified
        'num_trials': num_trials,
        'scheduler': 'local',
        'searcher': search_strategy,
    }
    file_path = "/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/Data/self_data1.csv"
    df = pd.read_csv(file_path)
    del df['label']
    train_data = TabularDataset(df)
    save_path = '/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/auto_gl' \
                '/edge_model/multi'
    label = 'module_labels'
    predictor = TabularPredictor(label=label, path=save_path)
    predictor.fit(train_data, num_bag_folds=5, num_bag_sets=1, num_stack_levels=0,
                  time_limit=time_limit, presets='optimize_for_deployment', hyperparameters=hyperparameters,
                  hyperparameter_tune_kwargs=hyperparameter_tune_kwargs, verbosity=4,
                  ag_args_fit={'num_gpus': 1},
                  )
    logger.info("multi:\n" + predictor.fit_summary())


# 一次性打包整个根目录。空子目录会被打包。
# 如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
def make_targz(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


# 逐个添加文件打包，未打包空子目录。可过滤文件。
# 如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
def make_targz_one_by_one(output_filename, source_dir):
    tar = tarfile.open(output_filename, "w:gz")
    for root, dir, files in os.walk(source_dir):
        for file in files:
            pathfile = os.path.join(root, file)
            tar.add(pathfile)
    tar.close()


def send_model(host):
    # 传输数据间隔符
    SEPARATOR = '<SEPARATOR>'
    # 服务器信息
    host = host
    port = 2234
    # 文件缓冲区
    Buffersize = 4096 * 10
    # 传输文件名字
    filename = "/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/Anomaly-Detection-IoT23/model.tar.gz"
    # 文件大小
    file_size = os.path.getsize(filename)
    # 创建socket链接
    s = socket.socket()
    print(f'服务器连接中{host}:{port}')
    s.connect((host, port))
    print('与服务器连接成功')

    # 发送文件名字和文件大小，必须进行编码处理
    s.send(f'{filename}{SEPARATOR}{file_size}'.encode())

    # 文件传输
    progress = tqdm.tqdm(range(file_size), f'发送{filename}', unit='B', unit_divisor=1024)

    with open(filename, 'rb') as f:
        # 读取文件
        for _ in progress:
            bytes_read = f.read(Buffersize)
            if not bytes_read:
                break
            # sendall 确保网络忙碌的时候，数据仍然可以传输
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
    # 关闭资源
    s.close()


def on_send_success(record_metadata, host=None):
    print(record_metadata.topic)
    print(record_metadata.offset)
    logger.log(1, (record_metadata.topic, record_metadata.offset))


def on_send_error(excp):
    logger.error('error' + str(excp))


def main():
    dt = datetime.datetime.now()
    logger.add(dt.strftime("%Y-%m-%d%H-%M-%S") + '_cloud_model.log')
    try:
        consumer = KafkaConsumer('parquet-topic', value_deserializer=lambda m: json.loads(m.decode('ascii')),
                                 bootstrap_servers='wuguo-buaa:9092', group_id='edge_group',
                                 enable_auto_commit=False)
        for message in consumer:
            # print(message, message.topic, str(message.value))
            print(message.value["type"])
            if message.value["type"] == 'new_parquet':
                global model_host
                model_host = message.value["data_host"]
                received()
                train_auto_gl()
                train_auto_gl_mul()
                make_targz('model.tar.gz',
                           "/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model"
                           "/auto_gl/edge_model")
                producer = KafkaProducer(bootstrap_servers='wuguo-buaa:9092',
                                         value_serializer=lambda m: json.dumps(m).encode('ascii'))
                json_content = {"type": 'new_model_k', "time": str(time.time()), "model_host": model_host}
                producer.send('new_train_topic', json_content).add_callback(on_send_success).add_errback(on_send_error)
                producer.close()
                send_model(model_host)
        consumer.close()
    except:
        print("open kafka server first!")


def send_slips_order():
    producer = KafkaProducer(bootstrap_servers='wuguo-buaa:9092',
                             value_serializer=lambda m: json.dumps(m).encode('ascii'))
    order_param = {"filepath": '', "interface": 'eth0', "order": 'start', "blocking": False}
    json_content = {"type": 'new_slips_order', "time": str(time.time()), "model_host": 'k', "order_param": order_param}
    producer.send('new_train_topic', json_content).add_callback(on_send_success).add_errback(on_send_error)
    producer.close()


if __name__ == '__main__':
    # while True:
    # main()
    send_slips_order()
    # producer = KafkaProducer(bootstrap_servers='wuguo-buaa:9092',value_serializer=lambda m: json.dumps(m).encode('ascii'))
    # json_content = {"type": 'new_model_k', "time": str(time.time()), "model_host": 'k'}
    # producer.send('new_train_topic', json_content).add_callback(on_send_success).add_errback(on_send_error)
    # send_model('k')

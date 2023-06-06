# NDFW-dev
# 下一代防火墙
下一代防火墙采用的是伪CS模式，即区别于传统的客户端调用服务器服务，而是各司其职，边缘侧运行StratosphereLinuxIPS-dev（详见该软件readme及附加文档）云端运行当前的软件，当前软件主要负责边缘侧防火墙规则的显示以及模型的训练、规则的下发，更多起到的是监视作用
运行过程中首先打开gui-main.py，其余页面都可以从这里实现跳转。

以下是文件结构说明

## gui/ngfw
### build_args
参数配置页面：
接口地址-->eth0
工作模式-->阻挡、不阻挡
日志模式
显示界面
### build_business
#### plot_multi
绘制多参数pca异常检测图
#### plot_multi
绘制单参数周期异常检测图
### build_command
配置文件管理页面：
活动超时时间
删除历史防御规则
生成日志
工作模式-->训练、测试
模型训练参数
### build_firewall
防火墙页面
管理（查看、修改）设备规则
### build_flow
流量检测页面
模型训练管理
训练结果展示
### build_log
日志页面
### build_login
登陆页面
### build_main
主页面-->引导至各功能页
### log
日志库
###Plotter
流量检测的功能页面（绘制训练结果）

## src
### client
**客户端后端代码**
#### receive_parquet_train.py
接收客户端传输的压缩数据并进行训练，将模型压缩为.gz后再传回边缘
#### data_receiver.py
接收工业载荷数据并在Mysql中持久化
#### redis_conn.py
从边缘侧收集redis缓存信息，生成防火墙规则并下发到相应设备的辅助功能

### Model
**模型相关代码**
#### auto_gl
##### edge_model
**binary**二分类-攻击检测模型
model parameters:
side = 'both'
c = 3
trend = False
**multi**多分类-攻击识别模型
model parameters:
k = 1
c_mul = 5
##### plot_files
对二分类与多分类的模型训练结果进行呈现
#### cache
存放每次训练的模型压缩文件以及边缘端防护的配置文件
#### Data
汇聚得到的训练数据
#### log
日志文件

# NDFW-dev
# 下一代防火墙

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

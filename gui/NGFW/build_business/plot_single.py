import tkinter
import random
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from adtk.data import validate_series

from adtk.detector import SeasonalAD
seasonal_ad = SeasonalAD(c=3.0, side="both")

class MY_SINGLE_GUI(tkinter.Toplevel):
    def __init__(self, single_window):
        super().__init__()
        self.single_window = single_window
        self.result = pd.DataFrame
        self.ts = 0

    def set_single_window(self):
        # 创建tkinter主界面
        self.root = tk.Tk()
        self.root.title("smart controller")
        self.root.geometry("800x450+0+0")
        self.root.configure(bg="gainsboro")

        # 创建一个容器用于显示matplotlib的fig
        self.frame1 = tk.Frame(self.root, bg="gainsboro")
        self.frame1.place(x=-100, y=-30, width=900, height=450)
        # # 创建画图figure
        self.fig1 = plt.figure(figsize=(16, 8))
        # fig2 放入画布
        self.canvas2 = FigureCanvasTkAgg(self.fig1, master=self.frame1)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().place(x=0, y=0)

        # 打开matplot交互模式
        plt.ion()
        # 使用一个定时器计算后台数据
        self.generate_data2()
        # fig更新
        self.plot_single()

    def generate_data2(self):
        global ts
        s = pd.read_csv('/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/Data/seasonal.csv', index_col="Time", parse_dates=True, squeeze=True)
        s = validate_series(s)
        anomalies = seasonal_ad.fit_detect(s)
        df = pd.DataFrame(anomalies, columns=['Traffic'])
        df = df[self.ts:self.ts+100]
        df.rename(columns={'Time': 'Time', 'Traffic': 'label'}, inplace=True)
        df1 = pd.DataFrame(s, columns=['Traffic'])
        df1 = df1[self.ts:self.ts+100]
        self.result = pd.concat([df, df1], axis=1)
        self.ts += 5
        self.root.after(5000, self.generate_data2)

    def plot_single(self):
        # global vacuum, efficiency, vacuumHisList, effiHisList, fig1
        self.fig1.clf()  # 清除上一帧内容
        g21 = self.fig1.add_subplot(2, 2, 1)

        g21.scatter(self.result.index, self.result['Traffic'], s=5, c=self.result['label'])
        g21.patch.set_facecolor('whitesmoke')
        self.canvas2.draw()

        self.root.after(1000, self.plot_single)


import tkinter
import random
import tkinter as tk
import tkinter.font as tkFont
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from adtk.data import validate_series
from adtk.detector import PcaAD

class MY_MULTI_GUI(tkinter.Toplevel):
    def __init__(self, multi_window, k, c):
        super().__init__()
        self.multi_window = multi_window
        self.result_mul = pd.DataFrame
        self.ts = 0
        self.pca_ad = PcaAD(k=k, c=c)

    def set_single_window(self):
        # 创建tkinter主界面
        self.root = tk.Tk()
        self.root.title("smart controller")
        self.root.geometry("800x450+0+0")
        self.root.configure(bg="gainsboro")
        # 创建一个容器用于显示matplotlib的fig
        self.frame1 = tk.Frame(self.root, bg="gainsboro")
        self.frame1.place(x=-100, y=-30, width=900, height=450)

        self.fig3 = plt.figure(figsize=(16, 8))
        # fig2 放入画布
        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=self.frame1)
        self.canvas3.draw()
        self.canvas3.get_tk_widget().place(x=0, y=0)
        # 打开matplot交互模式
        plt.ion()
        # 使用一个定时器计算后台数据

        self.generate_data3()
        # fig更新
        self.plot_multi()

    def generate_data3(self):
        s2 = pd.read_csv('/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/Data/generator.csv', index_col="Time", parse_dates=True, squeeze=True)
        s2 = validate_series(s2)

        anomalies = self.pca_ad.fit_detect(s2)
        df2 = pd.DataFrame(anomalies, columns=['data'])
        df2 = df2[self.ts:self.ts+100]
        df1 = pd.DataFrame(s2, columns=['Speed (kRPM)', 'Power (kW)'])
        df1 = df1[self.ts:self.ts+100]
        self.result_mul = pd.concat([df2, df1], axis=1)
        self.ts += 5
        self.root.after(5000, self.generate_data3)


    def plot_multi(self):
        # global vacuum, efficiency, vacuumHisList, effiHisList, fig1
        self.fig3.clf()  # 清除上一帧内容

        g21 = self.fig3.add_subplot(2, 2, 1)
        g21.set_ylim([0, 40])
        g21.plot(self.result_mul.index, self.result_mul['Speed (kRPM)'], linestyle='-', c='steelblue')
        g21.scatter(self.result_mul.index, self.result_mul['Power (kW)'], s=5, c=self.result_mul['data'])
        g21.patch.set_facecolor('whitesmoke')
        self.canvas3.draw()

        self.root.after(1000, self.plot_multi)

# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
import datetime
import json
import os
import time
import tkinter
from pathlib import Path

import pandas as pd
from autogluon.tabular import TabularPredictor, TabularDataset
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import filedialog, Canvas, Frame, Text, Button, PhotoImage, messagebox, BOTH, ACTIVE, END

from kafka import KafkaProducer
from loguru import logger

from gui.NGFW.Plotter.plotter import Plotter
from gui.NGFW.build_args.gui_args import MY_ARGS_GUI
from gui.NGFW.build_command.gui_command import MY_COMMAND_GUI
from src.client.receive_parquet_train import train_auto_gl, train_auto_gl_mul, make_targz, on_send_success, \
    on_send_error, send_model


class MY_FLOW_GUI(tkinter.Toplevel):
    def __init__(self, flow_window):
        super().__init__()
        self.flow_window = flow_window
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path("assets")
        self.interface = 'eth0'
        self.log_level = '1'
        self.mode = 3
        self.gui = False

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def goto_main(self):
        self.flow_window.destroy()

    def goto_config(self):
        # config file configure
        config_window = tkinter.Toplevel(self.flow_window)
        config_win = MY_COMMAND_GUI(config_window)
        config_win.set_command_window()
        logger.log(1, "config page start" + str(time.time()))
        config_window.mainloop()

    def goto_args(self):
        # window = tkinter.Toplevel(self.flow_window)
        pw = MY_ARGS_GUI(self)
        logger.log(1, "args page start" + str(time.time()))
        self.wait_window(pw)  # 这一句很重要！！！
        return

    def send_slips_order(self):
        blocking = False
        clear_blocking = False
        print((self.interface, self.gui, self.mode, self.log_level))
        if self.mode == 1:
            blocking = True
        elif self.mode == 2:
            clear_blocking = True
        producer = KafkaProducer(bootstrap_servers='wuguo-buaa:9092',
                                 value_serializer=lambda m: json.dumps(m).encode('ascii'))
        order_param = {"filepath": '', "interface": self.interface, "order": 'start', "blocking": blocking,
                       "clear_blocking": clear_blocking, "log_level": self.log_level, "gui": self.gui}
        json_content = {"type": 'new_slips_order', "time": str(time.time()), "model_host": 'k',
                        "order_param": order_param}
        producer.send('new_train_topic', json_content).add_callback(on_send_success).add_errback(on_send_error)
        producer.close()
        messagebox.showinfo('send', 'start message sent')

    def get_last_model(self):
        self.entry_1.delete(1.0, END)
        binary_summary = pd.read_csv('/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/auto_gl/plot_files/binary.csv',)
        header = binary_summary.head()
        self.entry_1.insert(END, 'binary:\n')
        self.entry_1.insert(END, header)
        data = binary_summary.values.tolist()
        print(data)
        for column in data:
            self.entry_1.insert(END, str(column))
        multi_summary = pd.read_csv('/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/auto_gl/plot_files/multi.csv',)
        header = multi_summary.head()
        self.entry_1.insert(END, 'multi:\n')
        self.entry_1.insert(END, header)
        data = multi_summary.values.tolist()
        print(data)
        for column in data:
            self.entry_1.insert(END, str(column))

    def go_to_plot(self):
        plot_window = tkinter.Toplevel(self.flow_window)
        plot_win = Plotter(plot_window)
        plot_win.run()

    def stop_thread(self):
        producer = KafkaProducer(bootstrap_servers='wuguo-buaa:9092',
                                 value_serializer=lambda m: json.dumps(m).encode('ascii'))
        order_param = {"order": 'stop'}
        json_content = {"type": 'new_slips_order', "time": str(time.time()), "model_host": 'k',
                        "order_param": order_param}
        producer.send('new_train_topic', json_content).add_callback(on_send_success).add_errback(on_send_error)
        producer.close()

    def upload_file(self):
        selectFiles = tkinter.filedialog.askopenfilenames()  # askopenfilename 1次上传1个；askopenfilenames1次上传多个
        for selectFile in selectFiles:
            if '.csv' not in selectFile and '.tar.gz' not in selectFile:
                messagebox.showwarning("Error", "must upload csv file or packed model")
                self.file_printout.delete(0, 'end')
                break
            self.file_printout.insert(tkinter.END, selectFile)  # 更新text中内容

    def train_cloud_upload_and_send(self):
        try:
            rule_index = self.file_printout.index(ACTIVE)
        except:
            rule_index = 0
        if self.file_printout.get(rule_index) is None or self.file_printout.get(rule_index) == '':
            messagebox.showwarning("Error", "No file select")
        else:
            file_name = self.file_printout.get(rule_index)
            dt = datetime.datetime.now()
            model_host = 'k'
            if '.csv' in file_name:
                logger.add('/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/log/'
                           + dt.strftime("%Y-%m-%d%H-%M-%S") + '_cloud_model.log')
                os.mkdir('/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/cache/'
                         + dt.strftime("%Y-%m-%d%H-%M-%S"))
                train_auto_gl(file_name)
                train_auto_gl_mul(file_name)
                make_targz('/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/cache/'
                           + dt.strftime("%Y-%m-%d%H-%M-%S") + '/model.tar.gz',
                           "/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/auto_gl/edge_model")
                logger.log(1, "new file trained" + dt.strftime("%Y-%m-%d%H-%M-%S") + '/model.tar.gz')
            producer = KafkaProducer(bootstrap_servers='wuguo-buaa:9092',
                                     value_serializer=lambda m: json.dumps(m).encode('ascii'))
            json_content = {"type": 'new_model_k', "time": dt.strftime("%Y-%m-%d%H-%M-%S"), "model_host": model_host}
            producer.send('new_train_topic', json_content).add_callback(on_send_success).add_errback(on_send_error)
            producer.close()
            # 二分类结果输出
            binary_pre = TabularPredictor.load(
                '/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/auto_gl/edge_model/binary')
            binary_summary = binary_pre.fit_summary()
            print('-----------' * 10)
            print(binary_summary.get('leaderboard'))
            binary_summary.get('leaderboard').to_csv(
                '/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/auto_gl/plot_files/binary.csv')
            # multi 分类结果输出
            multi_pre = TabularPredictor.load(
                '/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/auto_gl/edge_model/multi')
            multi_summary = multi_pre.fit_summary()
            print('-----------' * 10)
            print(multi_summary.get('leaderboard'))
            multi_summary.get('leaderboard').to_csv(
                '/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/src/Model/auto_gl/plot_files/multi.csv')
            time.sleep(1)
            if '.csv' not in file_name:
                send_model(model_host, dt, 2234, file_name=file_name)
                logger.log(1, "previous model send" + file_name)
            else:
                send_model(model_host, dt, 2234)
                logger.log(1, "new model send" + dt.strftime("%Y-%m-%d%H-%M-%S") + '/model.tar.gz')

    def set_flow_window(self):
        self.flow_window.geometry("1317x855")
        self.flow_window.iconphoto(False, tkinter.PhotoImage(
            file='/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/gui/NGFW/LOGO.png'))
        self.flow_window.configure(bg="#282B2D")
        self.flow_window.resizable(False, False)

        self.canvas = Canvas(
            self.flow_window,
            bg="#282B2D",
            height=855,
            width=1317,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            0.0,
            0.0,
            345.7995910644531,
            855.3531494140625,
            fill="#D9D9D9",
            outline="")

        self.button_image_1 = PhotoImage(
            file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(self.canvas,
                               image=self.button_image_1,
                               borderwidth=0,
                               highlightthickness=0,
                               command=self.goto_main,
                               relief="flat"
                               )
        self.button_1.place(
            x=70.5535888671875,
            y=736.8928833007812,
            width=193.36904907226562,
            height=64.45635986328125
        )

        self.button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(self.canvas,
                               image=self.button_image_2,
                               borderwidth=0,
                               highlightthickness=0,
                               command=lambda: print("button_2 clicked"),
                               relief="flat"
                               )
        self.button_2.place(
            x=68.8115234375,
            y=555.71826171875,
            width=196.85317993164062,
            height=64.45635986328125
        )

        self.button_image_3 = PhotoImage(
            file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(self.canvas,
                               image=self.button_image_3,
                               borderwidth=0,
                               highlightthickness=0,
                               command=lambda: print("button_3 clicked"),
                               relief="flat"
                               )
        self.button_3.place(
            x=101.91070556640625,
            y=481.6805419921875,
            width=166.3670654296875,
            height=32.228179931640625
        )

        self.button_image_4 = PhotoImage(
            file=self.relative_to_assets("button_4.png"))
        self.button_4 = Button(self.canvas,
                               image=self.button_image_4,
                               borderwidth=0,
                               highlightthickness=0,
                               command=lambda: print("button_4 clicked"),
                               relief="flat"
                               )
        self.button_4.place(
            x=102.78173828125,
            y=437.2579345703125,
            width=166.3670654296875,
            height=32.22817611694336
        )

        self.button_image_5 = PhotoImage(
            file=self.relative_to_assets("button_5.png"))
        self.button_5 = Button(self.canvas,
                               image=self.button_image_5,
                               borderwidth=0,
                               highlightthickness=0,
                               command=lambda: print("button_5 clicked"),
                               relief="flat"
                               )
        self.button_5.place(
            x=101.91070556640625,
            y=398.0614929199219,
            width=166.3670654296875,
            height=32.22817611694336
        )

        self.button_image_6 = PhotoImage(
            file=self.relative_to_assets("button_6.png"))
        self.button_6 = Button(self.canvas,
                               image=self.button_image_6,
                               borderwidth=0,
                               highlightthickness=0,
                               command=lambda: print("button_6 clicked"),
                               relief="flat"
                               )
        self.button_6.place(
            x=68.8115234375,
            y=314.4424743652344,
            width=202.079345703125,
            height=64.45635223388672
        )

        self.button_image_7 = PhotoImage(
            file=self.relative_to_assets("button_7.png"))
        self.button_7 = Button(self.canvas,
                               image=self.button_image_7,
                               borderwidth=0,
                               highlightthickness=0,
                               command=lambda: print("button_7 clicked"),
                               relief="flat"
                               )
        self.button_7.place(
            x=73.16668701171875,
            y=216.88690185546875,
            width=193.36904907226562,
            height=64.45635986328125
        )

        self.button_image_8 = PhotoImage(
            file=self.relative_to_assets("button_8.png"))
        self.button_8 = Button(self.canvas,
                               image=self.button_image_8,
                               borderwidth=0,
                               highlightthickness=0,
                               command=lambda: print("button_8 clicked"),
                               relief="flat"
                               )
        self.button_8.place(
            x=87.1031494140625,
            y=112.36309814453125,
            width=166.3670654296875,
            height=64.45635986328125
        )

        self.image_image_1 = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(
            158.1329345703125,
            42.130950927734375,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=self.relative_to_assets("image_2.png"))
        image_2 = self.canvas.create_image(
            677.3829345703125,
            165.297607421875,
            image=self.image_image_2
        )

        self.canvas.create_text(
            382.3829345703125,
            249.11508178710938,
            anchor="nw",
            text="云端模型训练与下发",
            fill="#D9D9D9",
            font=("Roboto Regular", 27 * -1)
        )

        self.canvas.create_text(
            966.0,
            250.0,
            anchor="nw",
            text="结果展示",
            fill="#D9D9D9",
            font=("Roboto Regular", 27 * -1)
        )

        self.canvas.create_rectangle(
            382.0,
            634.0,
            1271.0,
            819.0,
            fill="#958F93",
            outline="")

        self.button_image_9 = PhotoImage(
            file=self.relative_to_assets("button_9.png"))
        self.button_9 = Button(self.canvas,
                               image=self.button_image_9,
                               borderwidth=0,
                               highlightthickness=0,
                               command=self.stop_thread,
                               relief="flat"
                               )
        self.button_9.place(
            x=1079.0,
            y=725.0,
            width=157.84521484375,
            height=48.0
        )

        self.canvas.create_text(
            819.0,
            749.0,
            anchor="nw",
            text="-->",
            fill="#000000",
            font=("Roboto Regular", 15 * -1)
        )

        self.canvas.create_text(
            625.0,
            713.0,
            anchor="nw",
            text="2、",
            fill="#000000",
            font=("Roboto Regular", 15 * -1)
        )

        self.button_image_10 = PhotoImage(
            file=self.relative_to_assets("button_10.png"))
        self.button_10 = Button(self.canvas,
                                image=self.button_image_10,
                                borderwidth=0,
                                highlightthickness=0,
                                command=self.goto_config,
                                relief="flat"
                                )
        self.button_10.place(
            x=425.0,
            y=710.0,
            width=157.84524536132812,
            height=78.0
        )
        self.entry_1 = Text(
            self.canvas,
            bd=0,
            bg="#F8F8F8",
            highlightthickness=0
        )
        self.entry_1.place(
            x=835.0,
            y=324.0,
            width=391.0,
            height=161.0
        )
        self.button_image_11 = PhotoImage(
            file=self.relative_to_assets("button_11.png"))
        self.button_11 = Button(self.canvas,
                                image=self.button_image_11,
                                borderwidth=0,
                                highlightthickness=0,
                                command=self.train_cloud_upload_and_send,
                                relief="flat"
                                )
        self.button_11.place(
            x=425.0,
            y=507.0,
            width=157.84524536132812,
            height=48.0
        )

        self.button_image_12 = PhotoImage(
            file=self.relative_to_assets("button_12.png"))
        self.button_12 = Button(self.canvas,
                                image=self.button_image_12,
                                borderwidth=0,
                                highlightthickness=0,
                                command=self.get_last_model,
                                relief="flat"
                                )
        self.button_12.place(
            x=860.0,
            y=559.0,
            width=157.84524536132812,
            height=48.0
        )

        self.button_image_13 = PhotoImage(
            file=self.relative_to_assets("button_13.png"))
        self.button_13 = Button(self.canvas,
                                image=self.button_image_13,
                                borderwidth=0,
                                highlightthickness=0,
                                command=self.go_to_plot,
                                relief="flat"
                                )
        self.button_13.place(
            x=1022.0,
            y=559.0,
            width=157.84521484375,
            height=48.0
        )

        self.button_image_14 = PhotoImage(
            file=self.relative_to_assets("button_14.png"))
        self.button_14 = Button(self.canvas,
                                image=self.button_image_14,
                                borderwidth=0,
                                highlightthickness=0,
                                command=self.upload_file,
                                relief="flat"
                                )
        self.button_14.place(
            x=425.0,
            y=394.0,
            width=157.84524536132812,
            height=78.0
        )

        self.frame_top = Frame(self.canvas, borderwidth=1)
        self.frame_top.place(x=405.0,
                             y=304.0,
                             width=307.84524536132812,
                             height=58.0)

        self.file_select = Frame(self.frame_top)
        self.file_select.pack(padx=2, pady=2, ipady=2, ipadx=2, side='top')
        self.file_Scroll = tkinter.Scrollbar(self.file_select)
        self.file_Scroll.pack(side='right', fill='y')
        self.file_printout = tkinter.Listbox(self.file_select, yscrollcommand=self.file_Scroll.set, width=200, height=5)
        self.file_printout.pack(side='right', fill=BOTH)
        self.file_Scroll.config(command=self.file_printout.yview)

        self.canvas.create_text(
            385.0,
            474.0,
            anchor="nw",
            text="如果选择数据文件则先训练后下发，选择模型文件则直接下发",
            fill="#D9D9D9",
            font=("Roboto Regular", 13 * -1)
        )

        self.button_image_15 = PhotoImage(
            file=self.relative_to_assets("button_15.png"))
        self.button_15 = Button(self.canvas,
                                image=self.button_image_15,
                                borderwidth=0,
                                highlightthickness=0,
                                command=self.goto_args,
                                relief="flat"
                                )
        self.button_15.place(
            x=650.0,
            y=710.0,
            width=157.84524536132812,
            height=78.0
        )

        self.canvas.create_text(
            850.0,
            713.0,
            anchor="nw",
            text="3、",
            fill="#000000",
            font=("Roboto Regular", 15 * -1)
        )

        self.button_image_16 = PhotoImage(
            file=self.relative_to_assets("button_16.png"))
        self.button_16 = Button(self.canvas,
                                image=self.button_image_16,
                                borderwidth=0,
                                highlightthickness=0,
                                command=self.send_slips_order,
                                relief="flat"
                                )
        self.button_16.place(
            x=877.0,
            y=710.0,
            width=157.84524536132812,
            height=78.0
        )

        self.image_image_3 = PhotoImage(
            file=self.relative_to_assets("image_3.png"))
        image_3 = self.canvas.create_image(
            658.0,
            427.0,
            image=self.image_image_3
        )

        self.canvas.create_text(
            393.0,
            710.0,
            anchor="nw",
            text="1、",
            fill="#000000",
            font=("Roboto Regular", 15 * -1)
        )

        self.canvas.create_text(
            594.0,
            743.0,
            anchor="nw",
            text="-->",
            fill="#000000",
            font=("Roboto Regular", 15 * -1)
        )

        self.canvas.create_text(
            398.0,
            655.0,
            anchor="nw",
            text="边缘侧工作管理",
            fill="#000000",
            font=("Roboto Regular", 27 * -1)
        )

        self.canvas.create_rectangle(
            971.0,
            47.0,
            1229.0,
            160.0,
            fill="#3D3644",
            outline="")

        self.button_image_17 = PhotoImage(
            file=self.relative_to_assets("button_17.png"))
        self.button_17 = Button(self.canvas,
                                image=self.button_image_17,
                                borderwidth=0,
                                highlightthickness=0,
                                command=lambda: print("button_17 clicked"),
                                relief="flat"
                                )
        self.button_17.place(
            x=987.0,
            y=58.0,
            width=109.0,
            height=98.0
        )

        self.button_image_18 = PhotoImage(
            file=self.relative_to_assets("button_18.png"))
        self.button_18 = Button(self.canvas,
                                image=self.button_image_18,
                                borderwidth=0,
                                highlightthickness=0,
                                command=lambda: print("button_18 clicked"),
                                relief="flat"
                                )
        self.button_18.place(
            x=1108.0,
            y=57.0,
            width=100.88568115234375,
            height=98.00003051757812
        )

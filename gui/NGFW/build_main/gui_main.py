# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
import time
import tkinter
from pathlib import Path
from tkinter.messagebox import askyesno

from loguru import logger
from webbrowser import open as webopen
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel

from gui.NGFW.build_business.gui_business import MY_BUSINESS_GUI
from gui.NGFW.build_firewall.gui_firewall import MY_FIREWALL_GUI
from gui.NGFW.build_flow.gui_flow import MY_FLOW_GUI
from gui.NGFW.build_help.gui_help import MY_HELP_GUI
from gui.NGFW.build_log.gui_log import MY_LOG_GUI
from gui.NGFW.build_manage.gui_manage import MY_MANAGE_GUI


class MY_GUI():
    def __init__(self, init_window, log):
        # self.jobtxt = None
        self.init_window = init_window
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path("assets")
        self.log = log
        self.set_init_window()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def set_init_window(self):
        self.init_window.geometry("1317x855")
        self.init_window.configure(bg="#282B2D")
        self.init_window.iconphoto(False, tkinter.PhotoImage(file='/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects'
                                                                  '/NGFW-dev/gui/NGFW/LOGO.png'))

        self.canvas = Canvas(
            self.init_window,
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
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.close_window,
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
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_log,
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
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.goto_manage,
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
        self.button_4 = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.goto_ips_data,
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
        self.button_5 = Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.goto_ips_flow,
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
        self.button_6 = Button(
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
        self.button_7 = Button(
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=self.goto_firewall,
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
        self.button_8 = Button(
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
        self.image_1 = self.canvas.create_image(
            158.1329345703125,
            42.130950927734375,
            image=self.image_image_1
        )

        self.canvas.create_text(
            825.0,
            257.0,
            anchor="nw",
            text="下一代防火墙V1.0，感谢使用",
            fill="#FFFFFF",
            font=("Inter", 34 * -1)
        )

        self.image_image_2 = PhotoImage(
            file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            697.3829345703125,
            159.297607421875,
            image=self.image_image_2
        )

        self.canvas.create_text(
            386.0,
            380.0,
            anchor="nw",
            text="功能选择",
            fill="#D9D9D9",
            font=("Roboto Regular", 27 * -1)
        )

        self.image_image_3 = PhotoImage(
            file=self.relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(
            658.0,
            427.0,
            image=self.image_image_3
        )

        self.canvas.create_rectangle(
            388.0,
            424.0,
            1277.0,
            752.0,
            fill="#3D3644",
            outline="")

        self.button_image_9 = PhotoImage(
            file=self.relative_to_assets("button_9.png"))
        self.button_9 = Button(
            image=self.button_image_9,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_log,
            relief="flat"
        )
        self.button_9.place(
            x=966.0,
            y=426.0,
            width=267.0,
            height=281.0
        )

        self.button_image_10 = PhotoImage(
            file=self.relative_to_assets("button_10.png"))
        self.button_10 = Button(
            image=self.button_image_10,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_help,
            relief="flat"
        )
        self.button_10.place(
            x=712.0,
            y=422.0,
            width=241.7972412109375,
            height=261.4857177734375
        )

        self.button_image_11 = PhotoImage(
            file=self.relative_to_assets("button_11.png"))
        self.button_11 = Button(
            image=self.button_image_11,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: webopen('http://127.0.0.1:1880/ui/'),
            relief="flat"
        )
        self.button_11.place(
            x=426.0,
            y=419.0,
            width=261.3363952636719,
            height=312.0
        )
        self.log.info("main page start" + str(time.time()))

    def goto_firewall(self):
        firewall_window = Toplevel(self.init_window)
        firewall = MY_FIREWALL_GUI(firewall_window)
        firewall.set_firewall_window()
        self.log.info("firewall page start" + str(time.time()))
        firewall_window.mainloop()

    def goto_manage(self):
        manage_window = Toplevel(self.init_window)
        manage = MY_MANAGE_GUI(manage_window)
        manage.set_manage_window()
        self.log.info("manage_window page start" + str(time.time()))
        manage_window.mainloop()

    def goto_ips_flow(self):
        # supervised learning
        flow_window = Toplevel(self.init_window)
        flow_win = MY_FLOW_GUI(flow_window)
        flow_win.set_flow_window()
        self.log.info("flow page start" + str(time.time()))
        flow_window.mainloop()

    def goto_ips_data(self):
        # unsupervised learning
        business_window = Toplevel(self.init_window)
        business_win = MY_BUSINESS_GUI(business_window)
        business_win.set_business_window()
        self.log.info("business_window page start" + str(time.time()))
        business_window.mainloop()

    def open_log(self):
        log_window = Toplevel(self.init_window)
        LOG_window = MY_LOG_GUI(log_window)
        LOG_window.set_log_window()
        LOG_window.read_common_log()
        log_window.mainloop()

    def open_help(self):
        help_window = Toplevel(self.init_window)
        HELP_window = MY_HELP_GUI(help_window)
        HELP_window.set_help_window()
        help_window.mainloop()

    def close_window(self):
        ans = askyesno(title='Warning', message='are you sure to exit?')
        if ans:
            self.log.info("user exit " + str(time.time()))
            self.init_window.destroy()
        else:
            return


class Indus_Rule:
    def __init__(self, init_window, log):
        self.init_window = init_window
        self.gui = MY_GUI(init_window, log)


def gui_start(log):
    init_window = Tk()  # 实例化出一个父窗口
    tool = Indus_Rule(init_window, log)
    init_window.resizable(False, False)
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == '__main__':
    gui_start(logger)

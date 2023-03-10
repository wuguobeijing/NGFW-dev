# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
import tkinter
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import filedialog, Canvas, Frame, Text, Button, PhotoImage, messagebox, BOTH, ACTIVE, END

from gui.NGFW.build_business.plot_multi import MY_MULTI_GUI
from gui.NGFW.build_business.plot_single import MY_SINGLE_GUI


class MY_BUSINESS_GUI(tkinter.Toplevel):
    def __init__(self, business_window):
        super().__init__()
        self.business_window = business_window
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path("assets")

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def goto_main(self):
        self.business_window.destroy()

    def goto_single_flow(self):
        # single
        single_window = tkinter.Toplevel(self.business_window)
        single_win = MY_SINGLE_GUI(single_window)
        single_win.set_single_window()
        single_window.mainloop()

    def goto_multi_flow(self):
        # single
        multi_window = tkinter.Toplevel(self.business_window)
        multi_win = MY_MULTI_GUI(multi_window)
        multi_win.set_single_window()
        multi_window.mainloop()

    def set_business_window(self):
        self.business_window.geometry("1317x855")
        self.business_window.iconphoto(False, tkinter.PhotoImage(
            file='/media/wuguo-buaa/LENOVO_USB_HDD/PycharmProjects/NGFW-dev/gui/NGFW/LOGO.png'))
        self.business_window.configure(bg="#282B2D")
        self.business_window.resizable(True, True)
        self.canvas = Canvas(
            self.business_window,
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
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
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
            self.canvas,
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
        self.button_3 = Button(
            self.canvas,
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
        self.button_4 = Button(
            self.canvas,
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
        self.button_5 = Button(
            self.canvas,
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
        self.button_6 = Button(
            self.canvas,
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
            self.canvas,
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
        self.button_8 = Button(
            self.canvas,
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

        self.image_image_2 = PhotoImage(
            file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            677.3829345703125,
            165.297607421875,
            image=self.image_image_2
        )

        self.canvas.create_text(
            382.3829345703125,
            249.11508178710938,
            anchor="nw",
            text="异常结果判断",
            fill="#D9D9D9",
            font=("Roboto Regular", 27 * -1)
        )

        self.canvas.create_text(
            1056.0,
            821.0,
            anchor="nw",
            text="当前支持MQTT协议检测",
            fill="#D9D9D9",
            font=("Roboto Regular", 20 * -1)
        )

        self.canvas.create_rectangle(
            382.0,
            655.0,
            1271.0,
            819.0,
            fill="#958F93",
            outline="")

        self.button_image_9 = PhotoImage(
            file=self.relative_to_assets("button_9.png"))
        self.button_9 = Button(
            self.canvas,
            image=self.button_image_9,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_9 clicked"),
            relief="flat"
        )
        self.button_9.place(
            x=425.0,
            y=710.0,
            width=157.84524536132812,
            height=78.0
        )

        self.image_image_3 = PhotoImage(
            file=self.relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(
            658.0,
            427.0,
            image=self.image_image_3
        )

        self.canvas.create_rectangle(
            971.0,
            47.0,
            1229.0,
            160.0,
            fill="#3D3644",
            outline="")

        self.button_image_10 = PhotoImage(
            file=self.relative_to_assets("button_10.png"))
        self.button_10 = Button(
            self.canvas,
            image=self.button_image_10,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_10 clicked"),
            relief="flat"
        )
        self.button_10.place(
            x=983.0,
            y=58.0,
            width=117.0,
            height=98.0
        )

        self.button_image_11 = PhotoImage(
            file=self.relative_to_assets("button_11.png"))
        self.button_11 = Button(
            self.canvas,
            image=self.button_image_11,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_11 clicked"),
            relief="flat"
        )
        self.button_11.place(
            x=1108.0,
            y=57.0,
            width=100.88568115234375,
            height=98.00003051757812
        )

        self.button_image_12 = PhotoImage(
            file=self.relative_to_assets("button_12.png"))
        self.button_12 = Button(
            self.canvas,
            image=self.button_image_12,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_12 clicked"),
            relief="flat"
        )
        self.button_12.place(
            x=1103.0,
            y=698.0,
            width=115.0,
            height=101.0
        )

        self.button_image_13 = PhotoImage(
            file=self.relative_to_assets("button_13.png"))
        self.button_13 = Button(
            self.canvas,
            image=self.button_image_13,
            borderwidth=0,
            highlightthickness=0,
            command=self.goto_single_flow,
            relief="flat"
        )
        self.button_13.place(
            x=659.0,
            y=698.0,
            width=115.0,
            height=101.0
        )

        self.button_image_14 = PhotoImage(
            file=self.relative_to_assets("button_14.png"))
        self.button_14 = Button(
            self.canvas,
            image=self.button_image_14,
            borderwidth=0,
            highlightthickness=0,
            command=self.goto_multi_flow,
            relief="flat"
        )
        self.button_14.place(
            x=878.0,
            y=698.0,
            width=118.0,
            height=101.0
        )

# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
import subprocess
from pathlib import Path
from webbrowser import open as webopen
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, Frame, Scrollbar, Listbox, BOTH, END


class MY_FIREWALL_GUI():
    def __init__(self, firewall_window):
        self.firewall_window = firewall_window
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path("assets")
        self.selected_device = None

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def goto_main(self):
        self.firewall_window.destroy()

    def check_device(self):
        if self.selected_device is None:
            messagebox.showwarning("warning", "have to select device first")
            return False
        else:
            return True

    def query_iptables_rules_filter(self):
        if self.check_device():
            rules_content = 'sudo iptables -L -n --line-number'
            self.ssh_query_ip_tables(rules_content)

    def query_iptables_rules_nat(self):
        if self.check_device():
            rules_content = 'sudo iptables -t nat -L -n --line-number'
            self.ssh_query_ip_tables(rules_content)

    def query_iptables_rules_mangle(self):
        if self.check_device():
            rules_content = 'sudo iptables -t mangle -L -n --line-number'
            self.ssh_query_ip_tables(rules_content)

    def query_iptables_rules_raw(self):
        if self.check_device():
            rules_content = 'sudo iptables -t raw -L -n --line-number'
            self.ssh_query_ip_tables(rules_content)

    def ssh_query_ip_tables(self, rules_content):
        self.rule_printout.delete(0, 'end')
        ssh_content = "ssh %s \'%s\'" % (self.selected_device, rules_content)
        p = subprocess.Popen(ssh_content, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = p.communicate()
        if err is not None:
            messagebox.showwarning("query failed!", "try again later")
        else:
            self.show_select_rules(out.decode().strip())
            print(out)

    def show_select_rules(self, out):
        rules_list = out.split('Chain')
        for rules in rules_list:
            atom_rules = rules.split('\n')
            for i, atom_rule in enumerate(atom_rules):
                if "target" in atom_rule or atom_rule == '':
                    pass
                elif i == 0:
                    self.rule_printout.insert(END, atom_rule)
                else:
                    rule_to_print = atom_rule.strip(" ").split()
                    rule_print = rule_to_print[0] + " target:" + rule_to_print[1] + " prot:" + rule_to_print[
                        2] + " opt:" + rule_to_print[3] + " source:" + rule_to_print[4] + " dst:" + rule_to_print[5]
                    rule_content = atom_rules[0].split(' ')[1] + ' - ' + rule_print
                    self.rule_printout.insert(END, rule_content)

    def select_device_k(self):
        self.selected_device = "k"

    def set_firewall_window(self):
        self.firewall_window.geometry("1317x855")
        self.firewall_window.configure(bg="#282B2D")
        self.firewall_window.resizable(False, False)
        self.canvas = Canvas(
            self.firewall_window,
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
            command=self.goto_main,
            # relief="flat"
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
            # relief="flat"
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
            # relief="flat"
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
            # relief="flat"
        )
        self.button_4.place(
            x=102.78173828125,
            y=437.2579345703125,
            width=166.3670654296875,
            height=32.228179931640625
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
            width=202.07936096191406,
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
            x=73.16665649414062,
            y=216.88690185546875,
            width=193.36904907226562,
            height=64.45635223388672
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
            x=87.10317993164062,
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
            669.3829345703125,
            165.297607421875,
            image=self.image_image_2
        )

        self.canvas.create_text(
            382.3829345703125,
            249.11508178710938,
            anchor="nw",
            text="设备管理",
            fill="#D9D9D9",
            font=("Roboto Regular", 27 * -1)
        )

        self.button_image_9 = PhotoImage(
            file=self.relative_to_assets("button_9.png"))
        self.button_9 = Button(
            self.canvas,
            image=self.button_image_9,
            borderwidth=0,
            highlightthickness=0,
            command=self.select_device_k,
            relief="flat"
        )
        self.button_9.place(
            x=382.3829345703125,
            y=308.3452453613281,
            width=151.5595245361328,
            height=191.62698364257812
        )

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
            x=552.0,
            y=308.0,
            width=151.55950927734375,
            height=191.62698364257812
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
            x=723.0,
            y=308.0,
            width=151.55950927734375,
            height=191.62698364257812
        )

        self.canvas.create_rectangle(
            382.0,
            528.0,
            1271.0,
            819.0,
            fill="#958F93",
            outline="")

        # self.button_image_12 = PhotoImage(
        #     file=self.relative_to_assets("button_12.png"))
        # self.button_12 = Button(
        #     self.canvas,
        #     image=self.button_image_12,
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=lambda: print("button_12 clicked"),
        #     relief="flat"
        # )
        # self.button_12.place(
        #     x=1140.0,
        #     y=747.0,
        #     width=89.0,
        #     height=20.0
        # )

        self.button_image_13 = PhotoImage(
            file=self.relative_to_assets("button_13.png"))
        self.button_13 = Button(
            self.canvas,
            image=self.button_image_13,
            borderwidth=0,
            highlightthickness=0,
            command=self.query_iptables_rules_mangle,
            relief="flat"
        )
        self.button_13.place(
            x=458.0,
            y=767.0,
            width=66.0,
            height=24.0
        )

        self.button_image_14 = PhotoImage(
            file=self.relative_to_assets("button_14.png"))
        self.button_14 = Button(
            self.canvas,
            image=self.button_image_14,
            borderwidth=0,
            highlightthickness=0,
            command=self.query_iptables_rules_raw,
            relief="flat"
        )
        self.button_14.place(
            x=405.0,
            y=767.0,
            width=47.0,
            height=26.1309814453125
        )

        self.button_image_15 = PhotoImage(
            file=self.relative_to_assets("button_15.png"))
        self.button_15 = Button(
            self.canvas,
            image=self.button_image_15,
            borderwidth=0,
            highlightthickness=0,
            command=self.query_iptables_rules_filter,
            relief="flat"
        )
        self.button_15.place(
            x=467.0,
            y=725.0,
            width=47.0,
            height=26.0
        )

        self.button_image_16 = PhotoImage(
            file=self.relative_to_assets("button_16.png"))
        self.button_16 = Button(
            self.canvas,
            image=self.button_image_16,
            borderwidth=0,
            highlightthickness=0,
            command=self.query_iptables_rules_nat,
            relief="flat"
        )
        self.button_16.place(
            x=405.0,
            y=725.0,
            width=47.0,
            height=26.1309814453125
        )

        self.button_image_17 = PhotoImage(
            file=self.relative_to_assets("button_17.png"))
        self.button_17 = Button(
            self.canvas,
            image=self.button_image_17,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_17 clicked"),
            relief="flat"
        )
        self.button_17.place(
            x=1140.0,
            y=623.0,
            width=88.84521484375,
            height=23.517852783203125
        )

        self.image_image_3 = PhotoImage(
            file=self.relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(
            658.0,
            427.0,
            image=self.image_image_3
        )

        self.canvas.create_text(
            405.0,
            686.0,
            anchor="nw",
            text="查看规则列表",
            fill="#000000",
            font=("Roboto Regular", 15 * -1)
        )

        self.canvas.create_text(
            405.0,
            617.0,
            anchor="nw",
            text="添加指定规则",
            fill="#000000",
            font=("Roboto Regular", 15 * -1)
        )

        self.entry_image_1 = PhotoImage(
            file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            832.5,
            635.5,
            image=self.entry_image_1
        )
        self.entry_1 = Text(
            self.canvas,
            bd=0,
            bg="#F8F8F8",
            highlightthickness=0
        )
        self.entry_1.place(
            x=547.0,
            y=604.0,
            width=571.0,
            height=61.0
        )

        self.canvas.create_text(
            400.6745910644531,
            548.75,
            anchor="nw",
            text="防火墙规则管理",
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

        self.button_image_18 = PhotoImage(
            file=self.relative_to_assets("button_18.png"))
        self.button_18 = Button(
            self.canvas,
            image=self.button_image_18,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: webopen('http://127.0.0.1:1880/ui/'),
            relief="flat"
        )
        self.button_18.place(
            x=987.0,
            y=58.0,
            width=109.0,
            height=98.0
        )

        self.button_image_19 = PhotoImage(
            file=self.relative_to_assets("button_19.png"))
        self.button_19 = Button(
            self.canvas,
            image=self.button_image_19,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_19 clicked"),
            relief="flat"
        )
        self.button_19.place(
            x=1108.0,
            y=57.0,
            width=100.88568115234375,
            height=98.00003051757812
        )
        self.frame_top = Frame(self.canvas, borderwidth=2)
        self.frame_top.place(x=537.0,
                             y=705.0,
                             width=637.0,
                             height=106.0)
        self.rules_select = Frame(self.frame_top)
        self.rules_select.pack(padx=2, pady=2, ipady=2, ipadx=2, side='top')
        self.rules_Scroll = Scrollbar(self.rules_select)
        self.rules_Scroll.pack(side='right', fill='y')
        self.rule_printout = Listbox(self.rules_select, yscrollcommand=self.rules_Scroll.set, width=200, height=5)
        self.rule_printout.pack(side='right', fill=BOTH)
        self.rules_Scroll.config(command=self.rule_printout.yview)

        self.canvas.create_text(
            810.0,
            674.0,
            anchor="nw",
            text="使用【iptables】作为开头则视为通用防火墙规则配置",
            fill="#0D0101",
            font=("Roboto Regular", 13 * -1)
        )
        # self.firewall_window.mainloop()

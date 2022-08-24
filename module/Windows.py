import tkinter as tk
from tkinter import ttk
import clipboard  # 导入clipboard模块实现复制功能
import configparser  # 导入configparser模块以阅读配置文件
import time
from ctypes import windll  # 导入ctypes使tkinter窗口出现在任务栏中

from Modules import MakePassword

GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080


Config = configparser.ConfigParser()  # 实例化ConfigParser
Config.read("Modules\\Date\\Set.ini")


help_text = """帮助信息
关于软件
软件名称：密码生成器v3.0
软件作者：Lonely-Pea
软件版本：v3.0
软件简介
该软件用于生成强密码，防止破译
软件注意事项：
(1)软件设置后需要重启才能生效！
(2)软件已经放在Github上了，可以自由修改内容
(3)软件有bug可以加Up主QQ：1625396311反馈或在哔哩哔哩上私信反馈"""


class Window(tk.Tk):  # 主窗口
    def __init__(self, title, width, height):
        super(Window, self).__init__()
        self.title, self.width, self.height, self.screenwidth, self.screenheight = title, width, height + 30, self.winfo_screenwidth(), self.winfo_screenheight()
        self.size = "%dx%d+%d+%d" % (
        self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2)
        self.geometry(self.size)
        self.overrideredirect(True)

        self.x, self.y = 0, 0

        self.after(10, lambda: self.set_appwindow(self))

        self.title_bar()  # 显示标题栏

    def set_appwindow(self, root):  # 使tkinter窗口显示在任务栏中（这块代码抄的，我自己看不懂）（网址：https://codingdict.com/questions/196561）
        hwnd = windll.user32.GetParent(root.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        # re-assert the new window style
        root.wm_withdraw()
        root.wm_title("密码生成器v3.0")
        root.after(10, lambda: root.wm_deiconify())

    def title_bar(self) -> None:  # 标题栏
        """
        标题栏需要实现标题的显示，关闭按钮的显示和拖动标题栏实现拖动窗口自

        """
        self.wm_title("AppWindow Test")

        frm_title_bar = tk.Frame(self, bg="white")  # 标题栏框架
        frm_title_bar.place(x=0, y=0, width=self.width, height=30)

        title_label = tk.Label(frm_title_bar, text=self.title, bg="white", font=("微软雅黑",))
        title_label.place(x=0, y=0, height=30)

        button_quit = Button(text="X", bg="white", bg_touch="grey", font=("微软雅黑",), cursor="hand2",
                             command=self.quit_, master=frm_title_bar)
        button_quit.place(x=self.width - 30, y=0, width=30, height=30)

        frm_title_bar.bind("<Button-1>", self.start_move)
        frm_title_bar.bind("<B1-Motion>", self.move)
        title_label.bind("<Button-1>", self.start_move)
        title_label.bind("<B1-Motion>", self.move)

    def quit_(self, event=None):
        self.destroy()

    def restart(self, event=None):
        self.destroy()
        win = Window(title="密码生成器v3.0", width=300, height=100)
        desktop = Desktop(width=300, height=100, master=win)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def move(self, event):
        x = self.winfo_x() + event.x - self.x
        y = self.winfo_y() + event.y - self.y
        self.geometry("+%d+%d" % (x, y))


class Button(tk.Label):  # 按钮
    def __init__(self, text, bg, bg_touch, font, cursor, command, master=None):
        super(Button, self).__init__(master)
        self.master = master
        self.config(text=text)
        self.config(bg=bg)
        self.config(font=font)
        self.config(cursor=cursor)
        self.bg_touch = bg_touch
        self.bg = bg

        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)
        self.bind("<Button-1>", command)

    def Place(self, x, y, width, height):  # 放置对象
        self.place(x=x, y=y, width=width, height=height)

    def enter(self, event=None):
        self.config(bg=self.bg_touch)

    def leave(self, event=None):
        self.config(bg=self.bg)


class Text(tk.Text):  # 文本框
    def __init__(self, text, width, height, x, y, master=None):
        super(Text, self).__init__(master)
        self.master = master
        self.place(x=x, y=y, width=width, height=height)
        scrollbar = ttk.Scrollbar(self.master, command=self.yview)
        scrollbar.place(x=x+width, y=y, height=height)
        self.config(yscrollcommand=scrollbar.set)
        self.insert("end", text)
        self.config(state="disabled")


def InfoBox(title, text):  # 提示框
    def quit_(event=None):
        info_.destroy()
    info_ = Window(title=title, width=100, height=60)
    frm = tk.Frame(info_)
    frm.place(x=0, y=30, width=100, height=60)

    tk.Label(frm, text=text, font=("微软雅黑", )).place(x=0, y=0, height=25)

    Button(master=frm, text="确定", bg="white", bg_touch="grey", font=("微软雅黑", ), cursor="hand2", command=quit_).place(x=49, y=26, width=50, height=25)


class Desktop(tk.Frame):  # 窗口主要内容
    def __init__(self, width, height, master=None):
        super(Desktop, self).__init__(master)
        self.master = master
        self.width, self.height = width, height
        self.place(x=0, y=30, width=width, height=height)

        self.password_make = tk.StringVar()

        self.password_with_number = tk.IntVar()
        self.password_with_number.set(int(Config.get("Password-Format", "password_with_number")))
        self.password_with_letter = tk.IntVar()
        self.password_with_letter.set(int(Config.get("Password-Format", "password_with_letter")))
        self.password_with_symbol = tk.IntVar()
        self.password_with_symbol.set(int(Config.get("Password-Format", "password_with_symbol")))
        self.password_with_symbol_Underline_start = tk.IntVar()
        self.password_with_symbol_Underline_start.set(
            int(Config.get("Password-Format", "password_with_symbol_Underline_start")))
        self.password_with_symbol_Underline_finish = tk.IntVar()
        self.password_with_symbol_Underline_finish.set(
            int(Config.get("Password-Format", "password_with_symbol_Underline_finish")))
        self.password_long = tk.IntVar()
        self.password_long.set(int(Config.get("Password-Format", "password_long")))

        self.main()

    def main(self):  # 主要内容
        tk.Label(self, text="生成的密码：", anchor="w").place(x=0, y=10, width=80, height=25)
        ttk.Entry(self, textvariable=self.password_make).place(x=80, y=10, width=100, height=25)
        button_copy = Button(master=self, text="复制", bg="white", bg_touch="grey", font=("微软雅黑", 8),
                             cursor="hand2", command=self.copy)
        button_copy.place(x=187, y=10, width=50, height=24)
        button_delete = Button(master=self, text="X", bg="white", bg_touch="grey", font=("微软雅黑", 8), cursor="hand2",
                               command=self.delete)
        button_delete.place(x=245, y=10, width=25, height=24)

        button_set = Button(master=self, text="设置", bg="white", bg_touch="grey", font=("微软雅黑", 8), cursor="hand2",
                            command=self.set_)
        button_set.place(x=30, y=40, width=100, height=25)

        button_make = Button(master=self, text="生成", bg="white", bg_touch="grey", font=("微软雅黑", 8), cursor="hand2", command=self.Make)
        button_make.place(x=170, y=40, width=100, height=25)

        button_quit = Button(master=self, text="退出", bg="white", bg_touch="grey", font=("微软雅黑", 8),
                             cursor="hand2", command=self.quit_)
        button_quit.place(x=170, y=70, width=100, height=25)

        tk.Label(self, text="作者：Lonely-Pea", font=("微软雅黑", )).place(x=0, y=self.height - 25, height=25)

    def copy(self, event=None):
        clipboard.copy(self.password_make.get())

    def delete(self, event=None):
        self.password_make.set("")

    def set_(self, event=None):  # 设置选择界面
        global frm_set_middle
        frm_set_middle = tk.Frame(self)
        frm_set_middle.place(x=0, y=0, width=self.width, height=self.height)

        format_set_button = Button(master=frm_set_middle, text="格式设置", bg="white", bg_touch="grey", font=("微软雅黑", ), cursor="hand2", command=self.format_set)
        format_set_button.place(x=1, y=1, width=self.width / 2 - 2, height=self.height / 2 - 2)

        history_set_button = Button(master=frm_set_middle, text="历史记录", bg="white", bg_touch="grey", font=("微软雅黑", ), cursor="hand2", command=self.history_set)
        history_set_button.place(x=self.width / 2 + 1, y=1, width=self.width / 2 - 2, height=self.height / 2 - 2)

        about_set_button = Button(master=frm_set_middle, text="帮助信息", bg="white", bg_touch="grey", font=("微软雅黑", ), cursor="hand2", command=self.help_set)
        about_set_button.place(x=1, y=self.height / 2 + 1, width=self.width / 2 - 2, height=self.height / 2 - 2)

        back_button = Button(master=frm_set_middle, text="返回主界面", bg="white", bg_touch="grey", font=("微软雅黑", ), cursor="hand2", command=self.back_)
        back_button.place(x=self.width / 2 + 1, y=self.height / 2 + 1, width=self.width / 2 - 2, height=self.height / 2 - 2)

        self.master.wm_title("设置中心")

    def format_set(self, event=None):  # 格式设置
        def save(event=None):  # 保存修改
            if self.password_with_number.get() == 0 and self.password_with_letter.get() == 0 and self.password_with_symbol.get() == 0 and self.password_with_symbol_Underline_start.get() == 0 and self.password_with_symbol_Underline_finish.get() == 0:
                InfoBox(title="提示", text="保存失败！")
            else:
                Config.set("Password-Format", "password_with_number", str(self.password_with_number.get()))
                Config.set("Password-Format", "password_with_letter", str(self.password_with_letter.get()))
                Config.set("Password-Format", "password_with_symbol", str(self.password_with_symbol.get()))
                Config.set("Password-Format", "password_with_symbol_underline_start", str(self.password_with_symbol_Underline_start.get()))
                Config.set("Password-Format", "password_with_symbol_underline_finish", str(self.password_with_symbol_Underline_finish.get()))
                Config.set("Password-Format", "password_long", str(self.password_long.get()))
                Config.write(open("Modules\\Date\\Set.ini", "r+", encoding="utf-8"))

                InfoBox(title="提示", text="保存完毕！")

        def back(event=None):  # 返回设置总站
            # 不保存设置
            self.password_with_number.set(int(Config.get("Password-Format", "password_with_number")))
            self.password_with_letter.set(int(Config.get("Password-Format", "password_with_letter")))
            self.password_with_symbol.set(int(Config.get("Password-Format", "password_with_symbol")))
            self.password_with_symbol_Underline_start.set(
                int(Config.get("Password-Format", "password_with_symbol_Underline_start")))
            self.password_with_symbol_Underline_finish.set(
                int(Config.get("Password-Format", "password_with_symbol_Underline_finish")))
            self.password_long.set(int(Config.get("Password-Format", "password_long")))

            self.master.wm_title("设置中心")

            frm_format_set.destroy()

        frm_format_set = tk.Frame(frm_set_middle)
        frm_format_set.place(x=0, y=0, width=self.width, height=self.height)

        tk.Label(frm_format_set, text="密码格式设置", font=("微软雅黑", )).place(x=0, y=0, height=25)
        ttk.Checkbutton(frm_format_set, text="带数字", variable=self.password_with_number).place(x=0, y=25, height=25)
        ttk.Checkbutton(frm_format_set, text="带字母", variable=self.password_with_letter).place(x=0, y=50, height=25)
        ttk.Checkbutton(frm_format_set, text="带符号", variable=self.password_with_symbol).place(x=0, y=75, height=25)
        ttk.Checkbutton(frm_format_set, text="开头带下划线", variable=self.password_with_symbol_Underline_start).place(x=60, y=25, height=25)
        ttk.Checkbutton(frm_format_set, text="结尾带下划线", variable=self.password_with_symbol_Underline_finish).place(x=60, y=50, height=25)

        tk.Label(frm_format_set, text="密码长度：").place(x=60, y=75, height=25)
        ttk.Spinbox(frm_format_set, textvariable=self.password_long, from_=4, to=12).place(x=120, y=75, width=110)

        button_save = Button(master=frm_format_set, text="保存修改", bg="white", bg_touch="grey", font=("微软雅黑", ), cursor="hand2", command=save)
        button_save.place(x=160, y=24, width=70, height=24)

        button_back = Button(master=frm_format_set, text="返回", bg="white", bg_touch="grey", font=("微软雅黑", ), cursor="hand2", command=back)
        button_back.place(x=160, y=49, width=70, height=24)

        self.master.wm_title("设置中心-密码格式设置")

    def history_set(self, event=None):  # 历史记录
        def back(event=None):
            self.master.wm_title("设置中心")
            frm_history_set.destroy()

        frm_history_set = tk.Frame(frm_set_middle)
        frm_history_set.place(x=0, y=0, width=self.width, height=self.height)

        if open("Modules\\Date\\History.txt", "r").read() == "":
            text = Text(text="还没有生成过一次呢！能试一下先吗？", x=0, y=0, width=int(self.width - 20), height=self.height - 27, master=frm_history_set)

        else:
            open("Modules\\Date\\History.txt", "r").seek(0)
            text = Text(text=open("Modules\\Date\\History.txt", "r").read(), x=0, y=0, width=int(self.width - 20), height=self.height - 27, master=frm_history_set)

        open("Modules\\Date\\History.txt", "r").close()

        Button(master=frm_history_set, text="返回", bg="white", bg_touch="grey", font=("微软雅黑", ), cursor="hand2", command=back).place(x=(self.width - 50) / 2, y=self.height - 26, width=50, height=25)

        self.master.wm_title("设置中心-历史记录")

    def help_set(self, event=None):  # 帮助信息
        def back(event=None):
            self.master.wm_title("设置中心")
            frm_help_set.destroy()
        frm_help_set = tk.Frame(frm_set_middle)
        frm_help_set.place(x=0, y=0, width=self.width, height=self.height)

        text = Text(text=help_text, x=0, y=0, width=int(self.width - 20), height=self.height - 27, master=frm_help_set)

        Button(master=frm_help_set, text="返回", bg="white", bg_touch="grey", font=("微软雅黑", ), cursor="hand2", command=back).place(x=(self.width - 50) / 2, y=self.height - 26, width=50, height=25)

    def Make(self, event=None):
        password = MakePassword.Make()
        self.password_make.set(password)
        open("Modules\\Date\\History.txt", "a").write("[%s]\n%s\n" % (time.asctime(), password))
        open("Modules\\Date\\History.txt", "r").close()

    def back_(self, event=None):  # 返回到主界面
        frm_set_middle.destroy()
        self.master.wm_title("密码生成器v3.0")

    def quit_(self, event=None):
        self.master.destroy()


if __name__ == "__main__":
    win = Window(title="密码生成器v3.0", width=300, height=100)
    desktop = Desktop(width=300, height=100, master=win)

    win.mainloop()

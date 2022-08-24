# PasswordMakerv3.0
该软件完全使用tkinter模块编写，依赖的模块有tkinter, clipboard, configparser, time, stypes, random。
该软件的界面通过tkinter.Tk().overrideredirect(True)隐藏了窗口边框，然后又使用了以下代码：
hwnd = windll.user32.GetParent(root.winfo_id())
style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
style = style & ~WS_EX_TOOLWINDOW
style = style | WS_EX_APPWINDOW
res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
root.wm_withdraw()
root.wm_title("密码生成器v3.0")
root.after(10, lambda: root.wm_deiconify())
实现了窗口显示在任务栏中。
其他更多的请下载后在看吧！

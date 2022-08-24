from Modules.Windows import Window, Desktop

if __name__ == "__main__":
    win = Window(title="密码生成器v3.0", width=300, height=100)
    desktop = Desktop(width=300, height=100, master=win)

    win.mainloop()

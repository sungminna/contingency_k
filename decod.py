

#path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths" (control.exe)     uac, local
#path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"    startup, local
#path = r"Software\Microsoft\Windows NT\CurrentVersion", (History)    first, cu

# "iboxk kva" <ibox1313ak@inbox.lv> or ibox1313ak@inbox.lv

class Decod():
    def __init__(self):
        self.target = []
        self.tsr()

    def tsr(self):
        for item in self.target:
            res = item.decode('utf-16')
            print(res)

    def hide_scr(self):
        #win = win32console.GetConsoleWindow()
        #win32gui.ShowWindow(win, 0)
        pass

if __name__=="__main__":
    Decod()


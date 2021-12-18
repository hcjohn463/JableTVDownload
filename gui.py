import threading
import time
import tkinter.filedialog

from mywidget import *
from JableTVJob import JableTVJob
import os
import re


class JableTVDownloadWindow(tk.Tk):
    """JableTV downloader GUI Main Window"""
    def __init__(self, dest="download", urls='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self._on_window_closed)
        self._currentJob = None
        self._urls_list = []
        self._import_dest = dest
        self.create_widgets(dest, urls)
        self._is_abort = False
        self._clp_text = ""
        self.clipboard_checker = threading.Thread(target=self.check_clipboard).start()
        self.clipborad_thread = None

    def create_widgets(self, dest, urls):
        self.title('JableTV 下載器')
        self.geometry('640x480')

        self.tree = MyDownloadListView(self)
        self.tree.pack(side="top", fill='both', expand=True, padx = 4, pady = 4)
        self.tree.on_item_selected = self.on_treeitem_selected
        self.tree.bind('<<TreeviewSelect>>', self.on_treeitem_selected)

        dest_frame = tk.Frame(self)
        dest_frame.pack(side=tk.TOP)
        dest_label = tk.Label(dest_frame,text='存放位置',width=10)
        dest_label.pack(side=tk.LEFT)
        self.dest_entry = tk.Entry(dest_frame, width=70)
        self.dest_entry.pack(side=tk.LEFT,expand=True)

        url_frame = tk.Frame(self)
        url_frame.pack(side=tk.TOP)
        url_label = tk.Label(url_frame,text='下載網址',width=10)
        url_label.pack(side=tk.LEFT)
        self.url_entry = tk.Entry(url_frame,width=70)
        self.url_entry.pack(side=tk.LEFT)

        btn_frame = tk.Frame(self)
        btn_frame.pack(side=tk.TOP)
        self.btn_importlist = tk.Button(btn_frame,text='導入文件', command=self.on_import_list)
        self.btn_importlist.pack(side=tk.LEFT)
        self.btn_addlist = tk.Button(btn_frame,text='加入清單', command=self.on_add_list)
        self.btn_addlist.pack(side=tk.LEFT)
        self.btn_download = tk.Button(btn_frame,text='開始下載', command=self.on_start_download)
        self.btn_download.pack(side=tk.RIGHT)

        self.text = RedirectConsole(self)
        self.text.pack(side="top", fill="both", expand=True, padx=4, pady=4)

        self.dest = dest
        self.urls = urls

        self.load_on_create()
        self.dest_entry.insert(tk.END, dest)
        self.url_entry.insert(tk.END, urls)

    def on_treeitem_selected(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(tk.END, item['values'][2])
            self.url_entry.delete(0, tk.END)
            url_full = JableTVJob.get_urls_form(item['values'][0], shortform=False)
            self.url_entry.insert(tk.END, url_full)

    def _do_clipboard_list(self):
        try:
            while(self._urls_list != [] ):
                urls = self._urls_list.pop(0)
                self._add_url_to_tree(urls, self.dest)
        except Exception:
            pass
        finally:
            self.clipborad_thread = None

    def check_clipboard(self):
        while not self._is_abort:
            try:
                clp = self.clipboard_get()
                if not type(clp) is type(self._clp_text) or\
                    self._clp_text != clp:
                    self._clp_text = clp
                    result = re.findall("https://jable\.tv/videos/.+?/", clp)
                    for str in result:
                        self._urls_list.append(str.strip())
                        #self.text.clear_contents()
                        #self._add_url_to_tree(str.strip(), self._import_dest)
                        if self._urls_list != [] and  not self.clipborad_thread:
                            self.clipborad_thread = threading.Timer(0.5, self._do_clipboard_list)
                            self.clipborad_thread.start()
                time.sleep(0.2)
            except:
                pass

    def _on_window_closed(self):
        self._is_abort = True
        self._urls_list = []
        self.on_cancel_download()
        self.save_on_close()
        self.destroy()

    def _get_entry_values(self):
        self.dest = self.dest_entry.get()
        self.urls = self.url_entry.get()

    def toggle_download_button(self, is_cancel=1):
        if is_cancel == 1:
            self.btn_download['text'] = "取消下載"
            self.btn_download['command'] = self.on_cancel_download
        else:
            self.btn_download['text'] = "開始下載"
            self.btn_download['command'] = self.on_start_download

    def on_cancel_download(self):
        self.cancel_download()
        self.toggle_download_button(0)

    def on_start_download(self):
        self.text.clear_contents()
        self._get_entry_values()
        self.toggle_download_button(1)
        self._currentJob = JableTVJob(self.urls, self.dest)
        if self._currentJob.is_url_vaildate():
            self.tree.update_item_state(self.urls, "下載中")
            self._currentJob.begin_concurrent_download()
            threading.Timer(0.5, self._on_timer_downloading).start()
        else:
            if self.tree.exists(self.urls):
                self.tree.update_item_state(self.urls, "網址錯誤")
            self._currentJob = None
            self.toggle_download_button(0)

    def _on_timer_downloading(self):
        if self._currentJob:
            if self._currentJob.is_concurrent_dowload_completed():
                self._currentJob.end_concurrent_download()
                jjob, self._currentJob = self._currentJob, None
                self.tree.update_item_state(jjob.get_url_short(), "已下載")
                self.toggle_download_button(0)
                print('下載完成!')
            else:
                threading.Timer(0.5, self._on_timer_downloading).start()

    def _add_url_to_tree(self, url, savePath, showmsg=True):
        if not self.tree.exists(url):
            jjob = JableTVJob(url, savePath)
            if jjob.is_url_vaildate():
                self.tree.additem(url, jjob.target_name(), savePath)
                return True
            else:
                return False
        else:
            if showmsg:
                print(f"{url} 已存在下載清單中!!")
            return False

    def on_add_list(self):
        self.text.clear_contents()
        self._get_entry_values()
        return self._add_url_to_tree(self.urls, self.dest)

    def cancel_download(self):
        jjob, self._currentJob = self._currentJob, None
        if(jjob):
            self.tree.update_item_state(jjob.get_url_short(), "未完成")
            threading.Thread(target=jjob.cancel_download).start()

    def load_on_create(self):
        self.tree.load_from_csv(os.path.join(os.getcwd(), "JableTV.csv"))

    def save_on_close(self):
        self.tree.save_to_csv(os.path.join(os.getcwd(), "JableTV.csv"))

    def _do_import_list(self):
        try:
            self.text.clear_contents()
            for i in range(5):
                while self._urls_list != []:
                    urls = self._urls_list.pop(0)
                    if self._add_url_to_tree(urls, self._import_dest, showmsg=False): break;
            if self._urls_list != []:
                threading.Timer(0.05, self._do_import_list).start()
            else:
                print("網址載入完成!!")
        except Exception:
            pass

    def on_import_list(self):
        self._get_entry_values()
        filename = tkinter.filedialog.askopenfilename()
        try:
            self._urls_list = []
            self._import_dest = self.dest
            with open(filename, "r", encoding='utf-8') as f:
                for line in f.readlines():
                    result = re.findall("https://jable\.tv/videos/.+?/", line)
                    for str in result:
                        self._urls_list.append(str.strip())
            if self._urls_list != []:
                threading.Timer(0.5, self._do_import_list).start()
            else:
                print("無有效的網址!!")
        except Exception:
            return

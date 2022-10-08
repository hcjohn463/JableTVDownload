#!/usr/bin/env python
# coding: utf-8

import threading
import time
import tkinter
import tkinter.filedialog

from mywidget import *
from JableTVJob import JableTVJob
import os
import re

from PIL import ImageTk, Image


def gui_main(urls, dest):
    mainWnd = JableTVDownloadWindow(dest=dest, urls=urls)
    mainWnd.mainloop()
    mainWnd.cancel_download()


class JableTVDownloadWindow(tk.Tk):
    """JableTV downloader GUI Main Window"""
    def __init__(self, dest="download", urls='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self._on_window_closed)
        self._currentJob = None
        self._download_list = []
        self._cancel_all = False
        self._urls_list = []
        self._import_dest = dest
        self.create_widgets(dest, urls)
        self._is_abort = False
        self._clp_text = ""
        self.clipboard_checker = threading.Thread(target=self.check_clipboard).start()
        self.clipborad_thread = None
        self.toggle_download_button()
        self.loadthumbnail_thread = None


    def create_widgets(self, dest, urls):
        self.title('JableTV 下載器')
        self.geometry('1024x768')

        self.tree = MyDownloadListView(self)
        self.tree.pack(side="top", fill='both', expand=True, padx=4, pady=4)
        self.tree.on_item_selected = self.on_treeitem_selected
        self.tree.bind('<<TreeviewSelect>>', self.on_treeitem_selected)

        dest_frame = tk.Frame(self)
        #        dest_frame["highlightbackground"] = "blue"
        #        dest_frame["highlightthickness"] = 2
        dest_frame.pack(side=tk.TOP, fill='x', padx=12)
        dest_label = tk.Label(dest_frame, text='存放位置', width=10)
        dest_label.pack(side=tk.LEFT)
        self.dest_entry = tk.Entry(dest_frame, width=70)
        self.dest_entry.pack(side=tk.LEFT, fill='x', expand=True)

        url_frame = tk.Frame(self)
        url_frame.pack(side=tk.TOP, fill='x', padx=12)
        url_label = tk.Label(url_frame, text='下載網址', width=10)
        url_label.pack(side=tk.LEFT, fill="both")
        self.url_entry = tk.Entry(url_frame, width=70)
        self.url_entry.pack(side=tk.LEFT, fill='x', expand=True)

        btns_frame = tk.Frame(self)
        btns_frame.pack(side=tk.TOP, fill='x', padx=18, pady=2)
        btn_leftframe = tk.Frame(btns_frame)
        btn_leftframe.pack(side=tk.LEFT, padx=18, pady=1)
        btn_rightframe = tk.Frame(btns_frame)
        btn_rightframe.pack(side=tk.LEFT, padx=18, pady=1)

        self.btn_importlist = tk.Button(btn_leftframe, text='導入文件', command=self.on_import_list)
        self.btn_importlist.pack(side=tk.LEFT, padx=2)
        self.btn_addlist = tk.Button(btn_leftframe, text='加入清單', command=self.on_add_list)
        self.btn_addlist.pack(side=tk.LEFT, padx=2)
        self.btn_download = tk.Button(btn_leftframe, text='開始下載', command=self.on_start_download)
        self.btn_download.pack(side=tk.LEFT, padx=2)
        self.btn_download_all = tk.Button(btn_leftframe, text='全部下載', command=self.on_start_all_download)
        self.btn_download_all.pack(side=tk.LEFT, padx=2)
        self.btn_cancel = tk.Button(btn_leftframe, text='全部取消', command=self.on_cancel_all_download)
        self.btn_cancel.pack(side=tk.RIGHT, padx=2)

        self.btn_clearText = tk.Button(btn_rightframe, text="清除", command=self.on_clear_text)
        self.btn_clearText.pack(side=tk.RIGHT, padx=2, ipadx=12)

        self.text = RedirectConsole(self)
        self.text.pack(side=tk.LEFT, fill="both", expand=True, padx=8, pady=2)

        self.thumbnail_label = tk.Label(self)#, width=360, height=270)
        self.thumbnail_label.pack(side=tk.LEFT)

        self.thumbnail = None

        self.dest = dest
        self.urls = urls

        self.load_on_create()
        self.dest_entry.insert(tk.END, dest)
        self.url_entry.insert(tk.END, urls)

    def _loadThumbnail(self):
        jjob = JableTVJob(self.urls, self.dest, silence=True)
        url = jjob.download_image()
        if url is not None:
            img = Image.open(url)
            w = 360 / img.size[0]
            h = 270 / img.size[1]
            __sz = (360, (int)(img.size[1]*w) )
            if w>h: __sz = ((int)(img.size[0]*h), 270)
            self.thumbnail = ImageTk.PhotoImage(img.resize(__sz))
            self.thumbnail_label.pack_forget()
            self.thumbnail_label["image"] = self.thumbnail
            self.thumbnail_label.pack(side=tk.LEFT)
        self.loadthumbnail_thread = None

    def showThumbnail(self):
        if self.loadthumbnail_thread is None:
            self.loadthumbnail_thread = threading.Timer(0.5, self._loadThumbnail)
            self.loadthumbnail_thread.start()

    def on_treeitem_selected(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(tk.END, item['values'][2])
            self.url_entry.delete(0, tk.END)
            url_full = JableTVJob.get_urls_form(item['values'][0], shortform=False)
            self.url_entry.insert(tk.END, url_full)
            self._get_entry_values()
            self.toggle_download_button()
            self.showThumbnail()

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

    def toggle_download_button(self):
        self.btn_download['text'] = "開始下載"
        self.btn_download['command'] = self.on_start_download
        self._get_entry_values()
        if self.urls is None or self.urls == "":
            self.btn_download["state"] = tk.DISABLED
        else:
            self.btn_download["state"] = tk.NORMAL
        if self._download_list != []:
            for dlist in self._download_list:
                if dlist[0] == self.urls:
                    self.btn_download['text'] = "取消下載"
                    self.btn_download['command'] = self.on_cancel_download
        if self._currentJob and self.urls == self._currentJob.get_url_full():
                self.btn_download['text'] = "取消下載"
                self.btn_download['command'] = self.on_cancel_download

        if len(self.tree.selection()) > 1:
            self.btn_download_all["state"] = tk.NORMAL
        else:
            self.btn_download_all["state"] = tk.DISABLED

        if self._download_list != [] or self._currentJob:
            self.btn_cancel["state"] = tk.NORMAL
        else:
            self.btn_cancel["state"] = tk.DISABLED

    def on_cancel_all_download(self):
        self._cancel_all = True
        self.on_cancel_download()

    def on_cancel_download(self):
        if self._cancel_all or (self._currentJob and self.urls == self._currentJob.get_url_full()):
            jjob, self._currentJob = self._currentJob, None
            if(jjob):
                self.tree.update_item_state(jjob.get_url_short(), "未完成")
                threading.Thread(target=jjob.cancel_download).start()
        else:
            for urls in self._download_list:
                if urls[0] == self.urls:
                    self.tree.update_item_state(self.urls, "已取消")
                    self._download_list.remove(urls)
        self.toggle_download_button()

    def on_start_all_download(self):
        for it in self.tree.selection():
            data = self.tree.item(it)
            url_full = JableTVJob.get_urls_form(data['values'][0], shortform=False)
            self._download_list.append([url_full, data['values'][2]])
            self.tree.update_item_state(url_full, "等待中")
        self.toggle_download_button()
        if self._currentJob is None:
            threading.Timer(0.5, self._on_timer_downloading).start()

    def on_start_download(self):
        self._cancel_all = False
        self._get_entry_values()
        self._download_list.append([self.urls, self.dest])
        self.tree.update_item_state(self.urls, "等待中")
        self.toggle_download_button()
        if self._currentJob is None:
            threading.Timer(0.5, self._on_timer_downloading).start()

    def _on_timer_downloading(self):
        if self._currentJob:
            if self._currentJob.is_concurrent_dowload_completed():
                self._currentJob.end_concurrent_download()
                jjob, self._currentJob = self._currentJob, None
                self.tree.update_item_state(jjob.get_url_short(), "已下載")
                self.toggle_download_button()
                print('下載完成!')
                if self._download_list != []:
                    threading.Timer(0.5, self._on_timer_downloading).start()
            else:
                threading.Timer(0.5, self._on_timer_downloading).start()
        elif self._cancel_all :
            while self._download_list != []:
                download_urls, download_dest = self._download_list.pop(0)
                self.tree.update_item_state(download_urls, "已取消")
        elif self._download_list != [] :
            self.text.clear_contents()
            download_urls, download_dest = self._download_list.pop(0)
            self._currentJob = JableTVJob(download_urls, download_dest)
            if self._currentJob.is_url_vaildate():
                self.tree.update_item_state(download_urls, "下載中")
                self._currentJob.begin_concurrent_download()
                threading.Timer(0.5, self._on_timer_downloading).start()
            else:
                if self.tree.exists(self.urls):
                    self.tree.update_item_state(self.urls, "網址錯誤")
                self._currentJob = None
                self.toggle_download_button()

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

    def on_clear_text(self):
        self.text.clear_contents()

if __name__ == "__main__":
    gui_main("", "download")

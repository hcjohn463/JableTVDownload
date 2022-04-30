#!/usr/bin/env python
# coding: utf-8

import sys
import tkinter as tk
import tkinter.ttk as ttk
import os
import csv
from JableTVJob import JableTVJob


class RedirectConsole(tk.Listbox):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._cursor_y = 0
        self._old_stdout_write = sys.stdout.write
        sys.stdout.write = self._on_stdout_write

    def __del__(self):
        sys.stdout.write = self._old_stdout_write

    def _on_stdout_write(self, msg):
        try:
            self.configure(state="normal")
            msgs1 = msg.partition("\n")
            while True:
                msgs2 = msgs1[0].rpartition("\r")
                if msgs2[1] == '\r':
                    newline = msgs2[2]
                    newline = newline.lstrip()
                else:
                    newline = self.get(self._cursor_y) + msgs2[2]
                if newline != "":
                    self.delete(self._cursor_y, tk.END)
                    self.insert(self._cursor_y, newline)
                    self.see(self._cursor_y)
                if msgs1[1] != "\n": break
                self._cursor_y += 1
                if msgs1[2] == "": break
                msgs1 = msgs1[2].partition("\n")
            self.configure(state="disabled")
        except Exception:
            # 輸出到原來的 stdout IO
            self._old_stdout_write(msg)

    def clear_contents(self):
        self.configure(state="normal")
        self.delete(0, tk.END)
        self.configure(state="disabled")
        self._cursor_y = 0


class ScrollTreeView(ttk.Treeview):
    """ ttk.Treeview with a vertical scroll bar """
    _download_state_ = {'': 100, '已下載': 0, '未完成': 1, '下載中': 2, '等待中': 3, '已取消': 4, '網址錯誤': 99}

    def __init__(self, master, **kwargs):
        _frame = tk.Frame(master)
        super().__init__(_frame, **kwargs)
        self.scrollbar = ttk.Scrollbar(_frame, orient=tk.VERTICAL, command=self.yview)
        self.configure(yscrollcommand=self.scrollbar.set)
        self.grid(row=0, column=0, sticky='NSEW')
        self.scrollbar.grid(row=0, column=1, sticky='NSW')
        self._frame = _frame
        self._frame.columnconfigure(0, weight=1)
        self._frame.rowconfigure(0, weight=1)
        self.pack = self._frame.pack
        self.grid = self._frame.grid
        self.place = self._frame.place


class MyDownloadListView(ScrollTreeView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.list_modified = False
        self._colnames = ['網址', '名稱', '儲存位置', '狀態']
        self.config(columns=self._colnames, show="headings")

        self.heading(self._colnames[0], text=self._colnames[0], command=lambda:self._sort_column(self._colnames[0], False))
        self.heading(self._colnames[1], text=self._colnames[1], command=lambda:self._sort_column(self._colnames[1], False))
        self.heading(self._colnames[2], text=self._colnames[2], command=lambda:self._sort_column(self._colnames[2], False))
        self.heading(self._colnames[3], text=self._colnames[3], command=lambda:self._sort_column(self._colnames[3], False))
        self.column(self._colnames[0], width=80, minwidth=40, stretch=False)
        self.column(self._colnames[1], stretch=True)
        self.column(self._colnames[2], width=80, minwidth=40, stretch=False)
        self.column(self._colnames[3], width=64, minwidth=40, stretch=False)

        self.config(displaycolumns=[2, 0, 1, 3])
        self.bind("<Delete>", self._on_key_delete_event)
        self.bind("<B1-Motion>", self._move_row, add='+')

    def exists(self, item):
        url_short = JableTVJob.get_urls_form(item)
        if url_short: return super().exists(url_short)
        return False

    def _sort_column(self, col, reverse: bool):
        l = [(self.set(k, col), k) for k in self.get_children('')]
        if col == '狀態':
            l = sorted(l, key=lambda s: ScrollTreeView._download_state_.__getitem__(s[0]), reverse=reverse)
        else:
            l = sorted(l, key=lambda s: s[0].lower(), reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.move(k, '', index)
        self.heading(col, command=lambda:self._sort_column(col, not reverse))
        self.list_modified = True

    def _on_key_delete_event(self, event):
        for selected_item in self.selection():
            self.delete(selected_item)
            self.list_modified = True

    def _move_row(self, event):
        if len(self.selection()) > 1: return
        moveto = self.index(self.identify_row(event.y))
        for s in self.selection():
            self.move(s, '', moveto)

    def update_item_state(self, urls, state):
        url_short = JableTVJob.get_urls_form(urls)
        if url_short:
            if not self.exists(url_short):
                self.insert("", "end", iid=url_short, values=[url_short, "", "", state])
            else:
                self.set(url_short, column=self._colnames[3], value=state)
            self.list_modified = True

    def additem(self, urls, saveName="", savePath="", state=""):
        url_short = JableTVJob.get_urls_form(urls)
        if url_short:
            if not self.exists(url_short):
                self.insert("", "end", iid=url_short, values=[url_short, saveName, savePath, state])
                self.list_modified = True
            else:
                v_old = self.set(url_short)
                if savePath != v_old[2]:
                    self.set(url_short, column=self._colnames[2], value=savePath)
                    self.list_modified = True
                if saveName != '' and  saveName != v_old[1]:
                    self.set(url_short, column=self._colnames[1], value=saveName)
                    self.list_modified = True

    def save_to_csv(self, csvName):
        if not self.list_modified : return
        with open(csvName, 'w', encoding='utf-8') as f:
            csvwriter = csv.DictWriter(f, fieldnames=self._colnames)
            csvwriter.writeheader()
            items = self.get_children()
            for it in items:
                data = self.set(it)
                data[self._colnames[0]] = JableTVJob.get_urls_form(data[self._colnames[0]],shortform=False)
                csvwriter.writerow(data)
        self.list_modified = False

    def load_from_csv(self, csvName):
        if not os.path.exists(csvName): return
        with open(csvName, 'r',encoding='utf-8') as f:
            csvreader = csv.DictReader(f)
            for rd in csvreader:
                vv = [rd.pop(h, '') for h in self._colnames]
                self.additem(vv[0], vv[1], vv[2], vv[3])
        self.list_modified = False

import tkinter as tk
from tkinter import ttk


class ListBoxCol(tk.Frame):
    def __init__(self, *args, **kawrgs):
        super().__init__(*args, **kawrgs)

        self.data_cols = ("Category", "Spend", "Note")
        self.tree = ttk.Treeview(self, columns=self.data_cols, show="headings")
        self.vscroll_bar = ttk.Scrollbar(self, orient="vertical", command= self.tree.yview)
        self.hscroll_bar = ttk.Scrollbar(self, orient="horizontal", command= self.tree.xview)
        self.tree['yscroll'] = self.vscroll_bar.set
        self.tree['xscroll'] = self.hscroll_bar.set

        for c in self.data_cols:
            self.tree.heading(c, text=c.title())


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.vscroll_bar.grid(row=0, column=1, sticky="ns")
        self.hscroll_bar.grid(row=1, column=0, sticky="ew")
        self.tree.grid(row=0, column=0, sticky="nswe")

        self.bind("<Configure>", self.onFrameConfig)

    def get_selected(self):
        return self.tree.selection()

    def insert(self, val):
        self.tree.insert("", "end", value=val)

    def delete(self, item):
        self.tree.delete(item)

    def clear(self):
        self.tree.delete(*self.tree.get_children())

    def onFrameConfig(self, event):
        minWidth = self.tree.winfo_reqwidth()
        minHeight = self.tree.winfo_reqheight()

        if self.winfo_width() >= minWidth:
            newWidth = self.winfo_width()
            self.hscroll_bar.grid_remove()
        else:
            newWidth = minWidth
            self.hscroll_bar.grid()

        if self.winfo_height() >= minHeight:
            newHeight = self.winfo_height()
            self.vscroll_bar.grid_remove()
        else:
            newHeight = minHeight
            self.vscroll_bar.grid()


import json, datetime
import tkinter as tk
import tkinter.font as tkFont
from widget import ListBoxCol


class DateViewFrame(tk.Frame):
    def __init__(self, *args, **kawrgs):
        super().__init__(*args, **kawrgs)
        self.current_date = datetime.datetime.today()
        with open("data/data.json") as f:
            self.data = json.load(f)

        self.date_label = tk.Label(self, text=self.format_current_date())
        self.next_date_button = tk.Button(self, text=">", command=self.next_date)
        self.prev_date_button = tk.Button(self, text="<", command=self.prev_date)

        self.list_box_col = ListBoxCol(self)
        self.total = 0
        self.total_label = tk.Label(self)
        self.delete_button = tk.Button(self, text="Delete", command=self.delete)
        self.save_button = tk.Button(self, text='Save', command=self.save)

        for i in range(2):
            tk.Grid.rowconfigure(self, i, weight=1)
        for i in range(3):
            tk.Grid.columnconfigure(self, i, weight=1)

        self.prev_date_button.grid(row=0, column=0, sticky="we")
        self.date_label.grid(row=0, column=1, sticky="we")
        self.next_date_button.grid(row=0, column=2, sticky="we")
        self.list_box_col.grid(row=1, column=0, columnspan=3, sticky="nswe")
        self.total_label.grid(row=2, column=0)
        self.delete_button.grid(row=2, column=1)
        self.save_button.grid(row=2, column=2)

        self.update()

    def format_current_date(self):
        return self.current_date.strftime("%d-%m-%Y")

    def next_date(self):
        self.list_box_col.clear()
        self.current_date = self.current_date + datetime.timedelta(days=1)
        self.date_label.config(text=self.format_current_date())
        self.update()

    def prev_date(self):
        self.list_box_col.clear()
        self.current_date = self.current_date - datetime.timedelta(days=1)
        self.date_label.config(text=self.format_current_date())
        self.update()

    def insert(self, data):
        try:
            self.data[self.format_current_date()].append(data)
        except:
            self.data[self.format_current_date()] = [data]
        self.list_box_col.insert(data)
        self.total += int(data[1])
        self.total_label.config(text=format(self.total, ","))

    def delete(self):
        for i in self.list_box_col.get_selected():
            self.total -= self.list_box_col.tree.item(i)["values"][1]
            self.list_box_col.delete(i)
            del self.data[self.format_current_date()]

        self.total_label.config(text=format(self.total, ","))

    def save(self):
        with open("data/data.json", 'w') as f:
            json.dump(self.data, f, indent=4)

    def update(self):
        self.total = 0
        try:
            for val in self.data[self.format_current_date()]:
                self.total += int(val[1])
                self.list_box_col.insert(val)
        except:
            pass
        self.total_label.config(text=format(self.total, ","))


class InsertingFrame(tk.Frame):
    def __init__(self, parent, *args, **kawrgs):
        self.parent = parent
        super().__init__(parent, *args, **kawrgs)
        with open("data/category.json") as f:
            self.data = json.load(f)

        self.category_frame = tk.Frame(self)
        self.spend_frame = tk.Frame(self)

        self.spend_entry = tk.Entry(self.spend_frame)

        self.cate_var = tk.StringVar(value="0")
        self.spend_var = tk.IntVar(value=0)
        self.range_rbutton_list = []
        for key, val in self.data.items():
            clabel = tk.Radiobutton(self.category_frame, variable=self.cate_var, value=key, text=val["name"], anchor="w")
            clabel.pack(anchor="w")
        for i, price in enumerate(self.data["0"]["range"]):
            slabel = tk.Radiobutton(self.spend_frame, variable=self.spend_var, value=price, text=format(price, ","), anchor="w")
            self.range_rbutton_list.append(slabel)
            slabel.grid(row=i//2+1, column=i%2, sticky="we")

        self.spend_entry.grid(row=0, column=0, columnspan=2)
        self.cate_var.trace_add('write', self.cate_var_change)
        self.spend_var.trace_add("write", self.spend_var_change)

        self.add_button = tk.Button(self, text="Add", command=self.add_item)

        self.category_frame.pack(side="left")
        self.spend_frame.pack(side="left")
        self.add_button.pack(side="left")

    def cate_var_change(self, *args):
        self.spend_entry.delete(0, "end")
        self.spend_var.set("0")
        cate_id = self.cate_var.get()
        for slabel, price in zip(self.range_rbutton_list, self.data[cate_id]["range"]):
            slabel.config(value=price, text=format(price, ","))

    def spend_var_change(self, *args):
        p = self.spend_var.get()
        self.spend_entry.delete(0, "end")
        self.spend_entry.insert(0, format(p, ","))

    def add_item(self):
        cate_id = self.cate_var.get()
        cate = self.data[cate_id]["name"]
        spend = self.spend_var.get()
        self.parent.date_view_frame.insert([cate, spend, ""])
        self.spend_entry.delete(0, "end")


class MainApplication(tk.Frame):
    def __init__(self, *args, **kawrgs):
        super().__init__(*args, **kawrgs)
        self.date_view_frame = DateViewFrame(self)
        self.inserting_frame = InsertingFrame(self)

        self.date_view_frame.pack(fill="both", expand=True)
        self.inserting_frame.pack(fill="x", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1300x750")

    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(family="Roboto Regular", size=12, weight="normal")
    root.option_add("*Font", default_font)

    main = MainApplication(root)
    main.pack(fill="both", expand=True)
    root.mainloop()

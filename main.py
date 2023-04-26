from tkinter.simpledialog import askstring
import datasource
import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        self.command_menu = tk.Menu(self.menubar, tearoff=0)
        self.command_menu.add_command(
            label='用途查詢', command=self.menu_use_search_click)
        self.menubar.add_cascade(label='查詢', menu=self.command_menu)
        self.command_menu.add_command(
            label='地址查詢', command=self.menu_address_search_click)

        topFrame = ttk.LabelFrame(self,text='台北市行政區')
        length = len(datasource.area_list)
        self.radioStringVar = tk.StringVar()
        for i in range(length):
            cols = i % 3
            rows = i // 3
            ttk.Radiobutton(topFrame, text=datasource.area_list[i], value=datasource.area_list[i], variable=self.radioStringVar,command=self.radio_Event).grid(
                column=cols, row=rows, sticky=tk.W, padx=10, pady=10)
        topFrame.pack()

        self.radioStringVar.set('中山區')
        self.area_data = datasource.getInfoFromArea('中山區')

        self.bottomFrame = ttk.LabelFrame(self,text='中山區')
        self.bottomFrame.pack()

        columns = ('#1','#2','#3','#4','#5')
        self.tree = ttk.Treeview(self.bottomFrame, columns=columns,show='headings')
        self.tree.heading('#1',text='場地名稱')
        self.tree.column('#1',minwidth=0,width=150)
        self.tree.heading('#2',text='用途')
        self.tree.column('#2',minwidth=0,width=65)
        self.tree.heading('#3',text='地址')
        self.tree.column('#3',minwidth=0,width=300)
        self.tree.heading('#4',text='開放時間')
        self.tree.column('#4',minwidth=0,width=100)
        self.tree.heading('#5',text='結束時間')
        self.tree.column('#5',minwidth=0,width=100)
        self.tree.pack(side=tk.LEFT)

        for item in self.area_data:
            self.tree.insert('',tk.END,values=[item['Name'],item['SportType'],item['Address'],item['OpenTime'],item['CloseTime']])

        scrollbar = ttk.Scrollbar(self.bottomFrame,command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)

    def radio_Event(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        area_name = self.radioStringVar.get()
        self.area_data = datasource.getInfoFromArea(area_name)
        for item in self.area_data:
            self.tree.insert('',tk.END,values=[item['Name'],item['SportType'],item['Address'],item['OpenTime'],item['CloseTime']])

    def menu_use_search_click(self):
        retVal = askstring('用途搜尋', '請輸入用途名稱')
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.area_data:
            if retVal in item['SportType'] or retVal in item['Name']:
                self.tree.insert('',tk.END,values=[item['Name'],item['SportType'],item['Address'],item['OpenTime'],item['CloseTime']])

    def menu_address_search_click(self):
        retVal = askstring('地址搜尋', '請輸入地址')
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.area_data:
            if retVal in item['Address']:
                self.tree.insert('',tk.END,values=[item['Name'],item['SportType'],item['Address'],item['OpenTime'],item['CloseTime']])

def main():
    window = Window()
    window.title('台北市運動場地')
    window.mainloop()

if __name__ == '__main__':
    main()
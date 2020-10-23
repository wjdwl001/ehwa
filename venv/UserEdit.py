import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import uuid
import tkinter.font
import os
import tkcalendar
import pymysql
from tkinter import messagebox
from datetime import datetime
#color : #00462A #77E741

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.resizable(False,False)
        self.title("조선시대공예 DB입력기")

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class UserPage(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        val = ""
    self.master = master
    self.master.title("조선시대공예 DB입력기")
    self.pack(fill=tk.BOTH, expand=True)

    # 스크롤바
    super().__init__(master, *args, **kwargs)
    canvas = tk.Canvas(self, width=980, height=800)
    scrollbar = tkinter.Scrollbar(self, orient="vertical", command=canvas.yview)
    self.scrollable_frame = tk.Frame(canvas)

    self.scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(self.scrollable_frame, text="DB확인", bg="#00462A", width="100", height="3",
             fg="white",
             font=('맑은 고딕', 13)).pack()
    tk.Label(self.scrollable_frame, text="").pack()

def main():
    root = tk.Tk()
    root.geometry("1020x700+100+100")
    root.resizable(False,False)
    app = UserPage(root) 
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
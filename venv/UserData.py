import tkinter as tk
import tkinter.font
import tkinter.ttk
import pymysql

#color : #00462A #77E741

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(UserData)
        self.resizable(False,False)
        self.title("조선시대공예 DB입력기")

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class UserData(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self,master)
        val = ""
        self.master = master
        self.master.title("조선시대공예 DB입력기")
        self.pack(fill=tk.X, expand=True)


        tk.Label(self, text="입력 데이터 확인", bg="#00462A", width="100", height="3",
                 fg="white",
                 font=('맑은 고딕', 13)).pack(fill=tk.X)
        tk.Label(self, text="").pack()

        frame_treelist = tk.Frame(self, width = 800, height = 550)
        frame_treelist.pack()
        columns = ["고유번호", "색인어","정의"]
        treelist = [("1", "색인어1","임시1"), ("2", "색인어2", "임시2"), ("3", "색인어3", "임시3")
                    ,("1", "색인어1","임시1"), ("2", "색인어2", "임시2"), ("3", "색인어3", "임시3")
                    ,("1", "색인어1","임시1"), ("2", "색인어2", "임시2"), ("3", "색인어3", "임시3")
                    ,("1", "색인어1","임시1"), ("2", "색인어2", "임시2"), ("3", "색인어3", "임시3")
                    , ("1", "색인어1", "임시1"), ("2", "색인어2", "임시2"), ("3", "색인어3", "임시3")
                    , ("1", "색인어1", "임시1"), ("2", "색인어2", "임시2"), ("3", "색인어3", "임시3")
                    , ("1", "색인어1", "임시1"), ("2", "색인어2", "임시2"), ("3", "색인어3", "임시3")
                    , ("1", "색인어1", "임시1"), ("2", "색인어2", "임시2"), ("3", "색인어3", "임시3")
                    , ("1", "색인어1", "임시1"), ("2", "색인어2", "임시2"), ("3", "색인어3", "임시3")
                    , ("1", "색인어1", "임시1"), ("2", "색인어2", "임시2"), ("3", "색인어3", "임시3")
                    , ("1", "색인어1", "임시1"), ("2", "색인어2", "임시2"), ("3", "색인어3", "임시3")
                    , ("1", "색인어1", "임시1"), ("2", "색인어2", "임시2"), ("3", "색인어3", "임시3")]

        treeview = tkinter.ttk.Treeview(frame_treelist, columns=columns, show="headings", height=500, selectmode="browse")
        treeview.pack(side=tk.LEFT)

        vsb= tkinter.ttk.Scrollbar(frame_treelist, orient="vertical", command=treeview.yview)
        vsb.pack(side='right',fill='y')
        treeview.configure(yscrollcommand=vsb.set)

        treeview.column("#1", width = 100)
        treeview.column("#2", width = 200)
        treeview.column("#3", width = 500)
        treeview.heading("#1", text="고유번호")
        treeview.heading("#2", text="색인어")
        treeview.heading("#3", text="정의")

        for i in range(len(treelist)):
            treeview.insert('','end',text=i, values=treelist[i], iid=str(i)+"번")

def main():
    root = tk.Tk()
    root.geometry("1020x700+100+100")
    root.resizable(False,False)
    app = UserData(root)
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
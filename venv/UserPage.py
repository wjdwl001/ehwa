# import modules
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk
import tkinter.font
import os
import uuid

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
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master
        self.master.title("조선시대공예 DB입력기")
        self.pack(fill=tk.BOTH, expand=True)

        tk.Label(self, text="이화여자대학교 물질문화연구팀\n조선시대공예 DB입력기 #1", bg="#00462A", width="300", height="3", fg="white",
                 font=('맑은 고딕', 13)).pack()
        tk.Label(self, text="").pack()


        # 00. 상태
        frame00 = tk.Frame(self)
        frame00.pack(fill=tk.X)

        def check():
            val_state = ""
            if entry_state.get() == 1:
                val_state = "대상"
            if entry_state.get() == 2:
                val_state = "비대상"
            if entry_state.get() == 3:
                val_state = "보류"
            if entry_state.get() == 4:
                val_state = "삭제"

        entry_state = tk.IntVar()

        entry_state_subject = tk.Radiobutton(frame00, text = "대상", variable = entry_state, value=1)
        entry_state_nonsubject = tk.Radiobutton(frame00, text = "비대상", variable = entry_state, value=2)
        entry_state_defer = tk.Radiobutton(frame00, text = "보류", variable = entry_state, value=3)
        entry_state_delete = tk.Radiobutton(frame00, text = "삭제", variable = entry_state, value=4)

        entry_state_subject.select()
        entry_state_nonsubject.deselect()
        entry_state_defer.deselect()
        entry_state_delete.deselect()

        entry_state_delete.pack(side = tk.RIGHT, padx=10)
        entry_state_defer.pack(side = tk.RIGHT, padx=10)
        entry_state_nonsubject.pack(side = tk.RIGHT, padx=10)
        entry_state_subject.pack(side = tk.RIGHT,padx=10)
        action = tk.Button(frame00, text="확인", command=check)


        # 구분선
        canvas = tkinter.Canvas(self, height=10, width=1000)
        line = canvas.create_line(0, 10, 1000, 10, fill="#00462A")
        canvas.pack()


        # 저장
        frame = tk.Frame(self)
        frame.pack(side=tk.BOTTOM)
        btnSave = tk.Button(frame, text="저장")
        btnSave.pack(side=tk.LEFT, padx=10, pady=10)


        # 0. ID(고유번호)
        frame0 = tk.Frame(self)
        frame0.pack(fill=tk.X)

        lbl_ID = tk.Label(frame0, text="ID", width = 10)
        lbl_ID.pack(side=tk.LEFT, padx=10, pady=10)

        ID = uuid.uuid1()
        ID = ID.hex[0:10]

        entry_ID = tk.Text(frame0, width = 10, height=1)
        entry_ID.insert(1.0,ID)
        entry_ID.configure(state="disabled")
        entry_ID.pack(side=tk.LEFT,padx=10, pady=10)



        # 1.색인어(한글)
        frame1 = tk.Frame(self)
        frame1.pack(fill=tk.X)

        lbl_indexKorean = tk.Label(frame1, text="색인어(한글)", width=10)
        lbl_indexKorean.pack(side=tk.LEFT, padx=10, pady=10)

        entry_indexKorean = tk.Entry(frame1)
        entry_indexKorean.pack(side=tk.LEFT, padx=10)


        # 2. 색인어(한자)
        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.X)

        lbl_indexChinese = tk.Label(frame2, text="색인어(한자)", width=10)
        lbl_indexChinese.pack(side=tk.LEFT, padx=10, pady=10)

        entry_indexChinese = tk.Entry(frame2)
        entry_indexChinese.pack(side=tk.LEFT,padx=10)


        # 3. 이명
        frame3 = tk.Frame(self)
        frame3.pack(fill=tk.X)

        lbl_nickname = tk.Label(frame3, text="이명", width=10)
        lbl_nickname.pack(side=tk.LEFT, padx=10, pady=10)

        entry_nickname = tk.Entry(frame3)
        entry_nickname.pack(side=tk.LEFT, padx=10)


        # 4. 범칭
        frame4 = tk.Frame(self)
        frame4.pack(fill=tk.X)

        lbl_generalName = tk.Label(frame4, text="범칭", width=10)
        lbl_generalName.pack(side=tk.LEFT, padx=10, pady=10)

        entry_generalName = tk.Entry(frame4)
        entry_generalName.pack(side=tk.LEFT, padx=10)


        # 9. 대분류
        frame9 = tk.Frame(self)
        frame9.pack(fill=tk.X)

        values_detail = ["의궤", "실록", "승정원일기", "일성록", "전례서", "법전", "지리지", "등록", "발기", "유서류", "문집", "일기", "기타"]

        lbl_majorClass = tk.Label(frame9, text="대분류\n자료 유형별", width=10)
        lbl_majorClass.pack(side=tk.LEFT, padx=10, pady=10)

        drBox_majorClass = tkinter.ttk.Combobox(frame9, height=15, values=values_detail, state="readonly")
        drBox_majorClass.pack(side=tk.LEFT, pady=10, padx=10, expand=False)


        # 5. 중분류항목
        frame5 = tk.Frame(self)
        frame5.pack(fill=tk.X)

        array_middleClass = []
        def middleClass_array() :
            if entry_middleClass_product.get() :
                array_middleClass.append("제작품")
            if entry_middleClass_material.get() :
                array_middleClass.append("제작재료")
            if entry_middleClass_tool.get() :
                array_middleClass.append("제작도구")
            if entry_middleClass_producer.get() :
                array_middleClass.append("제작자")

        lbl_middleClass = tk.Label(frame5, text="중분류항목", width=10)
        lbl_middleClass.pack(side=tk.LEFT, padx=10, pady=10)

        entry_middleClass_product = tk.IntVar()
        entry_middleClass_material = tk.IntVar()
        entry_middleClass_tool = tk.IntVar()
        entry_middleClass_producer = tk.IntVar()

        entry_middleClass_product = tk.Checkbutton(frame5, text = "제작품", variable = entry_middleClass_product)
        entry_middleClass_material = tk.Checkbutton(frame5, text = "제작재료", variable = entry_middleClass_material)
        entry_middleClass_tool = tk.Checkbutton(frame5, text = "제작도구", variable = entry_middleClass_tool)
        entry_middleClass_producer = tk.Checkbutton(frame5, text = "제작자", variable = entry_middleClass_producer)

        entry_middleClass_product.deselect()

        entry_middleClass_product.pack(side = tk.LEFT,padx=10)
        entry_middleClass_material.pack(side = tk.LEFT, padx=10)
        entry_middleClass_tool.pack(side = tk.LEFT, padx=10)
        entry_middleClass_producer.pack(side = tk.LEFT, padx=10)


        # 6. 소분류항목
        frame6 = tk.Frame(self)
        frame6.pack(fill=tk.X)

        lbl_subClass = tk.Label(frame6, text="소분류항목", width=10)
        lbl_subClass.pack(side=tk.LEFT, padx=10, pady=10)

        array_subClass = []
        def subClass_array():
            if entry_subClass_metal.get():
                array_subClass.append("금속")
            if entry_subClass_wood.get():
                array_subClass.append("목재")
            if entry_middleClass_tool.get():
                array_middleClass.append("제작도구")
            if entry_middleClass_producer.get():
                array_middleClass.append("제작자")

        ckBox_subClass_metal = tk.IntVar()
        ckBox_subClass_wood = tk.IntVar()
        ckBox_subClass_rock = tk.IntVar()
        ckBox_subClass_fiber = tk.IntVar()
        ckBox_subClass_paper = tk.IntVar()
        ckBox_subClass_grain = tk.IntVar()
        ckBox_subClass_leather = tk.IntVar()
        ckBox_subClass_todo = tk.IntVar()
        ckBox_subClass_pigment = tk.IntVar()
        ckBox_subClass_etc = tk.IntVar()
        ckBox_subClass_multi = tk.IntVar()

        ckBox_subClass_metal = tk.Checkbutton(frame6, text="금속", variable=ckBox_subClass_metal)
        ckBox_subClass_wood = tk.Checkbutton(frame6, text="목재", variable=ckBox_subClass_wood)
        ckBox_subClass_rock = tk.Checkbutton(frame6, text="석제", variable=ckBox_subClass_rock)
        ckBox_subClass_fiber = tk.Checkbutton(frame6, text="섬유", variable=ckBox_subClass_fiber)
        ckBox_subClass_paper = tk.Checkbutton(frame6, text="지류", variable=ckBox_subClass_paper)
        ckBox_subClass_grain = tk.Checkbutton(frame6, text="초죽", variable=ckBox_subClass_grain)
        ckBox_subClass_leather = tk.Checkbutton(frame6, text="피모", variable=ckBox_subClass_leather)
        ckBox_subClass_todo = tk.Checkbutton(frame6, text="토도", variable=ckBox_subClass_todo)
        ckBox_subClass_pigment = tk.Checkbutton(frame6, text="안료", variable=ckBox_subClass_pigment)
        ckBox_subClass_etc = tk.Checkbutton(frame6, text="기타", variable=ckBox_subClass_etc)
        ckBox_subClass_multi = tk.Checkbutton(frame6, text="복합", variable=ckBox_subClass_multi)

        ckBox_subClass_metal.pack(fill=tk.X, side=tk.LEFT, padx=10, expand=True)
        ckBox_subClass_wood.pack(fill=tk.X, side=tk.LEFT, padx=10, expand=True)
        ckBox_subClass_rock.pack(fill=tk.X, side=tk.LEFT, padx=10, expand=True)
        ckBox_subClass_fiber.pack(fill=tk.X, side=tk.LEFT, padx=10, expand=True)
        ckBox_subClass_paper.pack(fill=tk.X, side=tk.LEFT, padx=10, expand=True)
        ckBox_subClass_grain.pack(fill=tk.X, side=tk.LEFT, padx=10, expand=True)
        ckBox_subClass_leather.pack(fill=tk.X, side=tk.LEFT, padx=10, expand=True)
        ckBox_subClass_todo.pack(fill=tk.X, side=tk.LEFT, padx=10, expand=True)
        ckBox_subClass_pigment.pack(fill=tk.X, side=tk.LEFT, padx=10, expand=True)
        ckBox_subClass_etc.pack(fill=tk.X, side=tk.LEFT, padx=10, expand=True)
        ckBox_subClass_multi.pack(fill=tk.X, side=tk.LEFT, padx=10, expand=True)


        # 7. 관련어
        frame7 = tk.Frame(self)
        frame7.pack(fill=tk.X)

        lbl_relatedWord = tk.Label(frame7, text="관련어", width=10)
        lbl_relatedWord.pack(side=tk.LEFT, padx=10, pady=10)

        entry_relatedWord = tk.Entry(frame7)
        entry_relatedWord.pack(side=tk.LEFT, padx=10)


        # 8. 상세정보
        frame8 = tk.Frame(self)
        frame8.pack(fill=tk.X)

        lbl_detail = tk.Label(frame8, text="상세정보", width=10)
        lbl_detail.pack(side=tk.LEFT, padx=10, pady=10)

        entry_detail = tk.Text(frame8)
        entry_detail.pack(fill=tk.X,padx=10,expand=True)




def main():
    root = tk.Tk()
    root.geometry("1000x700")
    root.resizable(False,False)
    app = UserPage(root)
    root.mainloop()

if __name__ == '__main__':
    main()


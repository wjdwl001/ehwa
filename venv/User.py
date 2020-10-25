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

#db접속 함수
def connect_db():
    mydb = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="",
        database="ehwa"
    )
    mc = mydb.cursor()
    return (mydb, mc)

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
        # 멤버변수
        val_username = ""  # 아이디
        val_password = ""  # 비밀번호
        val_state = ""  # 00. 상태
        val_ID = ""  # 0. ID(고유번호)
        val_indexKorean = ""  # 1. 색인어(한글)
        val_indexChinese = ""  # 2. 색인어(한자)
        val_nickname = ""  # 3. 이명
        val_generalName = ""  # 4. 범칭
        val_majorClass = ""  # 9. 대분류
        array_middleClass = []  # 5. 중분류항목
        array_subClass = []  # 6. 소분류항목
        val_relatedWord = ""  # 7. 관련어
        val_definition = ""  # 7-2. 정의
        val_detail = ""  # 8. 상세정보
        ############
        array_majorClass = []  # 9. 대분류 : ["자료1-대분류", "자료2-대분류" ,,,]
        array_referDoc = []  # 10. 자료원문 : ["자료1-자료원문", "자료2-자료원문" ,,,]
        array_refer = []  # 11. 출전 : [["자료1-한글", "자료1-한자", "자료1-저자", "자료1=저자활동시기" ,,,]["자료2-한글",,,],,,]
        array_entryPerson = []  # 12-1. 입력자 : [["자료1-입력자1","자료1-입력자2",,,],["자료2-입력자1","자료2-입력자2",,,,],,,]
        array_entryDate = []  # 12-2. 입력날짜   => 입력자와 동일
        array_inspecPerson = []  # 13-1. 검수자  => 입력자와 동일
        array_inspecDate = []  # 13-2. 검수날짜  => 입력자와 동일
        ############
        array_relic = [] #14. 유물 : [["유물1-분류", "유물1-이름",,,,],["유물2-분류", "유물2-이름",,,],,,]
        array_imageEntryPerson = [] #15-1. 이미지입력자
        array_imageEntryDate =[] #15-2. 이미지입력날짜
        array_imageInspecPerson = [] #16-1. 이미지검수자
        array_imageInspecDate = [] #16-2. 이미지 검수날짜
        ############
        val_note = ""  # 17. 비고


        def save():
            return

        #임시저장
        def save_temp():
            if entry_state.get() == 1:
                val_state = "대상"
            if entry_state.get() == 2:
                val_state = "비대상"
            if entry_state.get() == 3:
                val_state = "보류"
            if entry_state.get() == 4:
                val_state = "삭제"
            val_ID  # 0. ID(고유번호)
            val_indexKorean = indexKorean.get()  # 1. 색인어(한글)
            val_indexChinese = indexChinese.get()  # 2. 색인어(한자)
            val_nickname = nickname.get()  # 3. 이명
            val_generalName = generalName.get()  # 4. 범칭
            # 5. 중분류항목
            if entry_middleClass_product.get():
                array_middleClass.append("제작품")
            if entry_middleClass_material.get():
                array_middleClass.append("제작재료")
            if entry_middleClass_tool.get():
                array_middleClass.append("제작도구")
            if entry_middleClass_producer.get():
                array_middleClass.append("제작자")
            # 6. 소분류항목
            if entry_subClass_metal.get():
                array_subClass.append("금속")
            if entry_subClass_wood.get():
                array_subClass.append("목재")
            if entry_middleClass_tool.get():
                array_middleClass.append("제작도구")
            if entry_middleClass_producer.get():
                array_middleClass.append("제작자")
            # 7. 관련어
            val_relatedWord = relatedWord.get()
            # 7-2. 정의
            val_definition = definition.get()
            # 8. 상세정보
            val_detail = detail.get()
            # 9. 대분류
            array_majorClass.append(majorClass.get())
            #10. 자료원문
            array_referDoc.append(referDoc.get())
            #11. 출전
            array_refer_11(refer_korean.get())
            array_refer_11(refer_chinese.get())
            array_refer_11(refer_author.get())
            array_refer_11(refer_authorPeriod.get())
            array_refer_11(refer_publishPeriod.get())
            array_refer_11(refer_institurion.get())
            array_refer_11(refer_instInfo.get())
            array_refer.append(array_refer_11)
            #12. 입력자
            #13. 검수자
            # 17.비고
            val_note = note.get()


            mydb, mc = connect_db()
            sql = "INSERT INTO temp(대상, 고유번호, 색인어한글, 색인어한자, 이명, 범칭, 관련어, 상세정보, 대분류) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (val_state, val_ID, val_indexKorean, val_indexChinese, val_nickname, val_generalName, val_relatedWord, val_detail, val_majorClass)

            try:
                mc.execute(sql, val)
                mydb.commit()
                messagebox.showinfo("알림", "등록 완료!")
            except:
                messagebox.showinfo("알림", "입력에 실패했습니다!")


        #스크롤바
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


        #tkinter 화면 시작
        self.master = master
        self.master.title("조선시대공예 DB입력기")
        self.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.scrollable_frame, text="이화여자대학교 물질문화연구팀\n조선시대공예 DB입력기 #1", bg="#00462A", width="100", height="3", fg="white",
                 font=('맑은 고딕', 13)).pack()
        tk.Label(self.scrollable_frame, text="").pack()


        #임시저장버튼
        btnTempSave = tk.Button(master, text="임시저장", command=save_temp)
        btnTempSave.place(x=900,y=650)

        # 00. 상태
        frame00 = tk.Frame(self.scrollable_frame)
        frame00.pack(fill=tk.X)

        entry_state = tk.IntVar()

        entry_state_subject = tk.Radiobutton(frame00, text="대상", variable=entry_state, value=1)
        entry_state_nonsubject = tk.Radiobutton(frame00, text="비대상", variable=entry_state, value=2)
        entry_state_defer = tk.Radiobutton(frame00, text="보류", variable=entry_state, value=3)
        entry_state_delete = tk.Radiobutton(frame00, text="삭제", variable=entry_state, value=4)

        entry_state_subject.select()
        entry_state_nonsubject.deselect()
        entry_state_defer.deselect()
        entry_state_delete.deselect()

        entry_state_delete.pack(side=tk.RIGHT, padx=10)
        entry_state_defer.pack(side=tk.RIGHT, padx=10)
        entry_state_nonsubject.pack(side=tk.RIGHT, padx=10)
        entry_state_subject.pack(side=tk.RIGHT, padx=10)


        # 구분선
        canv = tk.Canvas(self.scrollable_frame, height=10, width=1000)
        line = canv.create_line(0, 10, 1000, 10, fill="#00462A")
        canv.pack()

        # 0. ID(고유번호)
        frame0 = tk.Frame(self.scrollable_frame)
        frame0.pack(fill=tk.X)

        val_ID = tk.StringVar()
        ID = uuid.uuid1()
        val_ID = ID.hex[0:9] #랜덤한 고유번호 16진수로 10자리로 만들었습니다

        lbl_ID = tk.Label(frame0, text="ID", width=10)
        lbl_ID.pack(side=tk.LEFT, padx=10, pady=10)


        entry_ID = tk.Text(frame0, width=10, height=1)
        entry_ID.insert(1.0, ID)
        entry_ID.configure(state="disabled")
        entry_ID.pack(side=tk.LEFT, padx=10, pady=10)

        # 1.색인어(한글)
        frame1 = tk.Frame(self.scrollable_frame)
        frame1.pack(fill=tk.X)

        indexKorean = tk.StringVar()

        lbl_indexKorean = tk.Label(frame1, text="색인어(한글)", width=10)
        lbl_indexKorean.pack(side=tk.LEFT, padx=10, pady=10)

        entry_indexKorean = tk.Entry(frame1, textvariable=indexKorean)
        entry_indexKorean.pack(side=tk.LEFT, padx=10)

        # 2. 색인어(한자)
        frame2 = tk.Frame(self.scrollable_frame)
        frame2.pack(fill=tk.X)

        indexChinese = tk.StringVar()

        lbl_indexChinese = tk.Label(frame2, text="색인어(한자)", width=10)
        lbl_indexChinese.pack(side=tk.LEFT, padx=10, pady=10)

        entry_indexChinese = tk.Entry(frame2, textvariable=indexChinese)
        entry_indexChinese.pack(side=tk.LEFT,padx=10)


        # 3. 이명
        frame3 = tk.Frame(self.scrollable_frame)
        frame3.pack(fill=tk.X)

        nickname = tk.StringVar()

        lbl_nickname = tk.Label(frame3, text="이명", width=10)
        lbl_nickname.pack(side=tk.LEFT, padx=10, pady=10)

        entry_nickname = tk.Entry(frame3, textvariable=nickname)
        entry_nickname.pack(side=tk.LEFT, padx=10)

        # 4. 범칭
        frame4 = tk.Frame(self.scrollable_frame)
        frame4.pack(fill=tk.X)

        generalName = tk.StringVar()

        lbl_generalName = tk.Label(frame4, text="범칭", width=10)
        lbl_generalName.pack(side=tk.LEFT, padx=10, pady=10)

        entry_generalName = tk.Entry(frame4, textvariable=generalName)
        entry_generalName.pack(side=tk.LEFT, padx=10)


        # 5. 중분류항목
        frame5 = tk.Frame(self.scrollable_frame)
        frame5.pack(fill=tk.X)

        lbl_middleClass = tk.Label(frame5, text="중분류항목", width=10)
        lbl_middleClass.pack(side=tk.LEFT, padx=10, pady=10)

        entry_middleClass_product = tk.IntVar()
        entry_middleClass_material = tk.IntVar()
        entry_middleClass_tool = tk.IntVar()
        entry_middleClass_producer = tk.IntVar()

        entry_middleClass_product = tk.Checkbutton(frame5, text="제작품", variable=entry_middleClass_product)
        entry_middleClass_material = tk.Checkbutton(frame5, text="제작재료", variable=entry_middleClass_material)
        entry_middleClass_tool = tk.Checkbutton(frame5, text="제작도구", variable=entry_middleClass_tool)
        entry_middleClass_producer = tk.Checkbutton(frame5, text="제작자", variable=entry_middleClass_producer)

        entry_middleClass_product.deselect()

        entry_middleClass_product.pack(side=tk.LEFT, padx=10)
        entry_middleClass_material.pack(side=tk.LEFT, padx=10)
        entry_middleClass_tool.pack(side=tk.LEFT, padx=10)
        entry_middleClass_producer.pack(side=tk.LEFT, padx=10)


        # 6. 소분류항목
        frame6 = tk.Frame(self.scrollable_frame)
        frame6.pack(fill=tk.X)

        lbl_subClass = tk.Label(frame6, text="소분류항목", width=10)
        lbl_subClass.pack(side=tk.LEFT, padx=10, pady=10)

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
        frame7 = tk.Frame(self.scrollable_frame)
        frame7.pack(fill=tk.X)

        relatedWord = tk.StringVar()

        lbl_relatedWord = tk.Label(frame7, text="관련어", width=10)
        lbl_relatedWord.pack(side=tk.LEFT, padx=10, pady=10)

        entry_relatedWord = tk.Entry(frame7, textvariable=relatedWord)
        entry_relatedWord.pack(side=tk.LEFT, padx=10)


        # 7-2. 정의
        frame7_2 = tk.Frame(self.scrollable_frame)
        frame7_2.pack(fill=tk.X)

        definition = tk.StringVar()

        lbl_definition = tk.Label(frame7_2, text="정의", width=10)
        lbl_definition.pack(side=tk.LEFT, padx=10, pady=10)

        entry_definition = tk.Entry(frame7_2, textvariable=definition)
        entry_definition.pack(side=tk.LEFT, padx=10)


        # 8. 상세정보
        frame8 = tk.Frame(self.scrollable_frame)
        frame8.pack(fill=tk.X, pady=10)

        detail = tk.StringVar()

        lbl_detail = tk.Label(frame8, text="상세정보", width=10)
        lbl_detail.pack(side=tk.LEFT, padx=10, pady=10)

        entry_detail = tk.Text(frame8)
        entry_detail.pack(fill=tk.X, padx=10, expand=True)


        #구분선
        canv = tk.Canvas(self.scrollable_frame, height=10, width=1000)
        line = canv.create_line(00, 10, 1000, 10, fill="#00462A")
        canv.pack()



        #자주색 부분-자료추가
        def AddFrame9():
            def Add_entryPerson():
                global num_entryPerson
                frame9_extra_12_extra = tk.Frame(frame9_extra_12)
                frame9_extra_12_extra.pack(fill=tk.X, padx=10)
                entryPerson = tk.StringVar()
                array_entryPerson_info = []
                array_entryPerson_info.append(entryPerson)
                lbl_entryPerson = tk.Label(frame9_extra_12, text="입력자", width=10).pack(side=tk.LEFT,padx=10)
                entry_entryPerson = tk.Entry(frame9_extra_12, textvariable = entryPerson).pack(side=tk.LEFT,padx=10)
                cal_entryPerson = tkcalendar.DateEntry(frame9_extra_12, width=12, background="#00462A",
                                                       foreground='white', borderwidth=2,
                                                       year=int(datetime.today().year),
                                                       month=int(datetime.today().month),
                                                       day=int(datetime.today().day)).pack(side=tk.LEFT, padx=10)
                entryDate = datetime.today().strftime("%Y%m%d")
                array_entryDate_info = []
                array_entryDate_info.append(entryDate)
                array_entryPerson.append(array_entryPerson_info)
                array_entryDate.append(array_entryDate_info)

            def Add_inspecPerson():
                frame9_extra_13_extra = tk.Frame(frame9_extra_13)
                frame9_extra_13_extra.pack(fill=tk.X, padx=10)
                inspecPerson = tk.StringVar()
                array_inspecPerson_info = []
                array_inspecPerson_info.append(inspecPerson)
                lbl_inspecPerson = tk.Label(frame9_extra_13, text="검수자", width=10).pack(side=tk.LEFT,padx=10)
                entry_inspecPerson = tk.Entry(frame9_extra_13, textvariable = inspecPerson).pack(side=tk.LEFT,padx=10)
                cal_inspecPerson = tkcalendar.DateEntry(frame9_extra_13, width=12, background="#00462A",
                                                        foreground='white', borderwidth=2,
                                                        year=int(datetime.today().year),
                                                        month=int(datetime.today().month),
                                                        day=int(datetime.today().day)).pack(side=tk.LEFT, padx=10)
                inspecDate = datetime.today().strftime("%Y%m%d")
                array_inspecDate_info = []
                array_inspecDate_info.append(inspecDate)
                array_inspecPerson.append(array_inspecPerson_info)
                array_inspecDate.append(array_inspecDate_info)



            frame9_extra = tk.Frame(frame9)
            frame9_extra.pack(fill=tk.X)
            #9. 대분류
            frame9_extra_9 = tk.Frame(frame9_extra)
            frame9_extra_9.pack(fill=tk.X, padx=10)
            majorClass = tk.StringVar()
            values_detail = ["의궤", "실록", "승정원일기", "일성록", "전례서", "법전", "지리지", "등록", "발기", "유서류", "문집", "일기", "기타"]
            lbl_majorClass = tk.Label(frame9_extra_9, textvariable=majorClass,text="대분류\n자료 유형별", width=10,padx=10)
            lbl_majorClass.pack(side=tk.LEFT, padx=10)
            drBox_majorClass = tk.ttk.Combobox(frame9_extra_9, height=15, values=values_detail,state="readonly")
            drBox_majorClass.current(0)
            drBox_majorClass.pack(side=tk.LEFT, pady=10, padx=10, expand=False)
            #10. 자료원문
            frame9_extra_10 = tk.Frame(frame9_extra)
            frame9_extra_10.pack(fill=tk.X, padx=10)
            referDoc = tk.StringVar()
            lbl_referDoc = tk.Label(frame9_extra_10, textvariable=referDoc, text="자료원문", width=10)
            lbl_referDoc.pack(side=tk.LEFT, padx=10, pady=10)
            entry_referDoc = tk.Text(frame9_extra_10)
            entry_referDoc.pack(fill=tk.X, padx=10, expand=True)
            #11. 출전
            frame9_extra_11 = tk.Frame(frame9_extra)
            frame9_extra_11.pack(fill=tk.X, padx=10)
            refer_korean = tk.StringVar()
            refer_chinese = tk.StringVar()
            refer_author = tk.StringVar()
            refer_authorPeriod = tk.StringVar()
            refer_publishPeriod = tk.StringVar()
            refer_institution = tk.StringVar()
            refer_instInfo = tk.StringVar()
            array_refer_info = []
            array_refer_info.append(refer_korean)
            array_refer_info.append(refer_chinese)
            array_refer_info.append(refer_author)
            array_refer_info.append(refer_authorPeriod)
            array_refer_info.append(refer_authorPeriod)
            array_refer_info.append(refer_institution)
            array_refer_info.append(refer_instInfo)
            empty = tk.Label(frame9_extra_11, text="", width=10)
            empty.grid(column="0", pady=5)
            lbl_refer = tk.Label(frame9_extra_11, text="출전", width=10).grid(column="0", row="4")
            lbl_refer_korean = tk.Label(frame9_extra_11, text="한글", width=20).grid(column="1", row="1")
            lbl_refer_chinese = tk.Label(frame9_extra_11, text="한자", width=20).grid(column="1", row="2")
            lbl_refer_author = tk.Label(frame9_extra_11, text="저자", width=20).grid(column="1", row="3")
            lbl_refer_authorPeriod = tk.Label(frame9_extra_11, text="저자활동시기", width=20).grid(column="1", row="4")
            lbl_refer_publishPeriod = tk.Label(frame9_extra_11, text="간행시기", width=20).grid(column="1", row="5")
            lbl_refer_institution = tk.Label(frame9_extra_11, text="텍스트소장처", width=20).grid(column="1", row="6")
            lbl_refer_instiInfo = tk.Label(frame9_extra_11, text="소장처번호/링크", width=20).grid(column="1", row="7")
            entry_refer_korean = tk.Entry(frame9_extra_11,textvariable=refer_korean).grid(column="2", row="1")
            entry_refer_chinese = tk.Entry(frame9_extra_11,textvariable=refer_chinese).grid(column="2", row="2")
            entry_refer_author = tk.Entry(frame9_extra_11,textvariable=refer_author).grid(column="2", row="3")
            entry_refer_authorPeriod = tk.Entry(frame9_extra_11,textvariable=refer_authorPeriod).grid(column="2", row="4")
            entry_refer_publishPeriod = tk.Entry(frame9_extra_11,textvariable=refer_publishPeriod).grid(column="2", row="5")
            entry_refer_institution = tk.Entry(frame9_extra_11,textvariable=refer_institution).grid(column="2", row="6")
            entry_refer_instInfo = tk.Entry(frame9_extra_11,textvariable=refer_instInfo).grid(column="2", row="7")
            tk.Label(frame9_extra_11).grid()
            #12. 입력자
            frame9_extra_12 = tk.Frame(frame9_extra)
            frame9_extra_12.pack(fill=tk.X, padx=10)
            button_entryPerson = tk.Button(frame9_extra_12, text="입력자 추가", command=Add_entryPerson)
            button_entryPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
            #13. 검수자
            frame9_extra_13 = tk.Frame(frame9_extra)
            frame9_extra_13.pack(fill=tk.X, padx=10)
            button_entryPerson = tk.Button(frame9_extra_13, text="검수자 추가", command=Add_inspecPerson)
            button_entryPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)


            array_majorClass.append(majorClass)
            array_referDoc.append(referDoc)
            array_refer.append(array_refer_info)


        # 9. 대분류
        # 10. 자료원문
        # 11. 출전
        # 12. 입력자
        # 13. 검수자

        #자료추가
        frame9 = tk.Frame(self.scrollable_frame)
        frame9.pack(fill=tk.X, expand=True)
        tk.Button(frame9,text="자료 추가",command=AddFrame9).pack(side=tk.TOP, anchor=tk.W,padx=10,pady=10)

        # 구분선
        canv = tk.Canvas(self.scrollable_frame, height=10, width=1000)
        line = canv.create_line(0, 10, 1000, 10, fill="#00462A")
        canv.pack()

        #하늘색부분-유물추가
        def AddFrame14():
            def Add_imagePerson():
                frame14_extra_15_extra = tk.Frame(frame14_extra_15)
                frame14_extra_15_extra.pack(fill=tk.X, side=tk.TOP,anchor=tk.W, padx=10)
                imageEntryPerson = tk.StringVar()
                array_imageEntryPerson_info = []
                array_imageEntryPerson_info.append(imageEntryPerson)
                lbl_imageEntryPerson = tk.Label(frame14_extra_15, text="입력자%s", width=10).pack(side=tk.LEFT, padx=10)
                entry_imageEntryPerson = tk.Entry(frame14_extra_15).pack(side=tk.LEFT, padx=10)
                cal_imageEntryPerson = tkcalendar.DateEntry(frame14_extra_15, width=12, background="#00462A",
                                                       foreground='white', borderwidth=2,
                                                       year=int(datetime.today().year),
                                                       month=int(datetime.today().month),
                                                       day=int(datetime.today().day)).pack(side=tk.LEFT, padx=10)
                imageEntryDate = datetime.today().strftime("%Y%m%d")
                array_imageEntryDate_info = []
                array_imageEntryDate_info.append(imageEntryDate)
                array_imageEntryPerson.append(array_imageEntryPerson_info)
                array_imageEntryDate.append(array_imageEntryDate_info)


            def Add_imageInspecPerson():
                frame14_extra_16_extra = tk.Frame(frame14_extra_16)
                frame14_extra_16_extra.pack(fill=tk.X, padx=10)
                imageInspecPerson = tk.StringVar()
                array_imageInspecPerson_info = []
                array_imageInspecPerson_info.append(imageInspecPerson)
                lbl_entryPerson = tk.Label(frame14_extra_16, text="검수자%s", width=10).pack(side=tk.LEFT, padx=10)
                entry_entryPerson = tk.Entry(frame14_extra_16).pack(side=tk.LEFT, padx=10)
                cal_entryPerson = tkcalendar.DateEntry(frame14_extra_16, width=12, background="#00462A",
                                                       foreground='white', borderwidth=2,
                                                       year=int(datetime.today().year),
                                                       month=int(datetime.today().month),
                                                       day=int(datetime.today().day)).pack(side=tk.LEFT, padx=10)
                imageInspecDate = datetime.today().strftime("%Y%m%d")
                array_imageInspecDate_info = []
                array_imageInspecDate_info.append(imageInspecDate)
                array_imageInspecPerson.append(array_imageInspecPerson_info)
                array_imageInspecDate.append(array_imageInspecDate_info)

            def Browser_relic_image():
                filename = filedialog.askopenfilename()

            frame14_extra = tk.Frame(frame14)
            frame14_extra.pack(fill=tk.X)
            #14. 유물
            #14-1. 유물-분류
            frame14_extra_14 = tk.Frame(frame14_extra)
            frame14_extra_14.pack(fill=tk.X, padx=10)
            lbl_relic=tk.Label(frame14_extra_14, text="유물", width=10).grid(column="0",row="4")
            lbl_relic_class = tk.Label(frame14_extra_14, text="분류", width=20).grid(column="1", row="1")
            frame_14_extra_14_frame = tk.Frame(frame14_extra_14).grid(column="2",row="1")
            entry_relic_class = tk.IntVar()
            entry_relic_class_1 = tk.Radiobutton(frame_14_extra_14_frame, text="전세", variable=entry_relic_class, value=1).pack(side=tk.LEFT)
            entry_relic_class_2 = tk.Radiobutton(frame_14_extra_14_frame, text="출토", variable=entry_relic_class,value=2).pack(side=tk.LEFT)
            entry_relic_class_3 = tk.Radiobutton(frame_14_extra_14_frame, text="도설", variable=entry_relic_class,value=3).pack(side=tk.LEFT)
            entry_relic_class_4 = tk.Radiobutton(frame_14_extra_14_frame, text="기타", variable=entry_relic_class,value=4).pack(side=tk.LEFT)
            val_relic_class = ""
            if entry_relic_class.get() == 1:
                val_relic_class = "전세"
            if entry_relic_class.get() == 2:
                val_relic_class = "출토"
            if entry_relic_class.get() == 3:
                val_relic_class = "도설"
            if entry_relic_class.get() == 4:
                val_relic_class = "기타"
            array_relic_info = []
            array_relic_info.append(val_relic_class)
            #14-2~8
            relic_name = tk.StringVar()
            relic_country = tk.StringVar()
            relic_period = tk.StringVar()
            relic_site = tk.StringVar()
            relic_sitePhone = tk.StringVar()
            relic_findSpot = tk.StringVar()
            relic_source = tk.StringVar()
            array_relic_info.append(relic_name)
            array_relic_info.append(relic_country)
            array_relic_info.append(relic_period)
            array_relic_info.append(relic_site)
            array_relic_info.append(relic_sitePhone)
            array_relic_info.append(relic_findSpot)
            array_relic_info.append(relic_source)
            lbl_relic_name = tk.Label(frame14_extra_14, text="명칭", width=20).grid(column="1", row="2")
            lbl_relic_country = tk.Label(frame14_extra_14, text="국명", width=20).grid(column="1", row="3")
            lbl_relic_period = tk.Label(frame14_extra_14, text="시기", width=20).grid(column="1", row="4")
            lbl_relic_site = tk.Label(frame14_extra_14, text="소장처", width=20).grid(column="1", row="5")
            lbl_relic_sitePhone = tk.Label(frame14_extra_14, text="소장처번호", width=20).grid(column="1", row="6")
            lbl_relic_findSpot = tk.Label(frame14_extra_14, text="출토지", width=20).grid(column="1", row="7")
            lbl_relic_source = tk.Label(frame14_extra_14, text="출전/출처", width=20).grid(column="1", row="8")
            lbl_relic_image = tk.Label(frame14_extra_14, text="이미지 첨부", width=20).grid(column="1", row="9")
            entry_relic_name = tk.Entry(frame14_extra_14, textvariable=relic_name).grid(column="2", row="2")
            entry_relic_country = tk.Entry(frame14_extra_14, textvariable=relic_country).grid(column="2", row="3")
            entry_relic_period = tk.Entry(frame14_extra_14, textvariable=relic_period).grid(column="2", row="4")
            entry_relic_site = tk.Entry(frame14_extra_14, textvariable=relic_site).grid(column="2", row="5")
            entry_relic_sitePhone = tk.Entry(frame14_extra_14, textvariable=relic_sitePhone).grid(column="2", row="6")
            entry_relic_findSpot = tk.Entry(frame14_extra_14, textvariable=relic_findSpot).grid(column="2", row="7")
            entry_relic_source = tk.Entry(frame14_extra_14, textvariable=relic_source).grid(column="2", row="8")
            entry_relic_image = tk.Button(frame14_extra_14, text="첨부파일", command=Browser_relic_image).grid(column="2", row="9")
            #15. 이미지입력자
            frame14_extra_15 = tk.Frame(frame14_extra)
            frame14_extra_15.pack(fill=tk.X, padx=10)
            button_entryPerson = tk.Button(frame14_extra_15, text="입력자 추가", command=Add_imagePerson)
            button_entryPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
            #16. 이미지검수자
            frame14_extra_16 = tk.Frame(frame14_extra)
            frame14_extra_16.pack(fill=tk.X, padx=10)
            button_entryPerson = tk.Button(frame14_extra_16, text="검수자 추가", command=Add_imageInspecPerson)
            button_entryPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

            array_relic.append(array_relic_info)

        # 유물추가
        frame14 = tk.Frame(self.scrollable_frame)
        frame14.pack(fill=tk.X)
        tk.Button(frame14, text="유물 추가", command=AddFrame14).pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

        #14. 유물
        #15. 이미지입력자
        #16. 이미지검수자

        #구분선
        canv = tk.Canvas(self.scrollable_frame, height=10, width=1000)
        line = canv.create_line(00, 10, 1000, 10, fill="#00462A")
        canv.pack()

        # 17. 비고
        frame17 = tk.Frame(self.scrollable_frame)
        frame17.pack(fill=tk.X, pady=20)

        note = tk.StringVar()

        lbl_note = tk.Label(frame17, text="비고", width=10)
        lbl_note.pack(side=tk.LEFT, padx=10, pady=10)

        entry_note = tk.Entry(frame17, textvariable=note)
        entry_note.pack(fill=tk.BOTH, padx=10, expand=True)

        # 구분선
        canv = tk.Canvas(self.scrollable_frame, height=10, width=1000)
        line = canv.create_line(0, 10, 1000, 10, fill="#00462A")
        canv.pack()

        # 저장
        frame = tk.Frame(self.scrollable_frame)
        frame.pack(side=tk.BOTTOM)
        btnSave = tk.Button(frame, text="저장", command=save_temp)
        btnSave.pack(side=tk.LEFT, padx=10, pady=10)



def main():
    root = tk.Tk()
    root.geometry("1020x700+100+100")
    root.resizable(False,False)
    app = UserPage(root)
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
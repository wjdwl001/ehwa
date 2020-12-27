import tkinter as tk
import tkinter.font
from tkinter import filedialog
import tkinter.ttk
import pymysql
import tkcalendar
from tkinter import messagebox
from datetime import datetime


# color : #00462A #77E741

def connect_db():
    mydb = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="",
        database="ehwa",
        charset='utf8'
    )
    mc = mydb.cursor()
    return (mydb, mc)


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(UserTemp)
        self.resizable(False, False)
        self.title("조선시대공예 DB입력기")

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class UserEdit(tk.Frame):
    refer = 0
    relic = 0
    num_entryPerson = []
    num_inspecPerson = []
    num_imageEntryPerson = []
    num_imageInspecPerson = []
    num_entryPerson.append(0)
    num_inspecPerson.append(0)
    num_imageEntryPerson.append(0)
    num_imageInspecPerson.append(0)

    def __init__(self, master, item, *args, **kwargs):
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

        tk.Label(self.scrollable_frame, text="이화여자대학교 물질문화연구팀\n조선시대공예 DB 수정", bg="#00462A", width="100",
                 height="3",
                 fg="white",
                 font=('맑은 고딕', 13)).pack()
        tk.Label(self.scrollable_frame, text="").pack()

        frame00 = tk.Frame(self.scrollable_frame)
        frame00.pack(fill=tk.X)

        # 멤버변수
        # val_username = par_id  # 아이디
        # val_password = par_password  # 비밀번호
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
        array_refer = []  # 9-11. 출전 : [["자료1-대분류", "자료1-자료원문", "자료1-한글", "자료1-한자", "자료1-저자", "자료1=저자활동시기" ,,,]["자료2-한글",,,],,,]
        array_refer_button = []
        real_array_refer = []
        array_entryPerson = []  # 12-1. 입력자 : [["자료1-입력자1","자료1-입력자2",,,],["자료2-입력자1","자료2-입력자2",,,,],,,]
        real_array_entryPerson = []
        array_entryDate = []  # 12-2. 입력날짜   => 입력자와 동일
        real_array_entryDate = []
        array_inspecPerson = []  # 13-1. 검수자  => 입력자와 동일
        real_array_inspecPerson = []
        array_inspecDate = []  # 13-2. 검수날짜  => 입력자와 동일
        real_array_inspecDate = []
        ############
        array_relic = []  # 14. 유물 : [["유물1-분류", "유물1-이름",,,,],["유물2-분류", "유물2-이름",,,],,,]
        array_relic_button = []
        real_array_relic = []
        array_imageEntryPerson = []  # 15-1. 이미지입력자
        real_array_imageEntryPerson = []
        array_imageEntryDate = []  # 15-2. 이미지입력날짜
        real_array_imageEntryDate = []
        array_imageInspecPerson = []  # 16-1. 이미지검수자
        real_array_imageInspecPerson = []
        array_imageInspecDate = []  # 16-2. 이미지 검수날짜
        real_array_imageInspecDate = []
        ############
        val_note = ""  # 17. 비고

        def check():
            if entry_indexKorean.get() == '': return False
            if entry_indexChinese.get() == '': return False  # 2. 색인어(한자)
            if entry_nickname.get() == '': return False  # 3. 이명
            if entry_generalName.get() == '': return False  # 4. 범칭
            if entry_relatedWord.get() == '': return False
            # 7-2. 정의
            if entry_definition.get() == '': return False
            # 8. 상세정보, 마지막 문자인 /n제거하기 위한 방법
            if entry_detail.get(1.0, tk.END + "-1c") == '': return False
            # 9-11. 자료
            for i in range(len(array_refer)):
                for e in array_refer[i]:
                    if e.get() == '': return False
            for i in range(len(array_relic)):
                for e in array_relic[i]:
                    if e.get() == '': return False

            for i in range(len(array_entryPerson)):
                for e in array_entryPerson[i]:
                    if e.get() == '': return False
            for i in range(len(array_inspecPerson)):
                for e in array_inspecPerson[i]:
                    if e.get() == '': return False

            for i in range(len(array_imageEntryPerson)):
                for e in array_imageEntryPerson[i]:
                    if e.get() == '': return False
            for i in range(len(array_imageInspecPerson)):
                for e in array_imageInspecPerson[i]:
                    if e.get() == '': return False

        def save():
            checkToSave = check()
            if checkToSave == False:
                messagebox.showinfo("알림", "빈칸이 존재합니다!")
                return

            if entry_state.get() == 1:
                val_state = "대상"
            if entry_state.get() == 2:
                val_state = "비대상"
            if entry_state.get() == 3:
                val_state = "보류"
            if entry_state.get() == 4:
                val_state = "삭제"
            val_ID  # 0. ID(고유번호)
            val_indexKorean = entry_indexKorean.get()  # 1. 색인어(한글)
            val_indexChinese = entry_indexChinese.get()  # 2. 색인어(한자)
            val_nickname = entry_nickname.get()  # 3. 이명
            val_generalName = entry_generalName.get()  # 4. 범칭
            # 5. 중분류항목
            if middleClass_product.get():
                array_middleClass.append("제작품")
            if middleClass_material.get():
                array_middleClass.append("제작재료")
            if middleClass_tool.get():
                array_middleClass.append("제작도구")
            if middleClass_producer.get():
                array_middleClass.append("제작자")
            # 6. 소분류항목
            if subClass_metal.get():
                array_subClass.append("금속")
            if subClass_wood.get():
                array_subClass.append("목재")
            if subClass_rock.get():
                array_subClass.append("석제")
            if subClass_fiber.get():
                array_subClass.append("섬유")
            if subClass_paper.get():
                array_subClass.append("지류")
            if subClass_grain.get():
                array_subClass.append("초죽")
            if subClass_leather.get():
                array_subClass.append("피모")
            if subClass_todo.get():
                array_subClass.append("토도")
            if subClass_pigment.get():
                array_subClass.append("안료")
            if subClass_etc.get():
                array_subClass.append("기타")
            if subClass_multi.get():
                array_subClass.append("복합")

            # 7. 관련어
            val_relatedWord = entry_relatedWord.get()
            # 7-2. 정의
            val_definition = entry_definition.get()
            # 8. 상세정보, 마지막 문자인 /n제거하기 위한 방법
            val_detail = entry_detail.get(1.0, tk.END + "-1c")
            # 9-11. 자료
            # 17.비고
            val_note = entry_note.get()

            for i in range(len(array_refer)):
                real_array_refer.append([e.get() for e in array_refer[i]])
            for i in range(len(array_relic)):
                real_array_relic.append([e.get() for e in array_relic[i]])

            for i in range(len(array_entryPerson)):
                real_array_entryPerson.append([e.get() for e in array_entryPerson[i]])
            for i in range(len(array_inspecPerson)):
                real_array_inspecPerson.append([e.get() for e in array_inspecPerson[i]])

            for i in range(len(array_imageEntryPerson)):
                real_array_imageEntryPerson.append([e.get() for e in array_imageEntryPerson[i]])
            for i in range(len(array_imageInspecPerson)):
                real_array_imageInspecPerson.append([e.get() for e in array_imageInspecPerson[i]])

            for i in range(len(array_entryDate)):
                real_array_entryDate.append([e.get_date() for e in array_entryDate[i]])
            for i in range(len(array_inspecDate)):
                real_array_inspecDate.append([e.get_date() for e in array_inspecDate[i]])

            for i in range(len(array_imageEntryDate)):
                real_array_imageEntryDate.append([e.get_date() for e in array_imageEntryDate[i]])
            for i in range(len(array_imageInspecDate)):
                real_array_imageInspecDate.append([e.get_date() for e in array_imageInspecDate[i]])

            mydb, mc = connect_db()

            sql1 = "INSERT INTO 조선시대공예정보(대상, 고유번호, 색인어한글, 색인어한자, 이명, 범칭, 관련어, 정의, 상세정보, 비고, userID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val1 = (val_state, val_ID, val_indexKorean, val_indexChinese, val_nickname, val_generalName, val_relatedWord, val_definition, val_detail, val_note, val_username)
            sql2 = "INSERT INTO 중분류항목(고유번호, 중분류) VALUES (%s, %s)"
            sql3 = "INSERT INTO 소분류항목(고유번호, 소분류) VALUES (%s, %s)"
            sql4 = "INSERT INTO 출전(대분류, 자료원문, 한글, 한자, 저자, 저자활동시기, 간행시기, 텍스트소장처, 소장처번호및링크, 고유번호) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql5 = "INSERT INTO 입력정보(입력자, 입력일, 고유번호, 출전한글) VALUES (%s, %s, %s, %s)"
            sql6 = "INSERT INTO 검수정보(검수자, 검수일, 고유번호, 출전한글) VALUES (%s, %s, %s, %s)"
            sql7 = "INSERT INTO 유물(분류, 명칭, 국명, 시기, 소장처, 소장처번호, 출토지, 출전및출처, 고유번호) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql8 = "INSERT INTO 이미지입력정보(입력자, 입력일, 고유번호, 유물명칭) VALUES (%s, %s, %s, %s)"
            sql9 = "INSERT INTO 이미지검수정보(검수자, 검수일, 고유번호, 유물명칭) VALUES (%s, %s, %s, %s)"

            try:
                mc.execute(sql1, val1)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "조선시대공예정보 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            try:
                for i in array_middleClass:
                    val2 = (val_ID, i)
                    mc.execute(sql2, val2)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "중분류항목 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            try:
                for i in array_subClass:
                    val3 = (val_ID, i)
                    mc.execute(sql3, val3)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "소분류항목 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            try:
                for i in real_array_refer:
                    val4 = i
                    val4.append(val_ID)
                    val4 = tuple(val4)
                    mc.execute(sql4, val4)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "출전 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            try:
                for i in range(0, len(real_array_refer)):
                    for j, k in zip(real_array_entryPerson[i], array_entryDate[i]):
                        val5 = (j, k.get_date(), val_ID, real_array_refer[i][2])
                        mc.execute(sql5, val5)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "입력정보 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            try:
                for i in range(0, len(real_array_refer)):
                    for l, m in zip(real_array_inspecPerson[i], array_inspecDate[i]):
                        val6 = (l, m.get_date(), val_ID, real_array_refer[i][2])
                        mc.execute(sql6, val6)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "검수정보 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            try:
                for i in real_array_relic:
                    val7 = i
                    val7.append(val_ID)
                    val7 = tuple(val7)
                    mc.execute(sql7, val7)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "유물 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            try:
                for i in range(0, len(real_array_relic)):
                    for j, k in zip(real_array_imageEntryPerson[i], real_array_imageEntryDate[i]):
                        val8 = (j, k, val_ID, real_array_relic[i][1])
                        mc.execute(sql8, val8)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "이미지입력정보 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            try:
                for i in range(0, len(real_array_relic)):
                    for l, m in zip(real_array_imageInspecPerson[i], real_array_imageInspecDate[i]):
                        val9 = (l, m, val_ID, real_array_relic[i][1])
                        mc.execute(sql9, val9)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "이미지검수정보 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            mydb.commit()

            del_sql1 = "DELETE FROM 임시입력정보 WHERE 고유번호=%s"
            del_sql2 = "DELETE FROM 임시검수정보 WHERE 고유번호=%s"
            del_sql3 = "DELETE FROM 임시이미지입력정보 WHERE 고유번호=%s"
            del_sql4 = "DELETE FROM 임시이미지검수정보 WHERE 고유번호=%s"
            del_sql5 = "DELETE FROM 임시유물 WHERE 고유번호=%s"
            del_sql6 = "DELETE FROM 임시소분류항목 WHERE 고유번호=%s"
            del_sql7 = "DELETE FROM 임시중분류항목 WHERE 고유번호=%s"
            del_sql8 = "DELETE FROM 임시출전 WHERE 고유번호=%s"
            del_sql9 = "DELETE FROM 임시조선시대공예정보 WHERE 고유번호=%s"
            mc.execute(del_sql1, val_ID)
            mc.execute(del_sql2, val_ID)
            mc.execute(del_sql3, val_ID)
            mc.execute(del_sql4, val_ID)
            mc.execute(del_sql5, val_ID)
            mc.execute(del_sql6, val_ID)
            mc.execute(del_sql7, val_ID)
            mc.execute(del_sql8, val_ID)
            mc.execute(del_sql9, val_ID)

            mydb.commit()
            messagebox.showinfo("알림", "임시정보 삭제 및 새 정보 등록 완료!")

        # item = 고유번호이므로 이 값을 기준으로 db불러오시면 됩니다
        mydb, mc = connect_db()
        sql1 = "select * from 임시조선시대공예정보 where 고유번호=%s"
        mc.execute(sql1, item)
        chosunList = mc.fetchall()

        entry_state = tk.IntVar()

        entry_state_subject = tk.Radiobutton(frame00, text="대상", variable=entry_state, value=1)
        entry_state_nonsubject = tk.Radiobutton(frame00, text="비대상", variable=entry_state, value=2)
        entry_state_defer = tk.Radiobutton(frame00, text="보류", variable=entry_state, value=3)
        entry_state_delete = tk.Radiobutton(frame00, text="삭제", variable=entry_state, value=4)

        entry_state_subject.deselect()
        entry_state_nonsubject.deselect()
        entry_state_defer.deselect()
        entry_state_delete.deselect()

        if (chosunList[0][0] == "대상"):
            entry_state_subject.select()
        elif (chosunList[0][0] == "비대상"):
            entry_state_nonsubject.select()
        elif (chosunList[0][0] == "보류"):
            entry_state_defer.select()
        elif (chosunList[0][0] == "삭제"):
            entry_state_delete.select()

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

        lbl_ID = tk.Label(frame0, text="ID", width=10)
        lbl_ID.pack(side=tk.LEFT, padx=10, pady=10)

        entry_ID = tk.Text(frame0, width=10, height=1)
        entry_ID.insert(1.0, item)
        entry_ID.configure(state="disabled")
        entry_ID.pack(side=tk.LEFT, padx=10, pady=10)

        # 1.색인어(한글)
        frame1 = tk.Frame(self.scrollable_frame)
        frame1.pack(fill=tk.X)

        lbl_indexKorean = tk.Label(frame1, text="색인어(한글)", width=10)
        lbl_indexKorean.pack(side=tk.LEFT, padx=10, pady=10)
        indexKorean = tk.StringVar()
        entry_indexKorean = tk.Entry(frame1, textvariable=indexKorean)
        entry_indexKorean.pack(side=tk.LEFT, padx=10)
        entry_indexKorean.insert(0, chosunList[0][2])

        # 2. 색인어(한자)
        frame2 = tk.Frame(self.scrollable_frame)
        frame2.pack(fill=tk.X)

        lbl_indexChinese = tk.Label(frame2, text="색인어(한자)", width=10)
        lbl_indexChinese.pack(side=tk.LEFT, padx=10, pady=10)
        indexChinese = tk.StringVar()
        entry_indexChinese = tk.Entry(frame2, textvariable=indexChinese)
        entry_indexChinese.pack(side=tk.LEFT, padx=10)
        entry_indexChinese.insert(0, chosunList[0][3])

        # 3. 이명
        frame3 = tk.Frame(self.scrollable_frame)
        frame3.pack(fill=tk.X)

        lbl_nickname = tk.Label(frame3, text="이명", width=10)
        lbl_nickname.pack(side=tk.LEFT, padx=10, pady=10)
        nickname = tk.StringVar()
        entry_nickname = tk.Entry(frame3, textvariable=nickname)
        entry_nickname.pack(side=tk.LEFT, padx=10)
        entry_nickname.insert(0, chosunList[0][4])

        # 4. 범칭
        frame4 = tk.Frame(self.scrollable_frame)
        frame4.pack(fill=tk.X)

        generalName = tk.StringVar()

        lbl_generalName = tk.Label(frame4, text="범칭", width=10)
        lbl_generalName.pack(side=tk.LEFT, padx=10, pady=10)

        entry_generalName = tk.Entry(frame4, textvariable=generalName)
        entry_generalName.pack(side=tk.LEFT, padx=10)
        entry_generalName.insert(0, chosunList[0][5])

        # 5. 중분류항목
        frame5 = tk.Frame(self.scrollable_frame)
        frame5.pack(fill=tk.X)

        lbl_middleClass = tk.Label(frame5, text="중분류항목", width=10)
        lbl_middleClass.pack(side=tk.LEFT, padx=10, pady=10)

        sql2 = "select * from 임시중분류항목 where 고유번호=%s"
        mc.execute(sql2, item)
        middleList = mc.fetchall()

        middleClass_product = tk.IntVar()
        middleClass_material = tk.IntVar()
        middleClass_tool = tk.IntVar()
        middleClass_producer = tk.IntVar()

        entry_middleClass_product = tk.Checkbutton(frame5, text="제작품", variable=middleClass_product)
        entry_middleClass_material = tk.Checkbutton(frame5, text="제작재료", variable=middleClass_material)
        entry_middleClass_tool = tk.Checkbutton(frame5, text="제작도구", variable=middleClass_tool)
        entry_middleClass_producer = tk.Checkbutton(frame5, text="제작자", variable=middleClass_producer)

        entry_middleClass_product.deselect()
        entry_middleClass_material.deselect()
        entry_middleClass_tool.deselect()
        entry_middleClass_producer.deselect()

        # 이런 방식으로 현재 데이터에 select/deselect 해주시면 됩니다
        for row in middleList:
            if row[1] == "제작품":
                entry_middleClass_product.select()
            elif row[1] == "제작재료":
                entry_middleClass_material.select()
            elif row[1] == "제작도구":
                entry_middleClass_tool.select()
            elif row[1] == "제작자":
                entry_middleClass_producer.select()

        entry_middleClass_product.pack(side=tk.LEFT, padx=10)
        entry_middleClass_material.pack(side=tk.LEFT, padx=10)
        entry_middleClass_tool.pack(side=tk.LEFT, padx=10)
        entry_middleClass_producer.pack(side=tk.LEFT, padx=10)

        # 6. 소분류항목
        frame6 = tk.Frame(self.scrollable_frame)
        frame6.pack(fill=tk.X)

        lbl_subClass = tk.Label(frame6, text="소분류항목", width=10)
        lbl_subClass.pack(side=tk.LEFT, padx=10, pady=10)

        sql3 = "select * from 임시소분류항목 where 고유번호=%s"
        mc.execute(sql3, item)
        subList = mc.fetchall()

        subClass_metal = tk.IntVar()
        subClass_wood = tk.IntVar()
        subClass_rock = tk.IntVar()
        subClass_fiber = tk.IntVar()
        subClass_paper = tk.IntVar()
        subClass_grain = tk.IntVar()
        subClass_leather = tk.IntVar()
        subClass_todo = tk.IntVar()
        subClass_pigment = tk.IntVar()
        subClass_etc = tk.IntVar()
        subClass_multi = tk.IntVar()

        ckBox_subClass_metal = tk.Checkbutton(frame6, text="금속", variable=subClass_metal)
        ckBox_subClass_wood = tk.Checkbutton(frame6, text="목재", variable=subClass_wood)
        ckBox_subClass_rock = tk.Checkbutton(frame6, text="석제", variable=subClass_rock)
        ckBox_subClass_fiber = tk.Checkbutton(frame6, text="섬유", variable=subClass_fiber)
        ckBox_subClass_paper = tk.Checkbutton(frame6, text="지류", variable=subClass_paper)
        ckBox_subClass_grain = tk.Checkbutton(frame6, text="초죽", variable=subClass_grain)
        ckBox_subClass_leather = tk.Checkbutton(frame6, text="피모", variable=subClass_leather)
        ckBox_subClass_todo = tk.Checkbutton(frame6, text="토도", variable=subClass_todo)
        ckBox_subClass_pigment = tk.Checkbutton(frame6, text="안료", variable=subClass_pigment)
        ckBox_subClass_etc = tk.Checkbutton(frame6, text="기타", variable=subClass_etc)
        ckBox_subClass_multi = tk.Checkbutton(frame6, text="복합", variable=subClass_multi)

        ckBox_subClass_metal.deselect()
        ckBox_subClass_wood.deselect()
        ckBox_subClass_rock.deselect()
        ckBox_subClass_fiber.deselect()
        ckBox_subClass_paper.deselect()
        ckBox_subClass_grain.deselect()
        ckBox_subClass_leather.deselect()
        ckBox_subClass_todo.deselect()
        ckBox_subClass_pigment.deselect()
        ckBox_subClass_etc.deselect()
        ckBox_subClass_multi.deselect()

        for row in subList:
            if row[1] == "금속":
                ckBox_subClass_metal.select()
            elif row[1] == "목재":
                ckBox_subClass_wood.select()
            elif row[1] == "석제":
                ckBox_subClass_rock.select()
            elif row[1] == "섬유":
                ckBox_subClass_fiber.select()
            elif row[1] == "지류":
                ckBox_subClass_paper.select()
            elif row[1] == "초죽":
                ckBox_subClass_grain.select()
            elif row[1] == "피모":
                ckBox_subClass_leather.select()
            elif row[1] == "토도":
                ckBox_subClass_todo.select()
            elif row[1] == "안료":
                ckBox_subClass_pigment.select()
            elif row[1] == "기타":
                ckBox_subClass_etc.select()
            elif row[1] == "복합":
                ckBox_subClass_multi.select()

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
        entry_relatedWord.insert(0, chosunList[0][6])

        # 7-2. 정의
        frame7_2 = tk.Frame(self.scrollable_frame)
        frame7_2.pack(fill=tk.X)

        definition = tk.StringVar()

        lbl_definition = tk.Label(frame7_2, text="정의", width=10)
        lbl_definition.pack(side=tk.LEFT, padx=10, pady=10)

        entry_definition = tk.Entry(frame7_2, textvariable=definition)
        entry_definition.pack(side=tk.LEFT, padx=10)
        entry_definition.insert(0, chosunList[0][7])

        # 8. 상세정보
        frame8 = tk.Frame(self.scrollable_frame)
        frame8.pack(fill=tk.X, pady=10)

        detail = tk.StringVar()

        lbl_detail = tk.Label(frame8, text="상세정보", width=10)
        lbl_detail.pack(side=tk.LEFT, padx=10, pady=10)

        entry_detail = tk.Text(frame8)
        entry_detail.insert(1.0, chosunList[0][8])
        entry_detail.pack(fill=tk.X, padx=10, expand=True)

        # 구분선
        canv = tk.Canvas(self.scrollable_frame, height=10, width=1000)
        line = canv.create_line(00, 10, 1000, 10, fill="#00462A")
        canv.pack()

        frame9 = tk.Frame(self.scrollable_frame)
        frame9.pack(fill=tk.X, padx=10)

        sql4 = "select * from 임시출전 where 고유번호=%s"
        mc.execute(sql4, item)
        referList = mc.fetchall()
        referList_length = len(referList)
        self.refer = referList_length

        # 자료 추가 함수
        def AddFrame9():
            self.refer += 1  # 만약 9번쨰 자료면 refer = 9
            self.num_entryPerson.append(0)
            self.num_inspecPerson.append(0)
            array_entryPerson.append([])
            array_entryDate.append([])
            array_inspecPerson.append([])
            array_inspecDate.append([])

            def Add_entryPerson(button):
                this_refer = self.refer  # 기존 저장해놓은 button들중 일치하는게 없으면 self.refer로
                for i in range(len(array_refer_button)):
                    if array_refer_button[i][0] == button:
                        this_refer = i + 1  # i번쨰에서 일치한다? -> 해당 버튼은 i+1번째 자료의 버튼
                self.num_entryPerson[this_refer] += 1
                frame9_extra_12_extra = tk.Frame(frame9_extra_12)
                frame9_extra_12_extra.pack(fill=tk.X, padx=10)
                lbl_entryPerson = tk.Label(frame9_extra_12_extra, text="입력자%s" % str(self.num_entryPerson[this_refer]),
                                           width=10).pack(side=tk.LEFT, padx=10)
                entry_entryPerson = tk.Entry(frame9_extra_12_extra)
                entry_entryPerson.pack(side=tk.LEFT, padx=10)
                cal_entryPerson = tkcalendar.DateEntry(frame9_extra_12_extra, width=12, background="#00462A",
                                                       foreground='white', borderwidth=2,
                                                       year=int(datetime.today().year),
                                                       month=int(datetime.today().month),
                                                       day=int(datetime.today().day))
                cal_entryPerson.pack(side=tk.LEFT, padx=10)
                array_entryPerson[this_refer - 1].append(entry_entryPerson)
                array_entryDate[this_refer - 1].append(cal_entryPerson)

            def Add_inspecPerson(button):
                this_refer = self.refer
                for i in range(len(array_refer_button)):
                    if array_refer_button[i][1] == button:
                        this_refer = i + 1
                self.num_inspecPerson[this_refer] += 1
                frame9_extra_13_extra = tk.Frame(frame9_extra_13)
                frame9_extra_13_extra.pack(fill=tk.X, padx=10)
                lbl_inspecPerson = tk.Label(frame9_extra_13_extra,
                                            text="검수자%s" % str(self.num_inspecPerson[this_refer]), width=10).pack(
                    side=tk.LEFT, padx=10)
                entry_inspecPerson = tk.Entry(frame9_extra_13_extra)
                entry_inspecPerson.pack(side=tk.LEFT, padx=10)
                cal_inspecPerson = tkcalendar.DateEntry(frame9_extra_13_extra, width=12, background="#00462A",
                                                        foreground='white', borderwidth=2,
                                                        year=int(datetime.today().year),
                                                        month=int(datetime.today().month),
                                                        day=int(datetime.today().day))
                cal_inspecPerson.pack(side=tk.LEFT, padx=10)
                array_inspecPerson[this_refer - 1].append(entry_inspecPerson)
                array_inspecDate[this_refer - 1].append(cal_inspecPerson)

            array_refer_new = []
            array_refer_button_new = []
            frame9_extra = tk.Frame(frame9_dynamic)
            frame9_extra.pack(fill=tk.X)
            tk.Label(frame9_extra, text="자료%s" % str(self.refer), bg="#00462A", fg="white").pack(side=tk.TOP,
                                                                                                 anchor=tk.W, padx=10,
                                                                                                 pady=10)
            # 9. 대분류
            frame9_extra_9 = tk.Frame(frame9_extra)
            frame9_extra_9.pack(fill=tk.X, padx=10)
            values_detail = ["의궤", "실록", "승정원일기", "일성록", "전례서", "법전", "지리지", "등록", "발기", "유서류", "문집", "일기", "기타"]
            lbl_majorClass = tk.Label(frame9_extra_9, text="대분류\n자료 유형별", width=10, padx=10)
            lbl_majorClass.pack(side=tk.LEFT, padx=10)
            drBox_majorClass = tk.ttk.Combobox(frame9_extra_9, height=15, values=values_detail, state="readonly")
            drBox_majorClass.current(0)
            drBox_majorClass.pack(side=tk.LEFT, pady=10, padx=10, expand=False)
            array_refer_new.append(drBox_majorClass)
            # 10. 자료원문
            frame9_extra_10 = tk.Frame(frame9_extra)
            frame9_extra_10.pack(fill=tk.X, padx=10)
            lbl_referDoc = tk.Label(frame9_extra_10, text="자료원문", width=10)
            lbl_referDoc.pack(side=tk.LEFT, padx=10, pady=10)
            entry_referDoc = tk.Entry(frame9_extra_10)
            entry_referDoc.pack(fill=tk.X, padx=10, expand=True)
            array_refer_new.append(entry_referDoc)
            # 11. 출전
            frame9_extra_11 = tk.Frame(frame9_extra)
            frame9_extra_11.pack(fill=tk.X, padx=10)
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
            entry_refer_korean = tk.Entry(frame9_extra_11)
            entry_refer_korean.grid(column="2", row="1")
            entry_refer_chinese = tk.Entry(frame9_extra_11)
            entry_refer_chinese.grid(column="2", row="2")
            entry_refer_author = tk.Entry(frame9_extra_11)
            entry_refer_author.grid(column="2", row="3")
            entry_refer_authorPeriod = tk.Entry(frame9_extra_11)
            entry_refer_authorPeriod.grid(column="2", row="4")
            entry_refer_publishPeriod = tk.Entry(frame9_extra_11)
            entry_refer_publishPeriod.grid(column="2", row="5")
            entry_refer_institution = tk.Entry(frame9_extra_11)
            entry_refer_institution.grid(column="2", row="6")
            entry_refer_instInfo = tk.Entry(frame9_extra_11)
            entry_refer_instInfo.grid(column="2", row="7")
            array_refer_new.append(entry_refer_korean)
            array_refer_new.append(entry_refer_chinese)
            array_refer_new.append(entry_refer_author)
            array_refer_new.append(entry_refer_authorPeriod)
            array_refer_new.append(entry_refer_publishPeriod)
            array_refer_new.append(entry_refer_institution)
            array_refer_new.append(entry_refer_instInfo)
            tk.Label(frame9_extra_11).grid()
            # 12. 입력자
            frame9_extra_12 = tk.Frame(frame9_extra)
            frame9_extra_12.pack(fill=tk.X, padx=10)
            button_entryPerson = tk.Button(frame9_extra_12, text="입력자 추가",
                                           command=lambda: Add_entryPerson(button_entryPerson))
            button_entryPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
            array_refer_button_new.append(button_entryPerson)
            # 13. 검수자
            frame9_extra_13 = tk.Frame(frame9_extra)
            frame9_extra_13.pack(fill=tk.X, padx=10)
            button_inspecPerson = tk.Button(frame9_extra_13, text="검수자 추가",
                                            command=lambda: Add_inspecPerson(button_inspecPerson))
            button_inspecPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
            array_refer_button_new.append(button_inspecPerson)

            array_refer_button.append(array_refer_button_new)
            array_refer.append(array_refer_new)

            canv = tk.Canvas(frame9_extra, height=10, width=1000)
            line = canv.create_line(00, 10, 1000, 10, fill="#00462A")
            canv.pack()

        # 기존 자료 데이터
        for i in range(0, referList_length):
            frame9_extra = tk.Frame(frame9)
            frame9_extra.pack(fill=tk.X)
            tk.Label(frame9_extra, text="자료%s" % str(i + 1), bg="#00462A", fg="white").pack(side=tk.TOP, anchor=tk.W,
                                                                                            pady=10)
            # 9. 대분류
            frame9_extra_9 = tk.Frame(frame9_extra)
            frame9_extra_9.pack(fill=tk.X, padx=10)
            values_detail = ["의궤", "실록", "승정원일기", "일성록", "전례서", "법전", "지리지", "등록", "발기", "유서류", "문집", "일기", "기타"]
            lbl_majorClass = tk.Label(frame9_extra_9, text="대분류\n자료 유형별", width=10, padx=10)
            lbl_majorClass.pack(side=tk.LEFT, padx=10)
            drBox_majorClass = tk.ttk.Combobox(frame9_extra_9, height=15, values=values_detail, state="readonly")

            majorClass_index = 0
            for index, value in enumerate(values_detail):
                if (value == referList[i][0]): majorClass_index = index
            drBox_majorClass.current(majorClass_index)
            drBox_majorClass.pack(side=tk.LEFT, pady=10, padx=10, expand=False)

            # 10. 자료원문
            frame9_extra_10 = tk.Frame(frame9_extra)
            frame9_extra_10.pack(fill=tk.X, padx=10)
            lbl_referDoc = tk.Label(frame9_extra_10, text="자료원문", width=10)
            lbl_referDoc.pack(side=tk.LEFT, padx=10, pady=10)
            entry_referDoc = tk.Entry(frame9_extra_10)
            entry_referDoc.insert(0, referList[i][1])
            entry_referDoc.pack(fill=tk.X, padx=10, expand=True)
            # 11. 출전
            frame9_extra_11 = tk.Frame(frame9_extra)
            frame9_extra_11.pack(fill=tk.X, padx=10)
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
            entry_refer_korean = tk.Entry(frame9_extra_11)
            entry_refer_korean.grid(column="2", row="1")
            entry_refer_korean.insert(0, referList[i][2])

            entry_refer_chinese = tk.Entry(frame9_extra_11)
            entry_refer_chinese.grid(column="2", row="2")
            entry_refer_chinese.insert(0, referList[i][3])

            entry_refer_author = tk.Entry(frame9_extra_11)
            entry_refer_author.grid(column="2", row="3")
            entry_refer_author.insert(0, referList[i][4])

            entry_refer_authorPeriod = tk.Entry(frame9_extra_11)
            entry_refer_authorPeriod.grid(column="2", row="4")
            entry_refer_authorPeriod.insert(0, referList[i][5])

            entry_refer_publishPeriod = tk.Entry(frame9_extra_11)
            entry_refer_publishPeriod.grid(column="2", row="5")
            entry_refer_publishPeriod.insert(0, referList[i][6])

            entry_refer_institution = tk.Entry(frame9_extra_11)
            entry_refer_institution.grid(column="2", row="6")
            entry_refer_institution.insert(0, referList[i][7])

            entry_refer_instInfo = tk.Entry(frame9_extra_11)
            entry_refer_instInfo.grid(column="2", row="7")
            entry_refer_instInfo.insert(0, referList[i][8])

            tk.Label(frame9_extra_11).grid()
            # 12. 입력자
            frame9_extra_12 = tk.Frame(frame9_extra)
            frame9_extra_12.pack(fill=tk.X, padx=10)
            # 이부분 range 안에 각 자료에 대한 입력자 수 불러오기

            sql6 = "select * from 임시입력정보 where 고유번호=%s and 출전한글=%s"
            referIndexKorean = referList[i][2]
            val6 = (item, referIndexKorean)
            mc.execute(sql6, val6)
            entryList = mc.fetchall()
            entryList_length = len(entryList)

            for n in range(entryList_length):
                frame9_extra_12_extra = tk.Frame(frame9_extra_12)
                frame9_extra_12_extra.pack(fill=tk.X, padx=10)
                lbl_entryPerson = tk.Label(frame9_extra_12_extra, text="입력자%s" % str(n + 1),
                                           width=10).pack(side=tk.LEFT, padx=10)
                entry_entryPerson = tk.Entry(frame9_extra_12_extra)
                entry_entryPerson.pack(side=tk.LEFT, padx=10)
                entry_entryPerson.insert(0, entryList[n][0])
                cal_entryPerson = tkcalendar.DateEntry(frame9_extra_12_extra, width=12, background="#00462A",
                                                       foreground='white', borderwidth=2,
                                                       year=int(entryList[n][1].year),
                                                       month=int(entryList[n][1].month),
                                                       day=int(entryList[n][1].day))
                cal_entryPerson.pack(side=tk.LEFT, padx=10)
            button_entryPerson = tk.Button(frame9_extra_12, text="입력자 추가")
            button_entryPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

            # 13. 검수자
            frame9_extra_13 = tk.Frame(frame9_extra)
            frame9_extra_13.pack(fill=tk.X, padx=10)

            # 이부분 range 안에 각 자료에 대한 검수자 수 불러오기
            sql7 = "select * from 임시검수정보 where 고유번호=%s and 출전한글=%s"
            val7 = (item, referIndexKorean)
            mc.execute(sql7, val7)
            inspecList = mc.fetchall()
            inspecList_length = len(inspecList)

            for n in range(inspecList_length):
                frame9_extra_13_extra = tk.Frame(frame9_extra_13)
                frame9_extra_13_extra.pack(fill=tk.X, padx=10)
                lbl_inspecPerson = tk.Label(frame9_extra_13_extra, text="검수자%s" % str(n + 1),
                                            width=10).pack(side=tk.LEFT, padx=10)
                entry_inspecPerson = tk.Entry(frame9_extra_13_extra)
                entry_inspecPerson.pack(side=tk.LEFT, padx=10)
                entry_inspecPerson.insert(0, inspecList[n][0])
                cal_inspecPerson = tkcalendar.DateEntry(frame9_extra_13_extra, width=12, background="#00462A",
                                                        foreground='white', borderwidth=2,
                                                        year=int(inspecList[n][1].year),
                                                        month=int(inspecList[n][1].month),
                                                        day=int(inspecList[n][1].day))
                cal_inspecPerson.pack(side=tk.LEFT, padx=10)
            button_inspecPerson = tk.Button(frame9_extra_13, text="검수자 추가")
            button_inspecPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

            # 구분선
            canv = tk.Canvas(frame9_extra, height=10, width=1000)
            line = canv.create_line(00, 10, 1000, 10, fill="#00462A")
            canv.pack()

        # 자료 추가 버튼
        frame9 = tk.Frame(self.scrollable_frame)
        frame9_dynamic = tk.Frame(frame9)
        frame9_dynamic.pack(fill=tk.X, expand=True)
        frame9.pack(fill=tk.X, expand=True)
        tk.Button(frame9, text="자료 추가", command=AddFrame9).pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

        sql5 = "select * from 임시유물 where 고유번호=%s"
        mc.execute(sql5, item)
        relicList = mc.fetchall()
        relicList_length = len(relicList)
        self.relic = relicList_length

        # 유물 추가 함수
        def AddFrame14():
            self.relic += 1
            self.num_imageEntryPerson.append(0)
            self.num_imageInspecPerson.append(0)
            array_imageEntryPerson.append([])
            array_imageEntryDate.append([])
            array_imageInspecPerson.append([])
            array_imageInspecDate.append([])

            def Add_imagePerson(button):
                this_relic = self.relic  # 기존 저장해놓은 button들중 일치하는게 없으면 self.refer로
                for i in range(len(array_relic_button)):
                    if array_relic_button[i][0] == button:
                        this_relic = i + 1  # i번쨰에서 일치한다? -> 해당 버튼은 i+1번째 자료의 버튼

                self.num_imageEntryPerson[this_relic] += 1
                frame14_extra_15_extra = tk.Frame(frame14_extra_15)
                frame14_extra_15_extra.pack(side=tk.TOP, anchor=tk.W, padx=10)
                lbl_imageEntryPerson = tk.Label(frame14_extra_15_extra,
                                                text="입력자%s" % str(self.num_imageEntryPerson[this_relic]),
                                                width=10).pack(side=tk.LEFT, padx=10)
                entry_imageEntryPerson = tk.Entry(frame14_extra_15_extra)
                entry_imageEntryPerson.pack(side=tk.LEFT, padx=10)
                cal_imageEntryPerson = tkcalendar.DateEntry(frame14_extra_15_extra, width=12, background="#00462A",
                                                            foreground='white', borderwidth=2,
                                                            year=int(datetime.today().year),
                                                            month=int(datetime.today().month),
                                                            day=int(datetime.today().day))
                cal_imageEntryPerson.pack(side=tk.LEFT, padx=10)
                imageEntryDate = datetime.today().strftime("%Y%m%d")
                array_imageEntryPerson[this_relic - 1].append(entry_imageEntryPerson)
                array_imageEntryDate[this_relic - 1].append(cal_imageEntryPerson)

            def Add_imageInspecPerson(button):
                this_relic = self.relic  # 기존 저장해놓은 button들중 일치하는게 없으면 self.refer로
                for i in range(len(array_relic_button)):
                    if array_relic_button[i][1] == button:
                        this_relic = i + 1  # i번쨰에서 일치한다? -> 해당 버튼은 i+1번째 자료의 버튼

                self.num_imageInspecPerson[this_relic] += 1
                frame14_extra_16_extra = tk.Frame(frame14_extra_16)
                frame14_extra_16_extra.pack(fill=tk.X, padx=10)
                lbl_entryPerson = tk.Label(frame14_extra_16_extra,
                                           text="검수자%s" % str(self.num_imageInspecPerson[this_relic]), width=10).pack(
                    side=tk.LEFT, padx=10)
                entry_imageInspecPerson = tk.Entry(frame14_extra_16_extra)
                entry_imageInspecPerson.pack(side=tk.LEFT, padx=10)
                cal_imageInspecPerson = tkcalendar.DateEntry(frame14_extra_16_extra, width=12, background="#00462A",
                                                             foreground='white', borderwidth=2,
                                                             year=int(datetime.today().year),
                                                             month=int(datetime.today().month),
                                                             day=int(datetime.today().day))
                cal_imageInspecPerson.pack(side=tk.LEFT, padx=10)
                array_imageInspecPerson[this_relic - 1].append(entry_imageInspecPerson)
                array_imageInspecDate[this_relic - 1].append(cal_imageInspecPerson)

            def Browser_relic_image():
                filename = filedialog.askopenfilename()

            array_relic_new = []
            array_relic_button_new = []
            frame14_extra = tk.Frame(frame14_dynamic)
            frame14_extra.pack(fill=tk.X)
            tk.Label(frame14_extra, text="유물%s" % str(self.relic), bg="#00462A", fg="white").pack(side=tk.TOP,
                                                                                                  anchor=tk.W, padx=10,
                                                                                                  pady=10)
            # 14. 유물
            # 14-1. 유물-분류
            frame14_extra_14 = tk.Frame(frame14_extra)
            frame14_extra_14.pack(fill=tk.X, padx=10)
            lbl_relic = tk.Label(frame14_extra_14, text="유물", width=10).grid(column="0", row="4")
            lbl_relic_class = tk.Label(frame14_extra_14, text="분류", width=20).grid(column="1", row="1")
            frame_14_extra_14_frame = tk.Frame(frame14_extra_14).grid(column="2", row="1")
            values_relic_class = ["전세", "출토", "도설", "기타"]
            drBox_relic_class = tk.ttk.Combobox(frame14_extra_14, height=15, width=15, values=values_relic_class,
                                                state="readonly")
            drBox_relic_class.grid(column="2", row="1")
            drBox_relic_class.current(0)
            # 14-2~8
            lbl_relic_name = tk.Label(frame14_extra_14, text="명칭", width=20).grid(column="1", row="2")
            lbl_relic_country = tk.Label(frame14_extra_14, text="국명", width=20).grid(column="1", row="3")
            lbl_relic_period = tk.Label(frame14_extra_14, text="시기", width=20).grid(column="1", row="4")
            lbl_relic_site = tk.Label(frame14_extra_14, text="소장처", width=20).grid(column="1", row="5")
            lbl_relic_sitePhone = tk.Label(frame14_extra_14, text="소장처번호", width=20).grid(column="1", row="6")
            lbl_relic_findSpot = tk.Label(frame14_extra_14, text="출토지", width=20).grid(column="1", row="7")
            lbl_relic_source = tk.Label(frame14_extra_14, text="출전/출처", width=20).grid(column="1", row="8")
            lbl_relic_image = tk.Label(frame14_extra_14, text="이미지 첨부", width=20).grid(column="1", row="9")
            entry_relic_name = tk.Entry(frame14_extra_14)
            entry_relic_name.grid(column="2", row="2")
            entry_relic_country = tk.Entry(frame14_extra_14)
            entry_relic_country.grid(column="2", row="3")
            entry_relic_period = tk.Entry(frame14_extra_14)
            entry_relic_period.grid(column="2", row="4")
            entry_relic_site = tk.Entry(frame14_extra_14)
            entry_relic_site.grid(column="2", row="5")
            entry_relic_sitePhone = tk.Entry(frame14_extra_14)
            entry_relic_sitePhone.grid(column="2", row="6")
            entry_relic_findSpot = tk.Entry(frame14_extra_14)
            entry_relic_findSpot.grid(column="2", row="7")
            entry_relic_source = tk.Entry(frame14_extra_14)
            entry_relic_source.grid(column="2", row="8")
            entry_relic_image = tk.Button(frame14_extra_14, text="첨부파일", command=Browser_relic_image)
            entry_relic_image.grid(column="2", row="9")
            array_relic_new.append(drBox_relic_class)
            array_relic_new.append(entry_relic_name)
            array_relic_new.append(entry_relic_country)
            array_relic_new.append(entry_relic_period)
            array_relic_new.append(entry_relic_site)
            array_relic_new.append(entry_relic_sitePhone)
            array_relic_new.append(entry_relic_findSpot)
            array_relic_new.append(entry_relic_source)
            # 15. 이미지입력자
            frame14_extra_15 = tk.Frame(frame14_extra)
            frame14_extra_15.pack(fill=tk.X, padx=10)
            button_imageEntryPerson = tk.Button(frame14_extra_15, text="입력자 추가",
                                                command=lambda: Add_imagePerson(button_imageEntryPerson))
            button_imageEntryPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
            array_relic_button_new.append(button_imageEntryPerson)
            # 16. 이미지검수자
            frame14_extra_16 = tk.Frame(frame14_extra)
            frame14_extra_16.pack(fill=tk.X, padx=10)
            button_imageInspecPerson = tk.Button(frame14_extra_16, text="검수자 추가",
                                                 command=lambda: Add_imageInspecPerson(button_imageInspecPerson))
            button_imageInspecPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
            array_relic_button_new.append(button_imageInspecPerson)

            array_relic.append(array_relic_new)
            array_relic_button.append(array_relic_button_new)

            canv = tk.Canvas(frame14_extra, height=10, width=1000)
            line = canv.create_line(0, 10, 1000, 10, fill="#00462A")
            canv.pack()

        frame14 = tk.Frame(self.scrollable_frame)
        frame14.pack(fill=tk.X, expand=True)
        frame14_dynamic = tk.Frame(frame14)
        frame14_dynamic.pack(fill=tk.X, expand=True)
        tk.Button(frame14, text="유물 추가", command=AddFrame14).pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
        frame14_extra = tk.Frame(frame14_dynamic)
        frame14_extra.pack(fill=tk.X)

        # 구분선
        canv = tk.Canvas(frame14_extra, height=10, width=1000)
        line = canv.create_line(00, 10, 1000, 10, fill="#00462A")
        canv.pack()

        # 기존 유물 데이터
        for i in range(0, relicList_length):
            frame14_extra = tk.Frame(frame14_dynamic)
            frame14_extra.pack(fill=tk.X)
            tk.Label(frame14_extra, text="유물%s" % str(i + 1), bg="#00462A", fg="white").pack(side=tk.TOP, anchor=tk.W,
                                                                                             padx=10, pady=10)
            # 14. 유물
            # 14-1. 유물-분류
            frame14_extra_14 = tk.Frame(frame14_extra)
            frame14_extra_14.pack(fill=tk.X, padx=10)
            lbl_relic = tk.Label(frame14_extra_14, text="유물", width=10).grid(column="0", row="4")
            lbl_relic_class = tk.Label(frame14_extra_14, text="분류", width=20).grid(column="1", row="1")
            frame_14_extra_14_frame = tk.Frame(frame14_extra_14).grid(column="2", row="1")
            values_relic_class = ["전세", "출토", "도설", "기타"]
            drBox_relic_class = tk.ttk.Combobox(frame14_extra_14, height=15, width=15, values=values_relic_class,
                                                state="readonly")
            drBox_relic_class.grid(column="2", row="1")

            relicClass_index = 0
            for index, value in enumerate(values_relic_class):
                if (value == relicList[i][0]): relicClass_index = index
            drBox_relic_class.current(relicClass_index)
            # 14-2~8
            lbl_relic_name = tk.Label(frame14_extra_14, text="명칭", width=20).grid(column="1", row="2")
            lbl_relic_country = tk.Label(frame14_extra_14, text="국명", width=20).grid(column="1", row="3")
            lbl_relic_period = tk.Label(frame14_extra_14, text="시기", width=20).grid(column="1", row="4")
            lbl_relic_site = tk.Label(frame14_extra_14, text="소장처", width=20).grid(column="1", row="5")
            lbl_relic_sitePhone = tk.Label(frame14_extra_14, text="소장처번호", width=20).grid(column="1", row="6")
            lbl_relic_findSpot = tk.Label(frame14_extra_14, text="출토지", width=20).grid(column="1", row="7")
            lbl_relic_source = tk.Label(frame14_extra_14, text="출전/출처", width=20).grid(column="1", row="8")
            lbl_relic_image = tk.Label(frame14_extra_14, text="이미지 첨부", width=20).grid(column="1", row="9")
            entry_relic_name = tk.Entry(frame14_extra_14)
            entry_relic_name.grid(column="2", row="2")
            entry_relic_name.insert(0, relicList[i][1])

            entry_relic_country = tk.Entry(frame14_extra_14)
            entry_relic_country.grid(column="2", row="3")
            entry_relic_country.insert(0, relicList[i][2])

            entry_relic_period = tk.Entry(frame14_extra_14)
            entry_relic_period.grid(column="2", row="4")
            entry_relic_period.insert(0, relicList[i][3])

            entry_relic_site = tk.Entry(frame14_extra_14)
            entry_relic_site.grid(column="2", row="5")
            entry_relic_site.insert(0, relicList[i][4])

            entry_relic_sitePhone = tk.Entry(frame14_extra_14)
            entry_relic_sitePhone.grid(column="2", row="6")
            entry_relic_sitePhone.insert(0, relicList[i][5])

            entry_relic_findSpot = tk.Entry(frame14_extra_14)
            entry_relic_findSpot.grid(column="2", row="7")
            entry_relic_findSpot.insert(0, relicList[i][6])

            entry_relic_source = tk.Entry(frame14_extra_14)
            entry_relic_source.grid(column="2", row="8")
            entry_relic_source.insert(0, relicList[i][7])

            entry_relic_image = tk.Button(frame14_extra_14, text="첨부파일")
            entry_relic_image.grid(column="2", row="9")
            # 15. 이미지입력자
            frame14_extra_15 = tk.Frame(frame14_extra)
            frame14_extra_15.pack(fill=tk.X, padx=10)
            # 이부분 range 안에 각 유물에 대한 이미지입력자 수 불러오기
            sql8 = "select * from 임시이미지입력정보 where 고유번호=%s and 유물명칭=%s"
            relicName = relicList[i][1]
            val8 = (item, relicName)
            mc.execute(sql8, val8)
            imageEntryList = mc.fetchall()
            imageEntryList_length = len(imageEntryList)

            for n in range(imageEntryList_length):
                frame14_extra_15_extra = tk.Frame(frame14_extra_15)
                frame14_extra_15_extra.pack(fill=tk.X, padx=10)
                lbl_imageEntryPerson = tk.Label(frame14_extra_15_extra, text="입력자%s" % str(n + 1),
                                                width=10).pack(side=tk.LEFT, padx=10)
                entry_imageEntryPerson = tk.Entry(frame14_extra_15_extra)
                entry_imageEntryPerson.pack(side=tk.LEFT, padx=10)
                entry_imageEntryPerson.insert(0, imageEntryList[n][0])
                cal_imageEntryPerson = tkcalendar.DateEntry(frame14_extra_15_extra, width=12, background="#00462A",
                                                            foreground='white', borderwidth=2,
                                                            year=int(imageEntryList[n][1].year),
                                                            month=int(imageEntryList[n][1].month),
                                                            day=int(imageEntryList[n][1].day))
                cal_imageEntryPerson.pack(side=tk.LEFT, padx=10)
            button_imageEntryPerson = tk.Button(frame14_extra_15, text="입력자 추가")
            button_imageEntryPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
            # 16. 이미지검수자
            frame14_extra_16 = tk.Frame(frame14_extra)
            frame14_extra_16.pack(fill=tk.X, padx=10)
            # 이부분 range 안에 각 유물에 대한 이미지검수자 수 불러오기
            sql9 = "select * from 임시이미지검수정보 where 고유번호=%s and 유물명칭=%s"
            val9 = (item, relicName)
            mc.execute(sql9, val9)
            imageInspecList = mc.fetchall()
            imageInspecList_length = len(imageInspecList)

            for n in range(imageInspecList_length):
                frame14_extra_16_extra = tk.Frame(frame14_extra_16)
                frame14_extra_16_extra.pack(fill=tk.X, padx=10)
                lbl_imageEntryPerson = tk.Label(frame14_extra_16_extra, text="검수자%s" % str(n + 1),
                                                width=10).pack(side=tk.LEFT, padx=10)
                entry_imageInspecPerson = tk.Entry(frame14_extra_16_extra)
                entry_imageInspecPerson.pack(side=tk.LEFT, padx=10)
                entry_imageInspecPerson.insert(0, imageInspecList[n][0])
                cal_imageInspecPerson = tkcalendar.DateEntry(frame14_extra_16_extra, width=12, background="#00462A",
                                                             foreground='white', borderwidth=2,
                                                             year=int(imageInspecList[n][1].year),
                                                             month=int(imageInspecList[n][1].month),
                                                             day=int(imageInspecList[n][1].day))
                cal_imageInspecPerson.pack(side=tk.LEFT, padx=10)
            button_imageInspecPerson = tk.Button(frame14_extra_16, text="검수자 추가")
            button_imageInspecPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

            canv = tk.Canvas(frame14_extra, height=10, width=1000)
            line = canv.create_line(0, 10, 1000, 10, fill="#00462A")
            canv.pack()

        canv = tk.Canvas(self.scrollable_frame, height=10, width=1000)
        line = canv.create_line(0, 10, 1000, 10, fill="#00462A")
        canv.pack()

        # 17. 비고
        frame17 = tk.Frame(self.scrollable_frame)
        frame17.pack(fill=tk.X, pady=20)
        note = tk.StringVar()
        lbl_note = tk.Label(frame17, text="비고", width=10)
        lbl_note.pack(side=tk.LEFT, padx=10, pady=10)
        entry_note = tk.Entry(frame17, textvariable=note)
        entry_note.pack(fill=tk.BOTH, padx=10, expand=True)
        entry_note.insert(0, chosunList[0][9])

        # 구분선
        canv = tk.Canvas(self.scrollable_frame, height=10, width=1000)
        line = canv.create_line(0, 10, 1000, 10, fill="#00462A")
        canv.pack()

        # 저장
        frame = tk.Frame(self.scrollable_frame)
        frame.pack(side=tk.BOTTOM)
        btnSave = tk.Button(frame, text="저장", command=save)
        btnSave.pack(side=tk.LEFT, padx=10, pady=10)


class UserTemp(tk.Frame):
    def __init__(self, master, par_id, par_password, *args, **kwargs):
        val_username = par_id

        def search_by_name():  # 검색하면 시행되는 함수입니다 내부 데이터 db코드 부탁드려요
            self.treeview.delete(*self.treeview.get_children())
            columns = ["고유번호", "색인어", "정의"]

            newlist = []
            for row in rowlist:
                if (row[1] == search_indexKo.get()): newlist.append(row)
            treelist = newlist

            self.treeview.column("#1", width=100)
            self.treeview.column("#2", width=200)
            self.treeview.column("#3", width=500)
            self.treeview.heading("#1", text="고유번호")
            self.treeview.heading("#2", text="색인어")
            self.treeview.heading("#3", text="정의")

            for i in range(len(treelist)):
                # 이부분에서 iid에 고유번호 들어가게 구성
                self.treeview.insert('', 'end', text=i, values=treelist[i], iid=treelist[i][0])

            self.treeview.pack(side=tk.LEFT)
            self.treeview.bind('<1>', self.NewFrame)

        def show_all():
            self.treeview.delete(*self.treeview.get_children())
            columns = ["고유번호", "색인어", "정의"]

            mydb, mc = connect_db()
            sql = "select 고유번호, 색인어한글, 정의 from 임시조선시대공예정보 where userID = %s"
            mc.execute(sql, val_username)
            rows = mc.fetchall()
            rowlist = []
            for row in rows:
                rowlist.append(row)

            columns = ["고유번호", "색인어", "정의"]
            treelist = rowlist

            for i in range(len(treelist)):
                # 이부분에서 iid에 고유번호 들어가게 구성
                self.treeview.insert('', 'end', text=i, values=treelist[i], iid=treelist[i][0])

            self.treeview.pack(side=tk.LEFT)
            self.treeview.bind('<1>', self.NewFrame)

        tk.Frame.__init__(self, master)
        val = ""
        self.master = master
        self.master.title("조선시대공예 DB입력기")
        self.pack(fill=tk.X, expand=True)
        userid = par_id
        userpw = par_password
        tk.Label(text="전체데이터 확인", bg="#00462A", width="100", height="3",
                 fg="white",
                 font=('맑은 고딕', 13)).pack(fill=tk.X)
        tk.Label(text="").pack()

        search_indexKo = tk.StringVar()

        frame_search = tk.Frame(width=300, height=20)
        frame_search.pack(anchor=tk.E, ipadx=60, ipady=5)
        entry_search = tk.Entry(frame_search, width=20, textvariable=search_indexKo)
        entry_search.grid(column="0", row="0")
        tk.Label(frame_search).grid(column="1", row="0")
        button_search = tk.Button(frame_search, width=3, height=1, text="검색", command=search_by_name)
        button_search.grid(column="2", row="0")
        tk.Label(frame_search).grid(column="3", row="0")
        button_all = tk.Button(frame_search, width=8, height=1, text="전체보기", command=show_all)
        button_all.grid(column="4", row="0")

        frame_treelist = tk.Frame(width=800, height=550)
        frame_treelist.pack()

        mydb, mc = connect_db()
        sql = "select 고유번호, 색인어한글, 정의 from 임시조선시대공예정보 where userID = %s"
        mc.execute(sql, val_username)
        rows = mc.fetchall()
        rowlist = []
        for row in rows:
            rowlist.append(row)

        columns = ["고유번호", "색인어", "정의"]
        treelist = rowlist

        self.treeview = tkinter.ttk.Treeview(frame_treelist, columns=columns, show="headings", height=500)
        vsb = tkinter.ttk.Scrollbar(frame_treelist, orient="vertical", command=self.treeview.yview)
        vsb.pack(side='right', fill='y')
        self.treeview.configure(yscrollcommand=vsb.set)

        self.treeview.column("#1", width=100)
        self.treeview.column("#2", width=200)
        self.treeview.column("#3", width=500)
        self.treeview.heading("#1", text="고유번호")
        self.treeview.heading("#2", text="색인어")
        self.treeview.heading("#3", text="정의")

        for i in range(len(treelist)):
            # 이부분에서 iid에 고유번호 들어가게 구성
            self.treeview.insert('', 'end', text=i, values=treelist[i], iid=treelist[i][0])

        self.treeview.pack(side=tk.LEFT)
        self.treeview.bind('<1>', self.NewFrame)

    def NewFrame(self, event):
        item = self.treeview.identify('item', event.x, event.y)
        self.master.title("조선시대공예 DB입력기")
        self.pack()
        UserEdit_tk = tk.Tk()
        UserEdit_tk.geometry("1020x700+100+100")
        UserEdit_tk.resizable(False, False)
        app = UserEdit(UserEdit_tk, str(item))
        app.pack()
        UserEdit.mainloop(self)


def main():
    root = tk.Tk()
    root.geometry("1020x700+100+100")
    root.resizable(False, False)
    app = UserTemp(root, "wjdwl001", "esther0916@")
    app.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
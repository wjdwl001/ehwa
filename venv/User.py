import tkinter as tk
from tkinter import ttk
import uuid
import tkinter.font
import os
from tkinter import messagebox
import pymysql
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
    #멤버변수
    val_state = "" #00. 상태
    val_ID = "" #0. ID(고유번호)
    val_indexKorean = "" #1. 색인어(한글)
    val_indexChinese = "" #2. 색인어(한자)
    val_nickname = "" #3. 이명
    val_generalName = "" #4. 범칭
    val_majorClass = "" #9. 대분류
    array_middleClass = [] #5. 중분류항목
    array_subClass = [] #6. 소분류항목
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
    val_relatedWord = "" #7. 관련어
    val_detail = "" #8. 상세정보

    def __init__(self, master, *args, **kwargs):
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
            val_majorClass = majorClass.get()  # 9. 대분류

            val_relatedWord = relatedWord.get()  # 7. 관련어
            val_detail = detail.get()  # 8. 상세정보

            mydb, mc = connect_db()
            sql = "INSERT INTO temp(대상, 고유번호, 색인어한글, 색인어한자, 이명, 범칭, 관련어, 상세정보, 대분류) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (val_state, val_ID, val_indexKorean, val_indexChinese, val_nickname, val_generalName, val_relatedWord, val_detail, val_majorClass)

            try:
                mc.execute(sql, val)
                mydb.commit()
                messagebox.showinfo("알림", "등록 완료!")
            except:
                messagebox.showinfo("알림", "입력에 실패했습니다!")

        super().__init__(master, *args, **kwargs)
        canvas = tk.Canvas(self, width=980, height=800)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
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

        self.master = master
        self.master.title("조선시대공예 DB입력기")
        self.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.scrollable_frame, text="이화여자대학교 물질문화연구팀\n조선시대공예 DB입력기 #1", bg="#00462A", width="100", height="3", fg="white",
                 font=('맑은 고딕', 13)).pack()
        tk.Label(self.scrollable_frame, text="").pack()

        # 00. 상태
        frame00 = tk.Frame(self.scrollable_frame)
        frame00.pack(fill=tk.X)

        def check():
            global val_state
            val_state = tk.StringVar()
            if entry_state.get() == 1:
                val_state = "대상"
            if entry_state.get() == 2:
                val_state = "비대상"
            if entry_state.get() == 3:
                val_state = "보류"
            if entry_state.get() == 4:
                val_state = "삭제"

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
        action = tk.Button(frame00, text="확인", command=check)

        # 구분선
        canv = tk.Canvas(self.scrollable_frame, height=10, width=1000)
        line = canv.create_line(0, 10, 1000, 10, fill="#00462A")
        canv.pack()

        # 0. ID(고유번호)
        frame0 = tk.Frame(self.scrollable_frame)
        frame0.pack(fill=tk.X)

        global val_ID
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


        # 9. 대분류
        frame9 = tk.Frame(self.scrollable_frame)
        frame9.pack(fill=tk.X)

        values_detail = ["의궤", "실록", "승정원일기", "일성록", "전례서", "법전", "지리지", "등록", "발기", "유서류", "문집", "일기", "기타"]
        majorClass = tk.StringVar()

        lbl_majorClass = tk.Label(frame9, text="대분류\n자료 유형별", width=10)
        lbl_majorClass.pack(side=tk.LEFT, padx=10, pady=10)

        drBox_majorClass = tk.ttk.Combobox(frame9, height=15, values=values_detail, textvariable=majorClass ,state="readonly")
        drBox_majorClass.pack(side=tk.LEFT, pady=10, padx=10, expand=False)


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


        # 8. 상세정보
        frame8 = tk.Frame(self.scrollable_frame)
        frame8.pack(fill=tk.X, pady=10)

        detail = tk.StringVar()

        lbl_detail = tk.Label(frame8, text="상세정보", width=10)
        lbl_detail.pack(side=tk.LEFT, padx=10, pady=10)

        entry_detail = tk.Text(frame8)
        entry_detail.pack(fill=tk.X, padx=10, expand=True)

        # 10. 자료원문
        frame10 = tk.Frame(self.scrollable_frame)
        frame10.pack(fill=tk.X, pady=10)

        lbl_detail = tk.Label(frame10, text="자료원문", width=10)
        lbl_detail.pack(side=tk.LEFT, padx=10, pady=30)

        entry_detail = tk.Entry(frame10)
        entry_detail.pack(fill=tk.BOTH, padx=10, expand=True)

        # 11. 출전
        frame11 = tk.Frame(self.scrollable_frame)
        frame11.pack(fill=tk.X)

        empty = tk.Label(frame11, text="", width=10)
        empty.grid(column="0", pady=5)
        lbl_refer = tk.Label(frame11, text="출전", width=10)
        lbl_refer.grid(column="0", row="4")

        lbl_refer_korean = tk.Label(frame11, text="한글", width =20)
        lbl_refer_korean.grid(column="1", row="1")
        lbl_refer_chinese = tk.Label(frame11, text="한자", width=20)
        lbl_refer_chinese.grid(column="1", row="2")
        lbl_refer_author = tk.Label(frame11, text="저자", width=20)
        lbl_refer_author.grid(column="1", row="3")
        lbl_refer_authorPeriod = tk.Label(frame11, text="저자활동시기", width=20)
        lbl_refer_authorPeriod.grid(column="1", row="4")
        lbl_refer_publishPeriod = tk.Label(frame11, text="간행시기", width=20)
        lbl_refer_publishPeriod.grid(column="1", row="5")
        lbl_refer_institution = tk.Label(frame11, text="텍스트소장처", width=20)
        lbl_refer_institution.grid(column="1", row="6")
        lbl_refer_instiInfo = tk.Label(frame11, text="소장처번호/링크", width=20)
        lbl_refer_instiInfo.grid(column="1", row="7")

        entry_refer_korean = tk.Entry(frame11)
        entry_refer_korean.grid(column="2", row="1")
        entry_refer_chinese = tk.Entry(frame11)
        entry_refer_chinese.grid(column="2", row="2")
        entry_refer_author = tk.Entry(frame11)
        entry_refer_author.grid(column="2", row="3")
        entry_refer_authorPeriod = tk.Entry(frame11)
        entry_refer_authorPeriod.grid(column="2", row="4")
        entry_refer_publishPeriod = tk.Entry(frame11)
        entry_refer_publishPeriod.grid(column="2", row="5")
        entry_refer_institution = tk.Entry(frame11)
        entry_refer_institution.grid(column="2", row="6")
        entry_refer_instInfo = tk.Entry(frame11)
        entry_refer_instInfo.grid(column="2", row="7")

        # 12. 입력자
        frame12 = tk.Frame(self.scrollable_frame)
        frame12.pack(fill=tk.X, expand=True, pady=30)

        lbl_entryPerson = tk.Label(frame12, text="입력자", width=10)
        lbl_entryPerson.grid(column="0", row ="0")
        lbl_entryDate = tk.Label(frame12, text="입력날짜", width=10)
        lbl_entryDate.grid(column="3", row="0")

        entry_entryPerson = tk.Entry(frame12)
        entry_entryPerson.grid(column="1", row="0")
        entry_entryDate = tk.Entry(frame12)
        entry_entryDate.grid(column="4", row="0")
        #항목 추가하는 부분 아직 구현안했습니다
        #이 부분 항목 추가해서 여러명의 입력자가 있는 경우 각각 변수명 entry_entryPerson_#(#:숫자)로 설정할게요



        # 13. 검수자
        frame13 = tk.Frame(self.scrollable_frame)
        frame13.pack(fill=tk.X, expand=True)

        lbl_inspecPerson = tk.Label(frame13, text="검수자", width=10)
        lbl_inspecPerson.grid(column="0", row="0")
        lbl_inspecDate = tk.Label(frame13, text="검수날짜", width=10)
        lbl_inspecDate.grid(column="3", row="0")

        entry_inspecPerson = tk.Entry(frame13)
        entry_inspecPerson.grid(column="1", row="0")
        entry_inspecDate = tk.Entry(frame13)
        entry_inspecDate.grid(column="4", row="0")


        # 14. 유물
        frame14 = tk.Frame(self.scrollable_frame)
        frame14.pack(fill=tk.X)

        empty = tk.Label(frame14, text="", width=10)
        empty.grid(column="0", pady=5)
        lbl_relic = tk.Label(frame14, text="유물", width=10)
        lbl_relic.grid(column="0", row="4")

        lbl_relic_class = tk.Label(frame14, text="분류", width =20)
        lbl_relic_class.grid(column="1", row="1")
        lbl_relic_name = tk.Label(frame14, text="명칭", width=20)
        lbl_relic_name.grid(column="1", row="2")
        lbl_relic_country = tk.Label(frame14, text="국명", width=20)
        lbl_relic_country.grid(column="1", row="3")
        lbl_relic_period = tk.Label(frame14, text="시기", width=20)
        lbl_relic_period.grid(column="1", row="4")
        lbl_relic_site = tk.Label(frame14, text="소장처", width=20)
        lbl_relic_site.grid(column="1", row="5")
        lbl_relic_sitePhone = tk.Label(frame14, text="소장처번호", width=20)
        lbl_relic_sitePhone.grid(column="1", row="6")
        lbl_relic_findSpot = tk.Label(frame14, text="출토지", width=20)
        lbl_relic_findSpot.grid(column="1", row="7")
        lbl_relic_source = tk.Label(frame14, text="출전/출처", width=20)
        lbl_relic_source.grid(column="1", row="8")
        lbl_relic_image = tk.Label(frame14, text="이미지 첨부", width=20)
        lbl_relic_image.grid(column="1", row="9")

        entry_relic_class = tk.Entry(frame14)
        entry_relic_class.grid(column="2", row="1")
        entry_relic_name = tk.Entry(frame14)
        entry_relic_name.grid(column="2", row="2")
        entry_relic_country = tk.Entry(frame14)
        entry_relic_country.grid(column="2", row="3")
        entry_relic_period = tk.Entry(frame14)
        entry_relic_period.grid(column="2", row="4")
        entry_relic_site = tk.Entry(frame14)
        entry_relic_site.grid(column="2", row="5")
        entry_relic_sitePhone = tk.Entry(frame14)
        entry_relic_sitePhone.grid(column="2", row="6")
        entry_relic_findSpot = tk.Entry(frame14)
        entry_relic_findSpot.grid(column="2", row="7")
        entry_relic_source = tk.Entry(frame14)
        entry_relic_source.grid(column="2", row="8")
        entry_relic_image = tk.Entry(frame14)
        entry_relic_image.grid(column="2", row="9")
        #이미지 첨부기능 아직 구현 안했는데 우선 변수이름만 봐주세요!
        #여러개 첨부하면 entry_relic_image_# (#: 숫자) 이런식으로 만들겁니다


        # 15. 이미지입력자
        frame15 = tk.Frame(self.scrollable_frame)
        frame15.pack(fill=tk.X, expand=True, pady=20)

        lbl_imageEntryPerson = tk.Label(frame15, text="이미지입력자", width=17)
        lbl_imageEntryPerson.grid(column="0", row="0")
        lbl_imageEntryDate = tk.Label(frame15, text="이미지입력자", width=17)
        lbl_imageEntryDate.grid(column="3", row="0")

        entry_imageEntryPerson = tk.Entry(frame15)
        entry_imageEntryPerson.grid(column="1", row="0")
        entry_imageEntryDate = tk.Entry(frame15)
        entry_imageEntryDate.grid(column="4", row="0")


        # 16. 이미지검수자
        frame16 = tk.Frame(self.scrollable_frame)
        frame16.pack(fill=tk.X, expand=True, pady=20)

        lbl_imageInspecPerson = tk.Label(frame16, text="이미지검수자", width=17)
        lbl_imageInspecPerson.grid(column="0", row="0")
        lbl_imageInspecDate = tk.Label(frame16, text="이미지검수날짜", width=17)
        lbl_imageInspecDate.grid(column="3", row="0")

        entry_imageInspecPerson = tk.Entry(frame16)
        entry_imageInspecPerson.grid(column="1", row="0")
        entry_imageInspecDate = tk.Entry(frame16)
        entry_imageInspecDate.grid(column="4", row="0")


        # 17. 비고
        frame17 = tk.Frame(self.scrollable_frame)
        frame17.pack(fill=tk.X, pady=20)

        lbl_note = tk.Label(frame17, text="비고", width=10)
        lbl_note.pack(side=tk.LEFT, padx=10, pady=10)

        entry_note = tk.Entry(frame17)
        entry_note.pack(fill=tk.BOTH, padx=10, expand=True)

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
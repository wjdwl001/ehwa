import tkinter as tk
import tkinter.font
import tkinter.ttk
import pymysql
import tkcalendar
from datetime import datetime

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

class UserEdit(tk.Frame):
    def __init__(self,master,item,*args,**kwargs):
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

        lbl_ID = tk.Label(frame0, text="ID", width=10)
        lbl_ID.pack(side=tk.LEFT, padx=10, pady=10)

        entry_ID = tk.Text(frame0, width=10, height=1)
        entry_ID.insert(1.0, item)
        entry_ID.configure(state="disabled")
        entry_ID.pack(side=tk.LEFT, padx=10, pady=10)

#item = 고유번호이므로 이 값을 기준으로 db불러오시면 됩니다

        # 1.색인어(한글)
        frame1 = tk.Frame(self.scrollable_frame)
        frame1.pack(fill=tk.X)

        lbl_indexKorean = tk.Label(frame1, text="색인어(한글)", width=10)
        lbl_indexKorean.pack(side=tk.LEFT, padx=10, pady=10)

        entry_indexKorean = tk.Entry(frame1, textvariable="#")
        entry_indexKorean.pack(side=tk.LEFT, padx=10)

        # 2. 색인어(한자)
        frame2 = tk.Frame(self.scrollable_frame)
        frame2.pack(fill=tk.X)

        lbl_indexChinese = tk.Label(frame2, text="색인어(한자)", width=10)
        lbl_indexChinese.pack(side=tk.LEFT, padx=10, pady=10)

        entry_indexChinese = tk.Entry(frame2, textvariable="#")
        entry_indexChinese.pack(side=tk.LEFT, padx=10)

        # 3. 이명
        frame3 = tk.Frame(self.scrollable_frame)
        frame3.pack(fill=tk.X)

        lbl_nickname = tk.Label(frame3, text="이명", width=10)
        lbl_nickname.pack(side=tk.LEFT, padx=10, pady=10)

        entry_nickname = tk.Entry(frame3, textvariable="#")
        entry_nickname.pack(side=tk.LEFT, padx=10)

        # 4. 범칭
        frame4 = tk.Frame(self.scrollable_frame)
        frame4.pack(fill=tk.X)

        generalName = tk.StringVar()

        lbl_generalName = tk.Label(frame4, text="범칭", width=10)
        lbl_generalName.pack(side=tk.LEFT, padx=10, pady=10)

        entry_generalName = tk.Entry(frame4, textvariable="#")
        entry_generalName.pack(side=tk.LEFT, padx=10)

        # 5. 중분류항목
        frame5 = tk.Frame(self.scrollable_frame)
        frame5.pack(fill=tk.X)

        lbl_middleClass = tk.Label(frame5, text="중분류항목", width=10)
        lbl_middleClass.pack(side=tk.LEFT, padx=10, pady=10)

        middleClass_product = tk.IntVar()
        middleClass_material = tk.IntVar()
        middleClass_tool = tk.IntVar()
        middleClass_producer = tk.IntVar()

        entry_middleClass_product = tk.Checkbutton(frame5, text="제작품", variable=middleClass_product)
        entry_middleClass_material = tk.Checkbutton(frame5, text="제작재료", variable=middleClass_material)
        entry_middleClass_tool = tk.Checkbutton(frame5, text="제작도구", variable=middleClass_tool)
        entry_middleClass_producer = tk.Checkbutton(frame5, text="제작자", variable=middleClass_producer)

        entry_middleClass_product.select() #이런 방식으로 현재 데이터에 select/deselect 해주시면 됩니다

        entry_middleClass_product.pack(side=tk.LEFT, padx=10)
        entry_middleClass_material.pack(side=tk.LEFT, padx=10)
        entry_middleClass_tool.pack(side=tk.LEFT, padx=10)
        entry_middleClass_producer.pack(side=tk.LEFT, padx=10)

        # 6. 소분류항목
        frame6 = tk.Frame(self.scrollable_frame)
        frame6.pack(fill=tk.X)

        lbl_subClass = tk.Label(frame6, text="소분류항목", width=10)
        lbl_subClass.pack(side=tk.LEFT, padx=10, pady=10)

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

        entry_relatedWord = tk.Entry(frame7, textvariable="#")
        entry_relatedWord.pack(side=tk.LEFT, padx=10)

        # 7-2. 정의
        frame7_2 = tk.Frame(self.scrollable_frame)
        frame7_2.pack(fill=tk.X)

        definition = tk.StringVar()

        lbl_definition = tk.Label(frame7_2, text="정의", width=10)
        lbl_definition.pack(side=tk.LEFT, padx=10, pady=10)

        entry_definition = tk.Entry(frame7_2, textvariable="#")
        entry_definition.pack(side=tk.LEFT, padx=10)

        # 8. 상세정보
        frame8 = tk.Frame(self.scrollable_frame)
        frame8.pack(fill=tk.X, pady=10)

        detail = tk.StringVar()

        lbl_detail = tk.Label(frame8, text="상세정보", width=10)
        lbl_detail.pack(side=tk.LEFT, padx=10, pady=10)

        entry_detail = tk.Text(frame8)
        entry_detail.pack(fill=tk.X, padx=10, expand=True)

        # 구분선
        canv = tk.Canvas(self.scrollable_frame, height=10, width=1000)
        line = canv.create_line(00, 10, 1000, 10, fill="#00462A")
        canv.pack()

        frame9 = tk.Frame(self.scrollable_frame)
        frame9.pack(fill=tk.X, padx=10)

#이부분 range 안에 자료 수 불러오기
        for i in range(0,3):
            frame9_extra = tk.Frame(frame9)
            frame9_extra.pack(fill=tk.X)
            tk.Label(frame9_extra, text="자료%s" % str(i+1), bg="#00462A", fg="white").pack(side=tk.TOP,anchor=tk.W,pady=10)
            # 9. 대분류
            frame9_extra_9 = tk.Frame(frame9_extra)
            frame9_extra_9.pack(fill=tk.X, padx=10)
            values_detail = ["의궤", "실록", "승정원일기", "일성록", "전례서", "법전", "지리지", "등록", "발기", "유서류", "문집", "일기", "기타"]
            lbl_majorClass = tk.Label(frame9_extra_9, text="대분류\n자료 유형별", width=10, padx=10)
            lbl_majorClass.pack(side=tk.LEFT, padx=10)
            drBox_majorClass = tk.ttk.Combobox(frame9_extra_9, height=15, values=values_detail, state="readonly")
            drBox_majorClass.current(0)
            drBox_majorClass.pack(side=tk.LEFT, pady=10, padx=10, expand=False)
            # 10. 자료원문
            frame9_extra_10 = tk.Frame(frame9_extra)
            frame9_extra_10.pack(fill=tk.X, padx=10)
            lbl_referDoc = tk.Label(frame9_extra_10, text="자료원문", width=10)
            lbl_referDoc.pack(side=tk.LEFT, padx=10, pady=10)
            entry_referDoc = tk.Entry(frame9_extra_10)
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
            tk.Label(frame9_extra_11).grid()
            # 12. 입력자
            frame9_extra_12 = tk.Frame(frame9_extra)
            frame9_extra_12.pack(fill=tk.X, padx=10)
#이부분 range 안에 각 자료에 대한 입력자 수 불러오기
            for n in range(2):
                frame9_extra_12_extra = tk.Frame(frame9_extra_12)
                frame9_extra_12_extra.pack(fill=tk.X, padx=10)
                lbl_entryPerson = tk.Label(frame9_extra_12_extra, text="입력자%s" % str("i번째 자료의 n번째 입력자"),
                                           width=10).pack(side=tk.LEFT, padx=10)
                entry_entryPerson = tk.Entry(frame9_extra_12_extra)
                entry_entryPerson.pack(side=tk.LEFT, padx=10)
                cal_entryPerson = tkcalendar.DateEntry(frame9_extra_12_extra, width=12, background="#00462A",
                                                       foreground='white', borderwidth=2,
                                                       year=int(datetime.today().year),
                                                       month=int(datetime.today().month),
                                                       day=int(datetime.today().day))
                cal_entryPerson.pack(side=tk.LEFT, padx=10)
            button_entryPerson = tk.Button(frame9_extra_12, text="입력자 추가")
            button_entryPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
            # 13. 검수자
            frame9_extra_13 = tk.Frame(frame9_extra)
            frame9_extra_13.pack(fill=tk.X, padx=10)
# 이부분 range 안에 각 자료에 대한 검수자 수 불러오기
            for n in range(2):
                frame9_extra_13_extra = tk.Frame(frame9_extra_13)
                frame9_extra_13_extra.pack(fill=tk.X, padx=10)
                lbl_inspecPerson = tk.Label(frame9_extra_13_extra, text="검수자%s" % str("i번째 자료의 n번째 검수자"),
                                           width=10).pack(side=tk.LEFT, padx=10)
                entry_inspecPerson = tk.Entry(frame9_extra_13_extra)
                entry_inspecPerson.pack(side=tk.LEFT, padx=10)
                cal_inspecPerson = tkcalendar.DateEntry(frame9_extra_13_extra, width=12, background="#00462A",
                                                       foreground='white', borderwidth=2,
                                                       year=int(datetime.today().year),
                                                       month=int(datetime.today().month),
                                                       day=int(datetime.today().day))
                cal_inspecPerson.pack(side=tk.LEFT, padx=10)
            button_entryPerson = tk.Button(frame9_extra_13, text="검수자 추가")
            button_entryPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
            # 구분선
            canv = tk.Canvas(frame9_extra, height=10, width=1000)
            line = canv.create_line(00, 10, 1000, 10, fill="#00462A")
            canv.pack()

        frame14 = tk.Frame(self.scrollable_frame)
        frame14.pack(fill=tk.X, expand=True)
        frame14_dynamic = tk.Frame(frame14)
        frame14_dynamic.pack(fill=tk.X, expand=True)
        tk.Button(frame14, text="유물 추가").pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
        frame14_extra = tk.Frame(frame14_dynamic)
        frame14_extra.pack(fill=tk.X)

#이부분 range 안에 유물 수 불러오기
        for i in range(0, 3):
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
            entry_relic_image = tk.Button(frame14_extra_14, text="첨부파일")
            entry_relic_image.grid(column="2", row="9")
            # 15. 이미지입력자
            frame14_extra_15 = tk.Frame(frame14_extra)
            frame14_extra_15.pack(fill=tk.X, padx=10)
# 이부분 range 안에 각 유물에 대한 이미지입력자 수 불러오기
            for n in range(2):
                frame14_extra_15_extra = tk.Frame(frame14_extra_15)
                frame14_extra_15_extra.pack(fill=tk.X, padx=10)
                lbl_imageEntryPerson = tk.Label(frame14_extra_15_extra, text="입력자%s" % str("i번째 유물의 n번째 이미지입력자"),
                                           width=10).pack(side=tk.LEFT, padx=10)
                entry_imageInspecPerson = tk.Entry(frame14_extra_15_extra)
                entry_imageInspecPerson.pack(side=tk.LEFT, padx=10)
                cal_imageEntryPerson = tkcalendar.DateEntry(frame14_extra_15_extra, width=12, background="#00462A",
                                                       foreground='white', borderwidth=2,
                                                       year=int(datetime.today().year),
                                                       month=int(datetime.today().month),
                                                       day=int(datetime.today().day))
                cal_imageEntryPerson.pack(side=tk.LEFT, padx=10)
            button_entryPerson = tk.Button(frame14_extra_15, text="입력자 추가")
            button_entryPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
            # 16. 이미지검수자
            frame14_extra_16 = tk.Frame(frame14_extra)
            frame14_extra_16.pack(fill=tk.X, padx=10)
# 이부분 range 안에 각 유물에 대한 이미지검수자 수 불러오기
            for n in range(2):
                frame14_extra_16_extra = tk.Frame(frame14_extra_16)
                frame14_extra_16_extra.pack(fill=tk.X, padx=10)
                lbl_imageEntryPerson = tk.Label(frame14_extra_16_extra, text="검수자%s" % str("i번째 유물의 n번째 이미지검수자"),
                                                width=10).pack(side=tk.LEFT, padx=10)
                entry_imageInspecPerson = tk.Entry(frame14_extra_16_extra)
                entry_imageInspecPerson.pack(side=tk.LEFT, padx=10)
                cal_imageEntryPerson = tkcalendar.DateEntry(frame14_extra_16_extra, width=12, background="#00462A",
                                                            foreground='white', borderwidth=2,
                                                            year=int(datetime.today().year),
                                                            month=int(datetime.today().month),
                                                            day=int(datetime.today().day))
                cal_imageEntryPerson.pack(side=tk.LEFT, padx=10)
            button_entryPerson = tk.Button(frame14_extra_16, text="검수자 추가")
            button_entryPerson.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
            # 구분선
            canv = tk.Canvas(frame14_extra, height=10, width=1000)
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
        btnSave = tk.Button(frame, text="저장")
        btnSave.pack(side=tk.LEFT, padx=10, pady=10)




class UserData(tk.Frame):
    def __init__(self, master, par_id, par_password, *args, **kwargs):
        tk.Frame.__init__(self,master)
        val = ""
        self.master = master
        self.master.title("조선시대공예 DB입력기")
        self.pack(fill=tk.X, expand=True)
        userid = par_id
        userpw = par_password
        tk.Label(text=userid + "님의 입력 데이터 확인", bg="#00462A", width="100", height="3",
                     fg="white",
                     font=('맑은 고딕', 13)).pack(fill=tk.X)
        tk.Label(text="").pack()
        frame_treelist = tk.Frame(width = 800, height = 550)
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
        self.treeview = tkinter.ttk.Treeview(frame_treelist, columns=columns, show="headings", height=500)
        vsb= tkinter.ttk.Scrollbar(frame_treelist, orient="vertical", command=self.treeview.yview)
        vsb.pack(side='right',fill='y')
        self.treeview.configure(yscrollcommand=vsb.set)

        self.treeview.column("#1", width = 100)
        self.treeview.column("#2", width = 200)
        self.treeview.column("#3", width = 500)
        self.treeview.heading("#1", text="고유번호")
        self.treeview.heading("#2", text="색인어")
        self.treeview.heading("#3", text="정의")

        for i in range(len(treelist)):
#이부분에서 iid에 고유번호 들어가게 구성
            self.treeview.insert('','end',text=i, values=treelist[i], iid=str(i))

        self.treeview.pack(side=tk.LEFT)
        self.treeview.bind('<1>', self.NewFrame)

    def NewFrame(self,event):
        item = self.treeview.identify('item', event.x, event.y)
        print(str(item))
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
    root.resizable(False,False)
    app = UserData(root,"wjdwl001","esther0916@")
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
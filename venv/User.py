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
        self.switch_frame(UserPage)
        self.resizable(False,False)
        self.title("조선시대공예 DB입력기")

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class UserPage(tk.Frame):
    refer = 0
    relic = 0
    num_entryPerson = []
    num_inspecPerson = []
    num_imageEntryPerson =[]
    num_imageInspecPerson = []
    num_entryPerson.append(0)
    num_inspecPerson.append(0)
    num_imageEntryPerson.append(0)
    num_imageInspecPerson.append(0)
    def __init__(self, master, par_id, par_password, *args, **kwargs):
        # 멤버변수
        val_username = par_id  # 아이디
        val_password = par_password  # 비밀번호
        print(val_username)
        print(val_password)
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
        array_refer = [] # 9-11. 출전 : [["자료1-대분류", "자료1-자료원문", "자료1-한글", "자료1-한자", "자료1-저자", "자료1=저자활동시기" ,,,]["자료2-한글",,,],,,]
        real_array_refer = []
        array_entryPerson = []  # 12-1. 입력자 : [["자료1-입력자1","자료1-입력자2",,,],["자료2-입력자1","자료2-입력자2",,,,],,,]
        real_array_entryPerson =[]
        array_entryDate = []  # 12-2. 입력날짜   => 입력자와 동일
        real_array_entryDate = []
        array_inspecPerson = []  # 13-1. 검수자  => 입력자와 동일
        real_array_inspecPerson = []
        array_inspecDate = []  # 13-2. 검수날짜  => 입력자와 동일
        real_array_inspecDate = []
        ############
        array_relic = [] #14. 유물 : [["유물1-분류", "유물1-이름",,,,],["유물2-분류", "유물2-이름",,,],,,]
        real_array_relic = []
        array_imageEntryPerson = [] #15-1. 이미지입력자
        real_array_imageEntryPerson = []
        array_imageEntryDate =[] #15-2. 이미지입력날짜
        real_array_imageEntryDate = []
        array_imageInspecPerson = [] #16-1. 이미지검수자
        real_array_imageInspecPerson = []
        array_imageInspecDate = [] #16-2. 이미지 검수날짜
        real_array_imageInspecDate = []
        ############
        val_note = ""  # 17. 비고

        def check():
            if indexKorean.get() == '': return False
            if indexChinese.get() == '': return False # 2. 색인어(한자)
            if nickname.get() == '': return False# 3. 이명
            if generalName.get() == '': return False# 4. 범칭
            if relatedWord.get() == '': return False
            # 7-2. 정의
            if definition.get() == '': return False
            # 8. 상세정보, 마지막 문자인 /n제거하기 위한 방법
            if entry_detail.get(1.0, tk.END+"-1c") == '': return False
            # 9-11. 자료
            # 17.비고
            if note.get() == '': return False

            for i in range(len(array_refer)):
                for e in array_refer[i]:
                    if e.get()== '': return False
            for i in range(len(array_relic)):
                for e in array_relic[i]:
                    if e.get()== '': return False

            for i in range(len(array_entryPerson)):
                for e in array_entryPerson[i]:
                    if e.get()== '': return False
            for i in range(len(array_inspecPerson)):
                for e in array_inspecPerson[i]:
                    if e.get()== '': return False

            for i in range(len(array_imageEntryPerson)):
                for e in array_imageEntryPerson[i]:
                    if e.get()== '': return False
            for i in range(len(array_imageInspecPerson)):
                for e in array_imageInspecPerson[i]:
                    if e.get()== '': return False

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
            val_indexKorean = indexKorean.get()  # 1. 색인어(한글)
            val_indexChinese = indexChinese.get()  # 2. 색인어(한자)
            val_nickname = nickname.get() # 3. 이명
            val_generalName = generalName.get()# 4. 범칭
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
            val_relatedWord = relatedWord.get()
            # 7-2. 정의
            val_definition = definition.get()
            # 8. 상세정보, 마지막 문자인 /n제거하기 위한 방법
            val_detail = entry_detail.get(1.0, tk.END+"-1c")
            # 9-11. 자료
            # 17.비고
            val_note = note.get()

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
                print(real_array_entryPerson)
                print(real_array_entryDate)
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
                print(real_array_inspecPerson)
                print(real_array_inspecDate)
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
                print(real_array_imageEntryPerson)
                print(real_array_imageEntryDate)
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
                print(real_array_imageInspecPerson)
                print(real_array_imageInspecDate)
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
            messagebox.showinfo("알림", "등록 완료!")

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
            val_relatedWord = relatedWord.get()
            # 7-2. 정의
            val_definition = definition.get()
            # 8. 상세정보
            val_detail = entry_detail.get(1.0, tk.END + "-1c")
            # 9-11. 자료
            # 17.비고
            val_note = note.get()

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
            sql1 = "INSERT INTO 임시조선시대공예정보(대상, 고유번호, 색인어한글, 색인어한자, 이명, 범칭, 관련어, 정의, 상세정보, 비고, userID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val1 = (
            val_state, val_ID, val_indexKorean, val_indexChinese, val_nickname, val_generalName, val_relatedWord,
            val_definition, val_detail, val_note, val_username)
            sql2 = "INSERT INTO 임시중분류항목(고유번호, 중분류) VALUES (%s, %s)"
            sql3 = "INSERT INTO 임시소분류항목(고유번호, 소분류) VALUES (%s, %s)"
            sql4 = "INSERT INTO 임시출전(대분류, 자료원문, 한글, 한자, 저자, 저자활동시기, 간행시기, 텍스트소장처, 소장처번호및링크, 고유번호) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql5 = "INSERT INTO 임시입력정보(입력자, 입력일, 고유번호, 출전한글) VALUES (%s, %s, %s, %s)"
            sql6 = "INSERT INTO 임시검수정보(검수자, 검수일, 고유번호, 출전한글) VALUES (%s, %s, %s, %s)"
            sql7 = "INSERT INTO 임시유물(분류, 명칭, 국명, 시기, 소장처, 소장처번호, 출토지, 출전및출처, 고유번호) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql8 = "INSERT INTO 임시이미지입력정보(입력자, 입력일, 고유번호, 유물명칭) VALUES (%s, %s, %s, %s)"
            sql9 = "INSERT INTO 임시이미지검수정보(검수자, 검수일, 고유번호, 유물명칭) VALUES (%s, %s, %s, %s)"

            try:
                mc.execute(sql1, val1)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "임시조선시대공예정보 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            try:
                for i in array_middleClass:
                    val2 = (val_ID, i)
                    mc.execute(sql2, val2)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "임시중분류항목 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            try:
                for i in array_subClass:
                    val3 = (val_ID, i)
                    mc.execute(sql3, val3)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "임시소분류항목 입력에 실패했습니다!")
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
                messagebox.showinfo("알림", "임시출전 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            try:
                for i in range(0, len(real_array_refer)):
                    for j, k in zip(real_array_entryPerson[i], array_entryDate[i]):
                        print(i)
                        print(real_array_refer[i])
                        val5 = (j, k.get_date(), val_ID, real_array_refer[i][2])
                        mc.execute(sql5, val5)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "임시입력정보 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            try:
                for i in range(0, len(real_array_refer)):
                    for l, m in zip(real_array_inspecPerson[i], array_inspecDate[i]):
                        val6 = (l, m.get_date(), val_ID, real_array_refer[i][2])
                        mc.execute(sql6, val6)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "임시검수정보 입력에 실패했습니다!")
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
                messagebox.showinfo("알림", "임시유물 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            try:
                for i in range(0, len(real_array_relic)):
                    for j, k in zip(real_array_imageEntryPerson[i], real_array_imageEntryDate[i]):
                        val8 = (j, k, val_ID, real_array_relic[i][1])
                        mc.execute(sql8, val8)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "임시이미지입력정보 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            try:
                for i in range(0, len(real_array_relic)):
                    for l, m in zip(real_array_imageInspecPerson[i], real_array_imageInspecDate[i]):
                        val9 = (l, m, val_ID, real_array_relic[i][1])
                        mc.execute(sql9, val9)
            except pymysql.InternalError as error:
                messagebox.showinfo("알림", "임시이미지검수정보 입력에 실패했습니다!")
                code, message = error.args
                print(">>>>>>>>>>>>>", code, message)
                return

            mydb.commit()
            messagebox.showinfo("알림", "임시 저장 완료!")


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

        middleClass_product = tk.IntVar()
        middleClass_material = tk.IntVar()
        middleClass_tool = tk.IntVar()
        middleClass_producer = tk.IntVar()

        entry_middleClass_product = tk.Checkbutton(frame5, text="제작품", variable=middleClass_product)
        entry_middleClass_material = tk.Checkbutton(frame5, text="제작재료", variable=middleClass_material)
        entry_middleClass_tool = tk.Checkbutton(frame5, text="제작도구", variable=middleClass_tool)
        entry_middleClass_producer = tk.Checkbutton(frame5, text="제작자", variable=middleClass_producer)

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
            self.refer+=1
            self.num_entryPerson.append(0)
            self.num_inspecPerson.append(0)
            array_entryPerson.append([])
            array_entryDate.append([])
            array_inspecPerson.append([])
            array_inspecDate.append([])
            def Add_entryPerson():
                self.num_entryPerson[self.refer] +=1
                frame9_extra_12_extra = tk.Frame(frame9_extra_12)
                frame9_extra_12_extra.pack(fill=tk.X, padx=10)
                lbl_entryPerson = tk.Label(frame9_extra_12_extra, text="입력자%s"%str(self.num_entryPerson[self.refer]), width=10).pack(side=tk.LEFT,padx=10)
                entry_entryPerson = tk.Entry(frame9_extra_12_extra)
                entry_entryPerson.pack(side=tk.LEFT,padx=10)
                cal_entryPerson = tkcalendar.DateEntry(frame9_extra_12_extra, width=12, background="#00462A",
                                                       foreground='white', borderwidth=2,
                                                       year=int(datetime.today().year),
                                                       month=int(datetime.today().month),
                                                       day=int(datetime.today().day))
                cal_entryPerson.pack(side=tk.LEFT, padx=10)
                array_entryPerson[self.refer-1].append(entry_entryPerson)
                array_entryDate[self.refer-1].append(cal_entryPerson)


            def Add_inspecPerson():
                self.num_inspecPerson[self.refer] += 1
                frame9_extra_13_extra = tk.Frame(frame9_extra_13)
                frame9_extra_13_extra.pack(fill=tk.X, padx=10)
                lbl_inspecPerson = tk.Label(frame9_extra_13_extra, text="검수자%s"%str(self.num_inspecPerson[self.refer]), width=10).pack(side=tk.LEFT,padx=10)
                entry_inspecPerson = tk.Entry(frame9_extra_13_extra)
                entry_inspecPerson.pack(side=tk.LEFT,padx=10)
                cal_inspecPerson = tkcalendar.DateEntry(frame9_extra_13_extra, width=12, background="#00462A",
                                                        foreground='white', borderwidth=2,
                                                        year=int(datetime.today().year),
                                                        month=int(datetime.today().month),
                                                        day=int(datetime.today().day))
                cal_inspecPerson.pack(side=tk.LEFT, padx=10)
                array_inspecPerson[self.refer-1].append(entry_inspecPerson)
                array_inspecDate[self.refer-1].append(cal_inspecPerson)

            array_refer_new = []
            frame9_extra = tk.Frame(frame9_dynamic)
            frame9_extra.pack(fill=tk.X)
            tk.Label(frame9_extra,text="자료%s"%str(self.refer),bg="#00462A",fg="white").pack(side=tk.TOP,anchor=tk.W,padx=10,pady=10)
            #9. 대분류
            frame9_extra_9 = tk.Frame(frame9_extra)
            frame9_extra_9.pack(fill=tk.X, padx=10)
            values_detail = ["의궤", "실록", "승정원일기", "일성록", "전례서", "법전", "지리지", "등록", "발기", "유서류", "문집", "일기", "기타"]
            lbl_majorClass = tk.Label(frame9_extra_9,text="대분류\n자료 유형별", width=10,padx=10)
            lbl_majorClass.pack(side=tk.LEFT, padx=10)
            drBox_majorClass = tk.ttk.Combobox(frame9_extra_9, height=15, values=values_detail,state="readonly")
            drBox_majorClass.current(0)
            drBox_majorClass.pack(side=tk.LEFT, pady=10, padx=10, expand=False)
            array_refer_new.append(drBox_majorClass)
            #10. 자료원문
            frame9_extra_10 = tk.Frame(frame9_extra)
            frame9_extra_10.pack(fill=tk.X, padx=10)
            lbl_referDoc = tk.Label(frame9_extra_10, text="자료원문", width=10)
            lbl_referDoc.pack(side=tk.LEFT, padx=10, pady=10)
            entry_referDoc = tk.Entry(frame9_extra_10)
            entry_referDoc.pack(fill=tk.X, padx=10, expand=True)
            array_refer_new.append(entry_referDoc)
            #11. 출전
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
            #구분선
            canv = tk.Canvas(frame9_extra, height=10, width=1000)
            line = canv.create_line(00, 10, 1000, 10, fill="#00462A")
            canv.pack()
            array_refer.append(array_refer_new)

        # 9. 대분류
        # 10. 자료원문
        # 11. 출전
        # 12. 입력자
        # 13. 검수자

        #자료추가 버튼
        frame9 = tk.Frame(self.scrollable_frame)
        frame9_dynamic = tk.Frame(frame9)
        frame9_dynamic.pack(fill=tk.X, expand=True)
        frame9.pack(fill=tk.X, expand=True)
        tk.Button(frame9,text="자료 추가",command=AddFrame9).pack(side=tk.TOP, anchor=tk.W,padx=10,pady=10)

        # 구분선
        canv = tk.Canvas(self.scrollable_frame, height=10, width=1000)
        line = canv.create_line(0, 10, 1000, 10, fill="#00462A")
        canv.pack()

        #하늘색부분-유물추가
        def AddFrame14():
            self.relic += 1
            self.num_imageEntryPerson.append(0)
            self.num_imageInspecPerson.append(0)
            array_imageEntryPerson.append([])
            array_imageEntryDate.append([])
            array_imageInspecPerson.append([])
            array_imageInspecDate.append([])
            def Add_imagePerson():
                self.num_imageEntryPerson[self.relic] +=1
                frame14_extra_15_extra = tk.Frame(frame14_extra_15)
                frame14_extra_15_extra.pack(side=tk.TOP,anchor=tk.W, padx=10)
                lbl_imageEntryPerson = tk.Label(frame14_extra_15_extra, text="입력자%s"%str(self.num_imageEntryPerson[self.relic]), width=10).pack(side=tk.LEFT, padx=10)
                entry_imageEntryPerson = tk.Entry(frame14_extra_15_extra)
                entry_imageEntryPerson.pack(side=tk.LEFT, padx=10)
                cal_imageEntryPerson = tkcalendar.DateEntry(frame14_extra_15_extra, width=12, background="#00462A",
                                                       foreground='white', borderwidth=2,
                                                       year=int(datetime.today().year),
                                                       month=int(datetime.today().month),
                                                       day=int(datetime.today().day))
                cal_imageEntryPerson.pack(side=tk.LEFT, padx=10)
                imageEntryDate = datetime.today().strftime("%Y%m%d")
                array_imageEntryPerson[self.relic-1].append(entry_imageEntryPerson)
                array_imageEntryDate[self.relic-1].append(cal_imageEntryPerson)


            def Add_imageInspecPerson():
                self.num_imageInspecPerson[self.relic] += 1
                frame14_extra_16_extra = tk.Frame(frame14_extra_16)
                frame14_extra_16_extra.pack(fill=tk.X, padx=10)
                lbl_entryPerson = tk.Label(frame14_extra_16_extra, text="검수자%s"%str(self.num_imageInspecPerson[self.relic]), width=10).pack(side=tk.LEFT, padx=10)
                entry_imageInspecPerson = tk.Entry(frame14_extra_16_extra)
                entry_imageInspecPerson.pack(side=tk.LEFT, padx=10)
                cal_imageInspecPerson = tkcalendar.DateEntry(frame14_extra_16_extra, width=12, background="#00462A",
                                                       foreground='white', borderwidth=2,
                                                       year=int(datetime.today().year),
                                                       month=int(datetime.today().month),
                                                       day=int(datetime.today().day))
                cal_imageInspecPerson.pack(side=tk.LEFT, padx=10)
                array_imageInspecPerson[self.relic-1].append(entry_imageInspecPerson)
                array_imageInspecDate[self.relic-1].append(cal_imageInspecPerson)
            def Browser_relic_image():
                filename = filedialog.askopenfilename()

            array_relic_new = []
            frame14_extra = tk.Frame(frame14_dynamic)
            frame14_extra.pack(fill=tk.X)
            tk.Label(frame14_extra, text="유물%s"%str(self.relic), bg="#00462A", fg="white").pack(side=tk.TOP,anchor=tk.W, padx=10, pady=10)
            #14. 유물
            #14-1. 유물-분류
            frame14_extra_14 = tk.Frame(frame14_extra)
            frame14_extra_14.pack(fill=tk.X, padx=10)
            lbl_relic=tk.Label(frame14_extra_14, text="유물", width=10).grid(column="0",row="4")
            lbl_relic_class = tk.Label(frame14_extra_14, text="분류", width=20).grid(column="1", row="1")
            frame_14_extra_14_frame = tk.Frame(frame14_extra_14).grid(column="2",row="1")
            values_relic_class = ["전세","출토","도설","기타"]
            drBox_relic_class = tk.ttk.Combobox(frame14_extra_14,height=15,width=15, values=values_relic_class,state="readonly")
            drBox_relic_class.grid(column="2",row="1")
            drBox_relic_class.current(0)
            #14-2~8
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
            array_relic.append(array_relic_new)
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

            # 구분선
            canv = tk.Canvas(frame14_extra, height=10, width=1000)
            line = canv.create_line(00, 10, 1000, 10, fill="#00462A")
            canv.pack()

        # 유물추가 버튼
        frame14 = tk.Frame(self.scrollable_frame)
        frame14_dynamic = tk.Frame(frame14)
        frame14_dynamic.pack(fill=tk.X,expand=True)
        frame14.pack(fill=tk.X,expand=True)
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
        btnSave = tk.Button(frame, text="저장", command=save)
        btnSave.pack(side=tk.LEFT, padx=10, pady=10)



def main():
    root = tk.Tk()
    root.geometry("1020x700+100+100")
    root.resizable(False,False)
    app = UserPage(root,"wjdwl0208","esther0916@")
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
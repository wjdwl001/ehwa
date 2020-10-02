# import modules
import tkinter as tk
import tkinter.ttk
import tkinter.font
import os

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

        tk.Label(self, text="이화여자대학교 물질문화연구팀\n조선시대공예 DB입력기 #2", bg="#00462A", width="300", height="3", fg="white",
                 font=('맑은 고딕', 13)).pack()
        tk.Label(self, text="").pack()




        # 10. 자료원문
        frame10 = tk.Frame(self)
        frame10.pack(fill=tk.X)

        lbl_detail = tk.Label(frame10, text="자료원문", width=10)
        lbl_detail.pack(side=tk.LEFT, padx=10, pady=10)

        entry_detail = tk.Entry(frame10)
        entry_detail.pack(fill=tk.BOTH, padx=10, expand=True)


        # 11. 출전
        frame11 = tk.Frame(self)
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
        frame12 = tk.Frame(self)
        frame12.pack(fill=tk.X, expand=True)

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
        frame13 = tk.Frame(self)
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
        frame14 = tk.Frame(self)
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
        frame15 = tk.Frame(self)
        frame15.pack(fill=tk.X, expand=True)

        lbl_imageEntryPerson = tk.Label(frame15, text="이미지입력자", width=10)
        lbl_imageEntryPerson.grid(column="0", row="0")
        lbl_imageEntryDate = tk.Label(frame15, text="이미지입력자", width=10)
        lbl_imageEntryDate.grid(column="3", row="0")

        entry_imageEntryPerson = tk.Entry(frame15)
        entry_imageEntryPerson.grid(column="1", row="0")
        entry_imageEntryDate = tk.Entry(frame15)
        entry_imageEntryDate.grid(column="4", row="0")


        # 16. 이미지검수자
        frame16 = tk.Frame(self)
        frame16.pack(fill=tk.X, expand=True)

        lbl_imageInspecPerson = tk.Label(frame16, text="이미지검수자", width=15)
        lbl_imageInspecPerson.grid(column="0", row="0")
        lbl_imageInspecDate = tk.Label(frame16, text="이미지검수날짜", width=15)
        lbl_imageInspecDate.grid(column="3", row="0")

        entry_imageInspecPerson = tk.Entry(frame16)
        entry_imageInspecPerson.grid(column="1", row="0")
        entry_imageInspecDate = tk.Entry(frame16)
        entry_imageInspecDate.grid(column="4", row="0")


        # 17. 비고
        frame17 = tk.Frame(self)
        frame17.pack(fill=tk.X)

        lbl_note = tk.Label(frame17, text="비고", width=10)
        lbl_note.pack(side=tk.LEFT, padx=10, pady=10)

        entry_note = tk.Entry(frame17)
        entry_note.pack(fill=tk.BOTH, padx=10, expand=True)

def main():
    root = tk.Tk()
    root.geometry("1000x600+100+100")
    root.resizable(False,False)
    app = UserPage(root)
    root.mainloop()

if __name__ == '__main__':
    main()

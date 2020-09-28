# import modules
import tkinter as tk
import tkinter.font
import os

#color : #00462A #77E741

#로그인 관련 팝업창
def password_not_recognised(self):
    global password_not_recog_screen
    password_not_recog_screen = tk.Toplevel(self)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100+300+300")
    tk.Label(password_not_recog_screen, text="Invalid Password ").pack()
    tk.Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()
def user_not_found(self):
    global user_not_found_screen
    user_not_found_screen = tk.Toplevel(self)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100+300+300")
    tk.Label(user_not_found_screen, text="User Not Found").pack()
    tk.Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
def delete_login_success():
    login_success_screen.destroy()
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
def delete_user_not_found_screen():
    user_not_found_screen.destroy()
#실무자 등록 확인/팝업창
def register_user():
    username_info = username.get()
    password_info = password.get()

    #이부분 DB에 맞게 바꾸면됩니다.
    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    tk.Label(self, text="등록 완료", fg="#00462A", font=("맑은 고딕", 11)).pack()

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.geometry("300x300+300+300")
        self.resizable(False,False)
        self.title("조선시대공예 DB입력기")

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="이화여자대학교 물질문화연구팀\n조선시대공예 DB입력기", bg="#00462A", width="300", height="3", fg="white",
              font=('맑은 고딕', 13)).pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="실무자 로그인", height="1", width="20",
                  command=lambda: master.switch_frame(Login), font=('맑은 고딕', 13)).pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="관리자 로그인", height="1", width="20",
                  command=lambda: master.switch_frame(AdminLogin), font = ('맑은 고딕', 13)).pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="실무자 등록", height="1", width="20", fg = "#00462A",
                  command=lambda: master.switch_frame(Register), font=('맑은 고딕', 13)).pack()

#실무자 로그인 페이지
class Login(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self,master)
        tk.Label(self, text="실무자 로그인", bg="#00462A", width="300", height="3", fg="white", font=('맑은 고딕', 13)).pack()
        tk.Label(self, text="").pack()

        global username_verify
        global password_verify

        username_verify = tk.StringVar()
        password_verify = tk.StringVar()

        global username_login_entry
        global password_login_entry

        tk.Label(self, text="ID * ").pack()
        username_login_entry = tk.Entry(self, textvariable=username_verify)
        username_login_entry.pack()
        tk.Label(self, text="").pack()
        tk.Label(self, text="Password * ").pack()
        password_login_entry = tk.Entry(self, textvariable=password_verify, show='*')
        password_login_entry.pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="로그인", width=10, height=1, bg="#00462A", fg="white",
                  command=lambda: login_verify(username_verify,password_verify,username_login_entry,password_login_entry)).pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="뒤로가기", width = 10, height=1,
                  command=lambda: master.switch_frame(StartPage)).pack()

        #실무자 아이디, 비밀번호 확인
        def login_verify(username_verify, password_verify, username_login_entry, password_login_entry):
            username1 = username_verify.get()
            password1 = password_verify.get()
            username_login_entry.delete(0, tk.END)
            password_login_entry.delete(0, tk.END)

            if username1 == "admin":
                if password1 == "admin":
                    master.switch_frame(UserPage).pack()
                else:
                    password_not_recognised(self)
            else:
                user_not_found(self)

#관리자 로그인 페이지
class AdminLogin(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self,master)
        tk.Label(self, text="관리자 로그인", bg="#00462A", width="300", height="3", fg="white", font=('맑은 고딕', 13)).pack()
        tk.Label(self, text="").pack()

        global admin_name_verify
        global admin_password_verify

        admin_username_verify = tk.StringVar()
        admin_password_verify = tk.StringVar()

        tk.Label(self, text="ID * ").pack()
        admin_username_login_entry = tk.Entry(self, textvariable=admin_username_verify)
        admin_username_login_entry.pack()
        tk.Label(self, text="").pack()
        tk.Label(self, text="Password * ").pack()
        admin_password_login_entry = tk.Entry(self, textvariable=admin_password_verify, show='*')
        admin_password_login_entry.pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="로그인", width=10, height=1, bg="#00462A", fg="white",
                  command=lambda:admin_login_verify(self,admin_username_verify, admin_password_verify, admin_username_login_entry, admin_password_login_entry)).pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="뒤로가기", width = 10, height=1,
                  command=lambda: master.switch_frame(StartPage)).pack()

        def admin_login_verify(self, admin_username_verify, admin_password_verify, admin_username_login_entry,
                               admin_password_login_entry):
            username = admin_username_verify.get()
            password = admin_password_verify.get()
            admin_username_login_entry.delete(0, tk.END)
            admin_password_login_entry.delete(0, tk.END)

            #관리자 아이디, 비밀번호 확인
            if username == "admin":
                if password == "admin":
                    master.switch_frame(AdminPage).pack()
                else:
                    password_not_recognised(self)
            else:
                user_not_found(self)

#실무자 등록 페이지
class Register(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self,master)
        global username
        global password
        global username_entry
        global password_entry
        username = tk.StringVar()
        password = tk.StringVar()

        tk.Label(self, text="실무자 등록", bg="#00462A", width="300", height="3", fg="white",
              font=('맑은 고딕', 13)).pack()
        tk.Label(self, text="").pack()
        username_lable = tk.Label(self, text="Username * ")
        username_lable.pack()
        username_entry = tk.Entry(self, textvariable=username)
        username_entry.pack()
        password_lable = tk.Label(self, text="Password * ")
        password_lable.pack()
        password_entry = tk.Entry(self, textvariable=password, show='*')
        password_entry.pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="실무자 등록", width=10, height=1, bg="#00462A", fg="white",
               command=register_user).pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="뒤로가기", width = 10, height=1,
                  command=lambda: master.switch_frame(StartPage)).pack()
#관리자 페이지
class AdminPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="관리자 페이지", bg="#00462A", width="300", height="3", fg="white", font=('맑은 고딕', 13)).pack()
        tk.Label(self, text="").pack()
#실무자 페이지
class UserPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="실무자 페이지", bg="#00462A", width="300", height="3", fg="white", font=('맑은 고딕', 13)).pack()
        tk.Label(self, text="").pack()



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
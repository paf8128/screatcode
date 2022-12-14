from SecretCodeDB import *
from SecretCodeWidgets import *
class App:
    def __init__(self,master):
        self.master = master
        self.conn = Connection()
        self.widgets = list()
        self.login()
    def clear(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
    def login(self):
        lb1 = Label(self.master,text="密码管理系统",font=("微软雅黑",44,"bold"))
        lb1.pack(side=TOP,fill=None)
        self.widgets.append(lb1)
        #账号
        fm1 = Frame(self.master)
        fm1.pack(side=TOP,fill=X)
        self.widgets.append(fm1)
        Label(fm1,text="账号:").pack(side=LEFT,fill=None)
        self.user_cbVar = StringVar()
        self.user_cb = Combobox(fm1,textvariable=self.user_cbVar)
        self.user_cb["values"] = self.conn.getusers()
        self.user_cb["state"] = "readonly"
        self.user_cb.pack(side=LEFT,fill=X)
        Button(fm1,text="注册",command=self.ask).pack(side=LEFT,fill=None)
        #密码
        fm2 = Frame(self.master)
        fm2.pack(side=TOP,fill=X)
        self.widgets.append(fm2)
        Label(fm2,text="密码:").pack(side=LEFT,fill=None)
        self.pass_entry = PassEntry(fm2,width=20,font=("宋体",15))
        self.pass_entry.pack(side=LEFT,fill=X)
        self.pass_entry.get_cb().pack(side=LEFT,fill=None)
        Button(fm2,text="忘记密码",command=self.ask_questions)\
                                .pack(side=LEFT,fill=None)
        #登录按钮
        bt1 = Button(self.master,text="登录",command=self.check_login)
        bt1.pack(side=TOP,fill=None)
        self.widgets.append(bt1)
        if len(self.conn.getusers()) == 0:
            self.ask()
        else:
            self.user_cbVar.set(self.user_cb["values"][0])
    def relogin(self):
        self.clear()
        self.login()
    def ask_questions(self):
        self.tl = Toplevel(self.master)
        self.tl.title("创建新账号")
        self.tl.grab_set()
        questions = self.conn.get_questions(self.user_cbVar.get())
        self.aes = list()
        for i in range(3):
            qafm = Frame(self.tl)
            qafm.pack(side=TOP,fill=X,pady=20)
            qfm = Frame(qafm)
            qfm.pack(side=TOP,fill=X)
            Label(qfm,text="问题"+str(i+1)+": "+questions[i])\
                                            .pack(side=LEFT,fill=X)
            afm = Frame(qafm)
            afm.pack(side=TOP,fill=X)
            Label(afm,text="答案:").pack(side=LEFT,fill=None)
            ae = Entry(afm,width=20,font=("宋体",15))
            ae.pack(side=LEFT,fill=X)
            self.aes.append(ae)
        fm2 = Frame(self.tl)
        fm2.pack(side=TOP,fill=X)
        Label(fm2,text="密码:").pack(side=LEFT,fill=None)
        self.newcode = PassEntry(fm2,width=20,font=("宋体",15))
        self.newcode.pack(side=LEFT,fill=X)
        self.newcode.get_cb().pack(side=LEFT,fill=None)
        bt1 = Button(self.tl,text="确定",command=self.check_answers)
        bt1.pack(side=TOP,fill=None)
    def check_answers(self):
        answers = list()
        for ae in self.aes:
            answers.append(ae.get().strip())
        result = self.conn.login_by_answers(self.user_cbVar.get(),answers,\
                                            self.newcode.get())
        if result == 0:
            self.tl.destroy()
            self.clear()
            self.show_main_window()
            msgbox.showinfo("消息","登录成功，欢迎使用本程序")
        else:
            msgbox.showerror("消息","问题{}回答错误".format(result))
    def ask(self):
        self.tl = Toplevel(self.master)
        self.tl.title("创建新账号")
        self.tl.grab_set()
        #账号
        fm1 = Frame(self.tl)
        fm1.pack(side=TOP,fill=X)
        Label(fm1,text="账号:").pack(side=LEFT,fill=None)
        self.tl_user_entry = Entry(fm1,width=20,font=("宋体",15))
        self.tl_user_entry.pack(side=LEFT,fill=X)
        #密码
        fm2 = Frame(self.tl)
        fm2.pack(side=TOP,fill=X)
        Label(fm2,text="密码:").pack(side=LEFT,fill=None)
        self.tl_pass_entry = PassEntry(fm2,width=20,font=("宋体",15))
        self.tl_pass_entry.pack(side=LEFT,fill=X)
        self.tl_pass_entry.get_cb().pack(side=LEFT,fill=None)
        #问题
        self.aes = list()
        self.qes = list()
        for i in range(3):
            qafm = Frame(self.tl)
            qafm.pack(side=TOP,fill=X,pady=20)
            qfm = Frame(qafm)
            qfm.pack(side=TOP,fill=X)
            Label(qfm,text="问题{}：".format(i+1))\
                                            .pack(side=LEFT,fill=X)
            qe = Entry(qfm,width=20,font=("宋体",15))
            qe.pack(side=LEFT,fill=X)
            self.qes.append(qe)
            afm = Frame(qafm)
            afm.pack(side=TOP,fill=X)
            Label(afm,text="答案:").pack(side=LEFT,fill=None)
            ae = Entry(afm,width=20,font=("宋体",15))
            ae.pack(side=LEFT,fill=X)
            self.aes.append(ae)
        #按钮
        Button(self.tl,text="确定",command=self.add_user)\
                .pack(side=TOP,fill=None)
    def check_login(self):
        if not self.user_cbVar.get():
            msgbox.showerror("消息","账号不能为空")
            return
        if self.conn.login(self.user_cbVar.get(),self.pass_entry.get()):
            self.clear()
            self.show_main_window()
            msgbox.showinfo("消息","登录成功，欢迎使用本程序")
        else:
            msgbox.showerror("消息","登录失败，密码错误")
    def add_user(self):
        if self.tl_user_entry.get() in self.conn.getusers():
            msgbox.showerror("消息","账号名已存在")
        elif self.tl_user_entry.get() == "":
            msgbox.showerror("消息","账号名不能为空")
        else:
            questions = list()
            for i in range(3):
                questions.append((self.qes[i].get().strip(),\
                                 self.aes[i].get().strip()))
            self.conn.add_user(self.tl_user_entry.get(),\
                               self.tl_pass_entry.get(),questions)
            self.tl.destroy()
            self.clear()
            self.show_main_window()
            msgbox.showinfo("消息","新账号创建成功，欢迎使用本程序")
    def show_main_window(self):
        fm = Frame(self.master)
        fm.pack(side=TOP,fill=BOTH)
        self.widgets.append(fm)
        Label(fm,text="请选择操作",font=("宋体",25))\
                    .grid(row=0,column=0,columnspan=2)
        #操作按钮
        bt1 = Button(fm,text="添加",font=("宋体",25),\
                     command=lambda :self.dialog("insert"))
        bt1.grid(row=1,column=0)
        #_
        bt2 = Button(fm,text="修改",font=("宋体",25),\
                     command=lambda :self.dialog("update"))
        bt2.grid(row=1,column=1)
        #_
        bt3 = Button(fm,text="查看",font=("宋体",25),\
                     command=lambda :self.dialog("select"))
        bt3.grid(row=2,column=0)
        #_
        bt4 = Button(fm,text="删除",font=("宋体",25),\
                     command=lambda :self.dialog("delete"))
        bt4.grid(row=2,column=1)
        #_
        bt5 = Button(fm,text="修改此账号密码",font=("宋体",25),\
                     command=lambda :self.dialog("change"))
        bt5.grid(row=3,column=0,columnspan=2)
        #_
        bt6 = Button(fm,text="重新登录",font=("宋体",25),command=self.relogin)
        bt6.grid(row=4,column=0,columnspan=2)
        #_
        bt7 = Button(fm,text="退出",font=("宋体",25),\
                     command=self.master.destroy)
        bt7.grid(row=5,column=0,columnspan=2)
    def dialog(self,mode):
        if mode not in ("insert","update","select","delete","change"):
            return
        if len(self.conn.getnames()) == 0 \
            and mode in ("update","select","delete"):
            msgbox.showerror("消息","还未存储密码")
            return
        self.tl = Toplevel(self.master)
        self.tl.title("")
        self.tl.grab_set()
        if mode in ("insert","update"):
            #名称
            fm1 = Frame(self.tl)
            fm1.pack(side=TOP,fill=X)
            Label(fm1,text="名称:").pack(side=LEFT,fill=None)
            if mode == "insert":
                self.name_entry = Entry(fm1,width=20,font=("宋体",15))
                self.name_entry.pack(side=LEFT,fill=X)
            else:
                self.name_cbVar = StringVar()
                self.name_cb = Combobox(fm1,textvariable=self.name_cbVar)
                self.name_cb["values"] = self.conn.getnames()
                self.name_cb["state"] = "readonly"
                self.name_cb.pack(side=LEFT,fill=X)
                self.name_cbVar.set(self.name_cb["values"][0])
            #账号
            fm2 = Frame(self.tl)
            fm2.pack(side=TOP,fill=X)
            Label(fm2,text="账号:").pack(side=LEFT,fill=None)
            self.user_entry = Entry(fm2,width=20,font=("宋体",15))
            self.user_entry.pack(side=LEFT,fill=X)
            #密码
            fm3 = Frame(self.tl)
            fm3.pack(side=TOP,fill=X)
            Label(fm3,text="密码:").pack(side=LEFT,fill=None)
            self.pass_entry = PassEntry(fm3,width=20,font=("宋体",15))
            self.pass_entry.pack(side=LEFT,fill=X)
            self.pass_entry.get_cb().pack(side=LEFT,fill=None)
            #按钮
            Button(self.tl,text="确定",\
            command=self.insert if mode=="insert" else self.update)\
            .pack(side=TOP,fill=None)
        elif mode in ("select","delete"):
            #名称
            fm1 = Frame(self.tl)
            fm1.pack(side=TOP,fill=X)
            Label(fm1,text="名称:").pack(side=LEFT,fill=None)
            self.name_cbVar = StringVar()
            self.name_cb = Combobox(fm1,textvariable=self.name_cbVar)
            self.name_cb["values"] = self.conn.getnames()
            self.name_cb["state"] = "readonly"
            self.name_cb.pack(side=LEFT,fill=X)
            self.name_cbVar.set(self.name_cb["values"][0])
            #按钮
            Button(self.tl,text="确定",\
            command=self.select if mode=="select" else self.delete)\
            .pack(side=TOP,fill=None)
        else:
            #密码
            fm1 = Frame(self.tl)
            fm1.pack(side=TOP,fill=X)
            Label(fm1,text="密码:").pack(side=LEFT,fill=None)
            self.pass_entry = PassEntry(fm1,width=20,font=("宋体",15))
            self.pass_entry.pack(side=LEFT,fill=X)
            self.pass_entry.get_cb().pack(side=LEFT,fill=None)
            #按钮
            Button(self.tl,text="确定",command=self.change)\
            .pack(side=TOP,fill=None)
    def insert(self):
        if self.name_entry.get() in self.conn.getnames():
            msgbox.showerror("消息","名称重复")
            return
        if self.name_entry.get() == "":
            msgbox.showerror("消息","名称不能为空")
            return
        if self.conn.insert((self.name_entry.get(),self.user_entry.get(),\
                             self.pass_entry.get())):
            self.tl.destroy()
            msgbox.showinfo("消息","操作成功")
        else:
            msgbox.showerror("消息","操作失败")
    def update(self):
        if not msgbox.askyesno("确认","是否确定?"):
            return
        if self.conn.update((self.name_cbVar.get(),self.user_entry.get(),\
                             self.pass_entry.get())):
            self.tl.destroy()
            msgbox.showinfo("消息","操作成功")
        else:
            msgbox.showerror("消息","操作失败")
    def select(self):
        result = self.conn.select(self.name_cbVar.get())
        if result:
            self.tl.destroy()
            msgbox.showinfo("消息","账号:{};\n密码:{}.".format(*result))
        else:
            msgbox.showerror("消息","操作失败")
    def delete(self):
        if not msgbox.askyesno("确认","是否确定?"):
            return
        if self.conn.delete(self.name_cbVar.get()):
            self.tl.destroy()
            msgbox.showinfo("消息","操作成功")
        else:
            msgbox.showerror("消息","操作失败")
    def change(self):
        self.conn.change(self.pass_entry.get())
        self.tl.destroy()
        msgbox.showinfo("消息","操作成功")
        

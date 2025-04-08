
from tkinter import *
from tkinter import messagebox


def login():
    if usrentry.get()=='' or passentry.get()=='':
      messagebox.showerror('eror','Fields cannot be empty')
    elif usrentry.get()=='Shuvo' and passentry.get()=="1234":
        messagebox.showinfo("Success",'Welcome to the system ')
        window.destroy()
        import Sms




    else:
        messagebox.showerror('error',"Unsucessful")
window = Tk()
window.geometry('1500x700')#the size of tkinter prompt
#window.resizable(False, False)
window.title('login')



myimage= PhotoImage(file='ff.png') #adding image
lbl=Label(image=myimage).pack() #labelling the image to show on the command prompt

Login=Frame (window)
Login.place(x=440,y=330)

logoimage=PhotoImage(file='ll.png')
lglbl=Label(Login,image=logoimage).pack()




usrimage=PhotoImage(file='kk.png')
usernamelbl=Label(Login,image=usrimage,text='username',compound=LEFT,font=('times new roman',10,'bold'))
usernamelbl.place(x=150,y=50)
#Frame is a container to keep labels or buttons

usrentry=Entry(Login,font=('times new roman',10,'bold'))
usrentry.place(x=200,y=70)



passimage=PhotoImage(file='p.png')
passnamelbl=Label(Login,image=passimage,text='password',compound=LEFT,font=('times new roman',10,'bold'))
passnamelbl.place(x=100,y=70)
passentry=Entry(Login,font=('times new roman',10,'bold'))
passentry.place(x=200,y=100)

logbutton=Button(Login,text='Login',command=login)
logbutton.place(x=120,y=10)

window.mainloop()
#keep our windows on loop so that we can see it continously
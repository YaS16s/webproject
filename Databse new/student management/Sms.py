








# Global connection objects
con = None
mycursor = None

# Function to connect to XAMPP MySQL
def connectDB():
    connectWindow = Toplevel()
    connectWindow.title("Connect to XAMPP MySQL")

    Label(connectWindow, text='Host name').grid(row=0, column=0, padx=10, pady=5)
    hostentry = Entry(connectWindow)
    hostentry.insert(0, "localhost")
    hostentry.grid(row=0, column=1, padx=10, pady=5)

    Label(connectWindow, text='User').grid(row=1, column=0, padx=10, pady=5)
    userentry = Entry(connectWindow)
    userentry.insert(0, "root")
    userentry.grid(row=1, column=1, padx=10, pady=5)

    Label(connectWindow, text='Password').grid(row=2, column=0, padx=10, pady=5)
    passent = Entry(connectWindow, show="*")
    passent.grid(row=2, column=1, padx=10, pady=5)

    def connect():
        global con, mycursor
        try:
            con = pymysql.connect(
                host=hostentry.get(),
                user=userentry.get(),
                password=passent.get()
            )
            mycursor = con.cursor()
            mycursor.execute("CREATE DATABASE IF NOT EXISTS studentdb")
            mycursor.execute("USE studentdb")
            mycursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    mobile VARCHAR(20),
                    email VARCHAR(100),
                    address TEXT,
                    dob VARCHAR(20)
                )
            ''')
            messagebox.showinfo('Success', 'Connected to XAMPP MySQL successfully!')
            connectWindow.destroy()
        except Exception as e:
            messagebox.showerror('Connection Error', f'Failed to connect to XAMPP MySQL.\n\n{e}')

    Button(connectWindow, text='CONNECT', command=connect).grid(row=3, column=1, pady=10)
















def clock():
   date=time.strftime("%d/%m/%Y")
   curTime=time.strftime('%H:%M:%S')
   datetimelabel.config(text=f'  Date:  {date}\n Time: {curTime}')
   datetimelabel.after(1000,clock)



#Gui part:
root=Tk()
root.geometry('1500x700')

root.title('ST Managment sytem')

datetimelabel=Label(root,font=("times new roman",18,"bold"))
datetimelabel.place(x=5,y=5)
clock()
s='Student management system '
sliderlabel=Label(root,text=s,font=("times new roman",18,"bold"))
sliderlabel.place(x=500,y=0)

cnctbuttn=Button(root,text="connect database",command=connectDB)
cnctbuttn.place(x=1300,y=0)

lftframe=Frame(root)
lftframe.place(x=50,y=80,width=300,height=600)

addSTbuttn=Button(lftframe,text='Add student',font=("times new roman",16,"bold"))
addSTbuttn.grid(row=1,column=0,pady=20)

searchSTbuttn=Button(lftframe,text='Search student',font=("times new roman",16,"bold"))
searchSTbuttn.grid(row=2,column=0,pady=20)

updateSTbuttn=Button(lftframe,text='Update student',font=("times new roman",16,"bold"))
updateSTbuttn.grid(row=3,column=0,pady=20)

deleteSTbuttn=Button(lftframe,text='Delete student',font=("times new roman",16,"bold"))
deleteSTbuttn.grid(row=4,column=0,pady=20)

showSTbuttn=Button(lftframe,text='Show student',font=("times new roman",16,"bold"))
showSTbuttn.grid(row=5,column=0,pady=20)

exportSTbuttn=Button(lftframe,text='Export Data',font=("times new roman",16,"bold"))
exportSTbuttn.grid(row=6,column=0,pady=20)

exitbuttn=Button(lftframe,text='Exit',font=("times new roman",16,"bold"))
exitbuttn.grid(row=7,column=0,pady=20)

rightframe=Frame(root)
rightframe.place(x=350,y=80,width=1000,height=600)

scroolx=Scrollbar(rightframe,orient=HORIZONTAL)
scrooly=Scrollbar(rightframe,orient=VERTICAL)
studenttable=ttk.Treeview(rightframe,columns=('Id','name','Mobile','Email','Address','D.O.B'),xscrollcommand=scroolx.set,yscrollcommand=scrooly.set)


scroolx.config(command=studenttable.xview)
scrooly.config(command=studenttable.yview)
scroolx.pack(side=BOTTOM,fill=X)
scrooly.pack(side=BOTTOM,fill=Y)
studenttable.pack(fill=BOTH,expand=1)

studenttable.heading('Id',text='Id')
studenttable.heading('name',text='name')
studenttable.heading('Mobile',text='Mobile')
studenttable.heading('Email',text='Email')
studenttable.heading('Address',text='Address')
studenttable.heading('D.O.B',text='D.O.B')

studenttable.config(show="headings")











root.mainloop()

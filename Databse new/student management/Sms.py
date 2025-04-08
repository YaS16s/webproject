from tkinter import *
from tkinter import ttk, messagebox, filedialog
import time
import pymysql
import pandas as pd

root = Tk()
root.geometry('1500x700')
root.title('Student Management System')

# Global variable for database connection
con = None
mycursor = None

# ------------------- Database Connection -------------------
def connectDB():
    global con, mycursor

    connectWindow = Toplevel()
    connectWindow.title("Connect to Database")

    Label(connectWindow, text='Host Name').grid(row=0, column=0)
    hostentry = Entry(connectWindow)
    hostentry.grid(row=0, column=1)

    Label(connectWindow, text='User').grid(row=1, column=0)
    userentry = Entry(connectWindow)
    userentry.grid(row=1, column=1)

    Label(connectWindow, text='Password').grid(row=2, column=0)
    passent = Entry(connectWindow, show='*')
    passent.grid(row=2, column=1)

    def connect():
        global con, mycursor
        try:
            con = pymysql.connect(host=hostentry.get(), user=userentry.get(), password=passent.get())
            mycursor = con.cursor()
            mycursor.execute('CREATE DATABASE IF NOT EXISTS studentmanagementsystem')
            mycursor.execute('USE studentmanagementsystem')
            mycursor.execute('''CREATE TABLE IF NOT EXISTS student(
                                id INT PRIMARY KEY,
                                name VARCHAR(30),
                                mobile VARCHAR(30),
                                address VARCHAR(100),
                                gender VARCHAR(20),
                                dob VARCHAR(20))''')
            messagebox.showinfo('Success', 'Database Connected and Ready!')
        except Exception as e:
            messagebox.showerror('Connection Error', f"Error: {e}")

    Button(connectWindow, text='CONNECT', command=connect).grid(row=3, column=1, pady=10)

# ------------------- Add Student -------------------
def addst():
    def submit():
        if not con:
            messagebox.showerror('Error', 'Connect to Database first')
            return
        try:
            mycursor.execute("INSERT INTO student VALUES(%s,%s,%s,%s,%s,%s)",
                             (ident.get(), nameent.get(), mobileent.get(), addressent.get(), genderent.get(), dobent.get()))
            con.commit()
            messagebox.showinfo('Success', 'Student Added')
            show_students()
            add_window.destroy()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    add_window = Toplevel()
    add_window.title('Add Student')

    Label(add_window, text='ID').grid(row=0, column=0)
    ident = Entry(add_window)
    ident.grid(row=0, column=1)

    Label(add_window, text='Name').grid(row=1, column=0)
    nameent = Entry(add_window)
    nameent.grid(row=1, column=1)

    Label(add_window, text='Mobile').grid(row=2, column=0)
    mobileent = Entry(add_window)
    mobileent.grid(row=2, column=1)

    Label(add_window, text='Address').grid(row=3, column=0)
    addressent = Entry(add_window)
    addressent.grid(row=3, column=1)

    Label(add_window, text='Gender').grid(row=4, column=0)
    genderent = Entry(add_window)
    genderent.grid(row=4, column=1)

    Label(add_window, text='DOB').grid(row=5, column=0)
    dobent = Entry(add_window)
    dobent.grid(row=5, column=1)

    Button(add_window, text='Submit', command=submit).grid(row=6, column=1)

# ------------------- Show Students -------------------
def show_students():
    if not con:
        return
    try:
        mycursor.execute("SELECT * FROM student")
        rows = mycursor.fetchall()
        studenttable.delete(*studenttable.get_children())
        for row in rows:
            studenttable.insert('', END, values=row)
    except:
        pass

# ------------------- Search Student -------------------
def search_student():
    def do_search():
        mycursor.execute("SELECT * FROM student WHERE id=%s", (ident.get(),))
        row = mycursor.fetchone()
        studenttable.delete(*studenttable.get_children())
        if row:
            studenttable.insert('', END, values=row)
        search_window.destroy()

    search_window = Toplevel()
    search_window.title('Search Student')
    Label(search_window, text='Enter ID').grid(row=0, column=0)
    ident = Entry(search_window)
    ident.grid(row=0, column=1)
    Button(search_window, text='Search', command=do_search).grid(row=1, column=1)

# ------------------- Delete Student -------------------
def delete_student():
    selected = studenttable.focus()
    if not selected:
        messagebox.showerror('Error', 'Select a student to delete')
        return
    values = studenttable.item(selected, 'values')
    mycursor.execute("DELETE FROM student WHERE id=%s", (values[0],))
    con.commit()
    show_students()
    messagebox.showinfo('Deleted', 'Student Deleted')

# ------------------- Update Student -------------------
def update_student():
    selected = studenttable.focus()
    if not selected:
        messagebox.showerror('Error', 'Select a student to update')
        return

    values = studenttable.item(selected, 'values')

    def update():
        mycursor.execute("UPDATE student SET name=%s, mobile=%s, address=%s, gender=%s, dob=%s WHERE id=%s",
                         (nameent.get(), mobileent.get(), addressent.get(), genderent.get(), dobent.get(), ident.get()))
        con.commit()
        show_students()
        messagebox.showinfo('Updated', 'Student Record Updated')
        update_window.destroy()

    update_window = Toplevel()
    update_window.title('Update Student')

    Label(update_window, text='ID').grid(row=0, column=0)
    ident = Entry(update_window)
    ident.insert(0, values[0])
    ident.grid(row=0, column=1)
    ident.config(state='readonly')

    Label(update_window, text='Name').grid(row=1, column=0)
    nameent = Entry(update_window)
    nameent.insert(0, values[1])
    nameent.grid(row=1, column=1)

    Label(update_window, text='Mobile').grid(row=2, column=0)
    mobileent = Entry(update_window)
    mobileent.insert(0, values[2])
    mobileent.grid(row=2, column=1)

    Label(update_window, text='Address').grid(row=3, column=0)
    addressent = Entry(update_window)
    addressent.insert(0, values[3])
    addressent.grid(row=3, column=1)

    Label(update_window, text='Gender').grid(row=4, column=0)
    genderent = Entry(update_window)
    genderent.insert(0, values[4])
    genderent.grid(row=4, column=1)

    Label(update_window, text='DOB').grid(row=5, column=0)
    dobent = Entry(update_window)
    dobent.insert(0, values[5])
    dobent.grid(row=5, column=1)

    Button(update_window, text='Update', command=update).grid(row=6, column=1)

# ------------------- Export Data -------------------
def export_data():
    if not con:
        return
    mycursor.execute("SELECT * FROM student")
    rows = mycursor.fetchall()
    df = pd.DataFrame(rows, columns=['ID', 'Name', 'Mobile', 'Address', 'Gender', 'DOB'])
    file = filedialog.asksaveasfilename(defaultextension=".xlsx")
    if file:
        df.to_excel(file, index=False)
        messagebox.showinfo('Exported', f'Data exported to {file}')

# ------------------- Clock -------------------
def clock():
    date = time.strftime("%d/%m/%Y")
    curTime = time.strftime('%H:%M:%S')
    datetimelabel.config(text=f'  Date:  {date}\n Time: {curTime}')
    datetimelabel.after(1000, clock)

# ------------------- GUI -------------------
datetimelabel = Label(root, font=("times new roman", 18, "bold"))
datetimelabel.place(x=5, y=5)
clock()

Label(root, text='Student Management System', font=("times new roman", 18, "bold")).place(x=500, y=0)
Button(root, text="Connect to XAMPP MySQL", command=connectDB).place(x=1300, y=0)

lftframe = Frame(root)
lftframe.place(x=50, y=80, width=300, height=600)

Button(lftframe, text='Add Student', font=("times new roman", 16, "bold"), command=addst).grid(row=1, column=0, pady=20)
Button(lftframe, text='Search Student', font=("times new roman", 16, "bold"), command=search_student).grid(row=2, column=0, pady=20)
Button(lftframe, text='Update Student', font=("times new roman", 16, "bold"), command=update_student).grid(row=3, column=0, pady=20)
Button(lftframe, text='Delete Student', font=("times new roman", 16, "bold"), command=delete_student).grid(row=4, column=0, pady=20)
Button(lftframe, text='Show Students', font=("times new roman", 16, "bold"), command=show_students).grid(row=5, column=0, pady=20)
Button(lftframe, text='Export Data', font=("times new roman", 16, "bold"), command=export_data).grid(row=6, column=0, pady=20)
Button(lftframe, text='Exit', font=("times new roman", 16, "bold"), command=root.destroy).grid(row=7, column=0, pady=20)

rightframe = Frame(root)
rightframe.place(x=350, y=80, width=1100, height=600)

scroolx = Scrollbar(rightframe, orient=HORIZONTAL)
scrooly = Scrollbar(rightframe, orient=VERTICAL)

studenttable = ttk.Treeview(
    rightframe,
    columns=('Id', 'Name', 'Mobile', 'Address', 'Gender', 'DOB'),
    xscrollcommand=scroolx.set,
    yscrollcommand=scrooly.set
)

scroolx.config(command=studenttable.xview)
scrooly.config(command=studenttable.yview)
scroolx.pack(side=BOTTOM, fill=X)
scrooly.pack(side=RIGHT, fill=Y)
studenttable.pack(fill=BOTH, expand=1)

for col in ['Id', 'Name', 'Mobile', 'Address', 'Gender', 'DOB']:
    studenttable.heading(col, text=col)
    studenttable.column(col, width=150)

studenttable.config(show="headings")

root.mainloop()












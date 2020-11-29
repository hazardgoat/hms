from tkinter import*
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

root = Tk()
root.title("Python: Simple CRUD Applition")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = int(screen_width/2)
height = int(screen_height/2)
root.geometry(f'{width}x{height}')
root.resizable(0, 0)

#==================================METHODS============================================
def Database():
    global conn, cursor
    conn = sqlite3.connect('mediadbtest.sqlite')
    cursor = conn.cursor()
    
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS director (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name    TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS genre (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name   TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS type (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name    TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS title (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT  UNIQUE,
        genre_id  INTEGER,
        type_id INTEGER,
        director_id INTEGER,
        length INTEGER, rating TEXT
    );
    ''')

def Create():
    Database()
    if  TITLE.get() == "":
        txt_result.config(text="Title must be entered!", fg="red")
    else:
        cursor.execute('''INSERT OR IGNORE INTO director (name)
            VALUES ( ? )''', (DIRECTOR.get(), ))
        cursor.execute('SELECT id FROM director WHERE name = ? ', (DIRECTOR.get(), ))
        director_id = cursor.fetchone()[0]
        cursor.execute('''INSERT OR IGNORE INTO type (name)
            VALUES ( ? )''', (TYPE.get(), ))
        cursor.execute('SELECT id FROM type WHERE name = ? ', (TYPE.get(), ))
        type_id = cursor.fetchone()[0]
        cursor.execute('''INSERT OR IGNORE INTO genre (name)
            VALUES ( ? )''', (GENRE.get(), ))
        cursor.execute('SELECT id FROM genre WHERE name = ? ', (GENRE.get(), ))
        genre_id = cursor.fetchone()[0]
        if MINUTES.get() not in ("", '', ' ', " "):
            try:
                int(MINUTES.get())
                minutesValidate = True
            except:
                MINUTES.set("")
                minutesValidate = False
        cursor.execute('''INSERT OR REPLACE INTO title (name, genre_id, type_id, director_id, length, rating)
            VALUES ( ?, ?, ?, ?, ?, ? )''', (TITLE.get(), genre_id, type_id, director_id, MINUTES.get(), RATING.get()))
        conn.commit()
        if minutesValidate == True:
            txt_result.config(text="Entry added to library!", fg="green")
        else:
            txt_result.config(text="Entry added to Library! Minutes not added; entry must be an integer!", fg="yellow")
        TITLE.set("")
        GENRE.set("")
        TYPE.set("")
        DIRECTOR.set("")
        MINUTES.set("")
        RATING.set("")
    cursor.close()
    conn.close()
    Read()

def Update():
    Database()
    if IDNUMBER.get() in ("", '', ' ', " "):
        txt_result.config(text="ID Number must be entered!", fg="red")
    else:
        try:
            int(IDNUMBER.get())
            if TITLE.get() not in ("", '', ' ', " "):
                cursor.execute('UPDATE title SET name=? WHERE id=?', (TITLE.get(), IDNUMBER.get()))
            if MINUTES.get() not in ("", '', ' ', " "):
                try:
                    int(MINUTES.get())
                    cursor.execute('UPDATE title SET length=? WHERE id=?', (MINUTES.get(), IDNUMBER.get()))
                    minutesValidate = True
                except:
                    MINUTES.set("")
                    minutesValidate = False
            if RATING.get() not in ("", '', ' ', " "):
                cursor.execute('UPDATE title SET rating=? WHERE id=?', (RATING.get(), IDNUMBER.get()))
            if GENRE.get() not in ("", '', ' ', " "):
                cursor.execute('SELECT id FROM genre WHERE name=? ', (GENRE.get(), ))
                try:
                    fetch = cursor.fetchone()[0]
                    cursor.execute('UPDATE title SET genre_id=? WHERE id=?', (fetch, IDNUMBER.get()))
                except:
                    cursor.execute('INSERT OR IGNORE INTO genre (name) VALUES ( ? )', (GENRE.get(), ))
                    cursor.execute('SELECT id FROM genre WHERE name = ? ', (GENRE.get(), ))
                    genre_id_UPDATE = cursor.fetchone()[0]
                    cursor.execute('UPDATE title SET genre_id=? WHERE id=?', (genre_id_UPDATE, IDNUMBER.get()))
            if TYPE.get() not in ("", '', ' ', " "):
                cursor.execute('SELECT id FROM type WHERE name=? ', (TYPE.get(), ))
                try:
                    fetch = cursor.fetchone()[0]
                    cursor.execute('UPDATE title SET type_id=? WHERE id=?', (fetch, IDNUMBER.get()))
                except:
                    cursor.execute('INSERT OR IGNORE INTO type (name) VALUES ( ? )', (TYPE.get(), ))
                    cursor.execute('SELECT id FROM type WHERE name = ? ', (TYPE.get(), ))
                    type_id_UPDATE = cursor.fetchone()[0]
                    cursor.execute('UPDATE title SET type_id=? WHERE id=?', (type_id_UPDATE, IDNUMBER.get()))
            if DIRECTOR.get() not in ("", '', ' ', " "):
                cursor.execute('SELECT id FROM director WHERE name=? ', (DIRECTOR.get(), ))
                try:
                    fetch = cursor.fetchone()[0]
                    cursor.execute('UPDATE title SET director_id=? WHERE id=?', (fetch, IDNUMBER.get()))
                except:
                    cursor.execute('INSERT OR IGNORE INTO director (name) VALUES ( ? )', (DIRECTOR.get(), ))
                    cursor.execute('SELECT id FROM director WHERE name = ? ', (DIRECTOR.get(), ))
                    director_id_UPDATE = cursor.fetchone()[0]
                    cursor.execute('UPDATE title SET director_id=? WHERE id=?', (director_id_UPDATE, IDNUMBER.get()))
            conn.commit()
            if minutesValidate == True:
                txt_result.config(text="Updated library!", fg="green")
            else:
                txt_result.config(text="Updated library! Minutes not updated; entry must be an integer!", fg="yellow")
            IDNUMBER.set("")
            TITLE.set("")
            GENRE.set("")
            TYPE.set("")
            DIRECTOR.set("")
            MINUTES.set("")
            RATING.set("")
        except:
            txt_result.config(text="ID Number must be an integer!", fg="red")
        cursor.close()
        conn.close()
        Read()

def Read():
    Database()
    tree.delete(*tree.get_children())
    cursor.execute('''
        SELECT title.id, title.name, genre.name, type.name, director.name, length, rating
        FROM title JOIN genre JOIN type JOIN director
        ON title.genre_id = genre.id AND title.type_id = type.id
        AND title.director_id = director.id''')
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))  #can also just say values=data
    cursor.close()
    conn.close()

def Exit():
    result = tkMessageBox.askquestion('Python: Simple CRUD Applition', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

#==================================VARIABLES==========================================
IDNUMBER = StringVar()
TITLE = StringVar()
GENRE = StringVar()
TYPE = StringVar()
DIRECTOR = StringVar()
MINUTES = StringVar()
RATING = StringVar()

#==================================FRAME==============================================
Top = Frame(root, width=900, height=50, bd=8)
Top.pack(side=TOP)
Left = Frame(root, width=300, height=500, bd=8)
Left.pack(side=LEFT)
Right = Frame(root, width=600, height=500, bd=8, relief="raise")
Right.pack(side=RIGHT)
Forms = Frame(Left, width=300, height=500)
Forms.pack(side=TOP)
Buttons = Frame(Left, width=300, height=100, bd=8)
Buttons.pack(side=BOTTOM)

#==================================LABEL WIDGET=======================================
txt_apptitle = Label(Top, width=900, font=('arial', 24), text = "Python: Simple CRUD Application")
txt_apptitle.pack()
txt_mediaID = Label(Forms, text="ID Number:", font=('arial', 16), bd=15)
txt_mediaID.grid(row=0, stick="e")
txt_mediaTitle = Label(Forms, text="Title:", font=('arial', 16), bd=15)
txt_mediaTitle.grid(row=1, stick="e")
txt_mediaGenre = Label(Forms, text="Genre:", font=('arial', 16), bd=15)
txt_mediaGenre.grid(row=2, stick="e")
txt_mediaType = Label(Forms, text="Type:", font=('arial', 16), bd=15)
txt_mediaType.grid(row=3, stick="e")
txt_mediaDirector = Label(Forms, text="Director:", font=('arial', 16), bd=15)
txt_mediaDirector.grid(row=4, stick="e")
txt_mediaMinutes = Label(Forms, text="Minutes:", font=('arial', 16), bd=15)
txt_mediaMinutes.grid(row=5, stick="e")
txt_mediaRating = Label(Forms, text="Rating:", font=('arial', 16), bd=15)
txt_mediaRating.grid(row=6, stick="e")
txt_result = Label(Buttons)
txt_result.pack(side=TOP)

#==================================ENTRY WIDGET=======================================
mediaID = Entry(Forms, textvariable=IDNUMBER, width=30)
mediaID.grid(row=0, column=1)
mediaTitle = Entry(Forms, textvariable=TITLE, width=30)
mediaTitle.grid(row=1, column=1)
mediaGenre = Entry(Forms, textvariable=GENRE, width=30)
mediaGenre.grid(row=2, column=1)
mediaType = Entry(Forms, textvariable=TYPE, width=30)
mediaType.grid(row=3, column=1)
mediaDirector = Entry(Forms, textvariable=DIRECTOR, width=30)
mediaDirector.grid(row=4, column=1)
mediaMinutes = Entry(Forms, textvariable=MINUTES, width=30)
mediaMinutes.grid(row=5, column=1)
mediaRating = Entry(Forms, textvariable=RATING, width=30)
mediaRating.grid(row=6, column=1)

#==================================BUTTONS WIDGET=====================================
btn_create = Button(Buttons, width=10, text="Create", command=Create)
btn_create.pack(side=LEFT)
btn_read = Button(Buttons, width=10, text="Read", command=Read)
btn_read.pack(side=LEFT)
#btn_update = Button(Buttons, width=10, text="Update", state=DISABLED)
btn_update = Button(Buttons, width=10, text="Update", command=Update)
btn_update.pack(side=LEFT)
btn_delete = Button(Buttons, width=10, text="Delete", state=DISABLED)
btn_delete.pack(side=LEFT)
btn_exit = Button(Buttons, width=10, text="Exit", command=Exit)
btn_exit.pack(side=LEFT)

#==================================LIST WIDGET========================================
scrollbary = Scrollbar(Right, orient=VERTICAL)
scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
tree = ttk.Treeview(Right, columns=("ID", "Title", "Genre", "Type", "Director", "Minutes", "Rating"), selectmode="extended", height=500, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('ID', text="ID", anchor=W)
tree.heading('Title', text="Title", anchor=W)
tree.heading('Genre', text="Genre", anchor=W)
tree.heading('Type', text="Type", anchor=W)
tree.heading('Director', text="Director", anchor=W)
tree.heading('Minutes', text="Minutes", anchor=W)
tree.heading('Rating', text="Rating", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=30)
tree.column('#2', stretch=NO, minwidth=0, width=100)
tree.column('#3', stretch=NO, minwidth=0, width=100)
tree.column('#4', stretch=NO, minwidth=0, width=100)
tree.column('#5', stretch=NO, minwidth=0, width=100)
tree.column('#6', stretch=NO, minwidth=0, width=100)
tree.column('#7', stretch=NO, minwidth=0, width=100)
tree.pack()

#==================================INITIALIZATION=====================================
if __name__ == '__main__':
    Read()
    root.mainloop()

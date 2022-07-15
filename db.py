from email.policy import strict
from tkinter import *
import sqlite3

root = Tk()
root.title('Hola mundo: archivos')
root.geometry('400x500')
root.config(bg='#0f2027')

conn = sqlite3.connect('todo.db')

c = conn.cursor()

c.execute("""
    CREATE TABLE if not exists todo(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );
""")

conn.commit()


def remove(id):
    def _remove():
        c.execute('DELETE FROM todo WHERE id = ?', (id, ))
        conn.commit()
        render_todo()

    return _remove


def complete(id):  # Currying!
    def _complete():
        todo = c.execute('SELECT * from todo WHERE id = ?', (id, )).fetchone()
        c.execute('UPDATE todo SET completed = ? WHERE id = ?',
                  (not todo[3], id))
        conn.commit()
        render_todo()

    return _complete


def render_todo():
    rows = c.execute('SELECT * FROM todo').fetchall()

    for widget in frame.winfo_children():  # Eliminar en la pantalla los render
        widget.destroy()  # los mandas a destruir con esta funcion

    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = '#555555' if completed else 'black'
        l = Checkbutton(frame, text=description, fg=color, width=42,
                        anchor='w', command=complete(id))
        l.grid(row=i, column=0, sticky='w')
        btn = Button(frame, text='Eliminar', command=remove(id), bg='#BDB7B7')
        btn.grid(row=i, column=1)
        l.select() if completed else l.deselect()


def addTodo():
    todo = e.get()
    if todo:
        c.execute(
            """
        INSERT INTO todo (description, completed) VALUES (?, ?)
        """, (todo, False)
        )
        conn.commit()
        e.delete(0, END)
        render_todo()
    else:
        pass


l = Label(root, text='Tarea', bg='#BDB7B7')
l.config(font=18)
l.grid(row=0, column=0)

e = Entry(root, width=40, bg='#BDB7B7', fg='Black')
e.grid(row=0, column=1)

btn = Button(root, text='Agregar', command=addTodo, font=18, bg='#BDB7B7')
btn.grid(row=0, column=2)

frame = LabelFrame(root, text='Mis tareas', font=18,
                   bg='#c31432', fg='#FFFFFF', padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nswe', padx=5)

e.focus()

root.bind('<Return>', lambda x: addTodo())

render_todo()

root.mainloop()

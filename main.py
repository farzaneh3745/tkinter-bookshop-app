from tkinter import Label,Tk,Button,Entry
from tkinter.ttk import Treeview,Combobox
from DataAccess.book_data_access import get_book_list,delete_book,insert_book,get_book_by_id,update_book
from DataAccess.get_author_list import get_author_list
from DataAccess.publisher_data_access import get_publisher_list

window=Tk()
window.title("BookShop Application")

window.grid_columnconfigure(1,weight=1)
window.grid_columnconfigure(2,weight=1)
window.grid_columnconfigure(3,weight=1)
window.grid_rowconfigure(2,weight=1)

search_label=Label(window,text="Search : ")
search_label.grid(row=0,column=0,padx=10,pady=10,sticky='ew')

search_entry=Entry(window)
search_entry.grid(row=0,column=1,columnspan=3,padx=(0,10),pady=10,sticky='ew')

def search_button_clicked():
    load_treeview()

search_button=Button(window,text="Search",command=search_button_clicked)
search_button.grid(row=0,column=4,padx=(0,10),pady=10,sticky='ew')

def show_book_form(book_id=None):
    book_form=Tk()
    book_form.title("Create Book" if not book_id else "Update Book")

    title_label=Label(book_form,text="Book Title")
    title_label.grid(row=0,column=0,padx=10,pady=10,sticky='e')

    title_entry=Entry(book_form,width=70)
    title_entry.grid(row=0,column=1,padx=10,pady=10,sticky='w')

    price_label=Label(book_form,text="Price")
    price_label.grid(row=1,column=0,padx=10,pady=10,sticky='e')

    price_entry = Entry(book_form,width=70)
    price_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    author_label=Label(book_form,text="Author")
    author_label.grid(row=2, column=0,padx=10,pady=10,sticky='e')

    author_list=get_author_list()
    author_combobox_data=[]
    for author in author_list:
        author_combobox_data.append(f"{author.id}-{author.firstname}{author.lastname}")

    author_combo=Combobox(book_form,values=author_combobox_data,state="readonly")
    author_combo.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    publisher_label=Label(book_form,text="Publisher")
    publisher_label.grid(row=3, column=0,padx=10,pady=10,sticky='e')

    publisher_list=get_publisher_list()
    publisher_combobox_data=[]
    for publisher in publisher_list:
        publisher_combobox_data.append(f"{publisher.id}-{publisher.title}")

    publisher_combo=Combobox(book_form,values=publisher_combobox_data,state="readonly")
    publisher_combo.grid(row=3, column=1, padx=10, pady=10, sticky='w')

    if book_id:
        book=get_book_by_id(book_id)
        title_entry.insert(0,book.title)
        price_entry.insert(0,book.price)
        author_value=f"{book.id}-{book.author.firstname}{book.author.lastname}"
        author_combo.set(author_value)
        publisher_value=f"{book.publisher.id}-{book.publisher.title}"
        publisher_combo.set(publisher_value)

    def submit():
        book_title=title_entry.get()
        price=float(price_entry.get())
        author_id=int(author_combo.get().split('-')[0])
        publisher_id=int(publisher_combo.get().split('-')[0])

        if not book_id:
            insert_book(book_title,price,author_id,publisher_id)
        else:
            update_book(book_id,book_title,price,author_id,publisher_id)

        load_treeview()
        book_form.destroy()

    submit_button=Button(book_form,text="Submit",command=submit)
    submit_button.grid(row=4,column=0,padx=(0,10),pady=10,sticky='e')

create_button=Button(window,text="Create",command=show_book_form)
create_button.grid(row=1,column=1,padx=(0,10),pady=(0,10),sticky='ew')

def get_book_id():
    selected_row_id=int(book_treeview.selection()[0])
    show_book_form(selected_row_id)

update_button=Button(window,text="Update",command=get_book_id)
update_button.grid(row=1,column=2,padx=(0,10),pady=(0,10),sticky='ew')

def delete_button_clicked():
    deleted_id=int(book_treeview.selection()[0])
    delete_book(deleted_id)
    load_treeview()

delete_button=Button(window,text="Delete",command=delete_button_clicked)
delete_button.grid(row=1,column=3,padx=(0,10),pady=(0,10),sticky='ew')

book_treeview=Treeview(window,columns=('title','price','author','publisher'))
book_treeview.grid(row=2,column=0,columnspan=5,padx=(0,10),pady=(0,10),sticky='ewns')

book_treeview.heading('#0',text='#')
book_treeview.heading('title',text='Title')
book_treeview.heading('price',text='Price')
book_treeview.heading('author',text='Author')
book_treeview.heading('publisher',text='Publisher')
book_treeview.column("title", anchor='center')
book_treeview.column("price", anchor='center')
book_treeview.column("author", anchor='center')
book_treeview.column("publisher", anchor='center')

book_treeview.column("#0",width=40)
book_treeview.column("price",width=60)
book_treeview.column("title",width=360)

def load_treeview():
    row_number=1
    book_treeview.delete(*book_treeview.get_children())
    term=search_entry.get()
    if term:
        books = get_book_list(term)
    else:
        books=get_book_list()

    for book in books:
        book_treeview.insert("",
                             'end',
                             iid=book.id,
                             text=row_number,
                             values=(book.title,book.price,book.author.get_fullname(),book.publisher.title))
        row_number+=1

load_treeview()
window.mainloop()
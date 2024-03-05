import tkinter


def main():
    m = tkinter.Tk()
    m.geometry('1000x500')
    btn = tkinter.Button(m, text='Click me !', bd='5',
                         command=m.destroy)
    btn.pack(side='top')
    m.mainloop()


if __name__ == "__main__":
    main()

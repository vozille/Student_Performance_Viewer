from Tkinter import *
import ttk

ind = [
    "MECHANICAL ENGINEERING ",
    "ELECTRICAL ENGINEERING ",
    "CIVIL ENGINEERING ",
    "INSTRUMENTATION & ELECTRONICS ENGINEERING ",
    "COMPUTER SCIENCE & ENGINEERING ",
    "BIO TECHNOLOGY ",
    "INFORMATION TECHNOLOGY ",
    "TEXTILE ENGINEERING ",
    "FASHION TECHNOLOGY ",
    "BACHELOR OF ARCHITECTURE "]


class Redir(object):  # redirects stdout to text box

    def __init__(self, text_area):
        self.text_area = text_area

    def write(self, strg):
        self.text_area.insert(END, strg)
        self.text_area.see(END)


app = Tk()
file = '---'


def foo(branchVar):
    file = 'sample_' + branchVar[:-1] + '.csv'
    import csv
    with open(file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        rolls.delete(0, END)
        for i in reader:
            break
        for i in reader:
            rolls.insert(END, i[1] + ' -> ' + i[0])
    csvFile.close()


def getData():
    file = 'sample_' + branchVar.get()[:-1] + '.csv'
    currId = map(str, rolls.get(ACTIVE).split())
    studentData = []
    import csv
    with open(file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for i in reader:
            if i[1] == currId[0]:
                studentData = i

    data.delete(1.0, END)
    compare.delete(1.0, END)
    grade = ['O', 'E', 'A', 'B', 'C', 'D', 'F', 'S']
    data.insert(END, 'Name : ' + studentData[0] + '\n')
    data.insert(END, 'Regd No. : ' + studentData[1] + '\n')
    data.insert(END,'Branch : '+branchVar.get()+'\n')
    for i in grade:
        data.insert(END, i + ' -> ' + str(studentData.count(i)) + '\n')
    grade = []
    for i in range(2, len(studentData)):
        try:
            r = float(studentData[i])
            grade.append(r)
        except ValueError:
            pass
    for i in range(len(grade)):
        data.insert(END, 'SGPA Semester: ' + str(i + 1) +
                    ' -> ' + str(grade[i]) + '\n')


def getData2():
    file = 'sample_' + branchVar.get()[:-1] + '.csv'
    currId = map(str, rolls.get(ACTIVE).split())
    studentData = []
    import csv
    with open(file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for i in reader:
            if i[1] == currId[0]:
                studentData = i

    compare.delete(1.0, END)
    grade = ['O', 'E', 'A', 'B', 'C', 'D', 'F', 'S']
    compare.insert(END, 'Name : ' + studentData[0] + '\n')
    compare.insert(END, 'Regd No. : ' + studentData[1] + '\n')
    compare.insert(END,'Branch : '+branchVar.get()+'\n')
    for i in grade:
        compare.insert(END, i + ' -> ' + str(studentData.count(i)) + '\n')
    grade = []
    for i in range(2, len(studentData)):
        try:
            r = float(studentData[i])
            grade.append(r)
        except ValueError:
            pass
    for i in range(len(grade)):
        compare.insert(END, 'SGPA Semester: ' + str(i + 1) +
                       ' -> ' + str(grade[i]) + '\n')
def getData3():
    file = 'sample_' + branchVar.get()[:-1] + '.csv'
    currId = map(str, rolls.get(ACTIVE).split())
    studentData = []
    ids = []
    import csv
    with open(file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for i in reader:
            ids = i
            break
        for i in reader:
            if i[1] == currId[0]:
                studentData = i
    app2 = Tk()
    tb1 = Listbox(app2,width = 80,height = 25)
    tb2 = Listbox(app2,width = 80,height = 25)
    
    for i in range(2):
        tb1.insert(END,ids[i])
        tb2.insert(END,studentData[i])
    tb1.insert(END,'')
    tb2.insert(END,'')
    for i in range(2,len(ids)):
        tb1.insert(END,ids[i])
        tb2.insert(END,studentData[i])
        if 'SGPA' in ids[i]:
            tb1.insert(END,'')
            tb2.insert(END,'')
    tb1.pack(side = LEFT)
    tb2.pack(side = LEFT)
    app2.title("Details")
    app2.mainloop()

def getData_x(x):
    file = 'sample_' + branchVar.get()[:-1] + '.csv'
    currId = map(str, rolls.get(ACTIVE).split())
    studentData = []
    import csv
    with open(file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for i in reader:
            if i[1] == currId[0]:
                studentData = i

    data.delete(1.0, END)
    compare.delete(1.0, END)
    grade = ['O', 'E', 'A', 'B', 'C', 'D', 'F', 'S']
    data.insert(END, 'Name : ' + studentData[0] + '\n')
    data.insert(END, 'Regd No. : ' + studentData[1] + '\n')
    data.insert(END,'Branch : '+branchVar.get()+'\n')
    for i in grade:
        data.insert(END, i + ' -> ' + str(studentData.count(i)) + '\n')
    grade = []
    for i in range(2, len(studentData)):
        try:
            r = float(studentData[i])
            grade.append(r)
        except ValueError:
            pass
    for i in range(len(grade)):
        data.insert(END, 'SGPA Semester: ' + str(i + 1) +
                    ' -> ' + str(grade[i]) + '\n')


Label(
    app,
    text='Select Branch',
    font=(
        'Gothic Bank',
        14,
        "bold"),
    fg='white',
    bg='#010101') .grid(
    row=0,
    column=1)

rolls = Listbox(app, height=20, width=45)
data = Text(app, height=20, width=35)
rolls.bind('<Double-Button-1>',getData_x)
rolls.bind('<Return>',getData_x)
compare = Text(app, height=20, width=35)
branchVar = StringVar(app)
branchVar.set(ind[0])
branches = OptionMenu(app, branchVar, *ind, command=foo)

branches.config(
    bg='forest green',
    fg='white',
    font=(
        'Gothic Bank',
        14,
        "bold"),
    activebackground='gray',
    activeforeground='white')

Go = Button(app, text='Get Data', command=getData, width=15)
Go.config(font=('Gothic Bank', 14, "bold"),
          background='forest green', foreground='white')
Compare = Button(app, text='Compare', command=getData2)
Compare.config(font=('Gothic Bank', 14, "bold"),
               background='forest green', foreground='white')

Details = Button(app, text='Get Details', command=getData3)
Details.config(font=('Gothic Bank', 14, "bold"),
               background='forest green', foreground='white')

branches.grid(row=1, column=1)
rolls.grid(row=2, column=0)
data.grid(row=2, column=1)
compare.grid(row=2, column=2)
Go.grid(row=3, column=1)
Compare.grid(row=3, column=2)
Details.grid(row = 3, column = 0)
app.resizable(width=False, height=False)
app.mainloop()


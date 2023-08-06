import tkinter, json
import logging
from fpdf import FPDF
from tkinter.filedialog import askopenfile
from edupage_api import Edupage, EduStudent, BadCredentialsException, LoginDataParsingException


logging.basicConfig(filename='log.txt',
                    level= logging.DEBUG,
                    format= '%(levelname)s %(asctime)s - %(message)s')
logger = logging.getLogger()

f2 = open('textdata.json','r', encoding='utf-8')
file2 = json.load(f2)

try:
    with open('result.json') as f3:
        file3 = json.load(f3)
    logger.info('result.json bol najdeny a otvoreny')
except Exception:
    file3 = {"test": ""}
    with open('result.json', 'w') as f3:
        json.dump(file3, f3, ensure_ascii=False, indent=1)
    logger.warning('vytvoril sa novy result.json')

try:
    with open('configuration.json') as f1:
        file1 = json.load(f1)
        file1 = {"username": "", "password": "", "idclass": ""}
except Exception:
    file1 = {"username": "", "password":"", "idclass":""}
    with open('configuration.json', 'w') as f1:
        json.dump(file1, f1, ensure_ascii=False, indent=1)

root = tkinter.Tk()
WIDTH = 600
HEIGHT = 900
root.geometry('900x600')
root.title('Tlačové zostavy')

for row in range(22):
    root.grid_rowconfigure(row, minsize=20)
t_height = ((12/72)*2.54)*10

class App_:
    def __init__(self):
        self.root1 = tkinter.Tk()
        self.root1.geometry("240x130")
        self.root1.title('Login')
        self.root1.resizable(0, 0)

        self.root1.columnconfigure(0, weight=1)
        self.root1.columnconfigure(1, weight=3)
    def create_widgets(self):
        # username
        self.username_label = tkinter.Label(self.root1, text="Užívateľské meno:")
        self.username_label.grid(column=0, row=0, sticky=tkinter.W, padx=5, pady=5)

        self.username_entry = tkinter.Entry(self.root1)
        self.username_entry.grid(column=1, row=0, sticky=tkinter.E, padx=5, pady=5)

        # password
        self.password_label = tkinter.Label(self.root1, text="Heslo:")
        self.password_label.grid(column=0, row=1, sticky=tkinter.W, padx=5, pady=5)

        self.password_entry = tkinter.Entry(self.root1,  show="*")
        self.password_entry.grid(column=1, row=1, sticky=tkinter.E, padx=5, pady=5)

        # id of class
        self.id_label = tkinter.Label(self.root1, text="ID triedy:")
        self.id_label.grid(column=0, row=2, sticky=tkinter.W, padx=5, pady=5)

        self.id_entry = tkinter.Entry(self.root1)
        self.id_entry.grid(column=1, row=2, sticky=tkinter.E, padx=5, pady=5)

        # login button
        self.login_button = tkinter.Button(self.root1, text="Login",activebackground=col2, command=self.get_login)
        self.login_button.grid(column=1, row=4, sticky=tkinter.E, padx=5, pady=5)
        self.root1.mainloop()
    def get_login(self):
        global file1
        file1["password"] = self.password_entry.get()
        file1["username"] = self.username_entry.get()
        file1["idclass"] = self.id_entry.get()
        edupage_students()
        self.root1.destroy()

class PDF(FPDF):
    c = 0
    def lines(self):
        self.set_line_width(0.5)
        self.rect(15.0, 35.0, 180.0, 244.0)
        self.line(15.0, 41.0, 195.0, 41.0)

    def titles(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        self.set_xy(0.0, 0.0)
        self.set_font('DejaVu1', '', 14)
        self.cell(w=210.0, h=30.0, align='C',
                  txt="Katalógový list žiaka strednej školy - príloha", border=0)
        self.set_xy(15.0, 0.0)
        self.set_font('DejaVu2', '', 8)
        self.cell(w=0.0, h=52.0, align='L',
                  txt='Priezvisko:'+85*'.')
        self.set_xy(15.0, 0.0)
        self.cell(w=0.0, h=65.0, align='L',
                  txt='Dátum narodenia:' + 73 * '.')
        self.set_xy(105.0, 0.0)
        self.cell(w=0.0, h=52.0, align='L',
                  txt='Meno:' + 100 * '.')
        self.set_xy(105.0, 0.0)
        self.cell(w=0.0, h=65.0, align='L',
                  txt='Rodné číslo:' + 91 * '.')
        self.set_xy(0.0, 0.0)
        self.set_font('DejaVu1', '', 8)
        self.cell(w=210.0, h=77.0, align='C',
                  txt="Zápisy triedneho učiteľa (komisionálne skúšky, záujmové útvary, a podobne)",
                  border=0)

    def txt_writing(self, x, y, txts, color):
        self.color = color
        self.x = float(x)
        self.y = float(y)
        self.txts = txts
        self.set_xy(self.x, self.y)
        self.set_font('TimesNewRoman', '', 10)
        self.multi_cell(w=170.0, h=6.0, align='L',
                        txt=self.txts,
                        border=0)
        self.cell(w=170.0, h=6.0, align='R',
                  txt='_________', ln=1)
        self.cell(w=170.0, h=6.0, align='R',
                  txt='tr. učiteľ')
    def footer(self):
        if self.c == 1:
            logger.debug("zapisuje sa footer")
            self.set_y(-13.0)
            self.set_font('DejaVu2', '', 7)
            self.cell(w=0.0, h=5.0, align='L',
                      txt='    522 MŠVVaŠ SR / od 01. 09. 2018     ')
            self.cell(w=0.0, h=5.0, align='R',
                      txt='Katalógový list žiaka strednej školy - príloha     ')

dic = {'writeDate': 'dátum', 'reason':'dôvod', 'number':'číslo', 'firstDate':'od (dátum)', 'lastDate':'do (dátum)',
       'subject':'predmet', 'year':'rok', 'state&schoolname':'štát a meno školy', 'mark':'slovom (napr. dobrý)',
       'date':'dátum', 'class': 'trieda', 'lastyear':'rok', 'firstyear':'rok'}

results_dic = {}
genders = {}
students = []

def startapp():
    global button_, students, file3
    try:
        file_ = askopenfile(parent=root, mode='r', title='Open file', filetype=[('TXT file', '*.txt')])
        fr = open(file_.name)
        logger.info('textový súbor bol načítaný')
    except Exception:
        logger.critical('problem so súborom')
    file_ = fr.readlines()
    if file_[0][-1] != 'M' and file_[0][-1] != 'F':
        students = [i.replace('\n', '') for i in file_]
    else:
        for i in file_:
            i = i.replace('\n', '')
            i = i.split(' ')
            if i[-1] == 'M' or i[-1] == 'F':
                students.append(' '.join([i[0], i[-2]]))
                genders[' '.join([i[0], i[-2]])] = i[-1]
    fr.close()
    button_.destroy()
    button_1.destroy()
    display_buttons()
    display_listbox()
    for k in students:
        file3[k] = file3.get(k, "")
    with open('result.json', 'w') as f3:
        json.dump(file3, f3, ensure_ascii=False, indent=1)


z = [file2[k]['shortdesc'] for k in file2.keys()]

col1 = "#DCF0F2"
col2 = "#48f820"
col3 = "#C0C0C0"

text_widgets = []

def get_loged_in():
    global file1
    app = App_()
    app.create_widgets()

def edupage_students():
    global file1, students, genders
    p = 0
    edupage = Edupage("gymmt", file1["username"], file1["password"])
    try:
        edupage.login()
    except BadCredentialsException:
        logger.warning("Wrong username or password!")
        p = 1
    except LoginDataParsingException:
        logger.warning("Try again or open an issue!")
        p = 1
    if p == 0:
        students_ = edupage.get_students()
        students_.sort(key=EduStudent.__sort__)
        for student in students_:
            if student.class_id == int(file1["idclass"]):
                students.append(student.fullname)
                genders[student.fullname] = student.gender
        button_.destroy()
        button_1.destroy()
        display_buttons()
        display_listbox()
        for k in students:
            file3[k] = file3.get(k, "")
        with open('result.json', 'w') as f3:
            json.dump(file3, f3, ensure_ascii=False, indent=1)


def displaying_text(row, text):
    global widgets, inputsI, text_widgets, student_names
    if len(text) > 2:
        text1 = text.split(' ')
    else:
        text1 = text[0].split(' ')
    poc, row1_ = 0, 0
    text_box = tkinter.Text(root, height=10, width=50, wrap=tkinter.WORD)
    text_box.tag_configure('center', justify='center')
    text_box.tag_add('center', 1.0, 'end')
    text_box.grid(row=row, column=2, rowspan=5, columnspan=3, sticky='WE')
    for q in range(len(text1)):
        poc += len(text1[q]) + 1
        if '{' in text1[q]:
            if '.' in text1[q] or ',' in text1[q]:
                text_box.insert(tkinter.END, '__'+str(inputsI[text1[q][:-1]])+'.__ '+text1[q][-1]+' ')
            else:
                text_box.insert(tkinter.END, '__'+str(inputsI[text1[q]])+'.__ ')
        elif '\\n' not in text1[q]:
            text_box.insert(tkinter.END, text1[q]+' ')
        elif '\\n' in text1[q]:
            w = text1[q].replace('\\n', '\n')
            text_box.insert(tkinter.END, w)
    widgets.append(text_box)
    text_widgets.append(text_box)

def displaying_existing():
    global checkbx_results, results_dic, file3, student_name, text_widgets, row
    for l in text_widgets:
        l.destroy()
    if (list(checkbx_results.values())).count(1) == 1:
        for w in checkbx_results.keys():
            if checkbx_results[w] == 1:
                for k in file3[student_name]:
                    if file3[student_name][k]['shortdesc'] == w[:w.index(',')]:
                        displaying_text(row+1, file3[student_name][k]['text'])
                        button5 = tkinter.Button(root, text='Vymazať z pamäte', command=lambda k=k: delete_item(k), bg=col2,
                                                 height=1, width=15)
                        button5.grid(row=row + 5, column=5, columnspan=2, rowspan=2)
                        widgets.append(button5)
                        checkbx_widgets.append(button5)


def delete_item(c):
    global student_name, file3, text_widgets
    del file3[student_name][c]
    with open('result.json', 'w') as f3:
        json.dump(file3, f3, ensure_ascii=False, indent=1)
    for l in text_widgets:
        l.destroy()
    display_checkbox()


def button_function(button_id):
    global buttons, clicked, student_name, checkbx_widgets, text_widgets, widgets, student_names
    for g in widgets:
        g.destroy()
    student_name = ''
    student_names.clear()
    x = [j.configure(bg="white") for j in buttons]
    button_id.configure(bg=col2)
    student_name += button_id.cget('text')
    logger.info('meno študenta: '+student_name)
    display_checkbox()

def multiple_st(event):
    global buttons, clicked, student_names, checkbx_widgets, student_name
    for l in checkbx_widgets:
        l.destroy()
    if len(student_name) > 0 and student_name not in student_names:
        student_names.append(student_name)
    button_id = event.widget
    if button_id.cget('bg') == 'white':
        button_id.configure(bg=col2)
        student_names.append(button_id.cget('text'))
    else:
        button_id.configure(bg='white')
        if button_id.cget('text') in student_names:
            student_names.remove(button_id.cget('text'))
    logger.info('mená študentov: '+ ', '.join(student_names))


buttons = []
row = 0
row_bt = 0
def display_buttons():
    global row, row_bt
    row = -1
    for i in range(len(students)):
        if i%6 == 0:
            row += 1
        button1 = tkinter.Button(root, text=students[i], bg='white', height=1, width= 20)
        button1.config(command=lambda b=button1: button_function(b)) #c=i: clicked.append(buttons[c].cget("text")) nothing))
        buttons.append(button1)
        button1.grid(row=row, column=i % 6)
        button1.bind('<Button-3>', multiple_st)
    row_bt = row + 1

checkbx_results, form_result = {}, tkinter.IntVar()
dic_ch = {}



def write_pdf():
    global checkbx_results, results_dic, file3, student_name
    xx, yy = 20.0, 45.0
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_font('DejaVu1', '', r'C:\Users\NAY\Desktop\dejavu-sans\ttf\DejaVuSansCondensed-Bold.ttf', uni=True)
    pdf.add_font('DejaVu2', '', r'C:\Users\NAY\Desktop\dejavu-sans\ttf\DejaVuSansCondensed.ttf', uni=True)
    pdf.add_font('TimesNewRoman', '', r'C:\Users\NAY\Desktop\times-new-roman-cufonfonts\times.ttf', uni=True)
    pdf.set_text_color(0, 0, 0)
    if checkbx_results['form_result'] == 1:
        pdf.c = 1
        pdf.add_page()
        pdf.lines()
        n = student_name.split(' ')
        pdf.titles(n[0], n[1]) #nie je mozne lebo niektori ziaci maju dve priezviska
    else:
        pdf.c = 0
        pdf.add_page()
    del checkbx_results['form_result']
    if file3[student_name] != "":
        for w in checkbx_results.keys():
            if checkbx_results[w] == 1:
                color = 0, 0, 0
                pdf.set_text_color(0, 0, 0)
            else:
                color = 255, 0, 0
                pdf.set_text_color(255, 255, 255)
            for v in file3[student_name]:
                if file3[student_name][v]['shortdesc'] == w[:(w.index(','))]:
                    text1 = (file3[student_name][v]['text']).replace('\\n', '\n')
                    pdf.txt_writing(xx, yy, text1, color)
                    last_y = pdf.get_y()
                    yy = last_y + 10
            pdf.set_text_color(0, 0, 0)

    pdf.output('output.pdf', 'F')

def checkbx_selection():
    global file3, student_name, checkbx_results, dic_ch, form_result
    checkbx_results.clear()
    for r in dic_ch.keys():
        checkbx_results[r] = dic_ch[r].get()
    checkbx_results['form_result'] = form_result.get()

def display_checkbox():
    global student_name, file3, widgets, row_bt, dic_ch, checkbx_widgets, form_result, zframe
    dic_ch, form_result = {}, tkinter.IntVar()
    # row = row_bt + 1
    zframe.columnconfigure(0, minsize=100, weight=1)
    zframe.columnconfigure(1, minsize=100, weight=1)
    row_ = row_bt + 2
    logger.debug('riadok (display_checkbox) ' + str(row))
    for l in checkbx_widgets:
        l.destroy()
    if student_name != '' and file3[student_name] != "":
        for r in file3[student_name]:
            dic_ch[file3[student_name][r]['shortdesc']+', '+file3[student_name][r]['writeDate']] = tkinter.IntVar()
    for s in dic_ch.keys():
        checkbox1 = tkinter.Checkbutton(zframe, text=s[0:s.index('-')] + s[s.index(','):] if '-' in s else s,
                                        variable=dic_ch[s],
                                        onvalue=1, offvalue=0, command=checkbx_selection, bg=col3)
        checkbox1.grid(row=row_, column=0, columnspan=2, sticky='WNS')
        row_ += 1
        widgets.append(checkbox1)
        checkbx_widgets.append(checkbox1)
    checkbox2 = tkinter.Checkbutton(zframe, text='Tlačiť aj s formulárom', variable=form_result,  onvalue=1, offvalue=0, command=checkbx_selection, bg=col3)
    checkbox2.grid(row=row_, column=0, columnspan=2, sticky='WNS')
    widgets.append(checkbox2)
    checkbx_widgets.append(checkbox2)
    button4 = tkinter.Button(zframe, text='Zobraziť znenie', command=displaying_existing, bg=col2, height=1, width=15)
    button4.grid(row=row_ + 1, column=0)
    button3 = tkinter.Button(zframe, text='Tlačiť', command= write_pdf, bg=col2, height=1, width= 15)
    button3.grid(row=row_+1, column=1, sticky='E', padx=10)
    widgets.append(button3)
    checkbx_widgets.append(button3)
    widgets.append(button4)
    checkbx_widgets.append(button4)

listbx = ''

def display_listbox():
    global row, z, listbx, zframe
    zframe = tkinter.LabelFrame(root, bg=col3)
    zframe.grid(row=row + 1, column=0, columnspan=2, rowspan=20, sticky='NSWE')
    row += 2 #4
    logger.debug('riadok (display_listbox) ' + str(row))
    yscrollbar = tkinter.Scrollbar(root)
    yscrollbar.grid(column=5, row=row, sticky='NSW', rowspan=3)

    label = tkinter.Label(root, text="Vyberte z možností :  ", font=("Calibri", 12), pady=10)
    label.grid(column=2, row=row-1,  columnspan=2, sticky='W')
    listbx = tkinter.Listbox(root, selectmode="single", yscrollcommand=yscrollbar.set, selectbackground=col2)
    listbx.grid(column=2, row=row, columnspan=3, sticky='WE', rowspan=3)
    for each_item in range(len(z)):
        listbx.insert(tkinter.END, z[each_item])
        listbx.itemconfig(each_item, bg='white')
    yscrollbar.config(command=listbx.yview)
    row += 3
    logger.debug('riadok (display_checkbox) ' + str(row))
    button2 = tkinter.Button(root, text='Zapíš', bg=col3, height=1, width=12, command=processing)
    button2.grid(row=row + 1, column=5)

text = ''
inputs, inputsI, widgets = {}, {}, []
student_name = ''
checkbx_widgets = []
student_names = []

def submit_rd(widgets):
    global text, inputs, inputsI, file3, results_dic, student_names
    if (len(list(genders.keys())) == 0 and len(student_names) > 1) or (len(student_names) <= 1 and len(list(genders.keys())) != 0) or (len(student_names) <= 1 and len(list(genders.keys())) == 0):
        for k, v in inputs.items():
            text = text.replace('{'+k+'}', v.get())
            results_dic[k] = v.get()
            v.set("")
        results_dic['text'] = text
        results_dic1 = results_dic.copy()
        if len(student_names) <= 1:
            if file3[student_name] == "":
                file3[student_name] = {}
                file3[student_name]['1'] = {}
                file3[student_name]['1'] = results_dic1
                logger.info('(submit_rd)'+student_name + results_dic1['shortdesc'])
            else:
                c = str(int(list(file3[student_name].keys())[-1]) + 1)
                file3[student_name][c] = {}
                file3[student_name][c] = results_dic1
                logger.info('(submit_rd)'+ student_name+ results_dic1['shortdesc'])
        else:
            for sn in student_names:
                if file3[sn] == "":
                    file3[sn] = {}
                    file3[sn]['1'] = {}
                    file3[sn]['1'] = results_dic1
                    logger.info('(submit_rd)' + sn + results_dic1['shortdesc'])
                else:
                    c = str(len(file3[sn].keys()) + 1)
                    file3[sn][c] = {}
                    file3[sn][c] = results_dic1
                    logger.info('(submit_rd)'+ sn + results_dic1['shortdesc'])
    else: #len viac ziakov a genders
        for sn in student_names:
            if genders[sn] == 'M':
                text1 = text[0]
            else:
                text1 = text[1]
            for k, v in inputs.items():
                text1 = text1.replace('{' + k + '}', v.get())
                results_dic[k] = v.get()
            results_dic['text'] = text1
            results_dic1 = results_dic.copy()
            if file3[sn] == "":
                file3[sn] = {}
                file3[sn]['1'] = {}
                file3[sn]['1'] = results_dic1
                logger.info('(submit_rd)' + sn + results_dic1['shortdesc'])
            else:
                c = str(len(file3[sn].keys()) + 1)
                file3[sn][c] = {}
                file3[sn][c] = results_dic1
                logger.info('(submit_rd)'+ sn + results_dic1['shortdesc'])
        for k, v in inputs.items():
            v.set("")
    for l in widgets:
        l.destroy()
    display_checkbox()
    with open('result.json', 'w') as f3:
        json.dump(file3, f3, ensure_ascii=False, indent=1)


def listbx_selection():
    global results_dic, student_name, listbx
    for i in listbx.curselection():
        listbx_results = listbx.get(i)
    results_dic['shortdesc'] = listbx_results
    return listbx_results


def processing():
    global text, reason, date, inputs, inputsI, row, widgets, dic, student_names, student_name, text_widgets
    if len(student_names) <= 1:
        if len(widgets) != 0:
            for l in widgets:
                l.destroy()
    text, row_, count = '', row, 1
    logger.debug('riadok (processing) ' + str(row_))
    widgets.clear()
    inputs.clear()
    inputsI.clear()
    display_checkbox()
    listbx_results = listbx_selection()
    for k, v in file2.items():
        if v['shortdesc'] == listbx_results:
            for j in v['Inputs'].keys():
                inputs[j] = tkinter.StringVar()
                inputsI['{' + j + '}'] = count
                label1 = tkinter.Label(root, text=str(count) + '. ' + dic[j], font=('calibre', 8))
                label1.grid(row=row_, column=2, sticky='E')
                entry1 = tkinter.Entry(root, textvariable=inputs[j], font=('calibre', 8))
                entry1.grid(row=row_, column=3, columnspan=2, sticky='WE')
                widgets.append(label1)
                widgets.append(entry1)
                row_ += 1
                logger.debug('riadok (processing) ' + str(row_))
                count += 1
            if len(student_names) <= 1:
                if len(list(genders.keys())) > 1:
                    if genders[student_name] == 'F':
                        text += v['longdescF']
                    else:
                        text += v['longdescM']
                else:
                    text += v['longdescM']
            else:
                if len(list(genders.keys())) > 1:
                    text = []
                    text.append(v['longdescM'])
                    text.append(v['longdescF'])
                else:
                    text += v['longdescM']
    sub_btn = tkinter.Button(root, text='Uložiť', command=lambda w=widgets: submit_rd(w), width=12, bg=col3)
    widgets.append(sub_btn)
    sub_btn.grid(row=row_, column=2, sticky='W', padx=10)
    displaying_text(row_+1, text)

button_ = tkinter.Button(root, text='Načítaj súbor', bg='white', activebackground=col2, height=1, width=30, command=startapp)
button_.grid(row=0, column=4, columnspan=4, rowspan=2 ,sticky='NSWE')
button_1 = tkinter.Button(root, text='Prihlás sa na Edupage', bg='white',activebackground=col2, height=1, width=30, command=get_loged_in)
button_1.grid(row=2, column=4, columnspan=4, rowspan=2 ,sticky='NSWE')

f3.close()
f2.close()
root.mainloop()

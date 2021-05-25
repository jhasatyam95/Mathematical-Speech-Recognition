
#---------------------------------------Importing modules---------------------------------------------------#

import speech_recognition as sr
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font,colorchooser,filedialog,messagebox
import os

import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
# from word2number import w2n
import threading



#---------------------------------------window formation---------------------------------------------------#

main_application = tk.Tk()
main_application.geometry("1200x600")
main_application.title("Mathematical Term and Word Recognizer")
main_application.iconbitmap("F:\\BE_Project\\assets\\icon\\icon.ico")

style = ttk.Style()
style.theme_use('winnative')

main_menu = tk.Menu()

#---------------------------------------File menu icons---------------------------------------------------#
new_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\new.png")
open_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\open.png")
save_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\save.png")
save_as_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\saveas.png")
exit_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\exit.png")

#---------------------------------------Edit menu icons---------------------------------------------------#
undo_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\undo.png")
redo_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\redo.png")
copy_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\copy.png")
paste_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\paste.png")
cut_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\cut.png")
clear_all_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\clearall.png")
find_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\find.png")

#---------------------------------------View menu icons---------------------------------------------------#
toolbar_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\toolbar.png")
statusbar_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\statusbar.png")

#---------------------------------------theme menu icons---------------------------------------------------#
light_default_icon = tk.PhotoImage(file='F:\\BE_Project\\assets\\icon\\lightdefault.png')
light_plus_icon = tk.PhotoImage(file='F:\\BE_Project\\assets\\icon\\lightplus.png')
dark_icon = tk.PhotoImage(file='F:\\BE_Project\\assets\\icon\\dark.png')
red_icon = tk.PhotoImage(file='F:\\BE_Project\\assets\\icon\\red.png')
monokai_icon = tk.PhotoImage(file='F:\\BE_Project\\assets\\icon\\monokai.png')
night_blue_icon = tk.PhotoImage(file='F:\\BE_Project\\assets\\icon\\nightblue.png')
color_theme = tk.Menu(main_menu, tearoff=False)

theme_choice = tk.StringVar()
color_icons = (light_default_icon, light_plus_icon, dark_icon, red_icon, monokai_icon, night_blue_icon)

color_dict = {
    'Light Default ' : ('#000000', '#ffffff'),
    'Light Plus' : ('#474747', '#e0e0e0'),
    'Dark' : ('#c4c4c4', '#2d2d2d'),
    'Red' : ('#2d2d2d', '#ffe8e8'),
    'Monokai' : ('#d3b774', '#474747'),
    'Night Blue' :('#ededed', '#6b9dc2')
}

#---------------------------------------making menubar---------------------------------------------------#

file = tk.Menu(main_menu,tearoff=False)
main_menu.add_cascade(label = "File",menu=file)

edit = tk.Menu(main_menu,tearoff=False)
main_menu.add_cascade(label = "Edit",menu=edit)

view = tk.Menu(main_menu,tearoff=False)
main_menu.add_cascade(label = "View",menu=view)

color_theme = tk.Menu(main_menu,tearoff=False)
main_menu.add_cascade(label = "Theme",menu=color_theme)

#---------------------------------------creating label---------------------------------------------------#

tool_bar_label = ttk.Label(main_application)
tool_bar_label.pack(side=tk.TOP,fill=tk.X)

#---------------------------------------Font family---------------------------------------------------#

font_tuple=tk.font.families()
font_family=tk.StringVar()
font_box=ttk.Combobox(tool_bar_label,width=30,textvariable=font_family,state="readonly")
font_box["values"]=font_tuple
font_box.current(font_tuple.index("Arial"))
font_box.grid(row=0,column=0,padx=5,pady=5)

#---------------------------------------Size selection---------------------------------------------------#

size_variable=tk.IntVar()
font_size=ttk.Combobox(tool_bar_label,width=20,textvariable=size_variable,state="readonly")
font_size["values"]=tuple(range(8,100,2))
font_size.current(4)
font_size.grid(row=0,column=1,padx=5,pady=5)

#---------------------------------------creating Bold,Italic,Underline,colorpicker,paragraph alignments---------------------------------------------------#
#---------------------------------------bold---------------------------------------------------#

bold_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\bold.png")
bold_button=Button(tool_bar_label,image=bold_icon,bd=0)
bold_button.grid(row=0,column=2,padx=5,pady=5)

#---------------------------------------italic---------------------------------------------------#

italic_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\italic.png")
italic_button=Button(tool_bar_label,image=italic_icon,bd=0)
italic_button.grid(row=0,column=3,padx=5,pady=5)

#---------------------------------------underline---------------------------------------------------#

u_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\underline.png")
u_button=Button(tool_bar_label,image=u_icon,bd=0)
u_button.grid(row=0,column=4,padx=5,pady=5)

#---------------------------------------colorpicker---------------------------------------------------#

cp_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\colorwheel.png")
cp_button=Button(tool_bar_label,image=cp_icon,bd=0)
cp_button.grid(row=0,column=5,padx=5,pady=5)

#---------------------------------------left---------------------------------------------------#

L_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\leftpara.png")
L_button=ttk.Button(tool_bar_label,image=L_icon)
L_button.grid(row=0,column=6,padx=5,pady=5)

#---------------------------------------right---------------------------------------------------#

C_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\centerpara.png")
C_button=Button(tool_bar_label,image=C_icon)
C_button.grid(row=0,column=7,padx=5,pady=5)

#---------------------------------------center---------------------------------------------------#

R_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\rightpara.png")
R_button=Button(tool_bar_label,image=R_icon)
R_button.grid(row=0,column=8,padx=5,pady=5)



#========================<Normal Specch Recognition system>=======================>

def speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        text_editor.insert(tk.END,"Listening...")
        audio = r.listen(source)
        text_editor.delete(1.0,tk.END)

        try:
            speech = r.recognize_google(audio)
            text_editor.insert(tk.END,speech)
                
            
        except Exception as e:
            print("Error: " + str(e))

#========================<Math Specch Recognition system>=======================>

def math():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        text_editor.insert(tk.END,"Listening...") #display Listening in text editor
        L = text_editor.get(1.0,"end")
        audio = r.listen(source)
        text_editor.delete("1.0",tk.END)
        text_editor.insert(tk.END, L.replace("Listening...","")) #remove Listening in text editor

        try:
            speech = r.recognize_google(audio)
            
           
            SUP = {ord(c): ord(t) for c, t in zip(u"0123456789abcdefghijklmnopqrstuvwxyz+-", u"⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖᑫʳˢᵗᵘᵛʷˣʸᶻ⁺⁻")} #zip of superscript
            SUB = {ord(c): ord(t) for c, t in zip(u"0123456789aehijklmnoprstuvx", u"₀₁₂₃₄₅₆₇₈₉ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ")}  #zip of subscript
            
            optr=[] # define empty list
            
            #<============================== Define power function ===================================>
            
            def power():
                # both = filtered_sentence
                # # both = [" ".join([wnl.lemmatize(word) for word in sentence.split(" ")]) for sentence in both]
                
                
                # for op in both:
                #     si = op.replace('plus','+').replace('add','+').replace('multiply','x').replace('into','x').replace('minus','-').replace('squared','\u00b2').replace('square','\u00b2').replace('equal','=').replace('equals','=').replace('cube','\u00b3').replace('+','+').replace('-','-').replace('zero','0').replace('one','1').replace('two','2').replace('three','3').replace('four','4').replace('five','5').replace('six','6').replace('seven','7').replace('eight','8').replace('nine','9').replace('theta','\u03B8')
                #     #print(si)
                #     optr.append(si)
                
                power=[]
                for n,i in enumerate(optr):
                    if i == 'power' or i == 'raise':
                        power.append(n)
                        optr[n] = ''
                print(power)
                print(optr)
                for x in power:
                    for n,i in enumerate(optr[x:]):
                        if i == 'stop':
                            optr[n+x] = ''
                            break
                        for j in range(x+1,n+x+1):
                            optr[j] = optr[j].translate(SUP)    
                # print(filtered_sentence)
                #print('only power')
                print(optr)
                print(optr)
                # if 'base' in optr:
                #     base()
                # print(PowBrack)
                eq = ''.join(optr)
                print(eq)
                text_editor.insert(tk.END,eq)
                
            #<============================== Define Bracket function ===================================>
            
            def bracket():
                # both = filtered_sentence
                # # both = [" ".join([wnl.lemmatize(word) for word in sentence.split(" ")]) for sentence in both]
                
                
                # for x in both:
                #     si = x.replace('plus','+').replace('add','+').replace('multiply','x').replace('into','x').replace('minus','-').replace('squared','\u00b2').replace('square','\u00b2').replace('equal','=').replace('equals','=').replace('cube','\u00b3').replace('+','+').replace('-','-').replace('vi','6')
                #     si = x.replace('zero','0').replace('one','1').replace('two','2').replace('three','3').replace('four','4').replace('five','5').replace('six','6').replace('seven','7').replace('eight','8').replace('nine','9')
                #     #print(si)
                #     optr.append(si)
                
                
                bracket=[]
                for n,i in enumerate(optr):
                    if i == "bracket":
                        bracket.append(n)
                        optr[n] = "("
                print(optr)
                for x in bracket:
                    for n,i in enumerate(optr[x:]):
                        if i == "stop":
                            optr[n+x] = ")"
                # print('only Bracket')
                print(optr)
                # print(PowBrack)
                
                # if 'base' in optr:
                #     base()
                eq = ''.join(optr)
                print(eq)
                text_editor.insert(tk.END,eq)
            
            #<============================== Define BracketPower function ===================================>
            
            def bracketPower():
                # both = filtered_sentence
                # # both = [" ".join([wnl.lemmatize(word) for word in sentence.split(" ")]) for sentence in both]
                
                
                # for op in both:
                #     si = op.replace('plus','+').replace('add','+').replace('multiply','x').replace('into','x').replace('minus','-').replace('squared','\u00b2').replace('square','\u00b2').replace('equal','=').replace('equals','=').replace('cube','\u00b3').replace('+','+').replace('-','-').replace('zero','0').replace('one','1').replace('two','2').replace('three','3').replace('four','4').replace('five','5').replace('six','6').replace('seven','7').replace('eight','8').replace('nine','9')
                #     #print(si)
                #     optr.append(si)
                
                PowBrack = []
                for n,i in enumerate(optr):
                    if i == 'bracket':
                        optr[n] = '('
                    elif i == "stop":
                        optr[n] = ")"
                    elif i == 'power' or i == 'raise':
                        optr[n] = ''
                        PowBrack.append(n)
                for x in PowBrack:
                    for n,i in enumerate(optr[x:]):
                        if i == ')':
                            optr[n+x] = ''
                            break
                        for j in range(x+1,n+x+1):               
                            optr[j] = optr[j].translate(SUP)
                print(optr)
                # print(PowBrack)
                
                # if 'base' in optr:
                #     base()
                eq = ''.join(optr)
                print(eq)
                text_editor.insert(tk.END,eq)
            
            #<============================== Define base function ===================================>
            
            # def base():
            #     base = []
            #     for n,i in enumerate(optr):
            #         if i == 'base':
            #             base.append(n)
            #             optr[n] = ''
            #     print(base)
            #     print(optr)
            #     for x in base:
            #         for n,i in enumerate(optr[x:]):
            #             if i == 'stop':
            #                 optr[n+x] = ''
            #                 break
            #             for j in range(x+1,n+x+1):
            #                 optr[j] = optr[j].translate(SUB)    
            #     # print(filtered_sentence)
            #     #print('only power')
            #     print(optr)
            #     # print(PowBrack)
            #     eq = ''.join(optr)
            #     print(eq)        

            stop_words = set(stopwords.words('english'))

            word_data = speech
            word_data = word_data.lower()
            print(word_data)
            wnltk_tokens = nltk.word_tokenize(word_data)

            stop_words = set(stopwords.words('english')) 
            stop_words = set(stopwords.words('english')) - set(['y', 'a','d','into'])
            word_tokens =  wnltk_tokens

            filtered_sentence = [w for w in word_tokens if not w in stop_words]  

            filtered = []  
            for w in word_tokens:  
                if w not in stop_words:  
                    filtered.append(w)  

            # print(word_tokens)  
            for n,i in enumerate(filtered):
                if i == "(":
                    filtered[n] = "bracket"
                if i == ")":
                    filtered[n] = "bracket"
            
            print(filtered)
            for op in filtered:
                    si = op.replace('plus','+').replace('add','+').replace('multiply','x').replace('into','x').replace('minus','-').replace('integration','\u222B').replace('factorial','\u0021').replace('squared','\u00b2').replace('square','\u00b2').replace('equal','=').replace('equals','=').replace('cube','\u00b3').replace('+','+').replace('-','-').replace('zero','0').replace('one','1').replace('two','2').replace('three','3').replace('four','4').replace('five','5').replace('six','6').replace('seven','7').replace('eight','8').replace('nine','9').replace('theta','\u03B8').replace('10','tan').replace('[','\u00b2(').replace(']','stop')
                    #print(si)
                    optr.append(si)
            if 'raise' in optr and not 'bracket' in optr or 'power' in optr and not 'bracket' in optr:
                power()
            elif 'bracket' in  optr and not 'raise' in optr and not 'power' in optr:
                bracket()
            elif 'bracket' and 'power' or 'raise' in optr:
                bracketPower()
            else:
                eq = ''.join(optr)
                print(eq)
                text_editor.insert(tk.END,eq)
           

            
                
            
        except Exception as e:
            print("Error: " + str(e))
    
#---------------------------------------Math button---------------------------------------#

speech_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\function.png")
speech_button=Button(tool_bar_label,image=speech_icon,bd=0,command=lambda:threading.Thread(target=math).start(),activebackground = '#c1bfbf',overrelief = 'groove')
speech_button.grid(row=0,column=11,padx=5,pady=5)

#---------------------------------------normal button---------------------------------------#
Nspeech_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\speech.png")
Nspeech_button=Button(tool_bar_label,image=Nspeech_icon,bd=0,command=lambda:threading.Thread(target=speech).start(),activebackground = '#c1bfbf')
Nspeech_button.grid(row=0,column=9,padx=5,pady=5)


#---------------------------------------def for root---------------------------------------#
def root_btn():
    box = tk.Tk()
    box.geometry("800x500")
    box.configure(bg='white')
    box.title("root & fraction")
    label = Label(box,text="follow these steps before using the software",bg='white')
    label.pack()


#---------------------------------------def for help---------------------------------------#
def help_btn():
    
    global helpsection
    helpsection = tk.Toplevel(main_application)
    helpsection.geometry("1100x650")
    helpsection.configure(bg='white')
    helpsection.title("HELP")
    book  = ttk.Notebook(helpsection)
    book.pack(fill="both", expand = True)
    
    frame0 = Frame(book,width=1100,height=650,bg="white")
    frame1 = Frame(book,width=1100,height=650,bg="white")
    frame2 = Frame(book,width=1100,height=650,bg="white")
    frame3 = Frame(book,width=1100,height=650,bg="white")

    frame0.pack(fill = "both", expand = True)
    frame1.pack(fill = "both" ,expand = True)
    frame2.pack(fill = "both", expand = True)
    frame3.pack(fill = "both", expand = True)

    book.add(frame0,text="Basic information")
    book.add(frame1,text="Algebraic")
    book.add(frame2,text="Trigonometric")
    book.add(frame3,text="Integration")
    
    global basic
    basic = tk.PhotoImage(file="F:\\BE_Project\\assets\\icon\\basic.png")
    basiclabel = Label(frame0,image=basic)
    basiclabel.grid(row=0,column=0)
    
    global algebra
    algebra = tk.PhotoImage(file="F:\\BE_Project\\assets\\icon\\algebra.png")
    algebralabel = Label(frame1,image=algebra)
    algebralabel.grid(row=0,column=0)
    
    global trigo
    trigo = tk.PhotoImage(file="F:\\BE_Project\\assets\\icon\\trigo.png")
    trigolabel = Label(frame2,image=trigo)
    trigolabel.grid(row=0,column=0)
    
    global int
    int = tk.PhotoImage(file="F:\\BE_Project\\assets\\icon\\int.png")
    intlabel = Label(frame3,image=int)
    intlabel.grid(row=0,column=0)
    
    
    
#---------------------------------------help---------------------------------------#
help_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\help.png")
help_button=Button(tool_bar_label,image=help_icon,bd = 0,command=help_btn)
help_button.grid(row=0,column=10)

# hover1 = HoverText(help_button, 'Help')

#---------------------------------------Root---------------------------------------#
root_icon = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\root.png")
root_button=Button(tool_bar_label,image=root_icon,bd = 0,command=root_btn)
root_button.grid(row=0,column=13)

#---------------------------------------textBOX---------------------------------------#
text_editor=tk.Text(main_application,undo=True)
text_editor.config(wrap="word",relief=tk.FLAT)

scroll_bar=tk.Scrollbar(main_application)
text_editor.focus_set()
scroll_bar.pack(side=tk.RIGHT,fill=tk.Y)
text_editor.pack(fill=tk.BOTH,expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

#---------------------------------------making status bar---------------------------------------#

status_bars=ttk.Label(main_application,text="Status Bar")
status_bars.pack(side=tk.BOTTOM)

text_change=False

def change_word(event=None):
    global text_change
    if text_editor.edit_modified():
        text_change=True
        word = len(text_editor.get(1.0,"end-1c").split())
        character=len(text_editor.get(1.0,"end-1c").replace(" ",""))
        status_bars.config(text = "character {} word {}".format(character,word))
    text_editor.edit_modified(False)

text_editor.bind("<<Modified>>",change_word)

#---------------------------------------working of Font assign---------------------------------------#
font_now='calibri'
font_size_now=16

def change_font(main_application):
    font_now=font_family.get()
    text_editor.config(font=(font_now,font_size_now))

def change_size(main_application):
    font_size_now=size_variable.get()
    text_editor.config(font=(font_now,font_size_now))

font_box.bind("<<ComboboxSelected>>",change_font)
font_size.bind("<<ComboboxSelected>>",change_size)

#---------------------------------------working of BOLD assign---------------------------------------#

def bold_fun():
    bold_font = font.Font(text_editor,text_editor.cget("font"))
    bold_font.configure(weight="bold")

    text_editor.tag_configure("bold",font=bold_font)

    current_tags = text_editor.tag_names("sel.first")

    if "bold" in current_tags:
        text_editor.tag_remove("bold","sel.first","sel.last")
        
    else:
        text_editor.tag_add("bold","sel.first","sel.last")
        

bold_button.configure(command=bold_fun)

#---------------------------------------working of Italic assign---------------------------------------#

def Italic_fun():
    I_font = font.Font(text_editor,text_editor.cget("font"))
    I_font.configure(slant="italic")

    text_editor.tag_configure("italic",font=I_font)

    current_tags = text_editor.tag_names("sel.first")

    if "italic" in current_tags:
        text_editor.tag_remove("italic","sel.first","sel.last")
        
    else:
        text_editor.tag_add("italic","sel.first","sel.last")
        

italic_button.configure(command=Italic_fun)

#---------------------------------------working of Underline assign---------------------------------------#

def u_fun():

    if text_editor.tag_nextrange('underline_selection', 'sel.first', 'sel.last') != ():
        text_editor.tag_remove('underline_selection', 'sel.first', 'sel.last')
    else:
        text_editor.tag_add('underline_selection', 'sel.first', 'sel.last')
        text_editor.tag_configure('underline_selection', underline=True)

u_button.configure(command=u_fun)

#---------------------------------------working of colorwheel assign---------------------------------------#

def color_choose_fun():
    try:
        color_var = tk.colorchooser.askcolor()[1]
        if text_editor.tag_nextrange(color_var, 'sel.first', 'sel.last') == ():
            text_editor.tag_add(color_var, 'sel.first', 'sel.last')
            text_editor.tag_configure(color_var, foreground = color_var)
    except TclError:
        pass

cp_button.configure(command=color_choose_fun)

#---------------------------------------working for text alignment LEFT,CENTER,RIGHT---------------------------------------#

def L_fun():
    text_get_all=text_editor.get(1.0,"end")
    text_editor.tag_config("left",justify=tk.LEFT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_get_all,"left")

L_button.configure(command=L_fun)

def C_fun():
    text_get_all=text_editor.get(1.0,"end")
    text_editor.tag_config("center",justify=tk.CENTER)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_get_all,"center")

C_button.configure(command=C_fun)

def R_fun():
    text_get_all=text_editor.get(1.0,"end")
    text_editor.tag_config("right",justify=tk.RIGHT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,text_get_all,"right")

R_button.configure(command=R_fun)


# def superscript():
#     text_editor.tag_configure('super_selection',font=(font_now,12))
#     if text_editor.tag_nextrange('super_selection', 'sel.first', 'sel.last') != ():
#         text_editor.tag_remove('super_selection', 'sel.first', 'sel.last')
#     else:
#         text_editor.tag_add('super_selection', 'sel.first', 'sel.last')
#         text_editor.tag_configure('super_selection',offset=12)
        

# def subscript():
#     text_editor.tag_configure('sub_selection',font=(font_now,12))
#     if text_editor.tag_nextrange('sub_selection', 'sel.first', 'sel.last') != ():
#         text_editor.tag_remove('sub_selection', 'sel.first', 'sel.last')
#     else:
#         text_editor.tag_add('sub_selection', 'sel.first', 'sel.last')
#         text_editor.tag_configure('sub_selection',offset=-8)

# #---------------------------------------superscript---------------------------------------------------#

# supers = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\sup.png")
# super_button=Button(tool_bar_label,image=supers,bd=0,command=superscript)
# super_button.grid(row=0,column=14,padx=5,pady=5)

# #---------------------------------------subscript---------------------------------------------------#

# subsc = tk.PhotoImage(file = "F:\\BE_Project\\assets\\icon\\sub.png")
# sub_button=Button(tool_bar_label,image=subsc,bd=0,command=subscript)
# sub_button.grid(row=0,column=15,padx=5,pady=5)

#---------------------------------------assign icons and sub-menus---------------------------------------#
#---------------------------------------file---------------------------------------#

#---------------------------------------File Options creating---------------------------------------#
#---------------------------------------NEW FILE---------------------------------------#

text_url = ""

def new_file(event=None):
    global text_url
    text_url = ""
    text_editor.delete(1.0,tk.END)

file.add_command(label="New",image = new_icon,compound=tk.LEFT,accelerator="Ctrl+N",command=new_file)

def open_file(event=None):
    global text_url
    text_url = filedialog.askopenfilename(initialdir=os.getcwd(),title="select file",filetypes=(("Text file","*.txt"),("All files","*.*")))
    try:
        with open(text_url,"r") as for_read:
            text_editor.delete(1.0,tk.END)
            text_editor.insert(1.0,for_read.read())
    except FileNotFoundError:
        return
    except:
        return
    main_application.title(os.path.basename(text_url))
    
file.add_command(label="Open",image = open_icon,compound=tk.LEFT,accelerator="Ctrl+O",command=open_file)

def save_file(event = None):
    global text_url
    try:
        if text_url == "":
            text_url = filedialog.asksaveasfilename(defaultextension="txt",filetypes=(("Text file","*.txt"),("All files","*.*"),('Word file', '*.doc'),('pdf file', '.pdf')))
        if text_url:
            content = text_editor.get(1.0, tk.END)
            with open(text_url, "w", encoding="utf-8") as file:
                file.write(content)
    except Exception as e:
        print(e)

file.add_command(label="Save",image = save_icon,compound=tk.LEFT,accelerator="Ctrl+S",command=save_file)

def saveas_file(event=None):
    global text_url
    try:
        content=text_editor.get(1.0,tk.END)
        text_url=filedialog.asksaveasfile(defaultextension="txt",filetypes=(("Text file","*.txt"),("All files","*.*"),('Word file', '*.doc')))
        with open(text_url, "w", encoding="utf-8") as file:
                file.write(content)
                text_url.write(content)
                text_url.close()
        
    except:
        return

file.add_command(label="Save As",image = save_as_icon,compound=tk.LEFT,accelerator="Ctrl+Alt+S",command = saveas_file)

                 
def exit_file(event=None):
    global text_url,text_change
    try:
        if text_change:
            mbox = messagebox.askyesnocancel("Warning","Do you want to save this file")
            if mbox is True:
                if text_url:
                    content = text_editor.get(1.0, tk.END)
                    with open(text_url, "w", encoding="utf-8") as file:
                        file.write(content)
                        main_application.destroy()
                else:
                    content2 = str(text_editor.get(1.0,tk.END))
                    text_url=filedialog.asksaveasfile(mode="w",defaultextension="txt",filetypes=(("Text file","*.txt"),("All files","*.*"),('Word file', '.doc')))
                    text_url.write(content2)
                    text_url.close()
                    main_application.destroy()
            elif mbox is False:
                main_application.destroy()
        else:
            main_application.destroy()
    except Exception as e:
        print(e)

file.add_command(label="Exit",image = exit_icon,compound=tk.LEFT,accelerator="Ctrl+E",command=exit_file)
#---------------------------------------Accelerator---------------------------------------#
main_application.bind('<Control-o>',open_file)
main_application.bind('<Control-e>',exit_file)
main_application.bind('<Control-s>',save_file)
main_application.bind('<Control-Alt-s>',saveas_file)

#---------------------------------------edit---------------------------------------#
edit.add_command(label="Undo",image = undo_icon,compound=tk.LEFT,accelerator="Ctrl+Z",command=lambda:text_editor.event_generate("<Control z>"))
edit.add_command(label="Redo",image = redo_icon,compound=tk.LEFT,accelerator="Ctrl+Y",command=lambda:text_editor.event_generate("<Control y>"))
edit.add_command(label="Copy",image = copy_icon,compound=tk.LEFT,accelerator="Ctrl+C",command=lambda:text_editor.event_generate("<Control c>"))
edit.add_command(label="Paste",image = paste_icon,compound=tk.LEFT,accelerator="Ctrl+V",command=lambda:text_editor.event_generate("<Control v>"))
edit.add_command(label="Cut",image = cut_icon,compound=tk.LEFT,accelerator="Ctrl+X",command=lambda:text_editor.event_generate("<Control x>"))
edit.add_command(label="Clea All",image = clear_all_icon,compound=tk.LEFT,accelerator="Ctrl+Alt+X",command=lambda:text_editor.delete(1.0,tk.END))

def find_box():
    
    def find():
        word = find_input.get()
        text_editor.tag_remove("match","1.0",tk.END)
        matches = 0
        if word:
            start_pos = "1.0"
            while True:
                start_pos = text_editor.search(word,start_pos,stopindex = tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(word)}c"
                text_editor.tag_add("match",start_pos,end_pos)
                matches+=1
                start_pos = end_pos
                text_editor.tag_config("match",foreground = "black",background = "yellow")

    def replace():
        word = find_input.get()
        replace_text = replace_input.get()
        content = text_editor.get(1.0,tk.END)
        new_content = content.replace(word,replace_text)
        text_editor.delete(1.0,tk.END)
        text_editor.insert(1.0,new_content)

    
    findpop=tk.Toplevel()
    findpop.geometry("450x200")
    findpop.title("Find")
    findpop.resizable(0,0)

    find_frame=ttk.LabelFrame(findpop,text = "Find and Replace Word")
    find_frame.pack(pady=20)

    text_find = ttk.Label(find_frame,text = "Find")
    text_replace = ttk.Label(find_frame,text = "Replace")

    find_input = ttk.Entry(find_frame,width = 30)
    replace_input = ttk.Entry(find_frame,width = 30)

    find_btn = ttk.Button(find_frame,text="Find",command=find)
    replace_btn = ttk.Button(find_frame,text="Replace",command=replace)

    text_find.grid(row = 0,column = 0,padx = 4,pady = 4)
    text_replace.grid(row = 1,column = 0,padx = 4,pady = 4)

    find_input.grid(row = 0,column = 1,padx = 4,pady = 4)
    replace_input.grid(row = 1,column = 1,padx = 4,pady = 4)

    find_btn.grid(row = 2,column = 0,padx = 8,pady = 4)
    replace_btn.grid(row = 2,column = 1,padx = 8,pady = 4)

edit.add_command(label="Find",image = find_icon,compound=tk.LEFT,accelerator="Ctrl+F",command=find_box)


#---------------------------------------view---------------------------------------#

show_status_bar = tk.BooleanVar()
show_status_bar.set(True)
show_tool_bar = tk.BooleanVar()
show_tool_bar.set(True)

def hide_toolbar():
    global show_tool_bar
    if show_tool_bar:
        tool_bar_label.pack_forget()
        show_tool_bar = False
    else:
        text_editor.pack_forget()
        status_bars.pack_forget()
        tool_bar_label.pack(side=tk.TOP,fill=tk.X)
        text_editor.pack(fill=tk.BOTH,expand=True)
        status_bars.pack(side=tk.BOTTOM)
        show_tool_bar = True


view.add_checkbutton(label="Tool Bar",onvalue=True,offvalue=0,variable=show_tool_bar,image = toolbar_icon,compound=tk.LEFT,command=hide_toolbar)

def hide_statusbar():
    global show_status_bar
    if show_status_bar:
        status_bars.pack_forget()
        show_status_bar = False
    else:
        status_bars.pack(side=tk.BOTTOM)
        show_status_bar = True

view.add_checkbutton(label="Status Bar",onvalue=True,offvalue=0,variable=show_status_bar,image = statusbar_icon,compound=tk.LEFT,command=hide_statusbar)


#---------------------------------------theme---------------------------------------#


def change_theme():
    chosen_theme = theme_choice.get()
    color_tuple = color_dict.get(chosen_theme)
    fg_color, bg_color = color_tuple[0], color_tuple[1]
    text_editor.config(background=bg_color, fg=fg_color)


count = 0
for i in color_dict:
    color_theme.add_radiobutton(label=i,image=color_icons[count],variable=theme_choice,compound=tk.LEFT,command=change_theme)
    count+=1



#---------------------------------------End of Code---------------------------------------#
    
 

main_application.config(menu=main_menu)


main_application.mainloop()
#---------------------------------------End of window---------------------------------------#
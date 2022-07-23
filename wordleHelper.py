from tkinter import *

#This program aims to solve the wordle problem in 3 - 4 attempts. There are 26 possible letters and each attempt can use 5, so in 3 attempts we are utilizing more than half the possible options.
#In order to have a greater possibility of success the program will prioritize letters that appear on more words(letterVal). When 3 or more letters are green or yellow, the program will prioritize the letters that are green/yellow.

def charVal(charList,char,blacklist,pos,loc,letterVal,mean,weight,posac,correct):

    if char in blacklist and char not in pos.keys():
        return 0 #letters in blacklist do not provide further information, so they are valued at 0


    if char in charList: #if the letter is in the word twice
        nmulti = True
    else:
        nmulti = False

    
    
    if posac >= 3:  #When correct letters + possible letters reaches a value of 3 or greater, then value those greater
        if nmulti:
            return 2   # if the letter appears a second time
        if char == correct[loc]:
            return 5 + weight   # if letter is in the correct spot
    else:
        if nmulti:     
            return 1

    if char in pos.keys():
        if loc in pos[char]: #If this char has already been used on this [index] and returned a yellow value.
            return 0
        else:
            if letterVal[ord(char)-97] > mean :  #If this letter has not yet been used at this index, and letterValue is greater than the mean.
                return 3 + weight
            else:
                return 2 + weight
        #Char that have not been used yet
    elif letterVal[ord(char)-97] > mean:        #If letterValue greater than mean.
        return 4
    elif letterVal[ord(char)-97] < mean:        #If letterValue lower than mean.
        return 3 


def caseYellow(char,pos,i):
    if char not in pos.keys():
        pos[char] = [i]
    elif i in pos[char]:
        print("This Value Had Already Been Entered")
    else:
        pos[char].append(i)

    return pos


def choice(event = None):
    txt= usere.get()
    txt = txt.lower()
    

    if txt.isalpha() and sendButton['state'] != DISABLED:
        if len(txt) == 5:
           sendButton['state']=DISABLED
           logicButton['state']=ACTIVE
           for i in range(5):
                buttons[i]['state'] = ACTIVE
                buttons[i].config(text=txt[i])

                

def iniLogic(event = None):
    if logicButton['state'] != DISABLED:
        if buttons[0].cget('bg') != buttondf and buttons[1].cget('bg') != buttondf and buttons[2].cget('bg') != buttondf and buttons[3].cget('bg') != buttondf and buttons[4].cget('bg') != buttondf:
            userin = buttons[0].cget('text') + buttons[1].cget('text') + buttons[2].cget('text') + buttons[3].cget('text') + buttons[4].cget('text')
            colorin = ""
            for i in range(5): 
                if buttons[i].cget('bg') == colorV[0]:
                    colorin = colorin + '1'
                elif buttons[i].cget('bg') == colorV[1]:
                    colorin = colorin + '2'
                else:
                    colorin = colorin + '3'
                    
                buttons[i].config(bg=buttondf,text="")
                buttons[i]['state'] = DISABLED

            logicButton['state'] = DISABLED
            sendButton['state']= ACTIVE

            options = logic(userin,colorin)
            ans1['text'] = options[0][0],"[",options[0][1],"]"
            ans2['text'] = options[1][0],"[",options[1][1],"]"
            ans3['text'] = options[2][0],"[",options[2][1],"]"

            return
            
            
def colorOP(event = None):
    bp = event.widget.value

    if buttons[bp]['state'] != DISABLED:
        buttonc = buttons[int(bp)].cget('bg')
        # 0 -> 1 -> 2 - > 0 ...
        if buttonc == buttondf:
            buttons[int(bp)].config(bg=colorV[0])
        elif buttonc == colorV[0]:
            buttons[int(bp)].config(bg=colorV[1])
        elif buttonc == colorV[1]:
            buttons[int(bp)].config(bg=colorV[2])
        else:
            buttons[int(bp)].config(bg=colorV[0])
    

def logic(userEntry,result):
    global blacklist,pos,correct,corrlen,dw

    for i in range(5):
        if result[i] == '1':
            blacklist.append(userEntry[i])
            if userEntry[i] in pos.keys():
                pos = caseYellow(userEntry[i],pos,i)

        elif result[i] == '2':
            pos = caseYellow(userEntry[i],pos,i)

        elif result[i] == '3':
            if correct[i] == '0':
                correct[i] = userEntry[i]
                corrlen = corrlen + 1
                pos = caseYellow(userEntry[i],pos,i)
        else:
            print("Error 3: Incorrect Input")# Can't happen on gui 
   
    newset = set()
    letterVal = []

    for i in range(26):
        letterVal.append(0)


    for word in dw:
        cb = True
        
        if len([x for x in word if x in blacklist]) >= 2: #If the word has 2 or more characters in blacklist, that word is deleted
            cb = False
        
        if cb:
            newset.add(word)
            for char in word: #count the occurence of each letter in all the remaining words.
                letterVal[ord(char)-97] = letterVal[ord(char)-97] + 1

    #create a new set of possible words
    dw = newset

    add = sum(letterVal)
    mean = add/26


    posac = len(pos.keys())
    weight = 0
    #When there are 3 or more values in Possible(yellow) + Correct(green), Letters that have already been used will have a priority over new letters.
    if posac >= 3:
        if posac == 4:
            weight = 2
        else:
            weight = 1
        
    options = [["null",-10],["null",-11],["null",-12]]

    for word in dw:
        point = 0 #Value of current Word
        loc = 0 # Index
        charList = []

        for char in word:

            #charVal calculates the value of char.
            charV = charVal(charList,char,blacklist,pos,loc,letterVal,mean,weight,posac,correct)

            point = point + charV
            charList.append(char)
            loc = loc + 1 #Index

        numbers = [num[1] for num in options]
        for i in range(len(numbers)):
            if point > numbers[i]:
                options[i][0] = word
                options[i][1] = point
                break

    print(options)
    return options


#LOGIC FUNCTION VARIABLES ---------
txtfile = 'words.txt'
blacklist = [] #Letters that have returned a Gray Value(They are not in the word)
pos = {}
#Pos{
#  x  = [Locations already checked 0 - 4]
#  x1 = [1,0]
#  x2
#  x...
# }
correct = ['0','0','0','0','0'] #Letters that have returned a Green Value(They are in the right spot). Default value 0.
corrlen = 0

file = open(txtfile,'r')
dw = set(line.strip() for line in file)
file.close()
print(len(dw))

#TKINTER VARIABLES AND STUFF --------
#Input
word = ""  #Here

#background colors
background= "#181818"
tbbg= "#404040"
buttondf = "#f0f0f0"

#Font and font size
tf= 'Arial 25'

#Main window
window = Tk(className="Wordle Word Guess")
window.config(bg=background)
window.geometry("800x500")

#Color Values
colorV = ["gray","yellow","green"]


#INPUT FRAME
inFrame = Frame(window)
inFrame.grid(row=1,column= 0,columnspan=5,pady=(25,0),padx=(75,0),stick=W)
inFrame.config(bg=background)

label1 = Label(inFrame,text="Word: ",font=(tf),bg=background,fg ="white")
label1.grid(row=1,column=0,stick=W)

usere = Entry(inFrame,font=(tf),bg=tbbg,fg="#FFFFFF")
usere.grid(row=1,column=1,stick=W)

sendButton = Button(inFrame,text="Enter",font=("Arial 13"),width = 10,height=2)
sendButton.bind('<Button>',choice)
sendButton.grid(row=1,column=2, stick=W, padx=25)


#OPTION FRAME
opFrame = Frame(window)
opFrame.grid(row = 2,column = 0,columnspan=6,stick=W,pady=(15,0),padx=(50,0))
opFrame.config(bg=background)


#Button Array/list
buttons = []
for n in range(5):
    b = Button(opFrame,font=('Arial 10 bold'),bg=buttondf)
    b.grid(row= 2, column= n, padx=25)
    b.config(height = 5 , width = 10)
    b.value = n 
    b.bind('<Button>',colorOP)
    b.config(state=DISABLED)
    buttons.append(b)

logicButton = Button(opFrame,text="Enter",font=("Arial 13"),width = 10,height=2 )
logicButton.bind('<Button>', iniLogic)
logicButton.grid(row=3,column=2, pady=(15,0))
logicButton["state"]=DISABLED


#Stats
stFrame = Frame(window) 
stFrame.grid(row = 3,column = 0  ,columnspan=6,stick=W,padx=(135,0),pady=(25,0))
stFrame.config(bg=background)

ans1 = Label(stFrame,text="",font=(tf),bg=background,fg ="white")
ans1.grid(row=4,column=0,padx=(0,25))

ans2 = Label(stFrame,text="",font=(tf),bg=background,fg ="white")
ans2.grid(row=4,column=2,padx=(0,25))

ans3 = Label(stFrame,text="",font=(tf),bg=background,fg ="white")
ans3.grid(row=4,column=4)



window.mainloop()
# Libraries
import tkinter
import threading
import time
import random
from PIL import ImageTk, Image

# Variables
YELLOW = "#FFFF00"
GREEN = "#64C361"
GREY = "#B2BEB5"
DARK_GREY = "#565656"
WIN_LOSE = False

FONT = "assets/Starting Tiles.png"
LABEL_LIST = [[], [], [], [], [], []]
GUESSES_LIST = [[], [], [], [], [], []]
INDICATORS = []
GUESSES = 0

CORRECT_ANSWER = str(random.choice(["{:05d}".format(i) for i in range(99999)]))

# FUNCTIONS
def countDown():
    global TIMER, GUESSES, WIN_LOSE
    
    TIMER = 30

    for i in range(30):
            TIMER -= 1
            time.sleep(1)
            if GUESSES < 6 and WIN_LOSE == False:
                TIME_LABEL["text"] = "TIME: " + str(TIMER)

    if TIMER == 0:
        GUESSES = 6
        check()

STARTCOUNTDOWN = threading.Thread(target=countDown)
STARTCOUNTDOWN.setDaemon(True)
STARTCOUNTDOWN.start()

def check():
    global CORRECT_ANSWER, YELLOW, GREEN, DARK_GREY, GREY, WIN_LOSE, GUESSES
    GUESSED_ANSWER = "".join(GUESSES_LIST[GUESSES - 1])
    leftOver = []
    
    for i in range(len(GUESSED_ANSWER)):
        if GUESSED_ANSWER[i] == CORRECT_ANSWER[i]:
            LABEL_LIST[GUESSES - 1][i].config(bg = GREEN)
            if INDICATORS[int(GUESSED_ANSWER[i])]["background"] in [GREY, YELLOW]:
                INDICATORS[int(GUESSED_ANSWER[i])].config(bg = GREEN)

            leftOver.append("")
            

        elif GUESSED_ANSWER[i] not in CORRECT_ANSWER:
            LABEL_LIST[GUESSES - 1][i].config(bg = DARK_GREY)
            LABEL_LIST[GUESSES - 1][i].config(fg = "white")
            if INDICATORS[int(GUESSED_ANSWER[i])]["background"] == GREY:
                INDICATORS[int(GUESSED_ANSWER[i])].config(bg = DARK_GREY)


            leftOver.append("")

        elif GUESSED_ANSWER[i] in CORRECT_ANSWER:
            leftOver.append(GUESSED_ANSWER[i])


    for i in range(len(leftOver)):
        count = 0
        if leftOver[i] != "":
            for j in range(5):
                if LABEL_LIST[GUESSES - 1][j]["text"] == GUESSED_ANSWER[i] and (LABEL_LIST[GUESSES - 1][j]["background"] == GREEN or LABEL_LIST[GUESSES - 1][j]["background"] == YELLOW):
                    count += 1

            if count >= CORRECT_ANSWER.count(GUESSED_ANSWER[i]):
                LABEL_LIST[GUESSES - 1][i].config(bg = DARK_GREY, fg = "white")
                if INDICATORS[int(GUESSED_ANSWER[i])]["background"] == GREY:
                    INDICATORS[int(GUESSED_ANSWER[i])].config(bg = DARK_GREY)


            elif count < CORRECT_ANSWER.count(GUESSED_ANSWER[i]):
                LABEL_LIST[GUESSES - 1][i].config(bg = YELLOW)
                if INDICATORS[int(GUESSED_ANSWER[i])]["background"] == GREY:
                    INDICATORS[int(GUESSED_ANSWER[i])].config(bg = YELLOW)
                

    if GUESSED_ANSWER == CORRECT_ANSWER:
        RESULT_LABEL["text"] = "Congratulations, you win.\n If you want to play again press Enter"
        WIN_LOSE == True
        GUESSES = 6

    elif GUESSES == 6:
        RESULT_LABEL["text"] = "Sorry, the correct answer was " + CORRECT_ANSWER + "\nIf you want to play again press Enter"

def writeNumber(number):
    global GUESSES
    LABEL_LIST[GUESSES][len(GUESSES_LIST[GUESSES]) - 1]["text"] = number

def deleteNumber():
    global GUESSES
    LABEL_LIST[GUESSES][len(GUESSES_LIST[GUESSES]) - 1]["text"] = ""

def main(event):
    global GUESSES, CORRECT_ANSWER, DARK_GREY, GUESSES_LIST, TIMER

    if GUESSES < 6:
        if event.keysym in [str(i) for i in range(10)]:
            if len(GUESSES_LIST[GUESSES]) < 5:
                GUESSES_LIST[GUESSES].append(event.keysym)
                writeNumber(event.keysym)

        elif event.keysym == "BackSpace":
            if len(GUESSES_LIST[GUESSES]) > 0:
                deleteNumber()
                GUESSES_LIST[GUESSES].pop()

        elif event.keysym == "Return" and len(GUESSES_LIST[GUESSES]) == 5:
            GUESSES+=1
            check()

    elif event.keysym in ["Return"]:
        RESULT_LABEL["text"] = ""
        GUESSES_LIST = [[], [], [], [], [], []]
        for i in range(len(INDICATORS)):
            INDICATORS[i].config(bg = GREY)

        for i in range(len(LABEL_LIST)):
            for j in range(len(LABEL_LIST[i])):
                LABEL_LIST[i][j]["text"] = ""
                LABEL_LIST[i][j].config(bg = "white", fg = "black")

        
        CORRECT_ANSWER = str(random.choice(["{:05d}".format(i) for i in range(99999)]))
        GUESSES = 0
        TIME_LABEL["text"] = "TIME: 30"
        STARTCOUNTDOWN = threading.Thread(target=countDown)
        STARTCOUNTDOWN.setDaemon(True)
        STARTCOUNTDOWN.start()

# Creating Window
SCREEN = tkinter.Tk()
SCREEN.title("Digitle")
SCREEN.geometry("633x900")
SCREEN.iconphoto(False, tkinter.PhotoImage(file="assets/Icon.png"))
LABEL = tkinter.Label(SCREEN, text = "D I G I T L E", font = (FONT, 50))
LABEL.pack()

# Placing Image in SCREEN
IMG = ImageTk.PhotoImage(Image.open("assets/Starting Tiles.png"))
IMGLABEL = tkinter.Label(SCREEN, image = IMG)
IMGLABEL.pack(pady = 40)

# Placing the Indicators at the bottom of the screen
x = 95
for i in range(10):
    LABEL = tkinter.Label(SCREEN, text = str(i), foreground = "white", font = (FONT, 30))
    LABEL.config(height = 0, width = 2, bg = GREY)
    LABEL.place(x = x, y = 730)
    INDICATORS.append(LABEL)


    x += 45


# Making Labels for each indivisual box
y = 113
for i in range(6):
    x = 109.3
    for j in range(5):
        LABEL = tkinter.Label(SCREEN, text = "", font = (FONT, 54))
        LABEL.config(height = -2, width = 2)
        LABEL.place(x = x, y = y)

        LABEL_LIST[i].append(LABEL)

        x += 85

    y += 100

RESULT_LABEL = tkinter.Label(SCREEN, text = "", font = (FONT, 25))
RESULT_LABEL.place(x = 110, y = 790)

TIME_LABEL = tkinter.Label(SCREEN, text = "TIME: 30", font = (FONT, 20))
TIME_LABEL.place(x = 500, y = 10)

SCREEN.bind("<Key>", main)
SCREEN.mainloop()

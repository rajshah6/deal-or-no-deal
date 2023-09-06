"""
Name: Raj Shah
Date Modified: September 4, 2023
Version 1.2
Description: In this version of "Deal or No Deal," players start by selecting one unopened briefcase containing a hidden prize value. 
They then progressively reveal the values in other briefcases while aiming to eliminate lower values. At intervals, they receive offers 
from a hypothetical banker based on the remaining values and must decide whether to "deal" (accept the offer) or "no deal" (continue playing).
The objective is to win as much money as possible by either accepting a profitable offer or holding out for the highest prize hidden in their 
selected briefcase. The game ends when they either accept an offer or open all other briefcases, revealing their ultimate prize in the chosen case.
"""

# import necessary modules
from tkinter import *
from tkinter import messagebox
import random                       
import math

# declare global variables
first, cases, money, moneylbls, moneyimgs, casesbtns, casesimgs, casesOpened, round, casesToOpen, usersCase = True, [[]], [], [], [], [], [], 0, 0, 0, 0

# function that rounds a number to two decimal places
def roundNumber(number):
    number *= 100
    number += .5
    number = math.floor(number)
    roundednumber = number / 100
    number = str(number)
    if number[-2] == '.':
        number += '0'       # debugging statement using string slicing for when a value ends in one decimal place
    number = float(number)
    return roundednumber

# function that creates lbls and btns and assigns each suitcase a $ value
def create_wids():
    global first, cases, money, moneylbls, moneyimgs, casesbtns, casesimgs, casesOpened, round, casesToOpen

    # reset all the variables
    first = True  # flag to determine if its user's first choice (to set user case)
    cases = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0]]  # suitcase 2d array
    
    money = [0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 750, 1000, 5000, 10000, 25000, 50000, 75000, 100000,
             200000, 300000, 400000, 500000, 750000, 1000000]  # list holding all money values
    
    moneylbls = []
    moneyimgs = []
    casesbtns = []  ##globals lists to store imgs, lbls and btns when created through loop
    casesimgs = []
    casesOpened = -1        #set variables to track cases and rounds
    round = 0
    casesToOpen = 6

    # cycle through each money image
    for i in range(len(money)):
        img = PhotoImage(file='images/money/' + str(money[i]) + '.png')
        if i > 12:  # put half labels on east and half on west
            i -= 13  # row value for east lbls
            lbl = Label(eastframe, image=img, bg='black').grid(row=i, column=0, pady=5)

        else:
            lbl = Label(westframe, image=img, bg='black').grid(row=i, column=0, pady=5)
        moneylbls.append(lbl)  # add all imgs and lbls to global lists
        moneyimgs.append(img)

    # create a top and bottom frame to center first 5 rows with the 6th
    top = Frame(centerframe, bg='black')
    top.grid(row = 0)
    bottom = Frame(centerframe, bg='black')
    bottom.grid(row = 1)

    m = list(money)  # clone the $ value list and shuffle the clone
    random.shuffle(m)

    x = 1  # counter for img cycling and case 

    for rows in range(len(cases)):
        for cols in range(len(cases[rows])):
            img = PhotoImage(file='images/suitcases/case' + str(x) + '.png')
            if rows == 4:  # set to function, pass the case # and money of the case
                btn = Button(bottom, image=img, bg='black', bd=0, activebackground='black',
                             command=lambda num=x, value=m[x - 1]: selected_case(num, value))
            else:
                btn = Button(top, image=img, bg='black', bd=0, activebackground='black',
                             command=lambda casenum=x, value=m[x - 1]: selected_case(casenum, value))
                
            btn.grid(row=rows, column=cols, padx=5, pady=5)
            cases[rows][cols] = m[x - 1]  # set money value of each case in the 2-D array
            x += 1
            casesbtns.append(btn)  # add all imgs and btns to global lists
            casesimgs.append(img)

def selected_case(casenum, value):  # function that blanks related cases and money lbls and sets the user case
    global first, casesOpened, money, round, casesToOpen, usersCase
    casesOpened += 1  # increase the number of cases opened
    casesbtns[casenum - 1].config(image=imgBlankCase, state='disabled')  # when user selects a case, clear it

    if first:  # if the user makes their first choice, display the case they chose as their own
        usersCase = money.index(value)  # gives the index of the value of the users case
        lblPlayersCase = Label(frame, image=casesimgs[casenum - 1], bg="black").grid(row=2, column=0)
        lblMessage.config(text="Open " + str(
            casesToOpen) + " suitcase(s)!")  # configure the label to show how many cases need to be opened
        first = False  # identify that user has made first choice
    else:
        casesToOpen -= 1
        lblMessage.configure(text="Open " + str(casesToOpen) + " suitcase(s)!")
        messagebox.showinfo('Case #' + str(casenum), 'Case #' + str(casenum) + ' contains $' + "{:,}".format(value))  # display case and amount
        i = money.index(value)  # find the index of the money value in the money list
        if i > 12:  # determine if related money lbl is on east or west
            x = i - 13  # row value for east lbls
            moneylbls[i] = Label(eastframe, image=imgBlankMoney, bg='black').grid(row=x, column=0,
                                                                                  pady=5)  # blank out the label
        else:  # replace the corresponding lbl to a blank one
            moneylbls[i] = Label(westframe, image=imgBlankMoney, bg='black').grid(row=i, column=0,
                                                                                  pady=5)  # blank out the label
        money[i] = 0  # give the selected case no cash value

    # after a certain amount of cases are opened, get the banker's deal
    if casesOpened == 6:
        casesToOpen = 5  # set the number of cases to open
        round += 1  # add to round number
        getBankerDeal(round)  # get the banker's deal
        lblMessage.config(text="Open " + str(casesToOpen) + " suitcase(s)!")  # show number of suitcases left to open
    elif casesOpened == 11:
        casesToOpen = 4  # set the number of cases to open
        round += 1  # add to round number
        getBankerDeal(round)  # get the banker's deal
        lblMessage.config(text="Open " + str(casesToOpen) + " suitcase(s)!")  # show number of suitcases left to open
    elif casesOpened == 15:
        casesToOpen = 3  # set the number of cases to open
        round += 1  # add to round number
        getBankerDeal(round)  # get the banker's deal
        lblMessage.config(text="Open " + str(casesToOpen) + " suitcase(s)!")  # show the number of suitcases left to open
    elif casesOpened == 18:
        casesToOpen = 2  # set the number of cases to open
        round += 1  # add to round number
        getBankerDeal(round)  # get the banker's deal
        lblMessage.config(text="Open " + str(casesToOpen) + " suitcase(s)!")  # show the number of suitcases left to open
    elif casesOpened >= 20:
        casesToOpen = 1  # set the number of cases to open
        round += 1  # add to round number
        getBankerDeal(round)  # get the banker's deal
        lblMessage.config(text="Open " + str(casesToOpen) + " suitcase(s)!")  # show the number of suitcases left to open

def getBankerDeal(roundNum):
    global casesOpened
    bankerDeal = 0  # create a variable for the bankers deal
    numCases = 0  # running total for the amount of unopened cases
    for value in money:  # cycle through each item in the money list
        bankerDeal += value  # add the value of the case to the total

        if value != 0:
            numCases += 1  # add to the number of cases still unopened

    bankerDeal = (bankerDeal / numCases) * (roundNum / 10)  # calculate the banker's deal
    bankerDeal = roundNumber(bankerDeal)  # round the banker's deal to 2 decimals
    
    if casesOpened == 24:  # the last case
        userBankerDeal = messagebox.askyesno("Banker's Offer", "The banker's offer is $" + "{:,}".format(
            bankerDeal) + ".\nWould you like to take the deal?")  # show the banker's offer
        
        if userBankerDeal == True:  # if the user chooses the banker's offer
            messagebox.showinfo("It's a Deal!", "Congratulations... You're going home with $" + "{:,}".format(
                bankerDeal) + '!')  # show user the amount in their case
            messagebox.showinfo("Deal or No Deal", "You could have gone home with $" + "{:,}".format(
                money[usersCase]) + '.')  # show user the value of the last suitcase
            userInput = messagebox.askyesno("Deal or No Deal",
                                            "Would you like to play again?")  # ask if user wants to play again
            
            if userInput == True:
                create_wids()  # start a new game
            else:
                messagebox.showinfo("Game Over", "Thank you for playing Deal or No Deal!")  # end the game
                exit()

        # find the value of last case
        for value in money:  # iterate through each value in the list
            if value != 0 and value != money[usersCase]:  # if the value is not zero and is not the user's case
                indexLastCase = money.index(value)  # the index of the last case value

        lastCase = messagebox.askyesno("Deal or No Deal",
                                       "There is only one case left! \nWould you like to keep your case?")  # ask user if they want to keep their case
        if lastCase == True:  # if they want to keep their case
            messagebox.showinfo("It's a Deal!", "Congratulations... You're going home with $" + "{:,}".format(
                money[usersCase]) + '!')  # show user the amount in their case
            messagebox.showinfo("Deal or No Deal", "You could have gone home with $" + "{:,}".format(
                money[indexLastCase]) + '.')  # show user the value of the last suitcase
            
        else:
            messagebox.showinfo("It's a Deal!", "Congratulations... You're going home with $" + "{:,}".format(
                money[indexLastCase]) + '!')  # show user the amount in the last case
            messagebox.showinfo("Deal or No Deal", "You could have gone home with $" + "{:,}".format(
                money[usersCase]) + '.')  # show user the value of their case
        userInput = messagebox.askyesno("Deal or No Deal", "Would you like to play again?")

        if userInput == True:
            create_wids()  # start a new game

        else:
            messagebox.showinfo("Game Over", "Thank you for playing Deal or No Deal!")  # output message
            exit()  # close the window
    else:
        userBankerDeal = messagebox.askyesno("Banker's Offer", "The banker's offer is $" + "{:,}".format(
            bankerDeal) + ".\nWould you like to take the deal?")  # show the banker's offer
        
        if userBankerDeal == True:  # if the user chooses the banker's offer
            messagebox.showinfo("It's a Deal!", "Congratulations... You're going home with $" + "{:,}".format(
                bankerDeal) + '!')  # show user the amount in their case
            messagebox.showinfo("Deal or No Deal", "You could have gone home with $" + "{:,}".format(
                money[usersCase]) + '.')  # show user the value of the last suitcase
            userInput = messagebox.askyesno("Deal or No Deal",
                                            "Would you like to play again?")  # ask if user wants to play again
            if userInput == True:
                create_wids()  # start a new game
            else:
                messagebox.showinfo("Game Over", "Thank you for playing Deal or No Deal!")  # end the game
                exit()

def exit_dond():       #confirm that user wants to exit if user clicks the window X
    answer = messagebox.askyesno("Deal or No Deal", "Would you like to exit?")
    if answer:      #if user clicks yes then close the window
        messagebox.showinfo("Game Over", "Thank you for playing Deal or No Deal!")
        exit()

root = Tk()
root.title("Deal or No Deal")
root.protocol("WM_DELETE_WINDOW", exit_dond)

frame = Frame(root, padx=10, pady=10, bg="black")
frame.pack()

imgTitle = PhotoImage(file="images/dond_logo.png")
lblTitle = Label(frame, image=imgTitle, border=0)
lblTitle.grid(row=0, column=0, columnspan=3)

westframe = Frame(frame, padx=10, pady=10, bg="black")
westframe.grid(row=1, column=0)
eastframe = Frame(frame, padx=10, pady=10, bg="black")
eastframe.grid(row=1, column=2)
centerframe = Frame(frame, padx=10, pady=10, bg="black", width=380, height=280)
centerframe.grid(row=1, column=1)

lblMessage = Label(frame, width=35, bg="black", font=("Century Gothic", 26, "bold"), fg="#fcea97",
                   text="Choose one of the suitcases!")
lblMessage.grid(row=2, column=1, padx=10, pady=5)

imgBlankCase = PhotoImage(file="images/suitcases/blankcase.png")
imgBlankMoney = PhotoImage(file='images/money/blankmoney.png')

create_wids()  # set the interface (money values on either sides and suitcases in the middle)
root.mainloop()

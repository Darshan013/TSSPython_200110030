import random
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

window = Tk()
window.title("Hangman")
window.geometry("1000x600")
window.minsize(1000,600)
window.maxsize(1000,600)

word_labels = list()
incorrect_text = "Incorrect guesses : "
incorrect = Label(window, text = incorrect_text, font = ('Helvetica',12))

guess_var = StringVar()
Text_Field = Entry(window, textvariable = guess_var, font = ('Helvetica',16))

hangman_drawing = Canvas(window, height = 500, width = 300)

prev_guesses = list()


def get_wordlist():
	File = open("wordlist.txt",encoding= 'UTF-8')
	wordlist = []
	for line in File.readlines():
		for word in line.split(' '):
			w = word.strip()
			wordlist.append(w)
	return wordlist


def get_word(wordlist):
	word = random.choice(wordlist)
	return word.upper(), len(word)


wl = get_wordlist()
word, length = get_word(wl)
correct_guesses = 0
incorrect_guesses = 0


def game_screen():
	global Text_Field, guess_var, guess_button
	heading = Label(window, text = "H A N G M A N", font=('Helvetica bold',40))
	guess_label = Label(window, text = "Enter your guess : ", font=('Helvetica', 12))
	heading.pack()
	guess_label.place(x = 25, y = 305)
	Text_Field.place(x = 175, y = 300, width = 200, height = 35)
	guess_button.place(x = 150, y = 400, width = 150, height = 40)
	surrender_button.place(x = 150, y = 475, width = 150, height = 40)
	hangman_drawing.place(x = 690, y = 90)


def display_blanks(l):
	global word_labels
	for i in range(l):
		word_labels.append(Label(window, text = "_", font = ('Helvetica', 16)))
		word_labels[i].place(x = 25*(i+1), y = 150)


def display_incorrect_guesses(incorrect_guess):
	global incorrect_text, incorrect, incorrect_guesses
	if incorrect_guess != '0':
		incorrect_text += incorrect_guess + ","
		incorrect.config(text = incorrect_text)
		incorrect_guesses += 1
		draw_hangman()
		return
	incorrect.place(x = 25, y = 200)


def guess():
	global guess_var, length, word_labels, word, correct_guesses
	guess_letter = guess_var.get()
	if guess_letter != "":
		guess_correct = False
		guess_letter = guess_letter[0]
		guess_var.set("")


		if not guess_letter.isalpha():
			messagebox.showerror("Invalid character", "Please enter an alphabet")
			return
		

		guess_letter = guess_letter.upper()
		if(guess_letter not in prev_guesses):
			prev_guesses.append(guess_letter)
			i = 0
			while i < length:
				if word[i] == guess_letter:
					guess_correct = True
					word_labels[i].config(text = guess_letter)
					correct_guesses += 1
				i += 1
			if not guess_correct:
				display_incorrect_guesses(guess_letter)
		else:
			messagebox.showerror("Already guessed","You have already made this guess")
	check_game_over()


def surrender():
	global word
	messagebox.showinfo("The word is", word)


def check_game_over():
	global correct_guesses, length, incorrect_guesses
	if correct_guesses == length:
		messagebox.showinfo("Congratulations", "You Won!!")
	if incorrect_guesses == 7:
		messagebox.showinfo("Game Over", "You Lost!!")


def draw_hangman():
	global incorrect_guesses, hangman_drawing
	if incorrect_guesses == 1:
		hangman_drawing.create_line(10,490,290,490, fill = "black")
		hangman_drawing.create_line(270,490,270,40, fill = "black")
		hangman_drawing.create_line(270,40,150,40, fill = "black")
		hangman_drawing.create_line(150,40,150,75, fill = "black")
	if incorrect_guesses == 2:
		hangman_drawing.create_oval(125,75,175,125)#center of circle is 150, 100 and radius is 25
	if incorrect_guesses == 3:
		hangman_drawing.create_line(150,125,150,250,fill = "black")
	if incorrect_guesses == 4:
		hangman_drawing.create_line(150,180,100,130,fill = "black")
	if incorrect_guesses == 5:
		hangman_drawing.create_line(150,180,200,130,fill = "black")
	if incorrect_guesses == 6:
		hangman_drawing.create_line(150,250,100,300,fill = "black")
	if incorrect_guesses == 7:
		hangman_drawing.create_line(150,250,200,300,fill = "black")
	hangman_drawing.place(x = 690, y = 90)



guess_button = Button(window, text = "Guess", command = guess)
surrender_button = Button(window, text = "Surrender", command = surrender)
game_screen()
display_blanks(length)
display_incorrect_guesses('0')
window.mainloop()
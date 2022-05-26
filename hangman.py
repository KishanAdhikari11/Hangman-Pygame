# importing module
import pygame as pg
import random
import math

# display
White = (255, 255, 255)
Blue = (0, 0, 255)
cyan = (0, 255, 255)
Black=(0,0,0)

pg.init()
width, height = 800, 800
win = pg.display.set_mode((width, height))
pg.display.set_caption("Hangman")

# button math
Radius = 23
Gap = 12
Distance_between_button = Radius * 2 + Gap
letters = []
startx = round((width - (Distance_between_button) * 13) // 2)
starty = 550

#letter
letter_font = pg.font.SysFont("comicsans", 40)
word_font = pg.font.SysFont("comicsans", 30)
title_font=pg.font.SysFont("comicsans",70)

A = 65
for a in range(26):
    x = startx + Gap * 2 + (Distance_between_button) * (a % 13)
    y = starty + (a // 13) * (Distance_between_button)
    letters.append([x, y, chr(A + a), True])
print(x,y)

FPS = 60
clock = pg.time.Clock()
run = True

hangman_status = 0
with open("words.txt") as f:
  wordlist=[]
  for line in f:
    wordlist.append(line.strip())

def get_randomword():
    word=random.choice(wordlist).upper()
    return word

word=get_randomword()
if len(word)<4:
        word=get_randomword()
        
def draw():
    win.fill((White))
    text=title_font.render("Hangman game",1,Blue)
    win.blit(text,(width/2-text.get_width()/1.5,20))

    # drawing button

    display_word = " "
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word +=  "_ "
        text=word_font.render(display_word,1,Black)
        win.blit(text,(380,400))

    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pg.draw.circle(win, cyan, (x, y), Radius, 2)
            text = letter_font.render(ltr, 1, Blue)
            win.blit(text, (x - text.get_width() / 1.3, y - text.get_width() /1.3))
    win.blit(images[hangman_status], (200, 200))
    pg.display.update()


# loading image
images = []
for i in range(7):
    image = pg.image.load("images/hangman" + str(i) + ".png")
    images.append(image)




guessed = []
def display_message(message):
    win.fill(Blue)
    text = word_font.render(message, 1, Black)
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    pg.display.update()
    pg.time.delay(1500)

# game loop


while run:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dis = math.sqrt((x - mouse_x) ** 2 + (y - mouse_y) ** 2)
                    if dis < Radius:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                           hangman_status+=1
    draw()
    won=True
    for letter in word:
        if letter not in guessed:
            won=False
            break
    if won:
        display_message(" Congratulation you won!")
        break

    if hangman_status==6:
        display_message("oops you lost")
        display_message("The word was " +  word.lower())
        break

pg.quit()

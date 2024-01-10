#Mathias Cheung
#June 8,2021
#space invaders

# resources I used to learnt new things
##class
#https://youtube.com/playlist?list=PLjcN1EyupaQkAQyBCYKyf1jt1M1PiRJEp
#https://docs.python.org/3/tutorial/classes.html

##sound effect
#https://pythonprogramming.net/adding-sounds-music-pygame/
#https://stackoverflow.com/questions/42393916/how-can-i-play-multiple-sounds-at-the-same-time-in-pygame

# extra things I added in game
#use class to create objects
#adding sounds effect to lasers, alert sound to alien boss, explosion sound when destorying aliens, player taking damage
#mouse click in game
#add different levels to the game
#adding a health bar to all walls/covers
#play again



import random
import pygame
from pygame import mixer
import sys
import os


# initialize pygame
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

# set screen size
size = (850, 750)
screen = pygame.display.set_mode(size)

# set the caption for the screen
pygame.display.set_caption("Space Invaders")

# get screen width and height
screenWidth = screen.get_width()
screenHeight = screen.get_height()
centreX = screenWidth / 2
centreY = screenHeight / 2
screenCentre = (centreX, centreY)

# define colours you will be using
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# set up a font to use
pygame.font.init()
IntroGameTitle = pygame.font.SysFont("Mathias space invaders/ 8-bit.ttf", 80)
ScoreFontTitle = pygame.font.SysFont("arial", 30, bold=True)
fontTitle3 = pygame.font.SysFont("arial", 30, bold=True)


#load Images

# get the directory of this file
sourceFileDir = os.path.dirname(os.path.abspath(__file__))

# join the filepath and the filename
#fondImgPath = os.path.join(sourceFileDir, "introBackground1.jpg")

Background = pygame.image.load(sourceFileDir + "//images//introBackground1.jpg")
RedAliensImage = pygame.image.load(sourceFileDir + "//images//alien boss.png")
IntroUFOImage = pygame.image.load(sourceFileDir + "//images//ufo_2.png.")
finalAlien = pygame.image.load(sourceFileDir + "//images//aliens2.png")
instructionAlien = pygame.image.load(sourceFileDir + "//images//aliens1 - Copy.png")
instructionAlienboss = pygame.image.load(sourceFileDir + "//images//alien boss1 - Copy.png")

#load sounds effect
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
channel4 = pygame.mixer.Channel(3)
channel5 = pygame.mixer.Channel(4)


laser_sound = pygame.mixer.Sound(sourceFileDir + "//sound//lasers sound.mp3")
laser_sound.set_volume(0.25)

explosion_sound = pygame.mixer.Sound(sourceFileDir + "//sound//Explosion sound.mp3")
explosion_sound.set_volume(0.10)

aliensLaser_sound = pygame.mixer.Sound(sourceFileDir + "//sound//aliens laser.mp3")
aliensLaser_sound.set_volume(0.15)

boss_sound = pygame.mixer.Sound(sourceFileDir + "//sound//alertsound.mp3")
boss_sound.set_volume(0.10)

damage_sound = pygame.mixer.Sound(sourceFileDir + "//sound//Taking Damage Sound Effect .mp3")
damage_sound.set_volume(0.50)

# set instructions, game and final loops to false so they won't run
final2 = False
final = False
instruction = False
game = False
play_already = False

#intro screen variables
introX = 50
introY = 600

#game variables
alienrows = 1
aliencols = 1
alienStartX = 270

heartCols = 3

wallsCols = 4


aliens_lasers_cooldown = 1000
last_aliens_shot = pygame.time.get_ticks()

score = 0
oldscore = score

#rect for final alien
finalAlienRect = finalAlien.get_rect()
finalAlienRect.center = (centreX, 200)

#intro image rect
controAlienRect = RedAliensImage.get_rect()
controAlienRect.center = (centreX,600)

instructionAlienRect = instructionAlien.get_rect()
instructionAlienRect.center = (200,400)

instructionAlienbossRect = instructionAlienboss.get_rect()
instructionAlienbossRect.center = (500,400)

#intro ufo rect
ufoRect = IntroUFOImage.get_rect()
ufoRect.center = (screenWidth - 200,screenHeight - 200)



#backgroung
def drawBg():
    screen.blit(Background, (0,0))



#********************learned the class function to make it easier to code the game************************************



#create class for player spaceship
class PlayerSpaceship(pygame.sprite.Sprite):
    def __init__(self,spaceshipX,spaceshipY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(sourceFileDir + "//images//spaceship1.png")
        self.rect = self.image.get_rect()
        self.rect.center = [spaceshipX,spaceshipY]
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        #spaceship move speed
        speed = 3
        cooldown = 400
        #key press to move spaceship
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screenWidth:
            self.rect.x += speed
        if key[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_d] and self.rect.right < screenWidth:
            self.rect.x += speed

        #get time to control lasers
        time_now = pygame.time.get_ticks()


        #key press to shoot lasers
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            lasers = Playerlasers(self.rect.centerx, self.rect.top)
            playerlasers_group.add(lasers)
            self.last_shot = time_now
            channel2.play(laser_sound)




#create class for player lasers
class Playerlasers(pygame.sprite.Sprite):
    def __init__(self,lasersX,lasersY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(sourceFileDir + "//images//spaceshipLaser.png")
        self.rect = self.image.get_rect()
        self.rect.center = [lasersX,lasersY]

    def update(self):
        global final
        global final2
        global game
        global score
        self.rect.y -= 3
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, aliens_group, True):
            self.kill()
            channel3.play(explosion_sound)
            score = score + 1
            aliens_list = aliens_group.sprites()
            i = len(aliens_list)
            if i == 0:
                final2 = True
                game = False

        if pygame.sprite.spritecollide(self, walls_group, False):
            self.kill()
        if pygame.sprite.spritecollide(self, redboss_group, True):
            self.kill()
            score = score + 5
            boss_sound.stop()






#create class for aliens
class Aliens(pygame.sprite.Sprite):
    setMoveDirectionX = 1
    setAliencols = 4
    setMoveCounter = 250
    def __init__(self,aliensX,aliensY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(sourceFileDir + "//images//aliens1.png")
        self.rect = self.image.get_rect()
        self.rect.center = [aliensX,aliensY]
        self.moveCounter = 0
        self.moveDirectionY = 8

    def update(self):
        global final
        global game
        self.rect.x += self.setMoveDirectionX
        self.moveCounter += 1
        if abs(self.moveCounter) > self.setMoveCounter:
            self.setMoveDirectionX *= -1
            self.moveCounter *= self.setMoveDirectionX
            self.rect.y += self.moveDirectionY
        if self.rect.bottom > screenHeight - 150:
            final = True
            game = False







#create class for heart
class PlayerRedheart(pygame.sprite.Sprite):
    def __init__(self, heartX, heartY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(sourceFileDir + "//images//Playerheart.png")
        self.rect = self.image.get_rect()
        self.rect.center = [heartX, heartY]




# create class for aliens lasers
class Alienslasers(pygame.sprite.Sprite):
    def __init__(self, lasersX, lasersY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(sourceFileDir + "//images//aliensLaser.png")
        self.rect = self.image.get_rect()
        self.rect.center = [lasersX, lasersY]

    def update(self):
        global final
        global game
        self.rect.y += 2
        if self.rect.top > screenHeight:
            self.kill()
        if pygame.sprite.spritecollide(self, playerSpaceship_group, False):
            self.kill()
            channel4.play(damage_sound)

            heart_list = heart_group.sprites()
            i = len(heart_list)
            if i > 0:
                kill = heart_list[i-1]
                heart_group.remove(kill)
            if i == 1:
                final = True
                game = False





#creat class for walls
class Walls(pygame.sprite.Sprite):
    health_remaining = 3
    def __init__(self, wallX, wallY,health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(sourceFileDir + "//images//shield.png")
        self.rect = self.image.get_rect()
        self.rect.center = [wallX, wallY]
        self.health_start = health



    def update(self):
        pygame.draw.rect(screen, RED, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 10))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, GREEN, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 10))

        if pygame.sprite.spritecollide(self, alienslasers_group, True):
            self.health_remaining -= 1
            if self.health_remaining == 0:
                self.kill()


#create class for alien boss
class Redboss(pygame.sprite.Sprite):
    setBossMoveDirectionX = 1
    def __init__(self, bossX, bossY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(sourceFileDir + "//images//alien boss1.png")
        self.rect = self.image.get_rect()
        self.rect.center = [bossX, bossY]


    def update(self):
        global play_already
        self.rect.x += self.setBossMoveDirectionX
        if self.rect.right > screenWidth + 800:
            self.setBossMoveDirectionX *= -1
        if self.rect.left < -800:
            self.setBossMoveDirectionX *= +1
        if self.rect.left > 0:
            if play_already == False:
                channel1.play(boss_sound)
                play_already = True
        if self.rect.left > screenWidth:
            boss_sound.stop()
            play_already = False
        if self.rect.right < 0:
            boss_sound.stop()







#create sprite group
playerSpaceship_group = pygame.sprite.Group()
playerlasers_group = pygame.sprite.Group()
aliens_group = pygame.sprite.Group()
heart_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
alienslasers_group = pygame.sprite.Group()
redboss_group = pygame.sprite.Group()






#------------------------methods--------------------------------------------


#menu function method
#prints menu selection and only exits after a choice has been made
def menu(titles, mainTitle):
    buttonTitleFont = pygame.font.SysFont("arial", 25, bold=True)
    selection = []
    rectWidth = 300
    rectHeight = 30
    x = int(screen.get_width()/2 - rectWidth/2)
    y = 300
    length = len(titles)
    num = 0
    hover = False
    # creates the Rects (containers) for the buttons
    for i in range (0,length,1):
        choiceRect = pygame.Rect(x,y,rectWidth,rectHeight)
        selection.append(choiceRect)
        y += 50

    #main loop in menu    
    go = True
    while go:
        drawBg()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    go = False
                    pygame.quit()
                    sys.exit()

            if event.type ==pygame.MOUSEMOTION:     # if mouse moved
                hover = False
                mx, my = pygame.mouse.get_pos()     # get the mouse position
                for i in range (length):            
                    if selection[i].collidepoint((mx,my)):  # check if x,y of mouse is in a button
                        num = i
                        hover = True
            if event.type == pygame.MOUSEBUTTONDOWN and hover == True:  #if mouse is in button
                go = False                                              # and has been clicked

        # draw all buttons                                                                
        for choice in selection:
            pygame.draw.rect(screen,BLACK,choice,0)
        
        # redraw selected button in another colour
        pygame.draw.rect(screen,RED,selection[num],0)

        screen.blit(IntroUFOImage, ufoRect)

        textTitle = IntroGameTitle.render("SPACE INVADERS", False, WHITE)
        textRect = textTitle.get_rect()
        textRect.center = (centreX, 100)
        screen.blit(textTitle, textRect)

        # draw all the titles on the buttons
        x = int(screen.get_width()/2 - 150)
        y = 300
        for i in range(0,length,1):
            buttonTitle = buttonTitleFont.render(titles[i],True,WHITE)
            screen.blit(buttonTitle,(x,y))
            y += 50



        pygame.display.update()
    return num




def option(num):


# set variables to global
    global alienrows
    global aliencols
    global alienStartX
    global last_aliens_shot
    global aliens_lasers_cooldown
    global oldscore
    global game
    global final
    global final2
    global main
    global instruction
    global score
    global play_already

    screen.fill(BLACK)
    game = False
    clock = pygame.time.Clock()
    FPS = 160




    # Selected Game mode
    if num == 1:
        game = True

        # create player
        playerSpaceship = PlayerSpaceship(int(screenWidth / 2), screenHeight - 50)
        playerSpaceship_group.add(playerSpaceship)

        # create aliens
        def createAliens():
            global alienrows
            global aliencols
            global alienStartX

            for row in range(alienrows):
                for item in range(aliencols):
                    alien = Aliens(alienStartX + (item * 100), 100 + row * 50)
                    aliens_group.add(alien)

        # create heart
        def createHeart():
            for item in range(heartCols):
                heart = PlayerRedheart(700 + item * 50, 50)
                heart_group.add(heart)

        createHeart()

        # create walls
        def createwalls():
            for item in range(wallsCols):
                wall = Walls(125 + item * 200, screenHeight - 150, 3)
                walls_group.add(wall)

        createwalls()

        redboss = Redboss(-800, 100)
        redboss_group.add(redboss)




        menuLevel = ["EASY", "NORMAL", "HARD","EXTREME"]

        screen.fill(BLACK)

        # for Game menu, this menu selects levels

        choose2 = menu(menuLevel, "LEVELS")
        # This is level selection
        if choose2 == 0:
            alienrows = 2
            aliencols = 4
            alienStartX = 270
            Aliens.setMoveDirectionX = 1
            Aliens.setMoveCounter = 250
            Aliens.setAliencols = 4
            aliens_lasers_cooldown = 1000

        elif choose2 == 1:
            alienrows = 3
            aliencols = 5
            alienStartX = 220
            Aliens.setMoveDirectionX = 1
            Aliens.setMoveCounter = 190
            Aliens.setAliencols = 5
            aliens_lasers_cooldown = 700

        elif choose2 == 2:
            alienrows = 4
            aliencols = 6
            alienStartX = 170
            Aliens.setMoveDirectionX = 1
            Aliens.setMoveCounter = 140
            Aliens.setAliencols = 6
            aliens_lasers_cooldown = 400

        elif choose2 == 3:
            alienrows = 5
            aliencols = 7
            alienStartX = 120
            Aliens.setMoveDirectionX = 1
            Aliens.setMoveCounter = 100
            Aliens.setAliencols = 7
            aliens_lasers_cooldown = 250


        createAliens()

        # this is the biggest loop, all the code for your game goes in here
        while game:

            screen.fill(BLACK)

            # ******************************************************************************************************


            #create random aliens lasers
            time_now = pygame.time.get_ticks()
            if time_now - last_aliens_shot > aliens_lasers_cooldown:
                aliens_shooting = random.choice(aliens_group.sprites())
                alienslasers = Alienslasers(aliens_shooting.rect.centerx, aliens_shooting.rect.centery)
                alienslasers_group.add(alienslasers)
                last_aliens_shot = time_now
                channel5.play(aliensLaser_sound)



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main = True
                    game = False
                    play_already = False
                    aliens_group.empty()
                    alienslasers_group.empty()
                    playerlasers_group.empty()
                    playerSpaceship_group.empty()
                    heart_group.empty()
                    walls_group.empty()
                    redboss_group.empty()
                    boss_sound.stop()
                    score = 0




            ## main code for your game goes here
            ## when the user wins or loses, it will exit this loop and go to final loop


            #update spaceship
            playerSpaceship.update()
            #update player lasers
            playerlasers_group.update()
            #update aliens
            aliens_group.update()
            #update heart
            heart_group.update()
            #update walls
            walls_group.update()
            #update aliens lasers
            alienslasers_group.update()
            #update redboss
            redboss_group.update()

            # draw player spaceship
            playerSpaceship_group.draw(screen)
            # draw player lasers
            playerlasers_group.draw(screen)
            #draw aliens
            aliens_group.draw(screen)
            #draw heart
            heart_group.draw(screen)
            #draw walls
            walls_group.draw(screen)
            #draw aliens lasers
            alienslasers_group.draw(screen)
            #draw redboss
            redboss_group.draw(screen)

            oldscore = score





            clock.tick(FPS)

            ## this code can be removed it is just for example purposes

            textTitle3 = fontTitle3.render("score: " + str(score), False, BLUE)
            textRect3 = textTitle3.get_rect()
            textRect3.center = (60, 50)
            screen.fill(BLACK, textRect3)
            screen.blit(textTitle3, textRect3)



            # update the screen
            pygame.display.flip()

        while final:
            boss_sound.stop()
            aliens_group.empty()
            alienslasers_group.empty()
            playerlasers_group.empty()
            playerSpaceship_group.empty()
            heart_group.empty()
            walls_group.empty()
            redboss_group.empty()
            boss_sound.stop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main = False
                    game = False
                    final = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        main = False
                        final = False
                    elif event.key == pygame.K_p:
                        final = False
                        game = True
                        score = 0
                        play_already = False


            screen.fill(BLACK)
            ## code for final screen
            # display score to user, ask to play again?  quit?
            finalfontTitle2 = pygame.font.SysFont("arial", 70, bold=True)

            textTitle2 = finalfontTitle2.render("Game Over", False, BLUE)
            textRect2 = textTitle2.get_rect()
            textRect2.center = (centreX, 350)
            screen.blit(textTitle2, textRect2)

            screen.blit(finalAlien, finalAlienRect)


            ## this code can be removed it is just for example purposes
            finalfontTitle = pygame.font.SysFont("arial", 30, bold=True)

            # display final score and timer
            textTitle1 = finalfontTitle.render("Your final score: " + str(oldscore), False, BLUE)
            textRect1 = textTitle1.get_rect()
            textRect1.center = (centreX, 550)
            pygame.draw.rect(screen, WHITE, textRect1, 0)
            screen.blit(textTitle1, textRect1)

            textTitle7 = finalfontTitle.render("PLAY AGAIN [P]", False, BLUE)
            textRect7 = textTitle7.get_rect()
            textRect7.center = (centreX + 200, screenHeight - 100)
            pygame.draw.rect(screen, RED, textRect7, 0)
            screen.blit(textTitle7, textRect7)

            textTitle8 = finalfontTitle.render("QUIT [Q]", False, BLUE)
            textRect8 = textTitle8.get_rect()
            textRect8.center = (centreX - 200, screenHeight - 100)
            pygame.draw.rect(screen, RED, textRect8, 0)
            screen.blit(textTitle8, textRect8)

            pygame.display.flip()

        while final2:
            boss_sound.stop()
            aliens_group.empty()
            alienslasers_group.empty()
            playerlasers_group.empty()
            playerSpaceship_group.empty()
            heart_group.empty()
            walls_group.empty()
            redboss_group.empty()
            boss_sound.stop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main = False
                    game = False
                    final = False
                    final2 = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        main = False
                        final2 = False
                    elif event.key == pygame.K_p:
                        final2 = False
                        game = True
                        score = 0
                        play_already = False

            screen.fill(BLACK)
            ## code for final screen
            # display score to user, ask to play again?  quit?
            finalfontTitle2 = pygame.font.SysFont("arial", 70, bold=True)

            textTitle3 = finalfontTitle2.render("YOU WIN !!", False, BLUE)
            textRect3 = textTitle3.get_rect()
            textRect3.center = (centreX, 350)
            screen.blit(textTitle3, textRect3)

            screen.blit(finalAlien, finalAlienRect)

            ## this code can be removed it is just for example purposes
            finalfontTitle = pygame.font.SysFont("arial", 30, bold=True)

            # display final score and timer
            textTitle4 = finalfontTitle.render("Your final score: " + str(oldscore), False, BLUE)
            textRect4 = textTitle4.get_rect()
            textRect4.center = (centreX, 550)
            pygame.draw.rect(screen, WHITE, textRect4, 0)
            screen.blit(textTitle4, textRect4)

            textTitle5 = finalfontTitle.render("PLAY AGAIN [P]", False, BLUE)
            textRect5 = textTitle5.get_rect()
            textRect5.center = (centreX + 200, screenHeight - 100)
            pygame.draw.rect(screen, RED, textRect5, 0)
            screen.blit(textTitle5, textRect5)

            textTitle6 = finalfontTitle.render("QUIT [Q]", False, BLUE)
            textRect6 = textTitle6.get_rect()
            textRect6.center = (centreX - 200, screenHeight - 100)
            pygame.draw.rect(screen, RED, textRect6, 0)
            screen.blit(textTitle6, textRect6)


            pygame.display.flip()







    # this is instructions
    elif num ==2:
        instruction = True

        while instruction:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main = True
                    game = False
                    final = False
                    instruction = False



            screen.fill(BLACK)
            textTitle = fontTitle3.render("Move player spaceship - A,D or left and right arrows ", False, RED)
            textTitle2 = fontTitle3.render("Spacebar to shoot lasers", False, BLUE)
            textRect = textTitle.get_rect()
            textRect2 = textTitle2.get_rect()
            textRect.center = (centreX, 200)
            textRect2.center = (centreX, 250)
            screen.blit(textTitle, textRect)
            screen.blit(textTitle2, textRect2)

            textTitle3 = fontTitle3.render("= 1 point", False, WHITE)
            textRect3 = textTitle3.get_rect()
            textRect3.center = (instructionAlienRect.right + 60, 400)
            screen.blit(textTitle3, textRect3)


            textTitle4 = fontTitle3.render("= 5 point", False, WHITE)
            textRect4 = textTitle4.get_rect()
            textRect4.center = (instructionAlienbossRect.right + 60, 400)
            screen.blit(textTitle4, textRect4)


            screen.blit(RedAliensImage, controAlienRect)
            screen.blit(instructionAlien, instructionAlienRect)
            screen.blit(instructionAlienboss, instructionAlienbossRect)


            pygame.display.flip()



    # QUIT
    elif num == 3:
        print("3")






    pygame.display.update()
    #pause()

# main program -----------------------------------------------------------




# titles for different menus
menuMain = ["PLAY","INSTRUCTIONS","Quit"]


screen.fill(WHITE)

newString = ""
inputtedString = ""
# main loop
main = True
while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main = False





    screen.fill(BLACK)

    # for main menu, this menu selects the submenu or quits program
   
    choose = menu(menuMain,"SPACE INVADERS")
    if choose == 0:
        option(1)
    elif choose ==1:
        option(2)
        instruction = True
    elif choose ==2:
        main = False


                
    pygame.display.update()

pygame.quit()
sys.exit()
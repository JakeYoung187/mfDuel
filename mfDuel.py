#imports
import pygame
import os
import time
import random
import shelve

#set up window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (250, 150)
pygame.init()

size = [1000, 700]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MF DUEL")

#getting tunes man
song=0
setlist = ['./music/a.mp3', './music/b.mp3', './music/c.mp3', './music/d.mp3', './music/e.mp3', './music/f.mp3', './music/g.mp3', './music/h.mp3', './music/i.mp3']
random.shuffle(setlist)
MUSIC_ENDED = pygame.USEREVENT
pygame.mixer.music.set_endevent(MUSIC_ENDED)
pygame.mixer.music.load(setlist[song])

pygame.mixer.music.play()

#create clock
clock = pygame.time.Clock()

#groups for sprites
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
targets = pygame.sprite.Group()

#class for me
class hero(pygame.sprite.Sprite):
    def __init__(self, ship):
        pygame.sprite.Sprite.__init__(self)
        #var for my movement
        self.xspeed = 0
        self.yspeed = 0
        #whip
        self.ship = ship

        #pic for my ship
        if ship is 1:
            self.image = pygame.image.load('./artwork/1.png')
        elif ship is 2:
            self.image = pygame.image.load('./artwork/2.png')
        elif ship is 3:
            self.image = pygame.image.load('./artwork/3.png')
        elif ship is 4:
            self.image = pygame.image.load('./artwork/4.png')
        elif ship is 9:
            self.image = pygame.image.load('./artwork/fuckinbrick.png')
        elif ship is 0:
            self.image = pygame.image.load('./artwork/666.png')

        #get rectangle around me
        self.rect = self.image.get_rect()
        #starting position
        self.rect.x = 555 #925
        self.rect.y = 655


    def update(self):
        self.xspeed = 0
        self.yspeed = 0

        #get key pressed
        keystate = pygame.key.get_pressed()
        #if keystate[pygame.K_LEFT]:
        if keystate[pygame.K_d]:
            self.xspeed = -33#-15
        #if keystate[pygame.K_RIGHT]:
        if keystate[pygame.K_f]:
            self.xspeed = 33#15
        #verical movement off
        #if keystate[pygame.K_UP]:
        #    self.yspeed = -17 #-12
        #if keystate[pygame.K_DOWN]:
        #    self.yspeed = 17 #12
        
        #move me
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        
        #keep me contained
        if self.rect.x > 925:
            self.rect.x = 925
        if self.rect.x < 5:
            self.rect.x = 5
        if self.rect.y < 5:
            self.rect.y = 5
        if self.rect.y > 650:
            self.rect.y = 650

    #blat blat
    def shoot(self):
        #ridin shotgun
        if self.ship is 2:
            lshot = bullet(self.rect.centerx-30, self.rect.top, 0)
            shotpopped = bullet(self.rect.centerx, self.rect.top, 0)
            rshot = bullet(self.rect.centerx+30, self.rect.top, 0)
            all_sprites.add(lshot)
            all_sprites.add(shotpopped)
            all_sprites.add(rshot)
            bullets.add(lshot)
            bullets.add(shotpopped)
            bullets.add(rshot)
        #famas
        elif self.ship is 3:
            index = 0
            for x in range(0, 3):
                s = bullet(self.rect.centerx, self.rect.top+index, 0)
                all_sprites.add(s)
                bullets.add(s)
                index += 20
        #shoot them w their friends
        elif self.ship is 9:
            s = bullet(self.rect.centerx, self.rect.top, 1)
            all_sprites.add(s)
            bullets.add(s)
        #just op
        elif self.ship is 0:
            index = -40
            for x in range(0,5):
                s = bullet(self.rect.centerx+index, self.rect.top, 1)
                all_sprites.add(s)
                bullets.add(s)
                index += 20
        #the semi
        else:
            shotpopped = bullet(self.rect.centerx, self.rect.top, 0)
            all_sprites.add(shotpopped)
            bullets.add(shotpopped)

#*ptsd voice* they're all the same
class target(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./artwork/badguy.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.made = False

    def update(self):
        #raining down
        if self.rect.y >= 650:
            self.made = True
        self.rect.y += self.speed
        #bouncing back and fourth
        #if self.rect.x >= 925:
        #    self.backwards = True
        #elif self.rect.x <= 0:
        #    self.backwards = False
        #if self.backwards is True:
        #    self.speed = -5
        #else:
        #    self.speed = 5
        #self.rect.x += self.speed

#ammo
class bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, z):
        self.green = (0, 255, 0)
        pygame.sprite.Sprite.__init__(self)
        
        #setting bullet vars
        if z is 0:
            self.image = pygame.Surface((10, 10))
            self.image.fill(self.green)
        elif z is 1:
            self.image = pygame.image.load('./artwork/fuckinbrick.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = -60

    def update(self):
        self.rect.y += self.speed
        #at the bottom? well pretty sure they die at the top, but you know what i mean
        if self.rect.bottom < 0:
            self.kill()

#ya know the game
class game():
    def __init__(self):
        #colors
        self.black = (0, 0, 0)
        self.grey = (100, 100, 100)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)

        #set up music
        self.song = 0
        #pygame.mixer.music.load('b.mp3')
        #pygame.mixer.music.queue('d.mp3')
        #pygame.mixer.music.queue('c.mp3')
        #pygame.mixer.music.queue('a.mp3')
        #pygame.mixer.music.play(0)

        #begin
        
        #read in highscore
        self.highscore = 0
        data = open(".highscore.txt", "r")
        temp = data.readline()
        self.highscore = int(temp[3:])
        data.close()

        #run it
        self.intro()
        self.gameloop()
        pygame.quit()
        quit()

    #menu
    def intro(self):
        running=True
        #playerShipSelect=0
        ship1 = pygame.image.load('./artwork/4.png')
        ship2 = pygame.image.load('./artwork/3.png')
        ship3 = pygame.image.load('./artwork/2.png')
        ship4 = pygame.image.load('./artwork/1.png')
        self.bckg = pygame.image.load('./artwork/space.jpeg')

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.playerShipSelect=1
                        running=False
                    if event.key == pygame.K_2:
                        self.playerShipSelect=2
                        running=False
                    if event.key == pygame.K_3:
                        self.playerShipSelect=3
                        running=False
                    if event.key == pygame.K_4:
                        self.playerShipSelect=4
                        running=False
                    if event.key == pygame.K_5:
                        self.playerShipSelect=5
                        running=False
                    if event.key == pygame.K_6:
                        self.playerShipSelect=6
                        running=False
                    if event.key == pygame.K_0:
                        self.playerShipSelect=0
                        running=False
                    if event.key == pygame.K_9:
                        self.playerShipSelect=9
                        running=False
                    if event.key == pygame.K_q:
                        running = False
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_n:
                        self.changesong()
                if event.type == MUSIC_ENDED:
                    self.changesong()

            screen.fill(self.grey)
            #adds logo
            logo = pygame.image.load('./artwork/logo.png')
            screen.blit(logo, (100, 80))
            #adds instructions
            stext = pygame.font.Font('freesansbold.ttf', 35)
            tsurf, trec = self.text_objects("Enter ship ID to start the game", stext)
            trec.center = (500, 350)
            screen.blit(tsurf, trec)
            
            #adds highscore to home
            hslabel = stext.render("Highscore: ", 1, self.black)
            vhslabel = stext.render(str(self.highscore), 1, self.black)
            screen.blit(hslabel, (350, 400))
            screen.blit(vhslabel, (580, 400))
            
            #adds ships and id numbers
            screen.blit(ship4, (155, 600))
            onesurf, onerec = self.text_objects("1", stext)
            onerec.center = (190, 575)
            screen.blit(onesurf, onerec)

            screen.blit(ship3, (355, 600))
            twsurf, twrec = self.text_objects("2", stext)
            twrec.center = (390, 575)
            screen.blit(twsurf, twrec)

            screen.blit(ship2, (555, 600))
            thsurf, threc = self.text_objects("3", stext)
            threc.center = (590, 575)
            screen.blit(thsurf, threc)

            screen.blit(ship1, (755, 600))
            fsurf, frec = self.text_objects("4", stext)
            frec.center = (790, 575)
            screen.blit(fsurf, frec)
            
            #update display
            pygame.display.update()

            clock.tick(15)

    
    #places ship
    def pship(self, x, y, ship):
        screen.blit(ship, (x, y))

    #change tunes
    def changesong(self):
        self.song += 1
        pygame.mixer.music.load(setlist[self.song])
        pygame.mixer.music.play()

    #text
    def text_objects(self, text, font):
        tsurf = font.render(text, True, self.black)
        return tsurf, tsurf.get_rect()

    #display text
    def msg_display(self, string):
        largetext = pygame.font.Font('freesansbold.ttf', 80)
        tsurf, trec = self.text_objects(string, largetext)
        trec.center = (500, 350)
        screen.blit(tsurf, trec)
        pygame.display.update()
        time.sleep(2)
        self.restart()
        #pygame.quit()
        #quit()

    def restart(self):
        all_sprites.empty()
        bullets.empty()
        targets.empty()
        main()

    #where the action is at
    def gameloop(self):
        #var to break game loop
        done = False

        #create player
        self.hero = hero(self.playerShipSelect)
        all_sprites.add(self.hero)

        #create targets
        tleft = 0

        for x in range(0,10):
            t = target(random.randint(0, 600), 0)
            targets.add(t)
            all_sprites.add(t)
            tleft += 1

        #set hero start pos
        self.x = 925
        self.y = 655

        #hero movement
        xchg = 0
        ychg = 0

        #get ready to tear
        screen.fill(self.grey)
        ready = pygame.font.Font("freesansbold.ttf", 40)
        rsurf, rrec = self.text_objects("get ready for the shit", ready)
        tsurf, trec = self.text_objects("if they get passed, all those kids are def dead", ready)
        ssurf, srec = self.text_objects("use d and f to move and j and k to shoot", ready) 
        vsurf, vrec = self.text_objects("Your whip", ready)

        rrec.center = (500, 200)
        trec.center = (500, 250)
        srec.center = (500, 350)
        vrec.center = (515, 550)

        screen.blit(rsurf, rrec)
        screen.blit(tsurf, trec)
        screen.blit(ssurf, srec)
        screen.blit(vsurf, vrec)
        screen.blit(self.hero.image, (480, 580))

        pygame.display.update()
        time.sleep(4)

        #score var
        self.score = 0
        myfont = pygame.font.SysFont("Times New Roman", 36)
        scorelabel = myfont.render("Score: ", 1, self.white)
        hscorelabel = myfont.render("Highscore: ", 1, self.white)
        sclabel = myfont.render(str(self.score), 1, self.white)
        hslabel = myfont.render(str(self.highscore), 1, self.white)
        screen.blit(scorelabel, (0, 500))
        screen.blit(sclabel, (100, 500))
        screen.blit(hscorelabel, (0, 530))
        screen.blit(hslabel, (170, 530))

        pygame.display.update()

        #start loop
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    #if event.key == pygame.K_SPACE:
                    #if event.key == pygame.K_f:
                    if event.key == pygame.K_j:
                        self.hero.shoot()
                    #if event.key == pygame.K_d:
                    if event.key == pygame.K_k:
                        self.hero.shoot()
                    if event.key == pygame.K_n:
                        self.changesong()
                elif event.type == MUSIC_ENDED:
                    self.changesong()

            screen.blit(self.bckg, (0, 0))
            all_sprites.update()

            sclabel = myfont.render(str(self.score), 1, self.white)
            screen.blit(scorelabel, (0, 500))
            screen.blit(sclabel, (100, 500))
            hslabel = myfont.render(str(self.highscore), 1, self.white)
            screen.blit(hscorelabel, (0, 530))
            screen.blit(hslabel, (170, 530))

            for t in targets:
                if t.rect.y >= 655:
                    if self.score > self.highscore:
                        self.highscore = self.score
                        d = open(".highscore.txt", "w+")
                        d.write("hs="+str(self.highscore))
                        d.close()
                        
                    self.msg_display("they fuckin got ya bud")
                    done = True

            hits = pygame.sprite.groupcollide(targets, bullets, True, True)
            for h in hits:
                t = target(random.randint(0, 700), 0)
                all_sprites.add(t)
                targets.add(t)
                self.score += 1

            all_sprites.draw(screen)

            pygame.display.update()

            clock.tick(30)


def main():
    g = game()

if __name__=="__main__":
        main()

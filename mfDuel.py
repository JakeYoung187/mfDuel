import pygame
import os
import time

#set up window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (250, 150)
pygame.init()

size = [1000, 700]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MF_DUEL")

clock = pygame.time.Clock()

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

        self.ship = ship

        #pic my ship
        if ship is 1:
            self.image = pygame.image.load('1.png')
        elif ship is 2:
            self.image = pygame.image.load('2.png')
        elif ship is 3:
            self.image = pygame.image.load('3.png')
        elif ship is 4:
            self.image = pygame.image.load('4.png')
        elif ship is 0:
            self.image = pygame.image.load('666.png')

        #get rectangle around me
        self.rect = self.image.get_rect()
        self.rect.x = 925
        self.rect.y = 655


    def update(self):
        self.xspeed = 0
        self.yspeed = 0

        #get key pressed
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.xspeed = -15
        if keystate[pygame.K_RIGHT]:
            self.xspeed = 15
        if keystate[pygame.K_UP]:
            self.yspeed = -12
        if keystate[pygame.K_DOWN]:
            self.yspeed = 12
        
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
        if self.ship is 2:
            lshot = bullet(self.rect.centerx-30, self.rect.top)
            shotpopped = bullet(self.rect.centerx, self.rect.top)
            rshot = bullet(self.rect.centerx+30, self.rect.top)
            all_sprites.add(lshot)
            all_sprites.add(shotpopped)
            all_sprites.add(rshot)
            bullets.add(lshot)
            bullets.add(shotpopped)
            bullets.add(rshot)
        elif self.ship is 0:
            index = -20
            for x in range(0,5):
                s = bullet(self.rect.centerx+index, self.rect.top)
                all_sprites.add(s)
                bullets.add(s)
                index += 10


        else:
            shotpopped = bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(shotpopped)
            bullets.add(shotpopped)

#*ptsd voice* they're all the same
class target(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('fuckinbrick.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.made = False

    def update(self):
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
    def __init__(self, x, y):
        self.green = (0, 255, 0)
        pygame.sprite.Sprite.__init__(self)
        
        #setting bullet vars
        self.image = pygame.Surface((10, 10))
        self.image.fill(self.green)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = -30

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

        #begin
        self.intro()
        self.gameloop()
        pygame.quit()
        quit()

    #menu
    def intro(self):
        running=True
        #playerShipSelect=0
        ship1 = pygame.image.load('4.png')
        ship2 = pygame.image.load('3.png')
        ship3 = pygame.image.load('2.png')
        ship4 = pygame.image.load('1.png')
        self.bckg = pygame.image.load('space.jpeg')

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

            screen.fill(self.grey)
            #adds logo
            logo = pygame.image.load('logo.png')
            screen.blit(logo, (100, 80))
            #adds instructions
            stext = pygame.font.Font('freesansbold.ttf', 35)
            tsurf, trec = self.text_objects("Enter Ship ID to Start the shit", stext)
            trec.center = (500, 350)
            screen.blit(tsurf, trec)
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
        pygame.quit()
        quit()

    #where the action is at
    def gameloop(self):
        #var to break game loop
        done = False

        #create player
        self.hero = hero(self.playerShipSelect)
        all_sprites.add(self.hero)

        #create targets
        tleft = 0

        t = target(100, 0)
        targets.add(t)
        all_sprites.add(t)
        tleft += 1

        t2 = target(600, 0)
        targets.add(t2)
        all_sprites.add(t2)
        tleft += 1

        t3 = target(200, 0)
        targets.add(t3)
        all_sprites.add(t3)
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
        rsurf, rrec = self.text_objects("get ready, shoot the targets", ready)
        tsurf, trec = self.text_objects("if they get passed, all those kids are def dead", ready)
        ssurf, srec = self.text_objects("use arrows to steer and f or d to bust caps", ready)
        
        rrec.center = (500, 200)
        trec.center = (500, 250)
        srec.center = (500, 350)

        screen.blit(rsurf, rrec)
        screen.blit(tsurf, trec)
        screen.blit(ssurf, srec)

        pygame.display.update()
        time.sleep(5)

        #start loop
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    #if event.key == pygame.K_SPACE:
                    if event.key == pygame.K_f:
                        self.hero.shoot()
                    if event.key == pygame.K_d:
                        self.hero.shoot()
            
            screen.blit(self.bckg, (0, 0))
            all_sprites.update()

            for t in targets:
                if t.rect.y >= 655:
                    self.msg_display("they fuckin got ya bud")
                    done = True

            hits = pygame.sprite.groupcollide(targets, bullets, True, True)
            if hits:
                #if more than one target use this
                tleft -= 1
                if tleft is 0:
                    self.msg_display("fuckin got 'em bud")
                    done = True

            all_sprites.draw(screen)
            
            pygame.display.update()

            clock.tick(30)


if __name__=="__main__":
    g = game()




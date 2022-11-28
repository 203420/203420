import pygame, math, time, os, threading

#IMAGES
PERSONAJE_IMG = pygame.image.load(os.path.join('Proyecto_Final/Assets','soldier.png'))
PERSONAJE = pygame.transform.scale(PERSONAJE_IMG, (70,75))

PERSONAJE2_IMG = pygame.image.load(os.path.join('Proyecto_Final/Assets','soldierL.png'))
PERSONAJE2 = pygame.transform.scale(PERSONAJE2_IMG, (70,75))

ZOMBIE_IMG = pygame.image.load(os.path.join('Proyecto_Final/Assets','zombie.png'))
ZOMBIE = pygame.transform.scale(ZOMBIE_IMG, (65,70))

ZOMBIE_IMGA = pygame.image.load(os.path.join('Proyecto_Final/Assets','zombieA.png'))
ZOMBIEA = pygame.transform.scale(ZOMBIE_IMGA, (65,70))

ZOMBIE_IMGB = pygame.image.load(os.path.join('Proyecto_Final/Assets','zombieB.png'))
ZOMBIEB = pygame.transform.scale(ZOMBIE_IMGB, (80,85))

SPEED_IMG = pygame.image.load(os.path.join('Proyecto_Final/Assets','speed.png'))
SPEED = pygame.transform.scale(SPEED_IMG, (50,50))

HEALTH_IMG = pygame.image.load(os.path.join('Proyecto_Final/Assets','health.png'))
HEALTH = pygame.transform.scale(HEALTH_IMG, (50,50))

DAMAGE_IMG = pygame.image.load(os.path.join('Proyecto_Final/Assets','damage.png'))
DAMAGE = pygame.transform.scale(DAMAGE_IMG, (60,60))

WHITE = 255,255,255
WIDTH, HEIGHT = 1080, 650


imgreload = pygame.image.load(os.path.join('Proyecto_Final/Assets','reload.png'))
relo = pygame.transform.scale(imgreload, (20,20))

contador = 0

#FONT
FONT = os.path.join('Proyecto_Final/Assets','UpheavalPro.ttf')

#CLASSES
class ZombieNormal(threading.Thread):
    spawn = True
    def __init__(self, x, y, speed):
        threading.Thread.__init__(self)
        self.image = ZOMBIE
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.health = 5
        self.damage = 1

    def run(self, WIN):
        global contador;

        if self.spawn == True:
            self.move()
            self.draw(WIN)            

        if self.rect.x < -1:
            contador += 1
            #self.rect.x = 10
            self.spawn = False

    def move(self):
        if self.direction == 'RIGHT':
            self.rect.x = self.rect.x+self.speed
        if self.direction == 'LEFT':
            self.rect.x = self.rect.x-self.speed
        if self.direction == 'UP':
            self.rect.y = self.rect.y-self.speed
        if self.direction == 'DOWN':
            self.rect.y = self.rect.y+self.speed

    def collided(self, other_rect):
        return self.rect.colliderect(other_rect)

    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        zombie_health = pygame.font.Font(FONT, 12).render("Vida: "+ str(self.health), True, WHITE)
        WIN.blit(zombie_health, (self.rect.x, self.rect.y - 20))

class ZombieAdvanced(threading.Thread):
    spawn = True
    def __init__(self, x, y, speed):
        threading.Thread.__init__(self)
        self.image = ZOMBIEA
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.health = 10
        self.damage = 2

    def run(self, WIN):
        global contador;

        if self.spawn == True:
            self.move()
            self.draw(WIN)            

        if self.rect.x < -1:
            contador += 1
            #self.rect.x = 10
            self.spawn = False

    def move(self):
        if self.direction == 'RIGHT':
            self.rect.x = self.rect.x+self.speed
        if self.direction == 'LEFT':
            self.rect.x = self.rect.x-self.speed
        if self.direction == 'UP':
            self.rect.y = self.rect.y-self.speed
        if self.direction == 'DOWN':
            self.rect.y = self.rect.y+self.speed

    def collided(self, other_rect):
        return self.rect.colliderect(other_rect)

    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        zombie_health = pygame.font.Font(FONT, 12).render("Vida: "+ str(self.health), True, WHITE)
        WIN.blit(zombie_health, (self.rect.x, self.rect.y - 20))



class ZombieBoss(threading.Thread):
    spawn = True
    def __init__(self, x, y, speed):
        threading.Thread.__init__(self)
        self.image = ZOMBIEB
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.health = 30
        self.damage = 5    

    def run(self, WIN):
        global contador;

        if self.spawn == True:
            self.move()
            self.draw(WIN)            

        if self.rect.x < -1:
            contador += 1
            #self.rect.x = 10
            self.spawn = False

    def move(self):
        if self.direction == 'RIGHT':
            self.rect.x = self.rect.x+self.speed
        if self.direction == 'LEFT':
            self.rect.x = self.rect.x-self.speed
        if self.direction == 'UP':
            self.rect.y = self.rect.y-self.speed
        if self.direction == 'DOWN':
            self.rect.y = self.rect.y+self.speed

    def collided(self, other_rect):
        return self.rect.colliderect(other_rect)

    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        zombie_health = pygame.font.Font(FONT, 12).render("Vida: "+ str(self.health), True, WHITE)
        WIN.blit(zombie_health, (self.rect.x, self.rect.y - 20))



class Player(threading.Thread):    
    
    def __init__(self, width, height, speed,WIN):
        threading.Thread.__init__(self)
        self.image = PERSONAJE
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.direction = 'RIGHT'
        self.speed = speed
        self.health = 10
        self.damage = 1
        self.balas = 10
        self.x = 100000
        self.shot = True
        self.WIN = WIN

    def run(self):
        
        while True:
            if self.x > 0 and self.shot == False:                 
                while self.x > 0:                    
                    self.drawReload()                
                    self.x -= 1
                self.shot = True
                self.x = 100000
                self.balas = 10


    def moveDirection(self, direction):
        if direction == 'RIGHT':
            self.rect.x = self.rect.x+self.speed
        if direction == 'LEFT':
            self.rect.x = self.rect.x-self.speed
        if direction == 'UP':
            self.rect.y = self.rect.y-self.speed
        if direction == 'DOWN':
            self.rect.y = self.rect.y+self.speed

    def rotate(self, x, y):
        rel_x, rel_y = x - self.rect.x, y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        if angle > 90 or angle < -90:
            self.image = PERSONAJE2
        else: 
            self.image = PERSONAJE

    def collided(self, other_rect):
        return self.rect.colliderect(other_rect)

    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

    def get_font(size):
        return pygame.font.Font(FONT, size)

    def drawReload(self):
        self.WIN.blit(relo, ( self.rect.x - 20 ,self.rect.y - 40 ))    


class PowerUp:
    def __init__(self, speed, type, direction, player):
        self.speed = speed
        self.type = type
        self.direction = direction
        self.player = player

        if self.type == 1:
            self.image = SPEED
        elif self.type == 2:
            self.image = HEALTH
        elif self.type == 3:
            self.image = DAMAGE

        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        
    def move(self):
        if self.direction == 'RIGHT':
            self.rect.x = self.rect.x+self.speed
        if self.direction == 'LEFT':
            self.rect.x = self.rect.x-self.speed
        if self.direction == 'UP':
            self.rect.y = self.rect.y-self.speed
        if self.direction == 'DOWN':
            self.rect.y = self.rect.y+self.speed

    def collided(self, other_rect):
        return self.rect.colliderect(other_rect)

    def activate(self):
        if self.type == 1:
            self.player.speed = 6
        elif self.type == 2:
            self.player.health = 10
        elif self.type == 3:
            self.player.damage = 2

    def draw(self,WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))


class Bullet:
    def __init__(self, color, x, y, width, height, speed, targetx,targety):
        self.rect = pygame.Rect(x,y,width,height)
        self.color = color
        self.direction = 'RIGHT'
        self.speed = speed
        angle = math.atan2(targety-y, targetx-x) 
        self.dx = math.cos(angle)*speed
        self.dy = math.sin(angle)*speed
        self.x = x
        self.y = y

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def collided(self, other_rect):
        return self.rect.colliderect(other_rect)

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, self.rect)


def recont():
    return contador
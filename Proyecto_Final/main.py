import pygame, random, os, time
from button import Button
from classes import ZombieNormal, Player, Bullet, PowerUp, ZombieAdvanced, recont, ZombieBoss

WIDTH, HEIGHT = 1080, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ZombieZ!")
clock = pygame.time.Clock()

pygame.mixer.init()

#COLORS
ALPHA = 0, 255, 0
GREEN = 0,255,0
RED = 255,0,0
BLUE = 0,0,255
YELLOW = 255,255,0
WHITE = 255,255,255
BLACK = 0,0,0
COLOR_TEXT = 251, 245, 188
ORANGE = 219, 134, 58

#FONT
FONT = os.path.join('Proyecto_Final/Assets','UpheavalPro.ttf')


#IMAGES
BACKGROUND_GAME = pygame.image.load(os.path.join('Proyecto_Final/Assets','background.jpg'))
BACKGROUND_MENU = pygame.image.load(os.path.join('Proyecto_Final/Assets','menu_background.jpg'))
CONTROLS = pygame.image.load(os.path.join('Proyecto_Final/Assets','controls.png'))


#SOUNDS
MUSIC = pygame.mixer.music.load(os.path.join('Proyecto_Final/Assets','game_music.mp3'))
pygame.mixer.music.set_volume(0.175)
pygame.mixer.music.play(-1)

shoot = pygame.mixer.Sound(os.path.join('Proyecto_Final/Assets','Gun12.wav'))
pygame.mixer.Sound.set_volume(shoot, 0.28)

reload = pygame.mixer.Sound(os.path.join('Proyecto_Final/Assets','reload.wav'))
pygame.mixer.Sound.set_volume(reload, 0.25)

alert = pygame.mixer.Sound(os.path.join('Proyecto_Final/Assets','alert.wav'))
pygame.mixer.Sound.set_volume(alert, 0.2)

alarm = pygame.mixer.Sound(os.path.join('Proyecto_Final/Assets','alarm.wav'))
pygame.mixer.Sound.set_volume(alarm, 0.25)

hit = pygame.mixer.Sound(os.path.join('Proyecto_Final/Assets','HIT.wav'))
pygame.mixer.Sound.set_volume(hit, 0.045)

hit_player = pygame.mixer.Sound(os.path.join('Proyecto_Final/Assets','Hit10.wav'))
pygame.mixer.Sound.set_volume(hit_player, 0.045)

zombie_attack = pygame.mixer.Sound(os.path.join('Proyecto_Final/Assets','zombie_attack.wav'))
pygame.mixer.Sound.set_volume(zombie_attack, 0.05)
 
#GAME ELEMENTS
bullets = []
enemies = []
powerUps = []

SCORE = 0
ZOMBIE_KILLED = 0
ACTIVATE = 0
BOOST = False
BOOST_IMG1 = 0
BOOST_IMG2 = 0
BOOST_IMG3 = 0


def draw_window(player, cont):
    WIN.blit(BACKGROUND_GAME,(0,0))
    
    for b in bullets:
        b.draw(WIN)
    for e in enemies:
        e.run(WIN)
        if e.rect.x < -10:
            del enemies[b]
    for p in powerUps:
        p.draw(WIN)
    player.draw(WIN)

    player_health = get_font(14).render("Vida: "+ str(player.health), True, WHITE)
    WIN.blit(player_health, (player.rect.x - 5, player.rect.y - 20))

    score = get_font(18).render("Puntos: "+ str(SCORE), True, WHITE)
    WIN.blit(score, (40, 25))

    zCont = get_font(18).render("Zombies avanzaron: "+ str(cont), True, WHITE)
    WIN.blit(zCont, (40, 625))

    if BOOST == True:
        if BOOST_IMG1 != 0:
            WIN.blit(BOOST_IMG1, (35, 45))
        if BOOST_IMG2 != 0:
            WIN.blit(BOOST_IMG2, (70, 45))
        if BOOST_IMG3 != 0:
            WIN.blit(BOOST_IMG3, (105, 45))



    pygame.display.flip()
    pygame.display.update()


def manage_movement(player):
    #Keys/Teclas        
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w] and player.rect.y - player.speed > 5:             
        player.moveDirection('UP')     
    if pressed[pygame.K_a] and player.rect.x - player.speed > 50:
        player.moveDirection('LEFT')
    if pressed[pygame.K_s] and player.rect.y + player.speed + player.height < HEIGHT:
        player.moveDirection('DOWN')
    if pressed[pygame.K_d] and player.rect.x + player.speed + player.width < 900:
        player.moveDirection('RIGHT')

    #Elements/Elementos
    for b in bullets:
        b.move()
    for p in powerUps:
        p.move()


def manage_collisions(player):
    global SCORE;
    global ZOMBIE_KILLED; 
    global ACTIVATE; 
    global BOOST;
    global BOOST_IMG1;
    global BOOST_IMG2;
    global BOOST_IMG3;

    for i in reversed(range(len(bullets))):
        for j in reversed(range(len(enemies))):
            if bullets[i].collided(enemies[j].rect):
                pygame.mixer.Sound.play(hit)
                del bullets[i]
                enemies[j].health -= player.damage
                if enemies[j].health < 1:
                    enemies[j].spawn = False
                    t = enemies[j].__class__.__name__
                    del enemies[j]
                    if t == "ZombieNormal":
                        SCORE += 100
                    elif t == "ZombieAdvanced":
                        SCORE += 250
                    ZOMBIE_KILLED += 1
                break

    for i in reversed(range(len(enemies))):
        if enemies[i].collided(player.rect):
            pygame.mixer.Sound.play(zombie_attack)
            #pygame.mixer.Sound.play(hit_player)
            player.health -= enemies[i].damage
            if player.rect.x > 50 and player.rect.x < 150:
                if player.rect.y > 450:
                    player.rect.y = player.rect.y - 95
                else:
                    player.rect.y = player.rect.y + 95
            elif player.rect.x > 150:
                if player.rect.y > 450:
                    player.rect.y = player.rect.y - 50
                    player.rect.x = player.rect.x - 100
                else:
                    player.rect.y = player.rect.y + 50
                    player.rect.x = player.rect.x - 100

            print(player.health)
            break

    for i in reversed(range(len(powerUps))):
        if powerUps[i].collided(player.rect):
            pygame.mixer.Sound.play(alert)
            ACTIVATE = SCORE
            powerUps[i].activate()
            BOOST = True
            if powerUps[i].type == 1:
                BOOST_IMG1 = powerUps[i].image
            elif powerUps[i].type == 2:
                BOOST_IMG2 = powerUps[i].image
            elif powerUps[i].type == 3:
                BOOST_IMG3 = powerUps[i].image
            del powerUps[i]
            break


def spawn_objects(player):
    global ZOMBIE_KILLED;
    if random.randint(1,115) == 1:
        y = random.randint(20 ,HEIGHT-50)
        if ZOMBIE_KILLED >= 20:   
            e = ZombieBoss(1050, y, 4)
            e.direction = 'LEFT'
            pygame.mixer.Sound.play(alarm)
            ZOMBIE_KILLED = 0
        else:
            ztype = random.randint(0, 10)
            if ztype <= 8:
                e = ZombieNormal(1050,y, 4)
                e.direction = 'LEFT'
            if ztype > 8:
                e = ZombieAdvanced(1050,y, 6)
                e.direction = 'LEFT'

        enemies.append(e)

    if random.randint(1,1250) == 1:
        t = random.randint(1,3)
        x = random.randint(60, WIDTH-200)
        p = PowerUp(5, t, 'DOWN', player)
        p.rect.x = x
        p.rect.y = -50
        powerUps.append(p)


def game_loop(player):
    global SCORE;
    global ACTIVATE;
    global BOOST;
    global BOOST_IMG1;
    global BOOST_IMG2;
    global BOOST_IMG3;

    run = True
    while run:
        clock.tick(45)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False                        

            contador = recont()            

            if player.health < 1 or contador > 10:
                game_text = get_font(120).render("Game Over", True, WHITE)
                text_rect = game_text.get_rect(center=(540, 150))
                WIN.blit(game_text, text_rect)
                pygame.display.update()
                time.sleep(3)
                run = False

            x,y = pygame.mouse.get_pos() 
            player.rotate(x,y)   
            
            if player.balas > 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    b = Bullet(WHITE, player.rect.centerx, player.rect.centery - 9, 5,3, 22, x,y)
                    pygame.mixer.Sound.play(shoot)
                    bullets.append(b)
                    player.balas -= 1
            else:                            
                player.shot = False
                #pygame.mixer.Sound.play(reload)

        if SCORE - ACTIVATE >= 1000:
            player.damage = 1
            player.speed = 4
            BOOST = False
            BOOST_IMG1 = 0
            BOOST_IMG2 = 0
            BOOST_IMG3 = 0
            
        manage_movement(player)
        spawn_objects(player)
        manage_collisions(player)
        draw_window(player, contador)

    pygame.quit()


def main_menu():
    while True:
        WIN.blit(BACKGROUND_MENU, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("ZombieZ!", True, ORANGE)
        menu_rect = menu_text.get_rect(center=(540, 150))

        PLAY_BUTTON = Button(image=pygame.image.load(os.path.join('Proyecto_Final/Assets','button-img.png')), pos=(540, 320), 
                            text_input="JUGAR", font=get_font(75), base_color= COLOR_TEXT, hovering_color= WHITE)

        WIN.blit(menu_text, menu_rect)

        PLAY_BUTTON.changeColor(menu_mouse_pos)
        PLAY_BUTTON.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(menu_mouse_pos):
                    player = Player(70, 75, 4,WIN)                    
                    player.start()                    # inicio de hilo de jugadorcito
                    player.rect.x = 340
                    player.rect.y = 250
                    WIN.fill(BLACK)
                    pygame.display.update()
                    time.sleep(0.25)
                    WIN.blit(CONTROLS,(0,0))
                    pygame.display.update()
                    time.sleep(5)
                    WIN.fill(BLACK)
                    pygame.display.update()
                    time.sleep(0.5)
                    game_loop(player)        
        pygame.display.update()
    

def get_font(size):
    return pygame.font.Font(FONT, size)


if __name__=="__main__":
    pygame.init()
    main_menu()
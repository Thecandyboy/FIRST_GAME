import pygame 
import os
pygame.font.init()
pygame.mixer.init()
pygame.init()

# Gaming Parameters :
WIDTH , HEIGHT = 900 , 500

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255,0,0)

FPS = 60 
VEL = 5
BULLET_VEL = 15
MAX_BULLET_COUNT = 3
BULLET_WIDTH , BULLET_HEIGHT = 10,5 

HEALTH = 5
HEALTH_FONT = pygame.font.SysFont("comicsans",40)
WINNER_FONT = pygame.font.SysFont("comicsans",80)

BORDER_WIDTH , BORDER_HEIGHT = 10,HEIGHT 
BORDER = pygame.Rect((WIDTH-BORDER_WIDTH)/2,0,BORDER_WIDTH,BORDER_HEIGHT)

#CUSTOM EVENT :
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2  

SPACE_SHIP_WIDTH ,SPACE_SHIP_HEIGHT = 55,40 
#IMAGE LOADING
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Spaceship shooter','Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP_SCALED = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACE_SHIP_WIDTH,SPACE_SHIP_HEIGHT))
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP_SCALED,90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Spaceship shooter','Assets','spaceship_red.png'))
RED_SPACESHIP_SCALED = pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACE_SHIP_WIDTH,SPACE_SHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP_SCALED,270)

SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Spaceship shooter',"Assets","space.png")),(WIDTH,HEIGHT))

#SOUND LOADING 
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Spaceship shooter","Assets","Gun+Silencer.mp3"))
BULLET_HIT_SOUND =pygame.mixer.Sound(os.path.join("Spaceship shooter","Assets","Assets_Grenade+1.mp3"))

#Display window   (pygame.quit()) => part of main function 
WIN = pygame.display.set_mode((WIDTH,HEIGHT))   #win => window
pygame.display.set_caption("SPACE SHOOTER GAME")

def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health,win_text,running) :
    WIN.blit(SPACE_BACKGROUND,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)

    red_health_text = HEALTH_FONT.render("Health :" + str(red_health) ,True,RED)
    yellow_health_text = HEALTH_FONT.render("Health :" + str(yellow_health) ,True,YELLOW)

    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10 , 10))
    WIN.blit(yellow_health_text,(10,10))

    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    if win_text != "" :
        winner_text = WINNER_FONT.render(win_text,True,WHITE)
        WIN.blit(winner_text,((WIDTH - winner_text.get_width())//2,(HEIGHT-winner_text.get_height())//2))
        pygame.display.update()
        pygame.time.delay(5000)
        red_bullets = []
        yellow_bullets = []
        
    for bullet in red_bullets :
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in yellow_bullets :
        pygame.draw.rect(WIN,YELLOW,bullet)   
    pygame.display.update()

def yellow_move(keys_pressed,yellow) :
    if(keys_pressed[pygame.K_w] and yellow.y - VEL > 0 ) :   #UP
        yellow.y -= VEL
    if(keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT) :  #DOWN
        yellow.y += VEL
    if(keys_pressed[pygame.K_a] and yellow.x - VEL > 0 ) :    #LEFT
        yellow.x -= VEL
    if(keys_pressed[pygame.K_d] and yellow.x + yellow.width + VEL < BORDER.x) :   #RIGHT
        yellow.x += VEL

def red_move(keys_pressed,red):
    if(keys_pressed[pygame.K_UP] and red.y - VEL > 0) :    #UP
        red.y -= VEL
    if(keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT) :   #DOWN
        red.y += VEL
    if(keys_pressed[pygame.K_LEFT] and red.x > BORDER.x + BORDER_WIDTH) :    #LEFT
        red.x -= VEL
    if(keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width< WIDTH) :   #RIGHT
        red.x += VEL

def move_bullets(yellow_bullets,red_bullets,yellow,red) :
    for bullet in red_bullets :
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet) :
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif (bullet.x + bullet.width < 0) :
            red_bullets.remove(bullet)
                            
    for bullet in yellow_bullets :
        bullet.x += BULLET_VEL
        if red.colliderect(bullet) :
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif (bullet.x > WIDTH) :
            yellow_bullets.remove(bullet)
    
def main() :
    yellow = pygame.Rect(20,HEIGHT//2,SPACE_SHIP_HEIGHT,SPACE_SHIP_WIDTH)
    red = pygame.Rect(WIDTH - SPACE_SHIP_WIDTH,HEIGHT//2,SPACE_SHIP_HEIGHT,SPACE_SHIP_WIDTH)
    
    yellow_bullets = []
    red_bullets = []

    yellow_health = HEALTH
    red_health = HEALTH
    
    clock = pygame.time.Clock()
    game_end = False
    running = True 
    while running :
        clock.tick(FPS)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
                pygame.quit()
                       
            if event.type == pygame.KEYDOWN and running == True :
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET_COUNT :    #For yellow
                    bullet = pygame.Rect((yellow.x + yellow.width) , yellow.y+(yellow.height/2),BULLET_WIDTH,BULLET_HEIGHT) 
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLET_COUNT :    #for red
                    bullet = pygame.Rect(red.x,red.y+(red.height/2),BULLET_WIDTH,BULLET_HEIGHT)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT :
                red_health = max(0,red_health-1)
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT :
                yellow_health = max(0,yellow_health-1)
                BULLET_HIT_SOUND.play()
 
        move_bullets(yellow_bullets,red_bullets,yellow,red) 
        
        keys_pressed = pygame.key.get_pressed()
        if running == True :
            yellow_move(keys_pressed,yellow) 
            red_move(keys_pressed,red)

        win_text =""

        if red_health == 0 :
            win_text = "YELLOW WINS !!!"
            running = False

        if yellow_health == 0 :
            win_text = "RED WINS !!!"
            running = False 
        
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health,win_text,running)
    main()

if __name__ == "__main__" :   #this line is to make sure that the following is executed only when this file is directely run and not when this is imported to some other file and it is run .
    main()
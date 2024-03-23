from pygame import *
from random import randint
from time import time as timer

win = display.set_mode((888,555))
display.set_caption('zxctir')
lost = 0
mixer.init()
mixer.music.load('ddd.mp3')
mixer.music.play()
mixer.init()
mixer.music.load('gun_shot.mp3')

font.init()
font1 = font.Font(None, 33)
won = font1.render('WIN',True,(0,4,222))
lose = font1.render('LOSE',True,(0,4,222))
font2 = font.Font(None, 22)

global score
score = 0
goal = 10
game = True
class GameSprite(sprite.Sprite):
    def __init__(self , p_img , p_x , p_y ,p_spe, p_s_x , p_s_y ):
        super().__init__()
        self.image = transform.scale(image.load(p_img) , (p_s_x , p_s_y ))
        self.speed = p_spe
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        win.blit(self.image,(self.rect.x , self.rect.y))

class wall(sprite.Sprite):
    def __init__(self, color_1,color_2,color_3, wall_x,wall_y,wall_width,wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width , self.height))
        self.image.fill((color_1,color_2,color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        win.blit(self.image, (self.rect.x , self.rect.y))
    pass
class Player(GameSprite):
    def update(self):
        global last_time
        global rel_time
        global num_fire
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0 :
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 800 :
            self.rect.x += self.speed
        if keys_pressed[K_w] and self.rect.y > 0 :
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 800 :
            self.rect.y += self.speed
        if keys_pressed[K_SPACE]:
            if num_fire < 30 and rel_time == False:
                num_fire += 1
                self.fire()
                mixer.music.play()
            if num_fire >= 30 and rel_time == False:
                last_time = timer()
                rel_time = True
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx , self.rect.top, 15,15,21)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Enemy1(GameSprite):
    direct = 'left'
    def update(self):
        if self.rect.x <= 500:
            self.direct = 'right'
        if self.rect.x >= 800:
            self.direct = 'left'

        if self.direct == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 888:
            self.rect.y = 0
            self.rect.x = randint(50,888-50)
            lost = lost + 1
            print(lost)
        
class Boss(GameSprite):
    def update(self):
        self.rect.y += self.speed
        
bg = GameSprite('orig.jpg', 0, 0, 0, 1000, 900)
play = Player('ппп.jpg', 300, 444, 25, 50 , 50)
boss = Boss('ddd.jfif', 0, 0, 0, 11 , 111)
end = GameSprite('Ананас.png',800 , 20,5,50,50)
enemy1 = Enemy1('Ананас.png', 600, 360, 5, 65 , 65)

Enemys = sprite.Group()
for i in range(1,5):
    enemy = Enemy('fg.png' , randint(50,888-50),5,3,50,50)
    Enemys.add(enemy)

bullets = sprite.Group()
life = 3
BossHP = 25
w1 = wall(155,5,222, 300,250,555,10) #blue
w2 = wall(1,1,1,1,400,650,10) #black
w3 = wall(255,5,3, 0,100,770,10) #red
clock = time.Clock()
last_time = timer()

rel_time = False
num_fire = 0
while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
    text_score = font2.render('Счет: '+str(score), True , (0,40,2))
    txt_lose = font2.render('Счет: '+str(lost), True , (111,40,2))
    txt_life = font2.render('life: '+str(life), True , (111,40,2))
    collid = sprite.groupcollide(Enemys , bullets , True,True)
    for v in collid:
        score += 1
        enemy = Enemy('fg.png' , randint(50,888-50),10,6,50,50)
    Enemys.add(enemy)

    if rel_time == True:
        now_time = timer()
        if now_time - last_time < 2:
            ammo_no = font2.render('NO AMMO',1,(150,100,0))
            win.blit(ammo_no,(222,333))
        else:
            num_fire = 0
            rel_time = False
    if score > 1:
        boss.reset()
    
    bg.reset()
    
    win.blit(text_score, (10,10))
    win.blit(txt_lose, (10,33))
    win.blit(txt_life, (500,33))
    play.update()
    play.reset()
    boss.update()
    end.reset()
    end.update()
    w1.draw_wall()
    w2.draw_wall()
    w3.draw_wall()
    Enemys.draw(win)
    Enemys.update()
    bullets.draw(win)
    enemy1.update()
    enemy1.reset()
    
    
    bullets.update()
    if sprite.collide_rect(play, end):
        win.blit(won , (350,300))
        play.rect.x = 0
        play.rect.y = 500
    if sprite.collide_rect(play, w1) or sprite.collide_rect(play, w2) or sprite.collide_rect(play, w3) or sprite.collide_rect(play, enemy1):
        win.blit(lose , (200,200))
        life -= 1
    if sprite.spritecollide(boss, bullets, True):
        BossHP -= 1
    if sprite.spritecollide(play, Enemys, True) or lost >=39 :
        life -= 1
        enemy = Enemy('fg.png' , randint(50,888-50),10,6,50,50)
        Enemys.add(enemy)
    if score >= goal:
        win.blit(won , (350,300))
    if life <= 0:
        win.blit(lose , (350,300))
    if BossHP <= 0 :
        boss.kill()
    if life == -1:
        breaka
    if sprite.collide_rect(play, end):
        win.blit(won , (200,200))
        hero.rect.x = 0
        hero.rect.y = 0
    display.update()
    clock.tick(60)
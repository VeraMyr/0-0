from pygame import *
import random
from pygame import mixer
from random import randint
from time import time as timer
font.init()

lost = 0
score = 0

class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, player_speed):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (65, 65))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
        if key_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction = 'down'
    def update(self):
        global lost
        self.direction = 'down'
        if self.direction == 'down':
            self.rect.y += self.speed
        if self.rect.y >= 405:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(0, 630)
class Bullet(GameSprite):
    def update(self):
        #global score
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


window = display.set_mode((700, 500))
display.set_caption('Шутер')

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

font1 = font.Font(None, 36)
text_count = font1.render('Счёт: ', 1, (255, 255, 255))
text_lost = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
text_win = font1.render('Вы выиграли!', 1, (255, 255, 255))
text_lose = font1.render('Вы проиграли!', 1, (255, 255, 255))


background = transform.scale(image.load('galaxy.jpg'), (700, 500))
player = Player('rocket.png', 290, 425, 7)
monsters = sprite.Group()
for i in range(1, 6):
    enemy = Enemy('asteroid.png', randint(0, 630), 0, 3.5)
    monsters.add(enemy)
    
bullets = sprite.Group()
fire_sound = mixer.Sound('fire.ogg')

events = event.get()

clock = time.Clock()
FPS = 60

score = 0

stop = True
rel_time = False

finish = False
game = True
while game:
    key_pressed = key.get_pressed()
    if key_pressed[K_SPACE]:
        player.fire()
        fire_sound.play()
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        sprite_list = sprite.spritecollide(player, monsters, False)
        if len(bullets) < 2 and rel_time == False:
            fire_sound.play()
            player.fire()
        if len(bullets) >= 2 and rel_time == False: 
            last_time = timer()
            rel_time = True
            if len(bullets) < 3:
                rel_time = False
        if len(sprite_list) > 0:
            window.blit(text_lose, (250, 230))
            finish = True
        if len(monsters) < 5:
            for i in range(len(monsters), 5):
                score += 5 - len(monsters)
                enemy = Enemy('asteroid.png', randint(0, 630), 0, 3.5)
                monsters.add(enemy)
        text_count = font1.render('Счёт: ' + str(score), 1, (255, 255, 255))
        text_lost = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_count, (15, 15))
        window.blit(text_lost, (15, 45))
        if lost >= 10:
            window.blit(text_lose, (250, 230))
            finish = True
        if score >= 10:
            window.blit(text_win, (250, 230))
            finish = True

    display.update()
    clock.tick(FPS)
# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
from os import path
import random
import time

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
# Dados gerais do jogo.
WIDTH = 480 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#Classe jogador que representa a nave
class Player(pygame.sprite.Sprite):
     
    #Construtor da Classe
    def __init__(self):
         
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        
        
        self.speedx = 0
        self.radius = 25
    #Metodo que atualiza a posicao da navinha
    def update(self):
        self.rect.x += self.speedx
        
        #Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left  < 0:
            self.rect.left = 0

class Mob(pygame.sprite.Sprite):
     
    #Construtor da Classe
    def __init__(self):
         
        pygame.sprite.Sprite.__init__(self)
        meteoro_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
        self.image = meteoro_img
        self.image = pygame.transform.scale(meteoro_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 600
        
        VX = random.randrange(-3,3)   
        VY = random.randrange(2,9)
        self.speedx = VX
        self.speedy = VY
        
        self.radius = int(self.rect.width * .85 / 2)
        
        
    #Metodo que atualiza a posicao da navinha
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #Mantem dentro da tela
        if self.rect.y > 600:
            self.rect.y = 0
            SX = random.randrange(0,WIDTH)
            self.rect.x = SX
            VX = random.randrange(-3,3)   
            VY = random.randrange(2,9)
            self.speedx = VX
            self.speedy = VY
            
class Bullet(pygame.sprite.Sprite):
     
    #Construtor da Classe
    def __init__(self):
         
        pygame.sprite.Sprite.__init__(self)
        bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
        self.image = bullet_img
        self.image = pygame.transform.scale(bullet_img, (10, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        
    def update(self):
            
        self.rect.y -= 10
        
        
        
    

# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Asteroids")
pygame.display.set_caption("Navinha")


# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()

# Carrega os sons do jogo
pygame.mixer.music.load(path.join(snd_dir, "carryon.ogg"))
pygame.mixer.music.set_volume(0.4)
boom_sound = pygame.mixer.Sound(path.join(snd_dir, "expl3.wav"))

player = Player()
mob = Mob()
mob1 = Mob()
mob2 = Mob()
mob3 = Mob()
mob4 = Mob()
mob5 = Mob()
mob6 = Mob()
mob7 = Mob()
mobs = pygame.sprite.Group()
mobs.add(mob)
mobs.add(mob1)
mobs.add(mob2)
mobs.add(mob3)
mobs.add(mob4)
mobs.add(mob5)
mobs.add(mob6)
mobs.add(mob7)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(mob)
all_sprites.add(mob1)
all_sprites.add(mob2)
all_sprites.add(mob3)
all_sprites.add(mob4)
all_sprites.add(mob5)
all_sprites.add(mob6)
all_sprites.add(mob7)
bullets = pygame.sprite.Group()



# Comando para evitar travamentos.
try:
    
    # Loop principal.
    pygame.mixer.music.play(loops=-1)
    running = True
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
        
            
            # Verifica se foi fechado
            if event.type == pygame.QUIT:
                running = False
                
            #Verifica se apertou alguma tecla
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speedx = -8
                if event.key == pygame.K_RIGHT:
                    player.speedx = 8
                if event.key == pygame.K_UP:
                    bullet = Bullet()
                    bullet.rect.x = player.rect.x + 20
                    bullet.rect.y = player.rect.y
                    all_sprites.add(bullet)
                    bullets.add(bullet)                    
                    
            #Verifica se soltou alguma tecla
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.speedx = 0
                if event.key == pygame.K_RIGHT:
                    player.speedx = 0
                    
        
        



                    
        all_sprites.update()                  
        
        #Verifica colisao
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            boom_sound.play()
            time.sleep(1)
            running = False
            
        hits2 = pygame.sprite.groupcollide(bullets, mobs, True, True)

        for hit in hits2:
            mob = Mob()
            mobs.add(mob)
            all_sprites.add(mob)
             
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()

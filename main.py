import pygame
import random
import math
from pygame import mixer

from urllib3 import Retry
#todos son eventos 
# la presion del dedo en la tecla 
#inicializar pygame 
pygame.init()


#crear la pantalla 
pantalla=pygame.display.set_mode((800,600))

#titulo e icono 
#display seria como mostrar
#set_caption es el titulo que establece arriba en la ventana 
pygame.display.set_caption('Invacion Zombie')
icono=pygame.image.load('zombi.png')
pygame.display.set_icon(icono)
fondo=pygame.image.load('Fondo.jpg')

#agregar musica 
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

#creamos a nuestro jugador
#variables del jugador
img_jugador=pygame.image.load('transbordador-espacial.png')
jugador_x=368  #ubicacion en el eje x 
jugador_y=500  #ubicacion en el eje y
jugador_x_cambio=0
#variables del enemigo
img_enemigo=[]
enemigo_x=[]
enemigo_y=[]
enemigo_x_cambio=[]
enemigo_y_cambio=[]
cantidad_enemigos=7

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('fantasma.png'))
    enemigo_x.append(random.randint(0,736))  #ubicacion en el eje x 
    enemigo_y.append(random.randint(50,200))  #ubicacion en el eje y
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)
    
#variables de la bala 
img_bala=pygame.image.load('bala.png')
bala_x=0 #ubicacion en el eje x 
bala_y=500  #ubicacion en el eje y
bala_x_cambio=0
bala_y_cambio=3
bala_visible=False
#variable para puntaje
puntaje=0
fuente=pygame.font.Font('freesansbold.ttf',32)
texto_x=10
texto_y=10

#texto final del juego
fuente_final=pygame.font.Font('freesansbold.ttf',40)

def texto_final(): 
     mi_fuente_final=fuente_final.render('JUEGO TERMINADO', True,(255,255,255))
     pantalla.blit(mi_fuente_final,(60,200))
                                 




#funcion mostrar puntaje
def mostrar_puntaje(x,y):
    texto=fuente.render(f'puntaje:{puntaje}',True, (255,255,255))
    pantalla.blit(texto,(x,y))


#funcion jugador
def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))  #arrojar al jugador
    
#funcion enemigo
def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene],(x,y))
    
#funcion disparar bala 
def disparar_bala(x,y):
    global bala_visible
    bala_visible=True
    pantalla.blit(img_bala,(x +16,y+10))


#funcion  detectar colisiones
def hay_colision(x_1,y_1,x_2,y_2):
    distancia= math.sqrt(math.pow(x_1-x_2,2) +math.pow(y_2-y_1,2))
    if distancia < 27:
        return True
    else:
        return False
   
    
    
    
#loop del juego 
se_ejecuta=True
while se_ejecuta:
    #nuestra pantalla
    pantalla.blit(fondo,(0,0))
     #evento cerrar el programa 
    for evento in pygame.event.get():
        if evento.type==pygame.QUIT: #evento para cerrar la ventana 
            se_ejecuta=False
        #evento presionar las teclas 
        if evento.type==pygame.KEYDOWN:  #tecla presionada
            if evento.key==pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key==pygame.K_RIGHT:
                jugador_x_cambio = 1 #velocidad
            if evento.key==pygame.K_SPACE:
                sonido_bala=mixer.Sound('disparo.mp3')
                sonido_bala.play()
                if not bala_visible:
                    bala_x= jugador_x
                    disparar_bala(bala_x, bala_y)
        #evento soltar flechas 
        if evento.type==pygame.KEYUP:
            if evento.key==pygame.K_LEFT or evento.key==pygame.K_RIGHT:
                jugador_x_cambio = 0
    
    
    #modificar la ubicacion del jugador 
    jugador_x += jugador_x_cambio
    #mantener dentro del borde la nave 
    if jugador_x <=0:
        jugador_x = 0
    elif jugador_x >=736:
        jugador_x =736
        
    #modificar la ubicacion del enemigo
    for e in range(cantidad_enemigos):
        
        #fin del juego
        if enemigo_y[e]>500:
            for k in range(cantidad_enemigos):
                enemigo_y[k]=1000
            texto_final()
            break
        
        enemigo_x[e] += enemigo_x_cambio[e]
    #mantener dentro del borde la nave al enemigo
        if enemigo_x[e] <=0:
            enemigo_x_cambio[e] = 1
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >=736:
            enemigo_x_cambio[e] = -1
            enemigo_y [e]+= enemigo_y_cambio[e]
        #verificacion de colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e],bala_x, bala_y )
        if colision:
            sonido_colision=mixer.Sound('golpe.mp3')
            sonido_colision.play()
            bala_y=500
            bala_visible=False
            puntaje +=1
            #print(puntaje)
            enemigo_x[e]=random.randint(0,736)  
            enemigo_y[e]=random.randint(50,200)
            
        enemigo(enemigo_x[e], enemigo_y[e],e)
    #movimiento bala
    if bala_y <= -64:
        bala_y=500
        bala_visible=False
        
    if bala_visible:
        disparar_bala(bala_x,bala_y)
        bala_y-=bala_y_cambio
    
    #verificacion de colision
    #colision = hay_colision(enemigo_x, enemigo_y,bala_x, bala_y )
    #if colision:
        #bala_y=500
        #bala_visible=False
        #puntaje +=1
        #print(puntaje)
        #enemigo_x=random.randint(0,736)  
        #enemigo_y=random.randint(50,200)
        
    
        
    jugador(jugador_x, jugador_y)
    #enemigo(enemigo_x, enemigo_y)
    mostrar_puntaje(texto_x, texto_y)
    #actaulizar
    pygame.display.update()  
            
            

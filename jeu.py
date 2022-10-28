#!/usr/bin/env python3
import pygame
import random
import time


pygame.init()

# Titre de la fenêtre
pygame.display.set_caption("SNACK")

# Taille de la fenêtre
fenetre = pygame.display.set_mode((1280, 720))

# Contrôle du nombre d'images par seconde, pour la vitesse du serpent
fps = pygame.time.Clock()

# Couleurs
vert = pygame.Color(0, 255, 0)
noir = pygame.Color(0, 0, 0)
blanc = pygame.Color(255, 255, 255)
gris = pygame.Color(100, 100, 100)
grisFonce = pygame.Color(25, 25, 25)
jaune = pygame.Color(255, 255, 0)

# initialisation des valeurs par défaut
def debutJeu():
    global xFruit, yFruit, fruitPlace, score, direction, posTeteSerpent, corps_snake, nouvelleDirection
    xFruit, yFruit = 0, 0
        
    # placer un fruit aléatoirement
    fruitPlace = False

    score = 0

    direction = "droite"
    nouvelleDirection = "droite"
    posTeteSerpent = [100, 100]

    # premiers 4 blocs du corps du serpent
    corps_snake = [[100, 100, "droite"], [90, 100, "droite"], [80, 100, "droite"], [70, 100, "droite"], [60, 100, "droite"], [50, 100, "droite"], [40, 100, "droite"]]

debutJeu()

# 1 => jeu en cours
# 0 => perdu
statutJeu = 1

def afficherTexte(texte, fenetre, couleur, posX, posY, taillePolice):
    police = pygame.font.Font(None, taillePolice)
    texte = police.render(texte, True, couleur)
    fenetre.blit(texte, texte.get_rect(x=posX, y=posY))

def afficherTexteCentre(texte, fenetre, couleur, posX, posY, taillePolice):
    police = pygame.font.Font(None, taillePolice)
    texte = police.render(texte, True, couleur)
    fenetre.blit(texte, texte.get_rect(centerx=posX, centery=posY))

tete = pygame.image.load("tete2.png")
corps = pygame.image.load("corps.png")
queue = pygame.image.load("queue2.png")
jointure = pygame.image.load("jointure.png")


while True:
    for event in pygame.event.get():
        # fermer le jeu si la fenêtre est fermée
        if event.type == pygame.QUIT: 
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                nouvelleDirection = ""
            elif event.key == pygame.K_z or event.key == pygame.K_UP:
                if direction != "bas":
                    nouvelleDirection = "haut"
            elif event.key == pygame.K_q or event.key == pygame.K_LEFT:
                if direction != "droite":
                    nouvelleDirection = "gauche"
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if direction != "haut":
                    nouvelleDirection = "bas"
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if direction != "gauche":
                    nouvelleDirection = "droite"
            elif event.key == pygame.K_SPACE:
                if statutJeu == 0:
                    debutJeu()
                    statutJeu = 1
    direction = nouvelleDirection

    fenetre.fill(noir)

    for y in range(0, 720, 20):
        for x in range(0, 1280, 20):
            pygame.draw.rect(fenetre, grisFonce, pygame.Rect(x, y, 10, 10))
            pygame.draw.rect(fenetre, grisFonce, pygame.Rect(x+10, y+10, 10, 10))

    # fenetre.fill(noir)

    if not fruitPlace:
        # placement du fruit
        # ------------------
        # le fruit fait la largeur du serpent, 10 pixels, il doit être placé sur la grille
        xFruit = (random.randint(2, 126)*10)
        yFruit = (random.randint(2, 70)*10)
        fruitPlace = True

    if statutJeu == 1:
        if direction == "droite" and posTeteSerpent[0] < 1270:
            posTeteSerpent[0]+=10
        elif direction == "gauche" and posTeteSerpent[0] > 0:
            posTeteSerpent[0]-=10
        elif direction == "haut" and posTeteSerpent[1] > 0:
            posTeteSerpent[1]-=10
        elif direction == "bas" and posTeteSerpent[1] < 710:
            posTeteSerpent[1]+=10
        
        if posTeteSerpent[0] <= 0 or posTeteSerpent[0] >= 1270 or posTeteSerpent[1] <= 0 or posTeteSerpent[1] >= 710:
            statutJeu = 0

        for bloc in corps_snake[1:]:
            if posTeteSerpent[0] == bloc[0] and posTeteSerpent[1] == bloc[1]:
                statutJeu = 0

        
        if posTeteSerpent[0] == xFruit and posTeteSerpent[1] == yFruit:
            score += 1
            fruitPlace = False
        else:
            corps_snake.pop()

        corps_snake.insert(0, [posTeteSerpent[0], posTeteSerpent[1], direction])

    else:
        afficherTexteCentre("perdu :(", fenetre, pygame.Color(255, 0, 0), fenetre.get_width()/2, fenetre.get_height()/2-100, 100)
        afficherTexteCentre("Appuyez sur espace pour recommencer", fenetre, pygame.Color(255, 0, 0), fenetre.get_width()/2, fenetre.get_height()/2+100, 60)
        # afficherTexte("appuyez sur espace pour recommencer", fenetre, pygame.Color(255, 0, 0), 10, 10)
    
    afficherTexte(f"Score : {score}", fenetre, pygame.Color(255, 0, 0), 10, 10, 50)


    for indexBloc in range(len(corps_snake)):
        # pygame.draw.rect(fenetre, blanc if indexBloc == 0 else gris, pygame.Rect(corps_snake[indexBloc][0], corps_snake[indexBloc][1], 10, 10))
        if indexBloc == 0:
            if corps_snake[indexBloc][2] == "gauche":
                fenetre.blit(pygame.transform.rotate(tete, 180), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
            elif corps_snake[indexBloc][2] == "bas":
                fenetre.blit(pygame.transform.rotate(tete, -90), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
            elif corps_snake[indexBloc][2] == "haut":
                fenetre.blit(pygame.transform.rotate(tete, 90), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
            else:
                fenetre.blit(tete, (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
        elif indexBloc == len(corps_snake)-1:
            if corps_snake[indexBloc][2] == corps_snake[indexBloc-1][2]:
                if corps_snake[indexBloc][2] == "gauche":
                    fenetre.blit(pygame.transform.rotate(queue, 180), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
                elif corps_snake[indexBloc][2] == "bas":
                    fenetre.blit(pygame.transform.rotate(queue, -90), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
                elif corps_snake[indexBloc][2] == "haut":
                    fenetre.blit(pygame.transform.rotate(queue, 90), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
                else:
                    fenetre.blit(queue, (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
            else:
                if corps_snake[indexBloc-1][2] == "gauche":
                    fenetre.blit(pygame.transform.rotate(queue, 180), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
                elif corps_snake[indexBloc-1][2] == "bas":
                    fenetre.blit(pygame.transform.rotate(queue, -90), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
                elif corps_snake[indexBloc-1][2] == "haut":
                    fenetre.blit(pygame.transform.rotate(queue, 90), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
                else:
                    fenetre.blit(queue, (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
        elif corps_snake[indexBloc][2] != corps_snake[indexBloc-1][2]:
            if corps_snake[indexBloc][2] == "droite":
                if corps_snake[indexBloc-1][2] == "bas":
                    fenetre.blit(jointure, (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
                elif corps_snake[indexBloc-1][2] == "haut":
                    fenetre.blit(pygame.transform.rotate(jointure, 270), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
            elif corps_snake[indexBloc][2] == "gauche":
                if corps_snake[indexBloc-1][2] == "bas":
                    fenetre.blit(pygame.transform.rotate(jointure, 90), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
                elif corps_snake[indexBloc-1][2] == "haut":
                    fenetre.blit(pygame.transform.rotate(jointure, 180), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
            elif corps_snake[indexBloc][2] == "bas":
                if corps_snake[indexBloc-1][2] == "droite":
                    fenetre.blit(pygame.transform.rotate(jointure, 180), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
                elif corps_snake[indexBloc-1][2] == "gauche":
                    fenetre.blit(pygame.transform.rotate(jointure, 270), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
            else:
                if corps_snake[indexBloc-1][2] == "droite":
                    fenetre.blit(pygame.transform.rotate(jointure, 90), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
                elif corps_snake[indexBloc-1][2] == "gauche":
                    fenetre.blit(jointure, (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
            """elif corps_snake[indexBloc][2] == "gauche":
                fenetre.blit(pygame.transform.rotate(jointure, 90), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
            elif corps_snake[indexBloc][2] == "bas":
                fenetre.blit(pygame.transform.rotate(jointure, -90), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))"""
        else:
            if corps_snake[indexBloc][2] == "bas" or corps_snake[indexBloc][2] == "haut":
                fenetre.blit(pygame.transform.rotate(corps, -90), (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
            else:
                fenetre.blit(corps, (corps_snake[indexBloc][0], corps_snake[indexBloc][1]))
            
    
    pygame.draw.rect(fenetre, jaune, pygame.Rect(xFruit, yFruit, 10, 10))

    # vitesse du jeu
    # --------------
    # 10 ==> facile
    # 15 ==> normal
    # 25 ==> moyen
    # 30 ==> difficile
    # 40 ==> très difficile
    # 60 ==> impossible
    fps.tick(40)

    afficherTexte(f"{round(fps.get_fps())}", fenetre, pygame.Color(255, 0, 0), 1220, 10, 50)


    # pygame.draw.rect(fenetre, blanc, pygame.Rect(posTeteSerpent[0], posTeteSerpent[1], 10, 10))
    pygame.display.update()


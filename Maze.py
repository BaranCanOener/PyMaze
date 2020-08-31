# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 20:00:53 2020

@author: Baran
"""

import pygame
from random import randrange

class Direction:
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3

class Tile:
    path_to_end = False
    visited = False
    path_north = False
    path_south = False
    path_west = False
    path_east = False
    
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

pygame.init()

tileCountX = 30
tileCountY = 30
tileSize = 20
wallThickness = 10

longHallwayBias = 3

screen = pygame.display.set_mode((tileCountX*(tileSize+wallThickness)+wallThickness, tileCountY*(tileSize+wallThickness)+wallThickness))

mazeStartX = 0
mazeStartY = 0
mazeEndX = tileCountX-1
mazeEndY = tileCountY-1

mazeEndFound = False
generating = False
doneGenerating = False
running = True

tiles = []

font_text = pygame.font.SysFont("arialms", 25)

def drawMaze(tiles, highlightX, highlightY):
    for x in range(tileCountX):
        for y in range(tileCountY):
            if (tiles[x][y].visited):
                pygame.draw.rect(screen, white, (wallThickness+(tileSize+wallThickness)*x,wallThickness+(tileSize+wallThickness)*y,tileSize,tileSize), 0) 
            if (tiles[x][y].path_north): 
                pygame.draw.rect(screen, white, (wallThickness+(tileSize+wallThickness)*x,(tileSize+wallThickness)*y,tileSize,wallThickness), 0) 
            if (tiles[x][y].path_east): 
                pygame.draw.rect(screen, white, ((tileSize+wallThickness)*x,wallThickness+(tileSize+wallThickness)*y,wallThickness,tileSize), 0) 
            if (tiles[x][y].path_to_end): 
                pygame.draw.circle(screen, blue, (int(wallThickness+tileSize/2+(tileSize+wallThickness)*x),int(wallThickness+tileSize/2+(tileSize+wallThickness)*y)),int(wallThickness/2), 0) 
            if (x == highlightX and y == highlightY):
                pygame.draw.rect(screen, blue, (wallThickness+(tileSize+wallThickness)*x,wallThickness+(tileSize+wallThickness)*y,tileSize,tileSize), 0) 
            if (x == mazeStartX and y == mazeStartY):
                pygame.draw.rect(screen, red, (wallThickness+(tileSize+wallThickness)*x,wallThickness+(tileSize+wallThickness)*y,tileSize,tileSize), 0)   
            if (x == mazeEndX and y == mazeEndY):
                pygame.draw.rect(screen, red, (wallThickness+(tileSize+wallThickness)*x,wallThickness+(tileSize+wallThickness)*y,tileSize,tileSize), 0)   
    
    pygame.display.update()

def checkUserUpdate():
    #Check for user updates and quit if required
    global generating
    global doneGenerating
    global running
    global tiles
    global longHallwayBias
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                generating = False
            if event.key == pygame.K_SPACE and not generating:
                generating = True
                generateMaze(tiles,mazeStartX, mazeStartY, Direction.EAST)
                solveMaze(tiles, mazeStartX, mazeStartY)
                doneGenerating = True
                generating = False
            if event.key == pygame.K_RETURN:
                generating = False
                doneGenerating = False
                tiles = []
                #Initialize the maze
                for x in range(tileCountX):
                    tiles.append([])
                    for y in range(tileCountY):
                        tiles[x].append([])
                        tiles[x][y] = Tile()
            if event.key == pygame.K_0:
                longHallwayBias = 0
            if event.key == pygame.K_1:
                longHallwayBias = 1
            if event.key == pygame.K_2:
                longHallwayBias = 2
            if event.key == pygame.K_3:
                longHallwayBias = 3
            if event.key == pygame.K_4:
                longHallwayBias = 4
            if event.key == pygame.K_5:
                longHallwayBias = 5
            if event.key == pygame.K_6:
                longHallwayBias = 6
            if event.key == pygame.K_7:
                longHallwayBias = 7
            if event.key == pygame.K_8:
                longHallwayBias = 8
            if event.key == pygame.K_9:
                longHallwayBias = 9

def generateMaze(tiles, posX, posY, lastDirection):
    checkUserUpdate()
    if running == False or generating == False:
        return
    
    #Draw the current maze and highlight the current position on the stack
    screen.fill(black)
    drawMaze(tiles, posX, posY)
    
    neighbours = []
    tiles[posX][posY].visited = True
    # North
    if (posY > 0):
        if (tiles[posX][posY-1].visited == False):
            neighbours.append(Direction.NORTH)
            if (lastDirection == Direction.NORTH):
                neighbours.extend([Direction.NORTH]*longHallwayBias)
    # South
    if (posY < tileCountY-1):
        if (tiles[posX][posY+1].visited == False):
            neighbours.append(Direction.SOUTH)
            if (lastDirection == Direction.SOUTH):
                neighbours.extend([Direction.SOUTH]*longHallwayBias)
    # West
    if (posX < tileCountX-1):
        if (tiles[posX+1][posY].visited == False):
            neighbours.append(Direction.WEST)
            if (lastDirection == Direction.WEST):
                neighbours.extend([Direction.WEST]*longHallwayBias)
    # East
    if (posX > 0):
        if (tiles[posX-1][posY].visited == False):
            neighbours.append(Direction.EAST)
            if (lastDirection == Direction.EAST):
                neighbours.extend([Direction.EAST]*longHallwayBias)
    
    while neighbours:
        rnd_index = randrange(len(neighbours))
        neighbour = neighbours[rnd_index]
        neighbours.pop(rnd_index)
        if (neighbour == Direction.NORTH and tiles[posX][posY-1].visited == False):
            tiles[posX][posY].path_north = True
            tiles[posX][posY-1].path_south = True
            generateMaze(tiles, posX, posY-1, Direction.NORTH)
        if (neighbour == Direction.SOUTH and tiles[posX][posY+1].visited == False):
            tiles[posX][posY].path_south = True
            tiles[posX][posY+1].path_north = True
            generateMaze(tiles, posX, posY+1, Direction.SOUTH)    
        if (neighbour == Direction.WEST and tiles[posX+1][posY].visited == False):
            tiles[posX][posY].path_west = True
            tiles[posX+1][posY].path_east = True
            generateMaze(tiles, posX+1, posY, Direction.WEST)   
        if (neighbour == Direction.EAST and tiles[posX-1][posY].visited == False):
            tiles[posX][posY].path_east = True
            tiles[posX-1][posY].path_west = True
            generateMaze(tiles, posX-1, posY, Direction.EAST)   
            
def solveMaze(tiles, posX, posY):
    checkUserUpdate()
    if running == False or generating == False:
        return

    screen.fill(black)
    drawMaze(tiles, posX, posY)
    
    global mazeEndFound
    if (tiles[posX][posY].path_to_end or mazeEndFound):
        return
    
    tiles[posX][posY].path_to_end = True
    
    if (posX == mazeEndX and posY == mazeEndY): 
        mazeEndFound = True
        return
    
    # North
    if (posY > 0):
        if (tiles[posX][posY].path_north == True):
            solveMaze(tiles, posX, posY-1)
    # South
    if (posY < tileCountY-1):
        if (tiles[posX][posY].path_south == True):
            solveMaze(tiles, posX, posY+1)
    # West
    if (posX < tileCountX-1):
        if (tiles[posX][posY].path_west == True):
            solveMaze(tiles, posX+1, posY)
    # East
    if (posX > 0):
        if (tiles[posX][posY].path_east == True):
            solveMaze(tiles, posX-1, posY)
    
    if (mazeEndFound == False):
        tiles[posX][posY].path_to_end = False


#Initialize the maze
for x in range(tileCountX):
    tiles.append([])
    for y in range(tileCountY):
        tiles[x].append([])
        tiles[x][y] = Tile()
        
while running:
    checkUserUpdate()         
    screen.fill(black)
    if not doneGenerating:
        srf = font_text.render("SPACE to generate maze, RETURN to reset", True, white)
        screen.blit(srf, ((tileCountX*(tileSize+wallThickness)+wallThickness)/3, (tileCountY*(tileSize+wallThickness)+wallThickness)/3))
        srf = font_text.render("Numbers 0, ..., 9 to set long hallway bias (currently: " + str(longHallwayBias) + ")", True, white)
        screen.blit(srf, ((tileCountX*(tileSize+wallThickness)+wallThickness)/3, (tileCountY*(tileSize+wallThickness)+wallThickness)/3+20))
    drawMaze(tiles, -1, -1)
    pygame.display.update()
    
pygame.quit()
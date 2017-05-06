import pygame
import stellar

grid = stellar.pathfinding.Grid()

tileSize = 32
startX = tileSize/2
startY = tileSize/2

for x in range(31):
    for y in range(31):
        grid.nodes.append(stellar.pathfinding.Node(startX+tileSize*x,startY+tileSize*y))


stellar.pathfinding.autoBuildNeighborsLists(grid, 33)

for z in range(30*30*.33):
    random.choice(grid.nodes).blocked = True

engine = stellar.base.Base()
    

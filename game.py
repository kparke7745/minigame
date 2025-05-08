import pygame
import random
import copy
import math

#### Mainloop

class Node():
    #Code by Nicholas Swift
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
        
# Class by Lukas Peraza
class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, row, col, image):
        super(GameObject, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.image = x, y, image
        self.row , self.col = row, col
        self.baseImage = image.copy()  # non-rotated version of image
        w, h = image.get_size()
        self.updateRect()

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def update(self, screenWidth, screenHeight):
        self.image = pygame.transform.scale(self.baseImage, (screenWidth//16, screenHeight//16))
        self.updateRect()
        # wrap around, and update the rectangle again
        if self.rect.right > screenWidth+self.width/2:
            self.x = 16
            self.col = 0
        elif self.rect.left < 0-self.width/2:
            self.x = screenWidth - 16
            self.col  = 15
        if self.rect.bottom > screenHeight + self.height/2:
            self.y = 16
            self.row = 0
        elif self.rect.top < 0-self.height/2:
            self.y = screenHeight - 16
            self.row = 15
        self.updateRect()

class OWPlayer(GameObject):
    @staticmethod
    def init(screenWidth, screenHeight):
        # Direct file path was used here to get sprite working. Attempt to use relative when testing,
        # but use direct if issues arise
        OWPlayer.image = pygame.transform.scale(pygame.image.load("C:/Users/krist/Desktop/112 Homework/Term Project/roy.png").convert_alpha(),(screenWidth//16,screenHeight//16))
        
    def __init__(self, x, y, row, col):
        super(OWPlayer,self).__init__(x,y,row,col,OWPlayer.image)
        self.lastMoves = []
        self.validPos = True
        self.moves = 5
        
    def update(self, keysDown, screenWidth, screenHeight):
        if self.validPos == False:
            lastMove = self.lastMoves.pop()
            if lastMove == "left":
                self.x += screenWidth/16
                self.col += 1
            elif lastMove == "right":
                self.x -= screenWidth/16
                self.col -= 1
            elif lastMove ==  "up":
                self.y += screenHeight/16
                self.row += 1
            elif lastMove == "down":
                self.y -= screenHeight/16
                self.row -= 1
            self.validPos = True
            self.moves += 1
        else:
            if keysDown(pygame.K_LEFT):
                self.x -= screenWidth/16
                self.col -= 1
                self.lastMoves.append("left")
            elif keysDown(pygame.K_RIGHT):
                self.x += screenWidth/16
                self.col += 1
                self.lastMoves.append("right")
            elif keysDown(pygame.K_UP):
                self.y -= screenHeight/16
                self.row -= 1
                self.lastMoves.append("up")
            elif keysDown(pygame.K_DOWN):
                self.y += screenHeight/16
                self.row += 1
                self.lastMoves.append("down")
            self.moves -= 1
        
        super(OWPlayer,self).update(screenWidth, screenHeight)

class BatPlayer(GameObject):
    @staticmethod
    def init(screenWidth, screenHeight):
        # Direct file path was used here to get sprite working. Attempt to use relative when testing,
        # but use direct if issues arise
        BatPlayer.image = pygame.transform.scale(pygame.image.load("C:/Users/krist/Desktop/112 Homework/Term Project/roy.png").convert_alpha(),(110,110))
        
    def __init__(self, x, y,row,col,health,attack,defense,level):
        super(BatPlayer,self).__init__(x,y,row,col,BatPlayer.image)
        self.health = health
        self.attack = attack
        self.defense = defense
        self.level = level
    
    def update(self, mouseDown, screenWidth, screenHeight):
        super(BatPlayer,self).update(screenWidth, screenHeight)
    
class OWEnemy(GameObject):
    @staticmethod
    def init(screenWidth, screenHeight):
        # Direct file path was used here to get sprite working. Attempt to use relative when testing,
        # but use direct if issues arise
        OWEnemy.image =  pygame.transform.scale(pygame.image.load("C:/Users/krist/Desktop/112 Homework/Term Project/ghost.png").convert_alpha(),(screenWidth//16, screenHeight//16))
        
    def __init__(self, x, y, row, col):
        super(OWEnemy,self).__init__(x,y,row,col,OWEnemy.image)
    
    def update(self, screenWidth, screenHeight):
        super(OWEnemy,self).update(screenWidth, screenHeight)
        
class OWBoss(GameObject):
    @staticmethod
    def init(screenWidth, screenHeight,wins):
        if wins == 3:
            OWBoss.image = pygame.transform.scale(pygame.image.load("C:/Users/krist/Desktop/112 Homework/Term Project/boss3.png").convert_alpha(),(screenWidth//16, screenHeight//16))
        elif wins == 6:
            OWBoss.image = pygame.transform.scale(pygame.image.load("C:/Users/krist/Desktop/112 Homework/Term Project/boss2.png").convert_alpha(),(screenWidth//16, screenHeight//16))
        elif wins == 9:
            OWBoss.image = pygame.transform.scale(pygame.image.load("C:/Users/krist/Desktop/112 Homework/Term Project/boss1.gif").convert_alpha(),(screenWidth//16, screenHeight//16))
        elif wins == 10:
            OWBoss.image = pygame.transform.scale(pygame.image.load("C:/Users/krist/Desktop/112 Homework/Term Project/finalboss.png").convert_alpha(),(screenWidth//16, screenHeight//16))
    
    def __init__(self,x,y,row,col):
        super(OWBoss,self).__init__(x,y,row,col,OWBoss.image)
        
    def update(self,screenWidth,screenHeight):
        super(OWBoss,self).update(screenWidth, screenHeight)
        
class BatEnemy(GameObject):
    @staticmethod
    def init(screenWidth, screenHeight):
        # Direct file path was used here to get sprite working. Attempt to use relative when testing,
        # but use direct if issues arise
        BatEnemy.image =  pygame.transform.scale(pygame.image.load("C:/Users/krist/Desktop/112 Homework/Term Project/ghost.png").convert_alpha(),(50, 50))
        
    def __init__(self,x,y,row,col,health,attack,defense):
        super(BatEnemy,self).__init__(x,y,row,col,BatEnemy.image)
        self.health = health
        self.attack =  attack
        self.defense = defense
    
    def update(self, screenWidth, screenHeight):
        super(BatEnemy,self).update(screenWidth, screenHeight)

class BatBoss(GameObject):
    @staticmethod
    def init(screenWidth, screenHeight,wins):
        if wins == 3:
            BatBoss.image = pygame.transform.scale(pygame.image.load("C:/Users/krist/Desktop/112 Homework/Term Project/boss3.png").convert_alpha(),(150,150))
        elif wins == 6:
            BatBoss.image = pygame.transform.scale(pygame.image.load("C:/Users/krist/Desktop/112 Homework/Term Project/boss2.png").convert_alpha(),(181,170))
        elif wins == 9:
            BatBoss.image = pygame.transform.scale(pygame.image.load("C:/Users/krist/Desktop/112 Homework/Term Project/boss1.gif").convert_alpha(),(180,175))
        elif wins == 10:
            BatBoss.image = pygame.transform.scale(pygame.image.load("C:/Users/krist/Desktop/112 Homework/Term Project/finalboss.png").convert_alpha(),(173, 146))
        
    def __init__(self,x,y,row,col,health,attack,defense):
        super(BatBoss,self).__init__(x,y,row,col,BatBoss.image)
        self.health = health
        self.attack = attack
        self.defense = defense
        
    def update(self,screenWidth,screenHeight):
        super(BatBoss,self).update(screenWidth,screenHeight)
        
# Framework Code created by Lukas Peraza
class Overworld(object):
    running = True
    firstTurn = True
    playerMove = True
    playerWin = False
    gameClear = 0
    wins = 0
    
    # Tile map represented as a 2D list
    tilemap = None
    
    # Game Dimensions
    TILESIZE = 600/16
    MAPWIDTH = 16
    MAPHEIGHT = 16
    
    def init(self):
        # Map elements
        self.GROUND = 0
        self.TREE = 1
        self.WATER = 2
        self.WALL = 3
        
        # Colors that represent the map elements
        self.BROWN = (153,76,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.GRAY = (169,169,169)
        
        self.colors = {self.GROUND: self.BROWN, self.TREE: self.GREEN, self.WATER: self.BLUE, self.WALL: self.GRAY}
        
    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if Overworld.playerMove == True:
            self.playerGroup.update(self.isKeyPressed, self.height, self.height)
            if Overworld.tilemap[self.playerSprite.row][self.playerSprite.col] == self.WATER:
                self.playerSprite.moves -= 1

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        for row in range(Overworld.MAPHEIGHT):
            for col in range(Overworld.MAPWIDTH):
                pygame.draw.rect(screen, self.colors[Overworld.tilemap[row][col]], (col*Overworld.TILESIZE, row*Overworld.TILESIZE, Overworld.TILESIZE, Overworld.TILESIZE))
        self.playerGroup.draw(screen)
        self.enemies.draw(screen)
        pygame.font.init()
        menuFont = pygame.font.SysFont('Algerian',22)
        remMoveText =  menuFont.render('Remaining Moves',False,(255,255,255))
        moveText = menuFont.render(str(self.playerSprite.moves),False,(255,255,255))
        remEnemyText = menuFont.render('Remaining Enemies',False,(255,255,255))
        enemiesText = menuFont.render(str(len(self.enemies.sprites())),False,(255,255,255))
        if Overworld.playerMove == True and Overworld.playerWin == False:
            screen.blit(remMoveText,(610,70))
            screen.blit(moveText,(700,120))
            screen.blit(remEnemyText,(605,480))
            screen.blit(enemiesText,(700,530))
        
    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)
        
    def screenChange(self):
        if pygame.sprite.groupcollide(self.playerGroup,self.enemies,False,False):
            if isinstance(pygame.sprite.spritecollideany(self.playerSprite, self.enemies),OWBoss):
                Battle.boss = True
            else:
                Battle.boss = False
            pygame.mixer.music.stop()
            curScreen = screens["battle"]
            curScreen.run()
    
    def generateMap(self):
        tilemap=[[random.choice([0,1,2]),random.choice([0,1,2]),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice([0,1,2]),random.choice([0,1,2]),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))],
        [random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys())),random.choice(list(self.colors.keys()))]]
        return tilemap
        
    def spawnPlayer(self):
        self.init()
        OWPlayer.init(self.height,self.height)
        self.playerSprite = OWPlayer(self.height/32, self.height/32,0,0)
        self.playerGroup = pygame.sprite.Group(self.playerSprite)
        
    def spawnEnemies(self):
        self.init()
        OWEnemy.init(self.height, self.height)
        self.enemies = pygame.sprite.Group()
        if Overworld.wins == 10:
            self.pos = []
            OWBoss.init(self.height,self.height,Overworld.wins)
            r = random.randint(8,15)
            c = random.randint(0,15)
            self.boss = OWBoss(c*self.height/16+self.height/32,r*self.height/16+self.height/32,r,c)
            self.enemies.add(self.boss)
            self.pos.append([self.boss.row,self.boss.col])
        elif Overworld.wins != 0 and Overworld.wins % 3 == 0:
            self.pos = []
            r = random.randint(8,15)
            c = random.randint(0,15)
            enemy1 = OWEnemy(c*self.height/16+self.height/32,r*self.height/16+self.height/32,r,c)
            self.enemies.add(enemy1)
            self.pos.append([enemy1.row,enemy1.col])
            r = random.randint(8,15)
            c = random.randint(0,15)
            enemy2 = OWEnemy(c*self.height/16+self.height/32,r*self.height/16+self.height/32,r,c)
            self.enemies.add(enemy2)
            self.pos.append([enemy2.row,enemy2.col])
            OWBoss.init(self.height, self.height,Overworld.wins)
            r = random.randint(8,15)
            c = random.randint(0,15)
            self.boss = OWBoss(c*self.height/16+self.height/32,r*self.height/16+self.height/32,r,c)
            self.enemies.add(self.boss)
            self.pos.append([self.boss.row,self.boss.col])
        else:
            self.pos = []
            r = random.randint(8,15)
            c = random.randint(0,15)
            enemy1 = OWEnemy(c*self.height/16+self.height/32,r*self.height/16+self.height/32,r,c)
            self.enemies.add(enemy1)
            self.pos.append([r,c])
            r = random.randint(8,15)
            c = random.randint(0,15)
            enemy2 = OWEnemy(c*self.height/16+self.height/32,r*self.height/16+self.height/32,r,c)
            self.enemies.add(enemy2)
            self.pos.append([r,c])
        
        
    def astarEnemyPathfinding(self, maze, start, end):
        #Code by Nicholas Swift
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        for i in range(5):

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] == self.WALL:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = (abs(child.position[0] - end_node.position[0])) + (abs(child.position[1] - end_node.position[1]))
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)
                
        path = []
        current = current_node
        while current is not None:
            path.append(current.position)
            current = current.parent
        return path[::-1] # Return reversed path
        
    def __init__(self, width=820, height=600, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (0, 0, 128)
        pygame.init()

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()
        
        self.init()
        if Overworld.firstTurn == True:
            self.spawnPlayer()
            self.spawnEnemies()
            Overworld.tilemap = self.generateMap()
            Overworld.firstTurn = False
            
        if Overworld.wins > 6:
            pygame.mixer.music.load("C:/Users/krist/Desktop/112 Homework/Term Project/Stage 3- FFIV Golbez Theme.mp3")
        elif Overworld.wins > 3:
            pygame.mixer.music.load("C:/Users/krist/Desktop/112 Homework/Term Project/Stage 2- FFIV Giant of Babil.mp3")
        else:
            pygame.mixer.music.load("C:/Users/krist/Desktop/112 Homework/Term Project/Stage 1- FFIV Cave Theme.mp3")
            
        if bool(self.enemies) == False:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("C:/Users/krist/Desktop/112 Homework/Term Project/Stage Clear- FFIV Victory.mp3")
        
        elif bool(self.playerGroup) == False:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("C:/Users/krist/Desktop/112 Homework/Term Project/Game Over- Chrono Trigger.mp3")
            
        pygame.mixer.music.play(-1)
        while Overworld.running:
                
            # call game-specific initialization
            if bool(self.enemies) == False:
                Overworld.playerWin = True
                menuFont = pygame.font.SysFont('Algerian',24)
                proceedFont = pygame.font.SysFont('Corbel',16)
                if Overworld.wins == 10:
                    winText = menuFont.render('GAME COMPLETE',False,(255,255,255))
                    contText = proceedFont.render('Press Enter to begin NG+',False,(255,255,255))
                else:
                    winText = menuFont.render('STAGE CLEARED',False,(255,255,255))
                    contText = proceedFont.render('Press Enter to continue',False,(255,255,255))
                self.redrawAll(screen)
                screen.blit(winText,(610,250))
                screen.blit(contText,(630,300))
                pygame.display.flip()
                pygame.event.clear()
                event = pygame.event.wait()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        Overworld.firstTurn = True
                        if Overworld.wins == 10:
                            Overworld.wins = 0
                            Overworld.gameClear += 1
                        else:
                            Overworld.wins += 1
                        Overworld.tilemap = self.generateMap()
                        Overworld.playerWin = False
                        startGame(Overworld.wins)
                        
            if bool(self.playerGroup) == False:
                Overworld.playerWin = True
                menuFont = pygame.font.SysFont('Algerian',24)
                proceedFont = pygame.font.SysFont('Corbel',16)
                loseText = menuFont.render('DEFEAT...',False,(255,255,255))
                contText = proceedFont.render('Press Enter to restart',False,(255,255,255))
                self.redrawAll(screen)
                screen.blit(loseText,(650,250))
                screen.blit(contText,(630,300))
                pygame.display.flip()
                pygame.event.clear()
                event = pygame.event.wait()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        Overworld.firstTurn = True
                        Overworld.wins = 0
                        Overworld.gameClear = 0
                        Overworld.tilemap = self.generateMap()
                        Overworld.playerWin = False
                        startGame(Overworld.wins)

            playing = True
            while playing and not Overworld.playerWin:
                time = clock.tick(self.fps)
                self.timerFired(time)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.mousePressed(*(event.pos))
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        self.mouseReleased(*(event.pos))
                    elif (event.type == pygame.MOUSEMOTION and
                          event.buttons == (0, 0, 0)):
                        self.mouseMotion(*(event.pos))
                    elif (event.type == pygame.MOUSEMOTION and
                          event.buttons[0] == 1):
                        self.mouseDrag(*(event.pos))
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE and self.playerSprite.moves < 5:
                            if Overworld.tilemap[self.playerSprite.row][self.playerSprite.col] == self.WATER:
                                self.playerSprite.moves += 1
                            p.validPos = False
                            self.playerGroup.update(self.isKeyPressed, self.height, self.height)
                        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            self._keys[event.key] = True
                            self.keyPressed(event.key, event.mod)
                    elif event.type == pygame.KEYUP:
                        self._keys[event.key] = False
                        self.keyReleased(event.key, event.mod)
                    elif event.type == pygame.QUIT:
                        Overworld.running = False
                        playing = False
            
                screen.fill(self.bgColor)
                for row in range(Overworld.MAPHEIGHT):
                    for col in range(Overworld.MAPWIDTH):
                        for p in self.playerGroup.sprites():
                            if Overworld.tilemap[row][col] == self.WALL and p.x > col*Overworld.TILESIZE and p.x < col*Overworld.TILESIZE+Overworld.TILESIZE and p.y > row*Overworld.TILESIZE and p.y < row*Overworld.TILESIZE+Overworld.TILESIZE:
                                p.validPos = False
                                self.playerGroup.update(self.isKeyPressed, self.height, self.height)
                        for e in self.enemies:
                            if Overworld.tilemap[row][col] == self.WALL and e.x > col*Overworld.TILESIZE and e.x < col*Overworld.TILESIZE+Overworld.TILESIZE and e.y > row*Overworld.TILESIZE and e.y < row*Overworld.TILESIZE+Overworld.TILESIZE:
                                while Overworld.tilemap[row][col] == self.WALL and e.x > col*Overworld.TILESIZE and e.x < col*Overworld.TILESIZE+Overworld.TILESIZE and e.y > row*Overworld.TILESIZE and e.y < row*Overworld.TILESIZE+Overworld.TILESIZE:
                                    if e.x == Overworld.TILESIZE/2:
                                        e.x = 15*Overworld.TILESIZE+Overworld.TILESIZE/2
                                    else:
                                        e.x -= Overworld.TILESIZE
                                self.enemies.update(self.height, self.height)
                if self.playerSprite.moves <= 0:
                    Overworld.playerMove = False
                    for e in self.enemies:
                        path = self.astarEnemyPathfinding(Overworld.tilemap,(e.row, e.col),(self.playerSprite.row, self.playerSprite.col))
                        for point in path:
                            if e.row - point[0] == 1:
                                e.y -= Overworld.TILESIZE
                                e.row -= 1
                            elif e.row - point[0] == -1:
                                e.y += Overworld.TILESIZE
                                e.row += 1
                            elif e.col - point[1] == -1:
                                e.x += Overworld.TILESIZE
                                e.col += 1
                            elif e.col - point[1] == 1:
                                e.x -= Overworld.TILESIZE
                                e.col -= 1
                            self.enemies.update(self.height,self.height)
                    for e in self.enemies:
                        if pygame.sprite.spritecollide(e,self.enemies,False):
                            e.y -= Overworld.TILESIZE
                            e.row -= 1
                            self.enemies.update(self.height,self.height)
                    self.playerSprite.moves = 5
                    self.playerSprite.lastMoves = []
                    Overworld.playerMove = True
                self.redrawAll(screen)
                self.screenChange()
                pygame.display.flip()
            
        pygame.quit()
        
        
class BattleCursor(GameObject):
    def __init__(self,points):
        self.points = points
        self.optPos = 0
        self.enPos = None
        self.itemPos = None
    
    def update(self,keysDown):
        if self.enPos == None and self.itemPos == None:
            if keysDown(pygame.K_DOWN):
                if self.points[2][1] >= 480:
                    self.points[0][1] = 370
                    self.points[1][1] = 380
                    self.points[2][1] = 390
                    self.optPos = 0
                else:
                    for p in self.points:
                        p[1] += 30
                    self.optPos += 1
            elif keysDown(pygame.K_UP):
                if self.points[0][1] <= 370:
                    self.points[0][1] = 460
                    self.points[1][1] = 470
                    self.points[2][1] = 480
                    self.optPos = 3
                else:
                    for p in self.points:
                        p[1] -= 30
                    self.optPos -= 1
        elif self.enPos == None and self.optPos ==  None:
            if keysDown(pygame.K_DOWN):
                if self.points[2][1] >= 445:
                    self.points[0][1] = 385
                    self.points[1][1] = 395
                    self.points[2][1] = 405
                    self.itemPos = 0
                else:
                    for p in self.points:
                        p[1] += 20
                    self.itemPos += 1
            elif keysDown(pygame.K_UP):
                if self.points[0][1] <= 385:
                    self.points[0][1] = 425
                    self.points[1][1] = 435
                    self.points[2][1] = 445
                    self.itemPos = 2
                else:
                    for p in self.points:
                        p[1] -= 20
                    self.itemPos -= 1
    
class Battle(object):
    boss = False
    playerTurn = True
    turnNum = 1
    playerDefTurn = None
    skillCoolDown = None
    selixerOn = None
    enemyDefTurn = None
    pHealth = 50
    pAttack = 5
    pDefense = 5
    pLevel = 1
    skillAtts = ["fire"]
    eHealth = 30
    eAttack = 5
    eDefense = 2
    eWeakness = ["light","star"]
    bHealth = 200
    bAttack = 15
    bDefense = 5
    bWeakness = []
    items = [["Potion",3],["S. Elixer",1],["Skill Refresh",1]]
    def init(self):
        BatPlayer.init(self.width,self.height)
        self.player = BatPlayer(200, self.height/2,None,None,Battle.pHealth,Battle.pAttack,Battle.pDefense,Battle.pLevel)
        self.curPlayerHealth = self.player.health
        self.items = Battle.items
        self.playerGroup = pygame.sprite.Group(self.player)
        if Battle.boss == False:
            BatEnemy.init(self.width, self.height)
            self.enemy = BatEnemy(self.width-200, self.height/2,None,None,Battle.eHealth,Battle.eAttack,Battle.eDefense)
            self.curEnemyHealth = self.enemy.health
            self.enemies = pygame.sprite.Group(self.enemy)
        elif Battle.boss == True:
            BatBoss.init(self.width, self.height,Overworld.wins)
            self.enemy = BatBoss(self.width-150, self.height/2,None,None,Battle.bHealth,Battle.bAttack,Battle.bDefense)
            self.curEnemyHealth = self.enemy.health
            self.enemies = pygame.sprite.Group(self.enemy)
        self.cursor = BattleCursor([[100,self.height/2+70],[120,self.height/2+80],[100,self.height/2+90]])
        self.cursorReturn = copy.deepcopy(self.cursor)
        self.itemCursor = BattleCursor([[100,self.height/2+85],[120,self.height/2+95],[100,self.height/2+105]])
        self.itemCursor.itemPos = 0
        self.itemCursor.optPos = None
        
    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        pygame.font.init()
        optFont = pygame.font.SysFont('Cambria', 18)
        iconFont = pygame.font.SysFont('Corbel',14)
        attackText = optFont.render('Attack',False,(255,255,255))
        skillText = optFont.render('Skill',False,(255,255,255))
        defenseText = optFont.render('Defend',False,(255,255,255))
        itemText = optFont.render('Item',False,(255,255,255))
        potionText = optFont.render(self.items[0][0]+' x'+str(self.items[0][1]),False,(255,255,255))
        selixerText = optFont.render(self.items[1][0]+' x'+str(self.items[1][1]),False,(255,255,255))
        srefreshText = optFont.render(self.items[2][0]+' x'+str(self.items[2][1]),False,(255,255,255))
        playerText = iconFont.render('Player',False,(255,255,255))
        playerHealthText = iconFont.render(str(self.curPlayerHealth)+'/'+str(self.player.health),False,(255,255,255))
        enemyText = iconFont.render('Enemy',False,(255,255,255))
        enemyHealthText = iconFont.render(str(self.curEnemyHealth)+'/'+str(self.enemy.health),False,(255,255,255))
        if bool(self.playerGroup) == True:
            self.playerGroup.draw(screen)
        if bool(self.enemies) == True:
            self.enemies.draw(screen)
        if bool(self.playerGroup) == True:
            screen.blit(playerText,(self.player.x-35,self.player.y-65))
            screen.blit(playerHealthText,(self.player.x-30,self.player.y-55))
        pygame.draw.rect(screen,(0,0,128),(100,25,375,100))
        pygame.draw.rect(screen,(255,255,255),(100,25,375,100),1)
        if Battle.boss == False and bool(self.enemies) ==  True:
            screen.blit(enemyText, (self.enemy.x+40, self.enemy.y-10))
            screen.blit(enemyHealthText,(self.enemy.x+45, self.enemy.y))
        elif Battle.boss == True and bool(self.enemies) == True:
            screen.blit(enemyText, (self.enemy.x+80, self.enemy.y-10))
            screen.blit(enemyHealthText,(self.enemy.x+85, self.enemy.y))
        if Battle.playerTurn == True and self.cursor.itemPos != None:
            pygame.draw.rect(screen,(0,0,128),(130,self.height/2+80,150,70))
            pygame.draw.rect(screen,(255,255,255),(130,self.height/2+80,150,70),1)
            screen.blit(potionText,(140,self.height/2+80))
            screen.blit(selixerText,(140,self.height/2+100))
            screen.blit(srefreshText,(140,self.height/2+120))
            pygame.draw.polygon(screen,(0,0,128),self.itemCursor.points)
            pygame.draw.polygon(screen,(255,255,255),self.itemCursor.points,1)
        elif Battle.playerTurn == True:
            pygame.draw.rect(screen,(0,0,128),(130,self.height/2+50,120,140))
            pygame.draw.rect(screen,(255,255,255),(130,self.height/2+50,120,140),1)
            screen.blit(attackText,(140,self.height/2+65))
            screen.blit(skillText,(140,self.height/2+95))
            screen.blit(defenseText,(140,self.height/2+125))
            screen.blit(itemText,(140,self.height/2+155))
            pygame.draw.polygon(screen,(0,0,128),self.cursor.points)
            pygame.draw.polygon(screen,(255,255,255),self.cursor.points,1)

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)
        
    def screenChange(self,screen):
        # Event for changing back to overworld
        if bool(self.enemies) == False:
            pygame.mixer.music.stop()
            if Overworld.wins == 10:
                pygame.mixer.music.load("C:/Users/krist/Desktop/112 Homework/Term Project/Destroyed!- SFX.mp3")
                screen.fill(self.bgColor)
                self.playerGroup.draw(screen)
                pygame.display.flip()
                pygame.event.set_blocked([pygame.KEYDOWN,pygame.KEYUP])
                pygame.mixer.music.play()
                wait = pygame.time.get_ticks()
                self.playerGroup.draw(screen)
                imp = pygame.transform.scale(pygame.image.load("C:/Users/krist/Desktop/112 Homework/Term Project/finalbossfade.png"),(173,146))
                imp = imp.convert()
                imp.set_alpha(None)
                i = 255
                while True:
                    check = pygame.time.get_ticks()
                    if check - wait >= 8000:
                        break
                    screen.fill(self.bgColor)
                    self.playerGroup.draw(screen)
                    imp.set_alpha(i)
                    screen.blit(imp,(self.enemy.x-86,self.enemy.y-73))
                    pygame.display.flip()
                    pygame.time.delay(150)
                    pygame.event.pump()
                    i -= 5
                pygame.event.set_allowed([pygame.KEYDOWN,pygame.KEYUP])
                pygame.mixer.music.stop()
            pygame.mixer.music.load("C:/Users/krist/Desktop/112 Homework/Term Project/Victory- DQVIII.mp3")
            pygame.mixer.music.play()
            screen.fill(self.bgColor)
            textBox = pygame.font.SysFont('Arial',18)
            if Overworld.wins == 10:
                battleText = textBox.render('Impetus has been slain!',False,(255,255,255))
            else:
                battleText = textBox.render('All the enemies have been defeated!',False,(255,255,255))
            self.redrawAll(screen)
            screen.blit(battleText,(110,35))
            pygame.display.flip()
            pygame.event.clear()
            userInput = pygame.event.wait()
            pygame.event.clear()
            userInput = pygame.event.wait()
            if Battle.boss == True and Overworld.wins < 10:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("C:/Users/krist/Desktop/112 Homework/Term Project/Level Up- DQVIII.mp3")
                pygame.mixer.music.play()
                battleText = textBox.render('Defeating the strong foe has made you stronger!',False,(255,255,255))
                if Overworld.gameClear > 0:
                    battleText2 = textBox.render('Max HP increased by 25. Attack increased by 2.',False,(255,255,255))
                elif Overworld.wins < 3:
                    battleText2 = textBox.render('Max HP increased to 150. Attack increased to 20.',False,(255,255,255))
                elif Overworld.wins < 6:
                    battleText2 = textBox.render('Max HP increased to 300. Attack increased to 35.',False,(255,255,255))
                elif Overworld.wins < 10:
                    battleText2 = textBox.render('Max HP increased to 500. Attack increased to 60.',False,(255,255,255))
                screen.fill(self.bgColor)
                self.redrawAll(screen)
                screen.blit(battleText,(110,35))
                screen.blit(battleText2,(110,60))
                pygame.display.flip()
                pygame.event.clear()
                userInput = pygame.event.wait()
                pygame.event.clear()
                userInput = pygame.event.wait()
                if Overworld.gameClear > 0:
                    battleText  = textBox.render('Defense increased by 1.',False,(255,255,255))
                    screen.fill(self.bgColor)
                    self.redrawAll(screen)
                    screen.blit(battleText,(110,35))
                else:
                    if Overworld.wins == 3:
                        battleText  = textBox.render('Defense increased to 7. Your skill turned into Infernal',False,(255,255,255))
                        battleText2 = textBox.render('Overdrive! It now has additional attributes!', False,(255,255,255))
                    elif Overworld.wins == 6:
                        battleText  = textBox.render('Defense increased to 9. Your skill turned into Reign of',False,(255,255,255))
                        battleText2 = textBox.render('Fire! It now has additional attributes!', False,(255,255,255))
                    elif Overworld.wins == 9:
                        battleText  = textBox.render("Defense increased to 10. Your skill turned into Hero's ",False,(255,255,255))
                        battleText2 = textBox.render('Glory! It now has additional attributes!', False,(255,255,255))
                    screen.fill(self.bgColor)
                    self.redrawAll(screen)
                    screen.blit(battleText,(110,35))
                    screen.blit(battleText2,(110,60))
                pygame.display.flip()
                pygame.event.clear()
                userInput = pygame.event.wait()
                pygame.event.clear()
                userInput = pygame.event.wait()
                potions = random.randint(1,3)
                selixer = random.randint(1,3)
                srefresh = random.randint(1,3)
                Battle.items[0][1] += potions
                Battle.items[1][1] += selixer
                Battle.items[2][1] += srefresh
                battleText = textBox.render('Obtained ' + str(potions) + ' Potions, ' + str(selixer) + ' Strength Elixers, and ',False,(255,255,255))
                battleText2 = textBox.render(str(srefresh) + ' Skill Refresh!',False,(255,255,255))
                screen.fill(self.bgColor)
                self.redrawAll(screen)
                screen.blit(battleText,(110,35))
                screen.blit(battleText2,(110,60))
                pygame.display.flip()
                pygame.event.clear()
                userInput = pygame.event.wait()
                pygame.event.clear()
                userInput = pygame.event.wait()
            Battle.playerTurn = True
            Battle.skillCoolDown = None
            Battle.selixerOn = None
            Battle.boss = False
            curScreen = screens["overworld"]
            pygame.sprite.groupcollide(curScreen.playerGroup,curScreen.enemies,False,True)
            curScreen.run()
        elif self.curPlayerHealth <= 0:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("C:/Users/krist/Desktop/112 Homework/Term Project/Defeat- DQVIII.mp3")
            pygame.mixer.music.play()
            screen.fill(self.bgColor)
            textBox = pygame.font.SysFont('Arial',18)
            battleText = textBox.render('You are slain...',False,(255,255,255))
            self.redrawAll(screen)
            screen.blit(battleText,(110,35))
            pygame.display.flip()
            pygame.event.clear()
            userInput = pygame.event.wait()
            pygame.event.clear()
            userInput = pygame.event.wait()
            Battle.playerTurn = True
            Battle.skillCoolDown = None
            Battle.selixerOn = None
            Battle.boss  = False
            (Battle.items[0][1] , Battle.items[1][1] , Battle.items[2][1]) = (3,1,1)
            curScreen = screens["overworld"]
            pygame.sprite.groupcollide(curScreen.playerGroup,curScreen.enemies,True,False)
            curScreen.run()
        

    def __init__(self, width=600, height=600, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        if Overworld.wins == 10:
            self.bgColor = (0,0,0)
        else:
            self.bgColor = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        pygame.init()
    
        
    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        textBox = pygame.font.SysFont('Arial', 18)
        if Overworld.wins == 10:
            self.bgColor = (0,0,0)
        if Battle.boss == True:
            if Overworld.wins == 3:
                pygame.mixer.music.load("C:/Users/krist/Desktop/112 Homework/Term Project/Boss 1- FFV Clash on the Bridge.mp3")
                battleText = textBox.render('Behemoth of Dread stands in your way!',False,(255,255,255))
            elif Overworld.wins == 6:
                pygame.mixer.music.load("C:/Users/krist/Desktop/112 Homework/Term Project/Boss 2- FFIV Boss Theme.mp3")
                battleText = textBox.render('Dragonic Emissary stands in your way!',False,(255,255,255))
            elif Overworld.wins == 9:
                pygame.mixer.music.load("C:/Users/krist/Desktop/112 Homework/Term Project/Boss 3- FFIV Dreadful Fight.mp3")
                battleText = textBox.render('Demonous Beheader stands in your way!',False,(255,255,255))
            elif Overworld.wins == 10:
                pygame.mixer.music.load("C:/Users/krist/Desktop/112 Homework/Term Project/Final Boss- FFVI Dancing Mad.mp3")
                battleText = textBox.render('Impetus appears before you...',False,(255,255,255))
        else:
            pygame.mixer.music.load("C:/Users/krist/Desktop/112 Homework/Term Project/Battle Theme- FFVI Decisive Battle.mp3")
            battleText = textBox.render('Enemies stand in your way!',False,(255,255,255))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()
        
        if Overworld.gameClear > 0:
            Battle.pHealth = 500*Overworld.gameClear + 25*(Overworld.wins//3)
            Battle.pAttack = 60*Overworld.gameClear + 2*(Overworld.wins//3)
            Battle.pDefense = 10*Overworld.gameClear + 1*(Overworld.wins//3)
            Battle.pLevel = 4*Overworld.gameClear + 1*(Overworld.wins//3)
            Battle.skillAtts = ["fire","star","cosmic","light"]
            Battle.eHealth = 400*Overworld.gameClear + 50*(Overworld.wins//3)
            Battle.eAttack = 30*Overworld.gameClear + 5*(Overworld.wins//3)
            Battle.eDefense = 9*Overworld.gameClear +  1*(Overworld.wins//3)
            Battle.eWeakness = ["light"]
            Battle.bHealth = 1000*Overworld.gameClear + 100*(Overworld.wins//3)
            Battle.bAttack = 75*Overworld.gameClear + 8*(Overworld.wins//3)
            Battle.bDefense = 12*Overworld.gameClear  + 1*(Overworld.wins//3)
            Battle.bWeakness = ["fire","star","cosmic","light"]
        elif Overworld.wins == 10:
            Battle.pHealth = 500
            Battle.pAttack = 60
            Battle.pDefense = 10
            Battle.pLevel = 4
            Battle.skillAtts = ["fire","star","cosmic","light"]
            Battle.eHealth = 400
            Battle.eAttack = 30
            Battle.eDefense = 9
            Battle.eWeakness = ["light"]
            Battle.bHealth = 1000
            Battle.bAttack = 75
            Battle.bDefense = 12
            Battle.bWeakness = ["light"]
        elif Overworld.wins > 6:
            Battle.pHealth = 300
            Battle.pAttack = 35
            Battle.pDefense = 9
            Battle.pLevel = 3
            Battle.skillAtts = ["fire","star","cosmic"]
            Battle.eHealth = 200
            Battle.eAttack = 25
            Battle.eDefense = 6
            Battle.eWeakness = ["light","star"]
            Battle.bHealth = 800
            Battle.bAttack = 50
            Battle.bDefense = 9
            Battle.bWeakness = ["cosmic"]
        elif Overworld.wins > 3:
            Battle.pHealth = 150
            Battle.pAttack = 20
            Battle.pDefense = 7
            Battle.pLevel = 2
            Battle.skillAtts = ["fire","star"]
            Battle.eHealth = 100
            Battle.eAttack = 15
            Battle.eDefense = 3
            Battle.eWeakness = ["light","star"]
            Battle.bHealth = 450
            Battle.bAttack = 30
            Battle.bDefense = 6
            Battle.bWeakness = ["fire"]
        else:
            Battle.pHealth = 50
            Battle.pAttack = 10
            Battle.pDefense = 5
            Battle.pLevel = 1
            Battle.skillAtts = ["fire"]
            Battle.eHealth = 30
            Battle.eAttack = 5
            Battle.eDefense = 2
            Battle.eWeakness = ["light","star"]
            Battle.bHealth = 200
            Battle.bAttack = 15
            Battle.bDefense = 3
            Battle.bWeakness = []
        
        self.init()
        if Overworld.wins == 10:
            screen.fill(self.bgColor)
            self.playerGroup.draw(screen)
            pygame.display.flip()
            pygame.event.set_blocked([pygame.KEYDOWN,pygame.KEYUP])
            pygame.mixer.music.play(-1)
            wait = pygame.time.get_ticks()
            self.playerGroup.draw(screen)
            imp = pygame.transform.scale(pygame.image.load("C:/Users/krist/Desktop/112 Homework/Term Project/finalbossfade.png"),(173,146))
            imp = imp.convert()
            imp.set_alpha(None)
            i = 1
            while True:
                check = pygame.time.get_ticks()
                if check - wait >= 27000:
                    break
                imp.set_alpha(i)
                screen.blit(imp,(self.enemy.x-86,self.enemy.y-73))
                pygame.display.flip()
                pygame.time.delay(750)
                pygame.event.pump()
                i += 1
            pygame.event.set_allowed([pygame.KEYDOWN,pygame.KEYUP])
            skill = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            screen.blit(battleText, (110,35))
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.event.set_blocked(pygame.MOUSEMOTION)
        else:
            pygame.mixer.music.play(-1)
            pygame.event.set_blocked(pygame.MOUSEMOTION)
            skill = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            screen.blit(battleText, (110,35))
            pygame.display.flip()
            pygame.event.clear()
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                pass
        poison = None
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            if self.cursor.optPos != None:
                battleText = textBox.render('What will you do?',False,(255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.cursor.optPos != None:
                        if self.cursor.optPos == 0:
                            skill = False
                            self.cursor.optPos = None
                            self.cursor.enPos = 0
                            battleText = textBox.render('Which enemy will you attack?',False,(255,255,255))
                            for p in self.cursor.points:
                                p[0] += 270
                                p[1] -= 80
                        elif self.cursor.optPos == 1 and Battle.skillCoolDown == None:
                            skill = True
                            self.cursor.optPos = None
                            self.cursor.enPos = 0
                            battleText = textBox.render('Which enemy will you attack?',False,(255,255,255))
                            for p in self.cursor.points:
                                p[0] += 270
                                p[1] -= 110
                        elif self.cursor.optPos == 1 and Battle.skillCoolDown != None:
                            battleText = textBox.render('Skill on cooldown! Cannot Use!', False,(255,255,255))
                            screen.fill(self.bgColor)
                            self.redrawAll(screen)
                            screen.blit(battleText,(110,35))
                            pygame.display.flip()
                            pygame.event.clear()
                            userInput = pygame.event.wait()
                            pygame.event.clear()
                            userInput = pygame.event.wait()
                            if userInput == pygame.KEYDOWN:
                                pass
                        elif self.cursor.optPos == 2:
                            Battle.playerTurn = False
                            skill = False
                            self.player.defense *= 2
                            Battle.playerDefTurn = True
                            battleText = textBox.render('You defended! The next attack will deal less damage!',False,(255,255,255))
                            screen.fill(self.bgColor)
                            self.redrawAll(screen)
                            screen.blit(battleText,(110,35))
                            pygame.display.flip()
                            pygame.event.clear()
                            userInput = pygame.event.wait()
                            if userInput == pygame.KEYDOWN:
                                pass
                        elif self.cursor.optPos == 3:
                            skill = False
                            #pass control to item cursor
                            self.cursor = self.itemCursor
                    elif event.key == pygame.K_RETURN and self.cursor.enPos != None:
                        Battle.playerTurn = False
                        if skill == True:
                            if Battle.boss == True:
                                for att in Battle.skillAtts:
                                    if att in Battle.bWeakness:
                                        damage = ((self.player.attack*2)*3//self.enemy.defense)*3
                                        battleText3 = textBox.render('Very effective! The enemy takes a massive ' + str(damage) + ' damage!',False,(255,255,255))
                                        break
                                    else:
                                        damage = int((random.randint(self.player.attack,self.player.attack*2)*3//self.enemy.defense)*1.5)
                                        battleText3 = textBox.render('Effective! The enemy takes ' + str(damage) + ' damage!',False,(255,255,255))
                            else:
                                for att in Battle.skillAtts:
                                    if att in Battle.eWeakness:
                                        damage = ((self.player.attack*2)*3//self.enemy.defense)*3
                                        battleText3 = textBox.render('Very effective! The enemy takes a massive ' + str(damage) + ' damage!',False,(255,255,255))
                                        break
                                    else:
                                        damage = int((random.randint(self.player.attack,self.player.attack*2)*3//self.enemy.defense)*1.5)
                                        battleText3 = textBox.render('Effective! The enemy takes ' + str(damage) + ' damage!',False,(255,255,255))
                            if Overworld.wins > 9 or Overworld.gameClear > 0:
                                battleText = textBox.render("You used the skill, Hero's Glory! You channel the strength",False,(255,255,255))
                                battleText2 = textBox.render('gained from your past battles and expel a great light!',False,(255,255,255))
                            elif Overworld.wins > 6:
                                battleText = textBox.render('You used the skill, Reign of Fire! Meteorites strike the',False,(255,255,255))
                                battleText2 = textBox.render('enemy from above!',False,(255,255,255))
                            elif Overworld.wins > 3:
                                battleText = textBox.render('You used the skill, Infernal Overdrive! The power of the',False,(255,255,255))
                                battleText2 = textBox.render('sun envelops your sword!',False,(255,255,255))
                            else:
                                battleText = textBox.render('You used the skill, Blazing Soul! Flames erupt from your',False,(255,255,255))
                                battleText2 = textBox.render('blade!',False,(255,255,255))
                            screen.fill(self.bgColor)
                            self.redrawAll(screen)
                            screen.blit(battleText,(110,35))
                            screen.blit(battleText2,(110,60))
                            screen.blit(battleText3,(110,85))
                            pygame.event.clear()
                            userInput = pygame.event.wait()
                            if userInput == pygame.KEYDOWN:
                                pass
                            self.curEnemyHealth -= damage
                            if self.curEnemyHealth <= 0:
                                self.enemies.remove(self.enemy)
                            Battle.skillCoolDown = 0
                            self.cursor.optPos = 0
                            self.cursor.enPos = None
                            skill = False
                            for p in self.cursor.points:
                                p[0] -= 270
                                p[1] += 80
                        else:
                            damage = random.randint(self.player.attack,self.player.attack*2)*3//self.enemy.defense
                            battleText = textBox.render('You attack! The enemy takes ' + str(damage) +' damage!',False,(255,255,255))
                            screen.fill(self.bgColor)
                            self.redrawAll(screen)
                            screen.blit(battleText,(110,35))
                            pygame.event.clear()
                            userInput = pygame.event.wait()
                            if userInput == pygame.KEYDOWN:
                                pass
                            self.curEnemyHealth -= damage
                            if self.curEnemyHealth <= 0:
                                 self.enemies.remove(self.enemy)
                            self.cursor.optPos = 0
                            self.cursor.enPos = None
                            for p in self.cursor.points:
                                p[0] -= 270
                                p[1] += 80
                    elif event.key == pygame.K_RETURN and self.cursor.itemPos != None:
                        Battle.playerTurn = False
                        if self.cursor.itemPos == 0:
                            if self.items[0][1] > 0 and self.curPlayerHealth == self.player.health:
                                battleText = textBox.render('Already at max health!',False,(255,255,255))
                            elif self.items[0][1] > 0 and self.player.health-self.curPlayerHealth >= Battle.pHealth//2:
                                self.curPlayerHealth += Battle.pHealth//2
                                self.items[0][1] -= 1
                                battleText = textBox.render('Restored ' + str(Battle.pHealth//2) + ' HP!',False,(255,255,255))
                            elif self.items[0][1] > 0 and self.player.health -self.curPlayerHealth < Battle.pHealth//2:
                                self.curPlayerHealth =  self.player.health
                                self.items[0][1] -= 1
                                battleText = textBox.render('Restored ' + str(Battle.pHealth - self.curPlayerHealth) + ' HP!',False,(255,255,255))
                            elif self.items[0][1] == 0:
                                battleText = textBox.render('Out of Potions!',False,(255,255,255))
                        elif self.cursor.itemPos == 1:
                            if self.items[1][1] > 0 and Battle.selixerOn == None:
                                Battle.selixerOn = 0
                                self.player.attack  *= 3
                                self.items[1][1] -= 1
                                battleText = textBox.render('Attack power has been tripled!',False,(255,255,255))
                            elif self.items[1][1] > 0 and Battle.selixerOn != None:
                                battleText = textBox.render('Already have an elixer activated!',False,(255,255,255))
                            elif self.items[1][1] == 0:
                                battleText = textBox.render('Out of Strength Elixers!',False,(255,255,255))
                        elif self.cursor.itemPos == 2:
                            if self.items[2][1] > 0 and Battle.skillCoolDown != None:
                                Battle.skillCoolDown = None
                                self.items[2][1] -= 1
                                battleText = textBox.render('Skill can be used again!',False,(255,255,255))
                            elif self.items[2][1] > 0 and Battle.skillCoolDown == None:
                                battleText = textBox.render('Skill is not on cooldown!',False,(255,255,255))
                            elif self.items[2][1] == 0:
                                battleText = textBox.render('Out of Skill Refresh!',False,(255,255,255))
                        screen.fill(self.bgColor)
                        self.redrawAll(screen)
                        screen.blit(battleText,(110,35))
                        pygame.display.flip()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                        if userInput == pygame.KEYDOWN:
                            pass
                        self.cursor = self.cursorReturn
                    elif event.key == pygame.K_BACKSPACE:
                        if self.cursor.optPos == None and self.cursor.itemPos == None:
                            self.cursor.optPos = 0
                            self.cursor.enPos = None
                            for p in self.cursor.points:
                                p[0] -= 270
                                p[1] +=  80
                        elif self.cursor.optPos == None and self.cursor.enPos == None:
                            self.cursor = self.cursorReturn
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                    self.cursor.update(self.isKeyPressed)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
                    
            if Battle.playerTurn == False:
                screen.blit(battleText,(110,35))
                pygame.display.flip()
                pygame.event.clear()
                userInput = pygame.event.wait()
                self.screenChange(screen)
                screen.blit(battleText,(110,35))
                pygame.display.flip()
                pygame.event.clear()
                userInput = pygame.event.wait()
                if Battle.enemyDefTurn == True:
                    self.enemy.defense //= 2
                    Battle.enemyDefTurn = None
                enemyAction = random.randint(1,10)
                if enemyAction == 10 and Battle.boss == True:
                    if Overworld.wins == 3:
                        damage = int((random.randint(self.enemy.attack,self.enemy.attack*2)*3//self.player.defense)*1.5)
                        battleText = textBox.render('Behemoth of Dread breathes a hot poisonous gas!',False,(255,255,255))
                        if poison == None and Battle.playerDefTurn == None:
                            battleText2 = textBox.render('Does ' + str(damage) + ' damage and poisons you!',False,(255,255,255))
                            poison = 0
                        else:
                            battleText2 = textBox.render('Does ' + str(damage) + ' damage!',False,(255,255,255))
                        screen.fill(self.bgColor)
                        self.redrawAll(screen)
                        screen.blit(battleText,(110,35))
                        screen.blit(battleText2,(110,60))
                        pygame.display.flip()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                        self.curPlayerHealth -= damage
                        if self.curPlayerHealth <= 0:
                            self.playerGroup.remove(self.player)
                    elif Overworld.wins == 6:
                        damage = int((random.randint(self.enemy.attack,self.enemy.attack*2)*3//self.player.defense)*1.5)
                        recover = damage//2
                        battleText = textBox.render('Dragonic Emissary shoots its heavenly scales at you!',False,(255,255,255))
                        battleText2 = textBox.render('Does ' + str(damage) + ' damage! Dragonic Emissary recovers ' + str(recover) + ' health!',False,(255,255,255))
                        screen.fill(self.bgColor)
                        self.redrawAll(screen)
                        screen.blit(battleText,(105,35))
                        screen.blit(battleText2,(105,60))
                        pygame.display.flip()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                        self.curPlayerHealth -= damage
                        self.curEnemyHealth += recover
                        if self.curEnemyHealth > self.enemy.health:
                            self.curEnemyHealth = self.enemy.health
                        if self.curPlayerHealth <= 0:
                            self.playerGroup.remove(self.player)
                    elif Overworld.wins == 9:
                        battleText = textBox.render('Demonous Beheader launches a flurry of attacks!',False,(255,255,255))
                        screen.fill(self.bgColor)
                        self.redrawAll(screen)
                        screen.blit(battleText,(110,35))
                        pygame.display.flip()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                        hits = random.randint(3,5)
                        for i in range(hits):
                            damage = int((random.randint(self.enemy.attack,self.enemy.attack*2)*3//self.player.defense)*1.5)
                            battleText = textBox.render('Does ' + str(damage) + ' damage!',False,(255,255,255))
                            self.curPlayerHealth -= damage
                            screen.fill(self.bgColor)
                            self.redrawAll(screen)
                            screen.blit(battleText,(110,35))
                            pygame.display.flip()
                            pygame.event.clear()
                            userInput = pygame.event.wait()
                            pygame.event.clear()
                            userInput = pygame.event.wait()
                            if self.curPlayerHealth <= 0:
                                self.playerGroup.remove(self.player)
                            self.screenChange(screen)
                    elif Overworld.wins == 10:
                        battleText = textBox.render('Impetus focuses and releases a wave of dark energy!',False,(255,255,255))
                        battleText2 = textBox.render('You barely hold on!',False,(255,255,255))
                        screen.fill(self.bgColor)
                        self.redrawAll(screen)
                        screen.blit(battleText,(110,35))
                        screen.blit(battleText2,(110,60))
                        pygame.display.flip()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                        self.curPlayerHealth = 1
                elif enemyAction >= 3:
                    damage = random.randint(self.enemy.attack,self.enemy.attack*2)*3//self.player.defense
                    battleText = textBox.render('The enemy attacks! Does ' + str(damage) + ' damage!',False,(255,255,255))
                    screen.fill(self.bgColor)
                    self.redrawAll(screen)
                    screen.blit(battleText,(110,35))
                    pygame.display.flip()
                    pygame.event.clear()
                    userInput = pygame.event.wait()
                    pygame.event.clear()
                    userInput = pygame.event.wait()
                    self.curPlayerHealth -= damage
                    if self.curPlayerHealth <= 0:
                        self.playerGroup.remove(self.player)
                elif enemyAction < 3:
                    self.enemy.defense *= 2
                    Battle.enemyDefTurn = True
                    battleText = textBox.render('The enemy defends!',False,(255,255,255))
                    screen.fill(self.bgColor)
                    self.redrawAll(screen)
                    screen.blit(battleText,(110,35))
                    pygame.display.flip()
                    pygame.event.clear()
                    userInput = pygame.event.wait()
                self.screenChange(screen)
                if poison !=  None:
                    damage = Battle.pHealth//5
                    battleText = textBox.render('You are hurt by the poison! Does ' + str(damage) + ' damage!',False,(255,255,255))
                    screen.fill(self.bgColor)
                    self.redrawAll(screen)
                    screen.blit(battleText,(110,35))
                    pygame.display.flip()
                    pygame.event.clear()
                    userInput = pygame.event.wait()
                    pygame.event.clear()
                    userInput = pygame.event.wait()
                    self.curPlayerHealth -= damage
                    if self.curPlayerHealth <= 0:
                        self.playerGroup.remove(self.player)
                    self.screenChange(screen)
                    poison += 1
                    if poison == 3:
                        poison = None
                        battleText = textBox.render('You overcame the effects of the poison!',False,(255,255,255))
                        screen.fill(self.bgColor)
                        self.redrawAll(screen)
                        screen.blit(battleText,(110,35))
                        pygame.display.flip()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                if Battle.skillCoolDown != None:
                    Battle.skillCoolDown += 1
                    if Battle.skillCoolDown == 3:
                        Battle.skillCoolDown = None
                        battleText = textBox.render('Skill can now be used again.',False,(255,255,255))
                        screen.fill(self.bgColor)
                        self.redrawAll(screen)
                        screen.blit(battleText,(110,35))
                        pygame.display.flip()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                if isinstance(Battle.selixerOn,int):
                    Battle.selixerOn += 1
                    if Battle.selixerOn == 4:
                        Battle.selixerOn = None
                        self.player.attack //= 3
                        battleText = textBox.render('Strength Elixer wore off.',False,(255,255,255))
                        screen.fill(self.bgColor)
                        self.redrawAll(screen)
                        screen.blit(battleText,(110,35))
                        pygame.display.flip()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                        pygame.event.clear()
                        userInput = pygame.event.wait()
                Battle.turnNum += 1
                Battle.playerTurn = True
            if Battle.playerDefTurn == True and Battle.playerTurn == True:
                self.player.defense //= 2
                Battle.playerDefTurn = None
                
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            screen.blit(battleText,(110,35))
            pygame.display.flip()
        
        pygame.quit()

screens = {"overworld": Overworld(), "battle": Battle()}

def startGame(wins,curScreen=screens["overworld"]):
    game = curScreen
    game.run()

if __name__ == '__main__':
    startGame(Overworld.wins)
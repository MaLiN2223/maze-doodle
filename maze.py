from enum import IntFlag
import pygame 
import random
    
wall = "*"
size = 20

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

class Vector:
    """ Vector class represents and manipulates x,y coords. """

    def __init__(self, x, y):
        """ Create a new point """
        self.x = x
        self.y = y

    def __mul__(self, other):
        if not isinstance(other, int):
            raise ValueError("Second multiplication object must be an int")
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return self is other or (self.x == other.x and self.y == other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return "Position ({0},{1})".format(self.x, self.y)

    def __getitem__(self, item):
        return self.x if item == 0 else self.y

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def toPoint(self):
        return [self.x,self.y]
    def copy(self):
        """
        Creates new object with the same position
        :rtype: Vector
        """
        return Vector(self.x, self.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

class Direction(IntFlag):
    Up = 0
    Right = 1
    Down = 2
    Left = 3

    
class Tile:
    downVector = Vector(0,size)
    rightVector = Vector(size,0)
    
    def __init__(self):
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.locked = [True]*4
        self.visited = False

    def unlock(self,direction):
        self.locked[direction] = False
        
    def draw(self,vector,surface):
        if self.locked[Direction.Up]:
            pygame.draw.line(surface,BLACK,vector.toPoint(),(vector+Tile.rightVector).toPoint())
        if self.locked[Direction.Right]:            
            pygame.draw.line(surface,BLACK,(vector+Tile.rightVector).toPoint(),(vector+Tile.rightVector + Tile.downVector).toPoint())
        if self.locked[Direction.Down]:            
            pygame.draw.line(surface,BLACK,(vector+Tile.downVector).toPoint(),(vector+Tile.rightVector + Tile.downVector).toPoint())
        if self.locked[Direction.Left]:            
            pygame.draw.line(surface,BLACK,vector.toPoint(),(vector+ Tile.downVector).toPoint())
            
    def getRandomNbr(self):
        nones = [
                    self.up is None or self.up.visited,
                    self.right is None or self.right.visited,
                    self.down is None or self.down.visited,
                    self.left is None or self.left.visited
                ]
        possible = []
        for i in range(4):
            if not nones[i]:
                possible.append(i) 
        if len(possible) == 0:
            return None
        dir = possible[random.randrange(len(possible))] 
        return self.getNbr(dir),dir
    
    def getNbr(self,direction):
        if direction == Direction.Up:
            return self.up
        if direction == Direction.Right:
            return self.right
        if direction == Direction.Down:
            return self.down
        if direction == Direction.Left:
            return self.left
        
    @property
    def wallCount(self):
        return sum(self.locked)
         
class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]
    @property
    def size(self):
        return len(self.items)

            
class Maze:
    def __init__(self,length,height):
        self.length = length
        self.height = height
        self.board = [[Tile() for i in range(length)] for j in range(height)]
        for i in range(height):
            for j in range(length):
                self.board[i][j] = Tile()
                
        for i in range(height):
            for j in range(length):
                if i < height - 1: 
                    self.board[i][j].right = self.board[i+1][j]
                    self.board[i+1][j].left = self.board[i][j]
                if j < length - 1:
                    self.board[i][j].down =  self.board[i][j+1]
                    self.board[i][j+1].up =  self.board[i][j]
        

    def print(self,surface):
        for i in range(self.height):
            for j in range(self.length): 
                self.board[i][j].draw(Vector(i*size,j*size),surface)

    def randomize(self,surface):
        stack = Stack()
        current = self.board[0][0]
        visitedCount = 0
        while True:
            q = current.getRandomNbr()
            if not current.visited:
                visitedCount+=1
            if visitedCount >= self.length*self.height:
                raise StopIteration()
            current.visited = True
            if q == None:
                print(stack.size)
                if stack.size > 0:
                    current = stack.pop()
                else:
                    print("OKDONE")
                    raise StopIteration()
            else:                
                next,x = q
                stack.push(current)
                current.unlock(x)
                next.unlock((x+2)%4)  
                current = next
            yield current
    def randomizeExits(self):
        pass
            
                
pygame.init()
screen = pygame.display.set_mode((800,600))
done = False

maze = Maze(25,25)
generator = maze.randomize(screen)
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        
        screen.fill(WHITE)
        try:
            next(generator)
        except StopIteration:
            pass
        maze.print(screen)
        #pygame.time.wait(100)
        pygame.display.flip()

pygame.quit()

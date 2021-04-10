import enum
from PIL import Image, ImageDraw, ImageFont

class Movements(enum.Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class CardinalNode(object):
    def __init__(self, pos, movement : Movements):
        self.pos = pos
        self.movement = movement
        self.actions = [Movements.UP, Movements.DOWN, Movements.LEFT, Movements.RIGHT]
    
    def __str__(self):
        val = ",".join(str(x)for x in self.pos)

        return "[" + val + ", " + str(self.movement) + "]"




class Maze (object):

    WALL = "#"
    WALK = " "
    START = "A"
    END = "B"


    def __init__(self, file):
        self.maze = []
        self.start = [0,0]
        self.__setupMaze(file)
    
    def __setupMaze(self, file):
        mazeFile = open(file, 'r')
        self.maze = mazeFile.readlines()
        start = [0,0]

        for c in range(len(self.maze)):
            self.maze[c] = self.maze[c].replace("\n", "")
            if self.maze[c].find(self.START) != -1:
                self.start = [c, self.maze[c].find(self.START)]

    def __posInList(self, _list, pos):
        for x in _list:
            if (x.pos == pos):
                return True

        return False

    def __positionOB(self, pos):
        if (pos[0] < 0 or pos[0] >= len(self.maze) 
            or pos[1] < 0 or pos[1] >= len(self.maze[0])):
            return True
        return False

    def __isWall(self, pos):
        if self.maze[pos[0]][pos[1]] == self.WALL:
            return True

        return False

    def __nodeNotInList(self, _list, node):
        for x in _list:
            if (x.pos == node.pos and x.movement == node.movement):
                return False

        return True

    def __checkNode(self, node : CardinalNode, traversed):        
        #Make sure new pos is in bounds
        if self.__positionOB(node.pos):
            return 0
        #Make sure new pos is not a wall
        if self.__isWall(node.pos):
            return 0
        #Check if new node has been used already
        if not(self.__nodeNotInList(traversed, node)):
            return 0

        return node

    def getMazeImage(self, pos, traversed):
        sizeX = 1080
        sizeY = 720

        boxSizeX = sizeX //  (len(self.maze[0]))
        boxSizeY = sizeY // len(self.maze)
        boxSize = boxSizeX + boxSizeY

        im = Image.new("RGB", (sizeX, sizeY), "#000000")
        draw = ImageDraw.Draw(im)
        
        x = 0
        y = 0

        for c in range(len(self.maze)):
            for i in range(len(self.maze[c])):
                sizeAndPos = (x, y, x + boxSizeX, y + boxSizeY)
                mazePos = self.maze[c][i]

                font = ImageFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', (boxSize//2))

                #Start Pos
                if(mazePos == self.START):
                    draw.rectangle(sizeAndPos, fill=(256, 0, 0), outline=(0, 0, 100))
                    textX = x + (boxSizeX//2) - font.getsize("A")[0] // 2
                    textY = y
                    draw.text((textX, textY), "A", font = font, align="center")
                #End Pos
                elif(mazePos == self.END):
                    draw.rectangle(sizeAndPos, fill=(0, 256, 0), outline=(0, 0, 100))
                    textX = x + (boxSizeX//2) - font.getsize("B")[0] // 2
                    textY = y
                    draw.text((textX, textY), "B", font = font, align="center")
                #Last known position
                elif (c == pos[0] and i == pos[1]):
                    draw.rectangle(sizeAndPos, fill=(256, 256, 256), outline=(0, 0, 0))
                #Traversed positions
                elif (self.__posInList(traversed, [c,i])):
                    draw.rectangle(sizeAndPos, fill=(256, 256, 0), outline=(0, 0, 0))
                #Walls
                elif(mazePos == self.WALL):
                    draw.rectangle(sizeAndPos, fill=(25, 25, 25), outline=(0, 0, 0))
                #Non travesered walkable spots
                elif(mazePos == self.WALK):
                    draw.rectangle(sizeAndPos, fill=(0, 0, 0), outline=(0, 0, 100), width=3)

                x += boxSizeX
            x = 0
            y += boxSizeY

        return im

    def isWin(self, pos):
        if self.__positionOB(pos):
            return False

        if self.maze[pos[0]][pos[1]] == self.END:
            return True

        return False

    def nearestNode(self, direction : Movements, node : CardinalNode, traversed):
        newNode = CardinalNode(node.pos, Movements.UP)
        pos = [0,0]
        if direction == Movements.UP:
            pos = [newNode.pos[0]-1, newNode.pos[1]]
        elif direction == Movements.DOWN:
            pos = [newNode.pos[0]+1, newNode.pos[1]]
        elif direction == Movements.LEFT:
            pos = [newNode.pos[0], newNode.pos[1] - 1]
        elif direction == Movements.RIGHT:
            pos = [newNode.pos[0], newNode.pos[1] + 1]
        
        newNode.pos = pos

        return self.__checkNode(newNode, traversed)

    def next(self, node, traversed, nodes = []):
        nodes = []
        movement = (Movements.UP, Movements.DOWN, Movements.LEFT, Movements.RIGHT)

        for c in movement:
            tmp = self.nearestNode(c, node, traversed)
            if isinstance(tmp, CardinalNode):
                nodes.append(tmp)

        return nodes


maze = Maze(r"C:\Users\andy.powell\OneDrive - wiregrass.edu\Docs\Class Resources\python\Programs\Maze Output\maze.txt")

traversed = []

nodes = [CardinalNode(maze.start, Movements.NONE)]

curr = None

count = 0
while True:
    if len(nodes) <= 0:
        print("No Path to winning")
        break
    
    #Breadth First Search (BFS)
    curr = nodes.pop(0)
    #Depth First Search (DFS)
    #curr = node.pop()
    traversed.append(curr)

    print("Current: ", curr)

    if(maze.isWin(curr.pos)):
        print("Winner")
        break
    
    print(len(maze.next(curr, traversed)))
    nodes.extend(maze.next(curr, traversed))
    
    #im = maze.getMazeImage(curr.pos, traversed)
    #im.save(r"C:\Users\andy.powell\OneDrive - wiregrass.edu\Pictures\Mazes\maze1\bfs\img" + str(count) + ".png")
    
    count+=1

currPos = curr.pos

print("Iterations: ", count)

im = maze.getMazeImage(currPos, traversed)
im.show()
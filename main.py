import sys
import argparse
import random

global args

EMPTY = '_'
LIGHTBULB = 'b'
WALL = 'W'

class AkariPuzzle:
    def __init__(self, width, height):
        puzzle = []
        for i in range(height):
            puzzle = puzzle + [ [ EMPTY ] * width ]
        self.puzzle = puzzle
        self.width = width
        self.height = height
        self.nBulbs = 0

    def countAdjacentBulbs(self, x, y):
        count = 0
        for dx,dy in [ [-1,0], [1,0], [0,-1], [0,1] ]:
            if ( x + dx  >= 0) and (x + dx < self.height):
                if ( y + dy >= 0 ) and ( y + dy < self.width ):
                    if ( self.puzzle[x+dx][y+dy] == LIGHTBULB):
                        count = count + 1
        return count

    def random(self, nBulbs, nWalls):
        self.__init__(self.width, self.height)
        if (nBulbs >= int(self.width * self.height * 0.25)):
            nBulbs = int(self.width * self.height * 0.25)
            print('Warning - changing number of light bulbs to maximum', nBulbs)
        toPlace = nBulbs
        while(toPlace > 0):
            x = random.randint(0,self.height-1)
            y = random.randint(0,self.width-1)
            if (self.puzzle[x][y] == EMPTY ):
                if (self.countAdjacentBulbs(x,y) == 0):
                    self.puzzle[x][y] = LIGHTBULB
                    toPlace = toPlace - 1
        self.nBulbs = nBulbs
        self.fixConflicts()
        toPlace = nWalls
        while(toPlace > 0):
            x = random.randint(0,self.height-1)
            y = random.randint(0,self.width-1)
            if (self.puzzle[x][y] == EMPTY ):
                self.puzzle[x][y] = WALL
                toPlace = toPlace - 1
        bw = self.calcBlackAndWhite()
        dark = self.getItems([ EMPTY ],bw)
        while(len(dark) > 0 ):
            x,y = random.choice(dark)
            self.puzzle[x][y] = LIGHTBULB
            bw = self.calcBlackAndWhite()
            dark = self.getItems([EMPTY], bw)
        self.calcWallHints()

    @staticmethod
    def getItems(things, puzzle):
        items = []
        height = len(puzzle)
        for i in range(height):
            width = len(puzzle[i])
            for j in range(width):
                if (puzzle[i][j] in things):
                    items = items + [(i,j)]
        return items

    def getLightBulbs(self):
        return self.getItems([ LIGHTBULB ], self.puzzle)

    def fixConflicts(self):
        # Place a wall between light bulbs that are in the same row or column
        bulbs = self.getLightBulbs()
        for x,y in bulbs:
            # Check row right
            dist = 0
            for yy in range(y+1,self.width):
                if ( self.puzzle[x][yy] == LIGHTBULB):
                    dist = yy - y
                    if (random.random() < 0.5):
                        if (random.random() < 0.5):
                            self.puzzle[x][y+1] = WALL
                        else:
                            self.puzzle[x][yy-1] = WALL
                    else:
                        ry = random.randint(y+1,yy-1)
                        self.puzzle[x][ry] = WALL
                    break
                elif ( self.puzzle[x][yy] != EMPTY):
                    break

            dist = 0
            for xx in range(x+1,self.height):
                if ( self.puzzle[xx][y] == LIGHTBULB):
                    dist = xx - x
                    if (random.random() < 0.5):
                        if (random.random() < 0.5):
                            self.puzzle[x+1][y] = WALL
                        else:
                            self.puzzle[xx-1][y] = WALL
                    else:
                        ry = random.randint(x+1,xx-1)
                        self.puzzle[ry][y] = WALL
                    break
                elif ( self.puzzle[xx][y] != EMPTY):
                    break

    def getPuzzle(self):
        p = []
        for i in range(self.height):
            r = []
            for j in range(self.width):
                r.append( self.puzzle[i][j] )
            p.append(r)
        return p

    def calcBlackAndWhite(self):
        npuzzle = self.getPuzzle()
        bulbs = self.getLightBulbs()
        for x,y in bulbs:
            #Light right
            for yy in range(y+1,self.width):
                if ( npuzzle[x][yy] in [ EMPTY, 'w' ] ):
                    npuzzle[x][yy] = 'w'
                else:
                    break
            # Light left
            for yy in range(y-1,-1,-1):
                if ( npuzzle[x][yy] in [ EMPTY, 'w'] ):
                    npuzzle[x][yy] = 'w'
                else:
                    break

            #Light down
            for xx in range(x+1,self.height):
                if ( npuzzle[xx][y] in [ EMPTY, 'w'] ):
                    npuzzle[xx][y] = 'w'
                else:
                    break
            # Light up
            for xx in range(x-1,-1,-1):
                if ( npuzzle[xx][y] in [ EMPTY, 'w'] ):
                    npuzzle[xx][y] = 'w'
                else:
                    break
        return npuzzle

    def calcWallHints(self):
        walls = self.getItems([WALL], self.puzzle)
        for x,y in walls:
            self.puzzle[x][y] = "{0}".format(self.countAdjacentBulbs(x,y))

    @staticmethod
    def createSolutionString(puzzle):
        s = ''
        for i in range(len(puzzle)):
            if (i > 0):
                s = s + '\n'
            s = s + '#   '
            for j in range(len(puzzle[i])):
                s = s + puzzle[i][j]
        return s

    @staticmethod
    def createPuzzleString(puzzle):
        s = ''
        for i in range(len(puzzle)):
            if (i > 0):
                s = s + '\n'
            for j in range(len(puzzle[i])):
                if ( puzzle[i][j] == LIGHTBULB):
                    s = s + EMPTY
                else:
                    s = s + puzzle[i][j]
        return s

def makePuzzles( count, width, height, bulbs, walls, solution):
    for i in range(count):
        puzzle = AkariPuzzle( width, height )
        if ( bulbs == -1):
            bulbs = int(width * height * 0.2)
        if ( walls == -1 ):
            walls = int(width * height * 0.3)
        puzzle.random(bulbs, walls)
        print('# Start of puzzle')
        print(height,width)
        print(puzzle.createPuzzleString(puzzle.puzzle))
        print('# End of puzzle')
        if ( solution ):
            print('#  Solution')
            print(puzzle.createSolutionString(puzzle.puzzle))


def t1():
    for n in range(6,32,2):
        makePuzzles(20, n, n, n*2, n*2, True)


def main( argv = None ):
    if (argv == None ):
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description='create a modified Akari Puzzle')
    parser.add_argument('--width', action='store', dest='width', type=int, default=8)
    parser.add_argument('--height', action='store', dest='height', type=int, default=8)
    parser.add_argument('--verbose', '-v', action='count', dest='verbose', default=0)
    parser.add_argument('--count', '-c', action='store', dest='count', default=1)
    parser.add_argument('--solution', '-s', action='store_true', dest='solution', default=False)
    parser.add_argument('--bulbs', '-b', action='store', dest='bulbs', type=int, default=-1)
    parser.add_argument('--walls', '-w', action='store', dest='walls', type=int, default=-1)

    args = parser.parse_args( argv )
    if (args.verbose > 0 ):
        print('AkariMaker {0}x{1} bulbs {2} walls {3}'.format(args.width, args.height, args.bulbs, args.walls ))

    makePuzzles(args.count, args.width, args.height, args.bulbs, args.walls, args.solution )


if __name__ == '__main__':
    main()

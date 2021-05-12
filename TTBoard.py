import copy

XMOVE = 1               # indicates a node in the tree where X has the next move
OMOVE = -1              # indicates a node in the tree where O has the next move
XMARK = 1               # mark for a cell with an X in it
NOMARK = 0              # mark for a cell with nothing in it
OMARK = -1              # mark for a cell with an O in it
XWIN = 1                # a terminal node where X wins
OWIN = -1               # a terminal node where O wins
DRAW = 0                # a terminal node that is a draw
NOTDONE = -100          # marks a non-terminal node
HUGEVAL = 1000000000    # just a large int, for comparison

class TTBoard():
    WIDTH = 3
    numboards = 0       # class-level variable for how many nodes in the tree
    numsearched = 0
    #pointAdj = bool

    def __init__(self, whosemove, pointAdj=bool):
        self.doPointAdj = pointAdj
        self.cells = [[NOMARK, NOMARK, NOMARK], [NOMARK, NOMARK, NOMARK], [NOMARK, NOMARK, NOMARK]]
        self.moves = 0
        self.whosemove = whosemove  # whosemove=XMOVE (1) means that X chooses the next move, OMOVE (-1) means O
        self.parentNode = None
        self.childNodes = []
        self.utility = NOTDONE
        self.index = TTBoard.numboards
        TTBoard.numboards += 1

    def addchild(self, objin):          # adds a new child board to a node
        self.childNodes.append(objin)

    def dup(self, boardin):             # uses deep copy to duplicate all cell info
        self.cells = copy.deepcopy(boardin.cells)
        self.moves = boardin.moves
        self.whosemove = boardin.whosemove

    def toString(self):                 # represents a board in a compact one-line form
        result = ""
        for spaces in range(self.moves):
            result += "  "
        result += "[["
        for r in range(self.WIDTH):
            for c in range(self.WIDTH):
                if (self.cells[r][c] == XMARK):
                    result += 'X'
                elif (self.cells[r][c] == OMARK):
                    result += 'O'
                else:
                    result += '.'
            if (r < self.WIDTH-1):
                result += "],["
        result += "]]"
        result += (", idx=" + str(self.index))
        result += (", moves=" + str(self.moves))
        result += (", whose=" + str(self.whosemove))
        if (self.parentNode is None):
            result += (", parent=None")
        else:
            result += (", parent=" + str(self.parentNode.index))
        result += (", numchild=" + str(len(self.childNodes)))
        result += (", util=" + str(self.utility))
        return result

    def drawboard(self):                    # draws a board as 3x3
        result = "|"
        for r in range(self.WIDTH):
            for c in range(self.WIDTH):
                if (self.cells[r][c] == XMARK):
                    result += 'x'
                elif (self.cells[r][c] == OMARK):
                    result += 'o'
                else:
                    result += '.'
                result += '|'
            if (r < (self.WIDTH-1)):
                result += '\n|'
        result += '\n'
        return result

    def setCell(self, r, c, v):                 # checks values then sets the cell[r,c] to v
        if ( (r < 0) or (r >= self.WIDTH)):
            return
        if ( (c < 0) or (c >= self.WIDTH)):
            return
        if ( (v != XMARK) and (v != OMARK) and (v != NOMARK)):
            return
        self.cells[r][c] = v
        self.moves += 1

    def moveIsValid(self, r, c):                # doesn't allow moving to invalid cells or to a nonempty cell
        if ( (r < 0) or (r >= self.WIDTH)):
            return False
        if ( (c < 0) or (c >= self.WIDTH)):
            return False
        if (self.cells[r][c] != NOMARK):
            return False
        return True

    def pointmethod(self):              #For incentivised utility function with X winning
        if self.moves == 9:
            self.utility = 1
        if self.moves == 8:
            self.utility = 2
        if self.moves == 7:
            self.utility = 3
        if self.moves == 6:
            self.utility = 4
        if self.moves == 5:
            self.utility = 5
        return self.utility

    def negpointmethod(self):               #For incentivised utility function with O winning
        if self.moves == 9:
            self.utility = -1
        if self.moves == 8:
            self.utility = -2
        if self.moves == 7:
            self.utility = -3
        if self.moves == 6:
            self.utility = -4
        if self.moves == 5:
            self.utility = -5
        return self.utility

    def isWinner(self):                         # if the cell is a winner, return the proper code
        posdiagcount = 0
        negdiagcount = 0
        self.utility = NOTDONE
        if (self.doPointAdj == False):
            for count in range(self.WIDTH):
                if ((sum([col[count] for col in self.cells]) == self.WIDTH) or (sum(self.cells[count]) == self.WIDTH)):
                    self.utility = 1
                    return self.utility
                if ((sum([col[count] for col in self.cells]) == -self.WIDTH) or (
                        sum(self.cells[count]) == -self.WIDTH)):
                    self.utility = -1
                    return self.utility
                posdiagcount += self.cells[count][count]
                negdiagcount += self.cells[count][self.WIDTH - count - 1]
            if ((posdiagcount == self.WIDTH) or (negdiagcount == self.WIDTH)):
                self.utility = 1
            elif ((posdiagcount == -self.WIDTH) or (negdiagcount == -self.WIDTH)):
                self.utility = -1
            elif (self.moves == 9):
                self.utility = DRAW
        else:
            for count in range(self.WIDTH):
                if ((sum([col[count] for col in self.cells]) == self.WIDTH) or (sum(self.cells[count]) == self.WIDTH)):
                    self.pointmethod()
                if ((sum([col[count] for col in self.cells]) == -self.WIDTH) or (sum(self.cells[count]) == -self.WIDTH)):
                    self.negpointmethod()
                posdiagcount += self.cells[count][count]
                negdiagcount += self.cells[count][self.WIDTH - count - 1]
            if ((posdiagcount == self.WIDTH) or (negdiagcount == self.WIDTH)):
                self.pointmethod()
            elif ((posdiagcount == -self.WIDTH) or (negdiagcount == -self.WIDTH)):
                self.negpointmethod()
            elif (self.moves == 9):
                self.utility = DRAW
        return self.utility

    def createchildren(self):                   # creates all possible next moves
        if (self.moves >= 9):
            return
        if (self.whosemove == XMOVE):
            nextmove = OMOVE
        else:
            nextmove = XMOVE

        # now for every possible subsequent move
        for r in range(3):
            for c in range(3):
                if (self.moveIsValid(r, c)):
                    newb = TTBoard(nextmove)
                    newb.dup(self)
                    newb.whosemove = nextmove
                    newb.setCell(r, c, self.whosemove)
                    newb.parentNode = self
                    newb.doPointAdj = self.doPointAdj
                    newb.utility = newb.isWinner()
                    self.addchild(newb)
                    if (newb.utility == NOTDONE):
                        newb.createchildren()

    def maxutilofchildren(self):
        result = -HUGEVAL
        for bd in self.childNodes:
            if (bd.utility > result):
                result = bd.utility
        return result

    def abmaxutilofchildren(self,alpha,beta):              #Maximazing using A-B pruning
        result = -HUGEVAL
        for bd in self.childNodes:
            if (bd.utility > result):
                result = bd.utility
                alpha = bd.utility

            if alpha < beta:
                TTBoard.numsearched += 1
                beta = alpha
            else:
                return NOTDONE              #Returns NOTEDONE/-100 when pruned
        return alpha

    def minutilofchildren(self):
        result = HUGEVAL
        for bd in self.childNodes:
            if (bd.utility < result):
                result = bd.utility
        return result

    def abminutilofchildren(self,alpha,beta):              #Minimizing using A-B pruning
        result = HUGEVAL
        for bd in self.childNodes:
            if (bd.utility < result):
                beta = bd.utility

            if beta > alpha:
                TTBoard.numsearched += 1
                alpha = beta
            else:
                return NOTDONE              #Returns NOTEDONE/-100 when pruned
        return beta

    def minimax(self):
        # we move down from the root until we find a node whose children all have defined utility
        for bd in self.childNodes:
            TTBoard.numsearched += 1
            if (bd.utility < -5):
                bd.minimax()
        if (self.whosemove == XMOVE):  # if it's an X move
            self.utility = self.maxutilofchildren()
        else:
            self.utility = self.minutilofchildren()
        return

    def alphabeta(self):                        #Funcition for A-B pruning
        alpha = -HUGEVAL
        beta = HUGEVAL
        for bd in self.childNodes:
            if (bd.utility < -5):
                bd.alphabeta()
        if (self.whosemove == XMOVE):  # if it's an X move
            self.utility = self.abmaxutilofchildren(alpha,beta)
        else:
            self.utility = self.abminutilofchildren(alpha,beta)
        return

    def __writeonelevel(self, file, depth):
        if (depth == 0):
            return
        for bd in self.childNodes:
            file.write(bd.toString() + "\n")
            bd.__writeonelevel(file, depth - 1)

    def treetofile(self, depth=3):
        logfile = open('C:/Users/Yogesh/PycharmProjects/pythonProject/treefile.txt', 'w')
        logfile.write(self.toString() + "\n")
        self.__writeonelevel(logfile, depth)
        logfile.close()

import TTBoard

def main():
    # create an empty board
    # this is the root of the tree
    doPointAdj = True
    doAlphaBeta = True
    TTBoard.TTBoard.numboards = 0
    TTBoard.TTBoard.numsearched = 0
    bd = TTBoard.TTBoard(TTBoard.XMOVE, pointAdj=doPointAdj)
    # create a board for every possible initial X move
    bd.createchildren()
    if (doAlphaBeta):
        bd.alphabeta()
    else:
        bd.minimax()
    bd.treetofile(depth=9)
    print('There are ', str(bd.numboards), ' boards; there were ', str(bd.numsearched), ' searched')

if __name__ == "__main__":
    main()
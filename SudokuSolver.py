import Tkinter as tk
from copy import copy,deepcopy

        

def keyPressed(event,data):
    row,col = data.row,data.col
    if data.isInHelp:
        data.isInHelp = False
    elif event.char == "h":
        data.isInHelp = True
    elif event.char == "r":
        resetSolver(data)
    elif event.char == "s":
        solvePuzzle(data)
    elif event.char in "123456789":
        placeNum(data,event.char,row,col)
    elif event.keysym == "BackSpace":
        deleteNumInCell(data)

def mousePressed(event,data):
    x,y = event.x, event.y
    row,col = -1,-1
    if (30 <= y <= 570 and 30 <= x <= 570):
        row = (y - 30)/60
        col = (x - 30)/60

    # if (row,col) == (data.row,data.col):
    #     data.row,data.col = -1,-1
    # elif (data.grid[row][col] == 0):
    
    data.row,data.col = row,col
    
    

def drawPlayerLoc(canvas,data):
    if data.row >= 0 and data.col >= 0 :
        x0 = 30 + data.col * 60 + 1
        y0 = 30 + data.row * 60 + 1
        x1 = 30 + (data.col + 1) * 60 - 1
        y1 = 30 + (data.row + 1) * 60 - 1
        canvas.create_rectangle(x0,y0,x1,y1,outline = "red")

def redrawAll(canvas,data):
    if data.isInHelp:
        return drawHelpScreen(canvas,data)
    canvas.create_rectangle(0,0,data.width,data.height,fill = "white")
    generateGrid(canvas,data)
    drawPlayerLoc(canvas,data)
    drawNumbers(canvas,data)
    if checkSolved(data):
        canvas.create_text(300,15,text = "This is the solution",font = "Tisa 25 bold")
    if not isSolvable(data) :
        canvas.create_text(300,15,text = "This board is unsolvable or incorrect.",font = "Tisa 20 bold")

    
    
def generateGrid(canvas,data):
    for i in range (10):
            color = "blue" if i % 3 == 0 else "gray"
            canvas.create_line(30 + 60 * i,30,30 + 60 * i,570,fill = color)
            canvas.create_line(30,30 + 60 * i ,570,30 + 60 * i,fill = color)


def drawHelpScreen(canvas,data):
    font = "Tisa 32 bold"
    title = canvas.create_text(300,50, text = "Sudoku Solver", font = font)
    font = "Tisa 20 bold"
    name = canvas.create_text(300,80, text= "By Yousef Hassen", font=font)

    messages = ["mouse to click into cells",
                "enter numbers 1-9 in the board",
                "r to reset solver",
                "s to find solution(if possible)",
                "h to go back to this screen",
                "press any key to continue"]
    
    for i in range(len(messages)):
        canvas.create_text(300,150 + 50*i,text = messages[i], font = font)

def drawNumbers(canvas,data):
    for row in range(9):
        for col in range(9):
            if data.grid[row][col] != 0:
                canvas.create_text(30 + 60 * col + 15,30 + 60 * row+ 15,text = str(data.grid[row][col]))


def findNextCell(data):
    for row in range(len(data.grid)):
        for col in range(len(data.grid[0])):
            if data.grid[row][col] == 0:
                return row,col
    
    return -1,-1


def isSolvable(data):
    gridDup0 = deepcopy(data.grid)
    gridDup1 = deepcopy(data.grid)
    
    for i in range(9):
        gridDup0[i] = [x for x in gridDup0[i] if x != 0]
        if len(set(gridDup0[i])) != len(gridDup0[i]) - gridDup0[i].count(0):
            return False
    
    for i in range(9):
        temp = [gridDup1[row][i] for row in range(9)]
        temp = [x for x in temp if x != 0]
        if len(set(temp)) != len(temp) - temp.count(0):
            return False
        
    for i in range(3):
        for j in range(3):
            temp = [gridDup1[row][col] for row in range(i * 3, (i + 1) * 3)
                                       for col in range(j * 3,(j+1) * 3)]
            temp = [x for x in temp if x != 0]
            if len(set(temp)) != len(temp) - temp.count(0):
                return False

    
    return True 

def possiblePlace(data,num,row,col):
    for i in range (len(data.grid[row])):
        if data.grid[row][i] == num and col != i:
            return False
    
    for i in range (len(data.grid)):
        if data.grid[i][col] == num and row != i:
            return False
    
    rowBox = row // 3
    colBox = col // 3

    for i in range(rowBox *3, (rowBox + 1) * 3):
        for j in range(colBox *3, (colBox + 1) * 3):
            if data.grid[i][j] == num and i != row and j != col:
                return False

    return True 

def checkSolved(data):
    for i in range (9):
        if set(range(1,10)) != set(data.grid[i]):
            return False
    
    for i in range (9):
        if set(range(1,10)) != set([data.grid[row][i] for row in range(9)]):
            return False
    
    for i in range (3):
        for j in range (3):
            if set(range(1,10)) != set([data.grid[row][col] 
                                        for row in range(i * 3, (i + 1) * 3)
                                        for col in range(j * 3,(j+1) * 3)]):
                return False
    
    return True




def solvePuzzle(data):
    if not isSolvable(data):
        return False
    
    row,col = findNextCell(data)
    if row == -1:
        return checkSolved(data)

    for num in range(1,10):
        if possiblePlace(data,num,row,col):
            data.grid[row][col] = num
        
            if solvePuzzle(data):
                return True
            
            data.grid[row][col] = 0
    
    return False


    
def placeNum(data,char,row,col):
    if row >= 0 and col >=0 and char in "123456789":
        data.grid[row][col] = int(char)


def deleteNumInCell(data):
    if data.row >= 0 and data.col >= 0 and data.grid[data.row][data.col] != 0:
        data.grid[data.row][data.col] = 0
    


def resetSolver(data):
    data.grid = [[0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0]]
    data.isInHelp = False
    data.row,data.col = -1,-1



def init(data):
    data.grid = [[0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0]]
    data.isInHelp = True
    data.row,data.col = -1,-1



def run(width = 300, height = 300):
    
    def redrawAllWrapper(canvas,data):
        canvas.delete("All")
        canvas.create_rectangle(0,0,data.width,data.height,fill = "white",width = 0)

        redrawAll(canvas,data)
        canvas.update()

    def mousePressedWrapper(event,canvas,data):
        mousePressed(event,data)
        redrawAllWrapper(canvas,data)
    
    def keyPressedWrapper(event,canvas,data):
        keyPressed(event,data)
        redrawAllWrapper(canvas,data)


    root = tk.Tk()
    canvas = tk.Canvas(root, width = width, height = height)
    canvas.pack()
    
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    init(data)
    
    
    root.bind("<Button-1>",lambda event : mousePressedWrapper(event,canvas,data))
    root.bind("<Key>", lambda event : keyPressedWrapper(event,canvas,data))
    
    root.mainloop()

run(600,600)
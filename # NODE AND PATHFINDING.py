# NODE AND PATHFINDING
import sys
import math
import random
from typing import Sized
import pygame
import numpy as NP
from pygame.constants import HAT_RIGHT, KEYDOWN, K_1, K_2, K_RETURN, K_a, K_c, K_d, K_e, K_f, K_k, K_l, K_m, K_r, K_s, K_w, SCALED
from collections import deque
pygame.init()
pygame.display.set_caption("Pathfinding Visualizer")
sys.setrecursionlimit(10**6)

#///COLOR//////////////////////////////////////////////////////////////
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
orange = (255,128,0)
black = (0,0,0)
purple = (127,0,255)
grey = (100,100,100)
yellow = (255,255,0)
brown = (160,82,45)
saddlebrown = (139,69,19)
DarkBlue = (0,51,102)
DarkGreen = (0,102,0)
pink = (255,0,255)
#///COLOR//////////////////////////////////////////////////////////////

font1 = pygame.font.Font('AllTheWayToTheSun-o2O0.ttf',15)
def AddText(name,size,color,x,y):
    font = pygame.font.Font('AllTheWayToTheSun-o2O0.ttf',size)
    text = font.render(name,True,color)
    screen.blit(text,(x,y))

ScreenWidth = 2000

ScreenHeight = 1200
screen = pygame.display.set_mode((ScreenWidth,ScreenHeight))

def UpdateScreen():
    pygame.display.update()

def ClearScreen(color):
    DrawRect(color,0,0,ScreenWidth,ScreenHeight)

def GetPressKey():
    return pygame.key.get_pressed()

def GetMousePosition():
    return pygame.mouse.get_pos()

def GetClickState():
    return pygame.mouse.get_pressed()

def Switch(num):
    if num == 0:
        return 1
    else: # num  == 1
        return 0

def Switch_1_2_(num):
    if num == 2:
        return 1
    else: # num  == 1
        return 2

def DrawRect(color,X,Y,W,H):
    pygame.draw.rect(screen,color,[X,Y,W,H])

def DrawLine(color,X1,Y1,X2,Y2,Thickness):
    pygame.draw.line(screen,color,(X1,Y1),(X2,Y2),Thickness)

def DrawButton(X,Y,W,H):
    DrawRect(black,X + 3,Y + 3,W + 3,H + 3)
    DrawRect(white,X,Y,W,H)
    DrawRect(DarkBlue,X + 2,Y + 2,W - 4,H - 4)

def GetTravelCost(TileType):
    if TileType == 2:
        return 1
    elif TileType == 1:
        return 1

def DrawSelectPointer(color,X,Y):
    pygame.draw.polygon(screen,color,[(X,Y),(X - 15,Y - 10),(X - 15,Y + 10)])

def IsInRect(X,Y,W,H,MX,MY):
    return X <= MX and X + W >= MX and Y <= MY and Y + H >= MY

def IsInCoordinateRect(X1,Y1,X2,Y2,OX,OY):
    if X1 > X2:
        LX = X2
        HX = X1
    else:
        LX = X1
        HX = X2
    if Y1 > Y2:
        LY = Y2
        HY = Y1
    else:
        LY = Y1
        HY = Y2 
    return LX <= OX and HX >= OX and LY <= OY and HY >= OY

def DistancePointToLine(OX,OY,VarX,VarY,VarC):
    return float(abs(VarX * OX + VarY * OY + VarC))/math.sqrt(math.pow(VarX,2) + math.pow(VarY,2))

def RandomODD(n):
    k = random.randint(1,n)
    while k % 2 == 0:
        k = random.randint(1,n)
    return k

def ReturnFadeColor1(Value):
    tmp1 = Value
    tmp2 = Value
    if Value >= 20:
        tmp2 = 20
    if Value >= 135:
        tmp1 = 135
    basecolor = (120 + tmp1,0,120 + tmp2)
    return basecolor

def RedFade(Value):
    if Value > 180:
        Value = Value % 180
    if (Value >= 0 and Value <= 30) or (Value >= 150 and Value <= 180):
        return 255
    elif (Value >= 60 and Value <= 120):
        return 0
    elif (Value >= 30 and Value <= 60):
        return math.floor((-255) * Value/30) + 510
    elif (Value >= 120 and Value <= 150):
        return math.floor((255) * Value/30) - 1020

def GreenFade(Value):
    if Value > 180:
        Value = Value % 180
    if (Value >= 30 and Value <= 90):
        return 255
    elif (Value >= 120 and Value <= 180):
        return 0
    elif (Value >= 90 and Value <= 120):
        return math.floor((-255) * Value/30) + 1020
    elif (Value >= 0 and Value <= 30):
        return math.floor((255) * Value/30)



def BlueFade(Value):
    if Value > 180:
        Value = Value % 180
    if (Value >= 90 and Value <= 150):
        return 255
    elif (Value >= 0 and Value <= 60):
        return 0
    elif (Value >= 150 and Value <= 180):
        return math.floor((-255) * Value/30) + 1530
    elif (Value >= 60 and Value <= 90):
        return math.floor((255) * Value/30) - 510





def ReturnFadeColor(Value):
    if Value < 0:
        if abs(Value) > 180:
            Value = -(abs(Value) % 180)
        Value = 180 + Value
    if Value > 180:
        Value = Value % 180
    return (RedFade(Value),GreenFade(Value),BlueFade(Value))


def ManhattanDistance(X1,Y1,X2,Y2):
    return abs(X1 - X2) + abs(Y1 - Y2)

def ConsiderThisTile(X,Y,Xcon,Ycon):
    if Xcon == -1 and Ycon == -1:
        return True
    else:
        return X == Xcon and Y == Ycon

def ReturnSlope(X1,Y1,X2,Y2): # x1 - x2 = 0 dont use this func
    return float((Y2 - Y1)/(X2 - X1))












    
    

PuaseAnimation = False
ShowGrid = True

# Set Data structure for my grid
Width_Grid = 40 # width grid were use at 0 to 29
Height_Grid = 20 # height grid were use at 0 to 29
TileState = NP.empty([Height_Grid,Width_Grid])
TileVisit = NP.empty([Height_Grid,Width_Grid])
TileWeight = NP.empty([Height_Grid,Width_Grid])
TileConsider = NP.empty([Height_Grid,Width_Grid])
TileIsShortestPath = NP.empty([Height_Grid,Width_Grid])
TileAlreadySelectShortestPath = NP.empty([Height_Grid,Width_Grid])
TileFillNext = NP.empty([Height_Grid,Width_Grid])
TileDirection = NP.empty([Height_Grid,Width_Grid])

for Y in range(0,Height_Grid):
    for X in range(0,Width_Grid):
        TileState[Y][X] = 2 # walkable tile
        TileVisit[Y][X] = 0
        TileWeight[Y][X] = -1 # -1 as inf
        TileConsider[Y][X] = 0
        TileIsShortestPath[Y][X] = 0
        TileAlreadySelectShortestPath[Y][X] = 0
        TileFillNext[Y][X] = 0
        TileDirection[Y][X] = 0

X1pos = -1
Y1pos = -1
X2pos = -1
Y2pos = -1

Var_Y = -1
Var_X = -1
Var_C = -1

LowestPriority = -1
LowestDistanceFromEnd = -1
X_consider = -1
Y_consider = -1

Start_PathFinding = True
PathNotExist = False
PathFound = False
X_start = -1
Y_start = -1
X_end = -1
Y_end = -1

def GetNeightbor(Xgrid,Ygrid):
    Result = []
    if Xgrid + 1 < Width_Grid:
        Result.append((Xgrid + 1,Ygrid))
    if Xgrid - 1 >= 0:
        Result.append((Xgrid - 1,Ygrid))
    if Ygrid + 1 < Height_Grid:
        Result.append((Xgrid,Ygrid + 1))
    if Ygrid - 1 >= 0:
        Result.append((Xgrid,Ygrid - 1))
    return Result

def MazeGetNextPath(Xgrid,Ygrid):
    Result = []
    if Xgrid + 2 < Width_Grid and TileState[Ygrid][Xgrid + 2] == 2:
        Result.append("+x")
    if Xgrid - 2 >= 0 and TileState[Ygrid][Xgrid - 2] == 2:
        Result.append("-x")
    if Ygrid + 2 < Height_Grid and TileState[Ygrid + 2][Xgrid] == 2:
        Result.append("+y")
    if Ygrid - 2 >= 0 and TileState[Ygrid - 2][Xgrid] == 2:
        Result.append("-y")
    return Result


timer = 1

User_ResetTileData = False
UpdateTile = False
invalid_sample = False

User_AddStartTile = True
User_AddEndTile = False
User_AddWalkTile = False
User_AddObstacleTile = False

User_EditTile = "SingleTile"
SetLine_initial = False
Setline_MouseRelease = True

Fill_initial = False
Fill_Finish = False
TileToFill = -1

User_ClearGrid = False
X_SetLine,Y_SetLine = -1,-1
X_SetLineEnd,Y_SetLineEnd = -1,-1
X_MouseOnTile,Y_MouseOnTile = -1,-1

DistanceStartToEnd = -1
Algorithm = "DIJKSTRA"
AddWeight = -1
AddWeight2 = -1
GenerateMaze = False
StopGenerateMaze = False
FillWithWall = False
WeightCorrection = False

ClickCoolDown = 0
ClickAllowTime = 4
AnimationDelay = 1

TileQueue = deque()
          


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = GetPressKey()
    mx ,my = GetMousePosition()
    Coordinate_mouse = NP.array([mx,my])
    click = GetClickState()
    ClearScreen(DarkBlue)

    DrawButton(1570,50,120,40)
    AddText("delay  :",20,yellow,1580,60)
    AddText(str(AnimationDelay),20,yellow,1650,60)

    DrawButton(1700,50,30,30)
    AddText("+",20,yellow,1710,55)
    if IsInRect(1700,50,30,30,mx,my) and click[0] == 1 and ClickCoolDown >= ClickAllowTime:
        ClickCoolDown = 0
        AnimationDelay += 1


    DrawButton(1740,50,30,30)
    AddText("-",20,yellow,1750,55)
    if IsInRect(1740,50,30,30,mx,my) and click[0] == 1 and ClickCoolDown >= ClickAllowTime:
        ClickCoolDown = 0
        AnimationDelay -= 1
        if AnimationDelay == 0:
            AnimationDelay += 1

    if PuaseAnimation:
        DrawSelectPointer(green,1580,140)
    DrawButton(1590,120,70,40)
    AddText("Puase",20,yellow,1600,130)
    if IsInRect(1590,120,70,40,mx,my) and click[0] == 1 and ClickCoolDown >= ClickAllowTime:
        ClickCoolDown = 0
        PuaseAnimation = not PuaseAnimation

    if ShowGrid:
        DrawSelectPointer(green,1690,140)
    DrawButton(1700,120,110,40)
    AddText("Show Grid",20,yellow,1710,130)
    if IsInRect(1700,120,110,40,mx,my) and click[0] == 1 and ClickCoolDown >= ClickAllowTime:
        ClickCoolDown = 0
        ShowGrid = not ShowGrid




    ###############################################################

    AddText("generate",30,yellow,20,220)

    DrawButton(20,270,150,40)
    AddText("maze",20,yellow,30,280)
    if IsInRect(20,270,150,40,mx,my) and click[0] == 1 and ClickCoolDown > ClickAllowTime:
        ClickCoolDown = 0
        GenerateMaze = True
        StopGenerateMaze = False
        User_ClearGrid = True
        FillWithWall = True

















































    AddText("ADD TILE",30,yellow,50,10)

    if User_AddStartTile:
        DrawSelectPointer(green,40,70)
    if User_EditTile == "Fill" or User_EditTile == "SetLine":
        AddText("Cannot place this tile",15,red,70,100)
    DrawButton(50,50,160,40)
    DrawRect(red,60,57,25,25)
    AddText("Start Tile",20,yellow,90,60)
    if IsInRect(50,50,160,40,mx,my) and click[0] == 1 and ClickCoolDown > ClickAllowTime:
        ClickCoolDown = 0
        User_AddStartTile = True
        User_AddEndTile = False
        User_AddWalkTile = False
        User_AddObstacleTile = False

    if User_AddEndTile:
        DrawSelectPointer(green,40,140)
    if User_EditTile == "Fill" or User_EditTile == "SetLine":
        AddText("Cannot place this tile",15,red,70,170)
    DrawButton(50,120,160,40)
    DrawRect(blue,60,127,25,25)
    AddText("End Tile",20,yellow,90,130)
    if IsInRect(50,120,160,40,mx,my) and click[0] == 1 and ClickCoolDown > ClickAllowTime:
        ClickCoolDown = 0
        User_AddStartTile = False
        User_AddEndTile = True
        User_AddWalkTile = False
        User_AddObstacleTile = False

    if User_AddWalkTile:
        DrawSelectPointer(green,240,70)
    DrawButton(250,50,160,40)
    DrawRect(white,260,57,25,25)
    AddText("Walk Tile",20,yellow,290,60)
    if IsInRect(250,50,160,40,mx,my) and click[0] == 1 and ClickCoolDown > ClickAllowTime:
        ClickCoolDown = 0
        User_AddStartTile = False
        User_AddEndTile = False
        User_AddWalkTile = True
        User_AddObstacleTile = False

    if User_AddObstacleTile:
        DrawSelectPointer(green,240,140)
    DrawButton(250,120,160,40)
    DrawRect(black,260,127,25,25)
    AddText("Obstacle Tile",20,yellow,290,130)
    if IsInRect(250,120,160,40,mx,my) and click[0] == 1 and ClickCoolDown > ClickAllowTime:
        ClickCoolDown = 0
        User_AddStartTile = False
        User_AddEndTile = False
        User_AddWalkTile = False
        User_AddObstacleTile = True





    DrawLine(white,450,0,450,200,5)############################################################################################

    AddText("EDIT",30,yellow,500,10)

    if User_EditTile == "SingleTile":
        DrawSelectPointer(green,490,70)
    DrawButton(500,50,160,40)
    AddText("edit single tile",20,yellow,510,60)
    if IsInRect(500,50,160,40,mx,my) and click[0] == 1 and ClickCoolDown > ClickAllowTime:
        ClickCoolDown = 0
        User_EditTile = "SingleTile"

    if User_EditTile == "SetLine":
        DrawSelectPointer(green,490,140)
    DrawButton(500,120,160,40)
    AddText("SetLine",20,yellow,510,130)
    if IsInRect(500,120,160,40,mx,my) and click[0] == 1 and ClickCoolDown > ClickAllowTime:
        ClickCoolDown = 0
        User_EditTile = "SetLine"

    if User_EditTile == "Fill":
        DrawSelectPointer(green,690,70)
    DrawButton(700,50,160,40)
    AddText("Fill",20,yellow,710,60)
    if IsInRect(700,50,160,40,mx,my) and click[0] == 1 and ClickCoolDown > ClickAllowTime:
        ClickCoolDown = 0
        User_EditTile = "Fill"

    DrawButton(700,120,160,40)
    AddText("clear grid",20,yellow,710,130)
    if IsInRect(700,120,160,40,mx,my) and click[0] == 1 and ClickCoolDown > ClickAllowTime:
        ClickCoolDown = 0
        User_ClearGrid = True

    DrawLine(white,900,0,900,200,5)#######################################################################################

    AddText("ALGORITHM",30,yellow,950,10)



    DrawButton(950,50,160,40)
    if Algorithm == "DIJKSTRA":
        DrawSelectPointer(green,940,70)
    AddText("DIJKSTRA",20,yellow,960,60)
    if IsInRect(950,50,160,40,mx,my) and click[0] == 1 and ClickCoolDown >= ClickAllowTime and not Start_PathFinding:
        Algorithm = "DIJKSTRA"

    if Algorithm == "A*_SEARCH":
        DrawSelectPointer(green,940,140)
    DrawButton(950,120,160,40)
    AddText("a* search",20,yellow,960,130)
    if IsInRect(950,120,160,40,mx,my) and click[0] == 1 and ClickCoolDown >= ClickAllowTime and not Start_PathFinding:
        Algorithm = "A*_SEARCH"

    if Algorithm == "DEPTH_FIRST_SEARCH":
        DrawSelectPointer(green,1140,70)
    DrawButton(1150,50,160,40)
    AddText("DFS",20,yellow,1160,60)
    if IsInRect(1150,50,160,40,mx,my) and click[0] == 1 and ClickCoolDown >= ClickAllowTime and not Start_PathFinding:
        Algorithm = "DEPTH_FIRST_SEARCH"

    if Algorithm == "BREADTH_FIRST_SEARCH":
        DrawSelectPointer(green,1140,140)
    DrawButton(1150,120,160,40)
    AddText("BFS",20,yellow,1160,130)
    if IsInRect(1150,120,160,40,mx,my) and click[0] == 1 and ClickCoolDown >= ClickAllowTime and not Start_PathFinding:
        Algorithm = "BREADTH_FIRST_SEARCH"

    if Algorithm == "BIDIRECTIONAL":
        DrawSelectPointer(green,1340,70)
    DrawButton(1350,50,160,40)
    AddText("BIDIRECTIONAL",20,yellow,1360,60)
    if IsInRect(1350,50,160,40,mx,my) and click[0] == 1 and ClickCoolDown >= ClickAllowTime and not Start_PathFinding:
        Algorithm = "BIDIRECTIONAL"

    DrawLine(white,1550,0,1550,200,5)

    # FUTURE ALGORITHM
    # if Algorithm == "B":
    #     DrawSelectPointer(green,1340,140)
    # DrawButton(1350,120,160,40)
    # AddText("B",20,yellow,1360,130)
    # if IsInRect(1350,120,160,40,mx,my) and click[0] == 1 and ClickCoolDown >= ClickAllowTime and not Start_PathFinding:
    #     Algorithm = "B"

    # DrawLine(white,1550,0,1550,200,5)#######################################################################################
    # FUTURE ALGORITHM

    DrawButton(1800,50,150,40)
    AddText("Reset Animation",20,yellow,1810,60)
    if IsInRect(1800,50,150,40,mx,my) and click[0] == 1 and ClickCoolDown > ClickAllowTime:
        ClickCoolDown = 0
        Start_PathFinding = 0
        User_ResetTileData = True

    DrawButton(1850,120,100,40)
    AddText("Find path",20,yellow,1860,130)
    if IsInRect(1850,120,100,40,mx,my) and click[0] == 1 and ClickCoolDown > ClickAllowTime:
        if (X_start,Y_start) != (-1,-1) and (X_end,Y_end) != (-1,-1):
            DistanceStartToEnd = ManhattanDistance(X_start,Y_start,X_end,Y_end)
            ClickCoolDown = 0
            invalid_sample = False
            User_ResetTileData = True
            Start_PathFinding = True
            TileQueue = deque()
            TileQueue.append((X_start,Y_start))
        else:
            invalid_sample = True
    
    if invalid_sample:
        AddText("start or end tile doesn't exist",15,red,1780,170)

    if IsInRect(200,300,ScreenWidth - 400,ScreenHeight - 400,mx,my):
        X_MouseOnTile,Y_MouseOnTile = math.floor((mx - 200)/40),math.floor((my - 300)/40)
    else:
        X_MouseOnTile,Y_MouseOnTile = -1,-1

    if IsInRect(200,300,ScreenWidth - 400,ScreenHeight - 400,mx,my) and click[0] == 1 and ClickCoolDown > ClickAllowTime:
        #print("click")
        X_TileToEdit,Y_TileToEdit = X_MouseOnTile,Y_MouseOnTile
        if User_EditTile == "SetLine":
            if (X_SetLine,Y_SetLine) == (-1,-1):
                X_SetLine,Y_SetLine = X_TileToEdit,Y_TileToEdit
                SetLine_initial = True
                Setline_MouseRelease = False
            else:
                X_SetLineEnd,Y_SetLineEnd = X_TileToEdit,Y_TileToEdit
        if User_EditTile == "Fill":
            ClickCoolDown = 0
            TileFillNext[Y_TileToEdit][X_TileToEdit] = 1
            TileToFill = TileState[Y_TileToEdit][X_TileToEdit]
            Fill_initial = True
            Fill_Finish = False
            if User_AddWalkTile:
                if TileToFill == 2:
                    Fill_initial = False
            if User_AddObstacleTile:
                if TileToFill == 3:
                    Fill_initial = False
        if PathFound or Start_PathFinding or PathNotExist:
            User_ResetTileData = True
        Start_PathFinding = False
    else:
        #print("notclick")
        Setline_MouseRelease = True
        X_TileToEdit,Y_TileToEdit = -1,-1
        if not SetLine_initial and Setline_MouseRelease: # F and T will reset
            X_SetLine,Y_SetLine = -1,-1
            X_SetLineEnd,Y_SetLineEnd = -1,-1

        

    if X_TileToEdit != -1 and Y_TileToEdit != -1 and User_EditTile == "SingleTile":
        if User_AddWalkTile:
            if X_start == X_TileToEdit and Y_start == Y_TileToEdit:
                X_start,Y_start = -1,-1
            if X_end == X_TileToEdit and Y_end == Y_TileToEdit:
                X_end,Y_end = -1,-1

            TileState[Y_TileToEdit][X_TileToEdit] = 2
            TileConsider[Y_TileToEdit][X_TileToEdit] = 0
            TileAlreadySelectShortestPath[Y_TileToEdit][X_TileToEdit] = 0
            TileIsShortestPath[Y_TileToEdit][X_TileToEdit] = 0
            TileWeight[Y_TileToEdit][X_TileToEdit] = -1
            TileVisit[Y_TileToEdit][X_TileToEdit] = 0
        elif User_AddObstacleTile:

            if X_start == X_TileToEdit and Y_start == Y_TileToEdit:
                X_start,Y_start = -1,-1
            if X_end == X_TileToEdit and Y_end == Y_TileToEdit:
                X_end,Y_end = -1,-1

            TileState[Y_TileToEdit][X_TileToEdit] = 3
            TileConsider[Y_TileToEdit][X_TileToEdit] = 0
            TileAlreadySelectShortestPath[Y_TileToEdit][X_TileToEdit] = 0
            TileIsShortestPath[Y_TileToEdit][X_TileToEdit] = 0
            TileWeight[Y_TileToEdit][X_TileToEdit] = -1
            TileVisit[Y_TileToEdit][X_TileToEdit] = 0
        elif User_AddStartTile:

            if X_end == X_TileToEdit and Y_end == Y_TileToEdit:
                X_end,Y_end = -1,-1

            TileState[Y_start][X_start] = 2
            TileConsider[Y_start][X_start] = 0
            TileAlreadySelectShortestPath[Y_start][X_start] = 0
            TileIsShortestPath[Y_start][X_start] = 0
            TileWeight[Y_start][X_start] = -1
            TileVisit[Y_start][X_start] = 0

            TileState[Y_TileToEdit][X_TileToEdit] = 0
            TileConsider[Y_TileToEdit][X_TileToEdit] = 1
            TileAlreadySelectShortestPath[Y_TileToEdit][X_TileToEdit] = 0
            TileIsShortestPath[Y_TileToEdit][X_TileToEdit] = 0
            TileWeight[Y_TileToEdit][X_TileToEdit] = 0
            TileVisit[Y_TileToEdit][X_TileToEdit] = 0
            X_start,Y_start = X_TileToEdit,Y_TileToEdit
        elif User_AddEndTile:

            if X_start == X_TileToEdit and Y_start == Y_TileToEdit:
                X_start,Y_start = -1,-1

            TileState[Y_end][X_end] = 2
            TileConsider[Y_end][X_end] = 0
            TileAlreadySelectShortestPath[Y_end][X_end] = 0
            TileIsShortestPath[Y_end][X_end] = 0
            TileWeight[Y_end][X_end] = -1
            TileVisit[Y_end][X_end] = 0

            TileState[Y_TileToEdit][X_TileToEdit] = 1
            TileConsider[Y_TileToEdit][X_TileToEdit] = 0
            TileAlreadySelectShortestPath[Y_TileToEdit][X_TileToEdit] = 0
            TileIsShortestPath[Y_TileToEdit][X_TileToEdit] = 1
            TileWeight[Y_TileToEdit][X_TileToEdit] = -1
            TileVisit[Y_TileToEdit][X_TileToEdit] = 0
            X_end,Y_end = X_TileToEdit,Y_TileToEdit

    if User_EditTile == "Fill" and Fill_initial:
        Fill_Finish = True
        User_ResetTileData = True
        for Y in range(0,Height_Grid):
            if User_AddStartTile or User_AddEndTile:
                break
            for X in range(0,Width_Grid):
                if TileFillNext[Y][X] == 1:
                    Fill_Finish = False
                    TileFillNext[Y][X] = 0
                    NB = GetNeightbor(X,Y)
                    for i in NB:
                        xNB,yNB = i
                        if TileState[yNB][xNB] == TileToFill:
                            TileFillNext[yNB][xNB] = 1
                    if X_start == X and Y_start == Y:
                        X_start,Y_start = -1,-1
                    elif X_end == X and Y_end == Y:
                        X_end,Y_end = -1,-1
                    if User_AddWalkTile:
                        TileState[Y][X] = 2
                    elif User_AddObstacleTile:
                        TileState[Y][X] = 3
                else:
                    continue
        

    if Fill_Finish:
        Fill_initial = False
        Fill_Finish = False

    if User_EditTile == "SetLine":
        X1pos = float(X_SetLine)
        Y1pos = float(Y_SetLine)
        X2pos = float(X_SetLineEnd)
        Y2pos = float(Y_SetLineEnd)
        if X_SetLine - X_SetLineEnd == 0:
            Var_Y = float(0)
            Var_X = float(-1)
            Var_C = X1pos
        else:
            Var_Y = float(-1)
            Var_X = ReturnSlope(X_SetLine,Y_SetLine,X_SetLineEnd,Y_SetLineEnd)
            Var_C = -Var_X * X1pos + Y1pos

    if User_EditTile == "SetLine" and SetLine_initial and Setline_MouseRelease and (X_SetLineEnd,Y_SetLineEnd) != (-1,-1):
    

        for Y in range(0,Height_Grid):
            if User_AddStartTile or User_AddEndTile:
                break
            for X in range(0,Width_Grid):
                if IsInCoordinateRect(X_SetLine,Y_SetLine,X_SetLineEnd,Y_SetLineEnd,X,Y):
                    if DistancePointToLine(float(X),float(Y),Var_X,Var_Y,Var_C) <= 0.5:
                        if User_AddWalkTile:
                            if X_start == X and Y_start == Y:
                                X_start,Y_start = -1,-1
                            if X_end == X and Y_end == Y:
                                X_end,Y_end = -1,-1

                            TileState[Y][X] = 2
                            TileConsider[Y][X] = 0
                            TileAlreadySelectShortestPath[Y][X] = 0
                            TileIsShortestPath[Y][X] = 0
                            TileWeight[Y][X] = -1
                            TileVisit[Y][X] = 0
                        elif User_AddObstacleTile:

                            if X_start == X and Y_start == Y:
                                X_start,Y_start = -1,-1
                            if X_end == X and Y_end == Y:
                                X_end,Y_end = -1,-1

                            TileState[Y][X] = 3
                            TileConsider[Y][X] = 0
                            TileAlreadySelectShortestPath[Y][X] = 0
                            TileIsShortestPath[Y][X] = 0
                            TileWeight[Y][X] = -1
                            TileVisit[Y][X] = 0
                        
                else:
                    continue

        SetLine_initial = False
        Setline_MouseRelease = True

    if User_ClearGrid:
        User_ResetTileData = True
        for Y in range(0,Height_Grid): 
            for X in range(0,Width_Grid):
                if FillWithWall:
                    TileState[Y][X] = 3
                else:
                    TileState[Y][X] = 2
        if FillWithWall and GenerateMaze:
            TileState[RandomODD(19)][RandomODD(39)] = 2
        FillWithWall = False
        User_ClearGrid = False
        Start_PathFinding = False









    DrawLine(white,0,200,ScreenWidth,200,4)

    

    DrawRect(DarkGreen,200,300,ScreenWidth - 400,ScreenHeight - 400)

    if User_ResetTileData: ##############################################################
        for Y in range(0,Height_Grid):
            for X in range(0,Width_Grid):
                

                if TileState[Y][X] == 2: # walk tile
                    
                    TileDirection[Y][X] = 0
                    TileConsider[Y][X] = 0
                    TileAlreadySelectShortestPath[Y][X] = 0
                    TileIsShortestPath[Y][X] = 0
                    TileWeight[Y][X] = -1
                    TileVisit[Y][X] = 0

                elif TileState[Y][X] == 3: # obstacle tile

                    TileDirection[Y][X] = 0
                    TileConsider[Y][X] = 0
                    TileAlreadySelectShortestPath[Y][X] = 0
                    TileIsShortestPath[Y][X] = 0
                    TileWeight[Y][X] = -1
                    TileVisit[Y][X] = 0

                elif TileState[Y][X] == 0: # start

                    TileDirection[Y][X] = 1
                    TileConsider[Y][X] = 1
                    TileAlreadySelectShortestPath[Y][X] = 0
                    TileIsShortestPath[Y][X] = 0
                    TileWeight[Y][X] = 0
                    TileVisit[Y][X] = 0

                elif TileState[Y][X] == 1: # end

                    if Algorithm == "BIDIRECTIONAL":
                        TileDirection[Y][X] = 2
                        TileConsider[Y][X] = 1
                        TileWeight[Y][X] = 0
                    else:
                        TileDirection[Y][X] = 0
                        TileConsider[Y][X] = 0
                        TileWeight[Y][X] = -1
                    TileIsShortestPath[Y][X] = 1###
                    TileAlreadySelectShortestPath[Y][X] = 0
                    TileVisit[Y][X] = 0

        #print("work")
        PuaseAnimation = False
        User_ResetTileData = False
        LowestPriority = -1
        LowestDistanceFromEnd = -1
        X_consider = -1
        Y_consider = -1
        PathNotExist = False
        PathFound = False
        WeightCorrection = False
        AddWeight = -1
        AddWeight2 = -1
                

    if (timer % AnimationDelay) == 0 and Algorithm != "DEPTH_FIRST_SEARCH" and not PuaseAnimation:
        PathNotExist = True
    if GenerateMaze:
        StopGenerateMaze = True
    for Y in range(0,Height_Grid):
        for X in range(0,Width_Grid):
            if (X_SetLineEnd,Y_SetLineEnd) != (-1,-1) and IsInCoordinateRect(X_SetLine,Y_SetLine,X_SetLineEnd,Y_SetLineEnd,X,Y) and DistancePointToLine(float(X),float(Y),Var_X,Var_Y,Var_C) <= 0.5 and User_EditTile == "SetLine":               
                DrawRect(green,200 + 40 * X,300 + 40 * Y,40,40)
            elif (Y,X) == (Y_MouseOnTile,X_MouseOnTile):
                DrawRect(pink,200 + 40 * X,300 + 40 * Y,40,40)
                if TileWeight[Y][X] != -1:
                    AddText(str(int(TileWeight[Y][X])),20,yellow,200 + 40 * X + 7,300 + 40 * Y + 10)
            elif TileState[Y][X] == 2: # walkable path
                if (Y,X) == (Y_MouseOnTile,X_MouseOnTile):
                    DrawRect(pink,200 + 40 * X,300 + 40 * Y,40,40)
                elif TileIsShortestPath[Y][X] == 1:
                    DrawRect(black,200 + 40 * X,300 + 40 * Y,40,40)
                    DrawRect(yellow,200 + 40 * X + 5,300 + 40 * Y + 5,30,30)
                    NB = GetNeightbor(X,Y)
                    for i in NB:
                        xNB,yNB = i
                        if (xNB,yNB) == (X + 1,Y) and TileIsShortestPath[yNB][xNB] == 1 and (TileWeight[Y][X] == TileWeight[yNB][xNB] - 1 or TileWeight[Y][X] == TileWeight[yNB][xNB] + 1) : #  or TileDirection[Y][X] == Switch_1_2_(TileDirection[yNB][xNB])
                            DrawRect(yellow,200 + 40 * X + 35,300 + 40 * Y + 5,5,30)
                        elif (xNB,yNB) == (X - 1,Y) and TileIsShortestPath[yNB][xNB] == 1 and (TileWeight[Y][X] == TileWeight[yNB][xNB] - 1 or TileWeight[Y][X] == TileWeight[yNB][xNB] + 1):
                            DrawRect(yellow,200 + 40 * X,300 + 40 * Y + 5,5,30)
                        elif (xNB,yNB) == (X,Y + 1) and TileIsShortestPath[yNB][xNB] == 1 and (TileWeight[Y][X] == TileWeight[yNB][xNB] - 1 or TileWeight[Y][X] == TileWeight[yNB][xNB] + 1):
                            DrawRect(yellow,200 + 40 * X + 5,300 + 40 * Y + 35,30,5)
                        elif (xNB,yNB) == (X,Y - 1) and TileIsShortestPath[yNB][xNB] == 1 and (TileWeight[Y][X] == TileWeight[yNB][xNB] - 1 or TileWeight[Y][X] == TileWeight[yNB][xNB] + 1):
                            DrawRect(yellow,200 + 40 * X + 5,300 + 40 * Y,30,5)
                elif TileVisit[Y][X] == 1:
                    if ShowGrid:
                        DrawRect(ReturnFadeColor(TileWeight[Y][X]),200 + 40 * X + 1,300 + 40 * Y + 1,38,38)
                    else:
                        DrawRect(ReturnFadeColor(TileWeight[Y][X]),200 + 40 * X,300 + 40 * Y,40,40)
                elif TileVisit[Y][X] == 0:
                    if TileWeight[Y][X] != -1:
                        if ShowGrid:
                            DrawRect(white,200 + 40 * X + 1,300 + 40 * Y + 1,38,38)
                        else:
                            DrawRect(white,200 + 40 * X,300 + 40 * Y,40,40)
                        d_var = ManhattanDistance(X,Y,X_end,Y_end)
                        if d_var > DistanceStartToEnd:
                            d_var = DistanceStartToEnd
                        k_var = int((d_var/DistanceStartToEnd) * 16)
                        DrawRect(blue,200 + 40 * X + k_var,300 + 40 * Y + k_var,40 - 2 * k_var,40 - 2 * k_var)
                    else:
                        if ShowGrid:
                            DrawRect(white,200 + 40 * X + 1,300 + 40 * Y + 1,38,38)
                        else:
                            DrawRect(white,200 + 40 * X,300 + 40 * Y,40,40)
                
            elif TileState[Y][X] == 3: # obstacle
                if (Y,X) == (Y_MouseOnTile,X_MouseOnTile):
                    DrawRect(pink,200 + 40 * X,300 + 40 * Y,40,40)
                else:
                    if ShowGrid:
                        DrawRect(black,200 + 40 * X + 1,300 + 40 * Y + 1,38,38)
                    else:
                        DrawRect(black,200 + 40 * X,300 + 40 * Y,40,40)
            elif TileState[Y][X] == 1: # end
                if (Y,X) == (Y_MouseOnTile,X_MouseOnTile):
                    DrawRect(pink,200 + 40 * X,300 + 40 * Y,40,40)
                DrawRect(white,200 + 40 * X,300 + 40 * Y,40,40)
                DrawRect(blue,200 + 40 * X + 1,300 + 40 * Y + 1,38,38)
            elif TileState[Y][X] == 0: # start
                if (Y,X) == (Y_MouseOnTile,X_MouseOnTile):
                    DrawRect(pink,200 + 40 * X,300 + 40 * Y,40,40)
                DrawRect(white,200 + 40 * X,300 + 40 * Y,40,40)
                DrawRect(red,200 + 40 * X + 1,300 + 40 * Y + 1,38,38)
            if TileIsShortestPath[Y][X] == 1: # end
                if TileWeight[Y][X] != - 1:
                    if TileState[Y][X] != 1:
                        if TileWeight[Y][X] % 5 == 0:
                            AddText(str(int(TileWeight[Y][X])),20,black,200 + 40 * X + 7,300 + 40 * Y + 10)
                    else:
                        AddText(str(int(TileWeight[Y][X])),20,yellow,200 + 40 * X + 7,300 + 40 * Y + 10)

            if GenerateMaze:
                if X % 2 == 1 and Y % 2 == 1:
                    if TileState[Y][X] == 3:
                        StopGenerateMaze = False
                        IdealDirection = MazeGetNextPath(X,Y)
                        NBcount = len(IdealDirection)
                        if NBcount == 4:
                            NBcount = 1
                        for i in IdealDirection:
                            if random.randint(1,math.pow(4,NBcount)) == 1:
                                if i == "+x":
                                    TileState[Y][X] = 2
                                    TileState[Y][X + 1] = 2
                                elif i == "-x":
                                    TileState[Y][X] = 2
                                    TileState[Y][X - 1] = 2
                                elif i == "+y":
                                    TileState[Y][X] = 2
                                    TileState[Y + 1][X] = 2
                                elif i == "-y":
                                    TileState[Y][X] = 2
                                    TileState[Y - 1][X] = 2
                    else:
                        continue
                else:
                    continue

            

            if Start_PathFinding and (timer % AnimationDelay) == 0 and not PuaseAnimation:
                
                if Algorithm == "DIJKSTRA":
                    if TileVisit[Y][X] == 0 and TileState[Y][X] != 3 and TileWeight[Y][X] != -1 and TileConsider[Y][X] == 1: # not obstacleor not visit node
                        PathNotExist = False
                        AccessableNeighbor = GetNeightbor(X,Y)
                        for i in AccessableNeighbor: #####
                            xNB,yNB = i
                            if TileState[yNB][xNB] != 3 and TileVisit[yNB][xNB] == 0: # not obstacle or not visit node
                                if TileWeight[yNB][xNB] == -1 or TileWeight[Y][X] + GetTravelCost(TileState[yNB][xNB]) < TileWeight[yNB][xNB]:
                                    TileWeight[yNB][xNB] = TileWeight[Y][X] + GetTravelCost(TileState[yNB][xNB])
                        #######
                        if TileWeight[Y_end][X_end] != -1:
                            PathFound = True
                            Start_PathFinding = False
                        TileVisit[Y][X] = 1
                    else:
                        continue 

                elif Algorithm == "A*_SEARCH":
                    if TileVisit[Y][X] == 0 and TileState[Y][X] != 3 and TileWeight[Y][X] != -1 and TileConsider[Y][X] == 1:# not obstacle or not visit node
                        PathNotExist = False
                        
                        if LowestPriority == TileWeight[Y][X] + ManhattanDistance(X,Y,X_end,Y_end):
                            if LowestDistanceFromEnd > ManhattanDistance(X,Y,X_end,Y_end):
                                LowestDistanceFromEnd = ManhattanDistance(X,Y,X_end,Y_end)
                                X_consider,Y_consider = X,Y
                            
                        if LowestPriority == -1 or LowestPriority > TileWeight[Y][X] + ManhattanDistance(X,Y,X_end,Y_end):
                            LowestDistanceFromEnd = ManhattanDistance(X,Y,X_end,Y_end)
                            LowestPriority = TileWeight[Y][X] + ManhattanDistance(X,Y,X_end,Y_end)
                            X_consider,Y_consider = X,Y
                            
                    else:
                        continue
                        
                elif Algorithm == "BREADTH_FIRST_SEARCH":
                    if TileVisit[Y][X] == 0 and TileState[Y][X] != 3 and TileWeight[Y][X] != -1 and TileConsider[Y][X] == 1:# not obstacle or not visit node
                        PathNotExist = False
                        AccessableNeighbor = GetNeightbor(X,Y)
                        for i in AccessableNeighbor: #####
                            xNB,yNB = i
                            if TileState[yNB][xNB] != 3 and TileVisit[yNB][xNB] == 0:
                                if TileWeight[yNB][xNB] == -1:
                                    TileWeight[yNB][xNB] = TileWeight[Y][X] + GetTravelCost(TileState[yNB][xNB])
                        if TileWeight[Y_end][X_end] != -1:
                            PathFound = True
                            Start_PathFinding = False
                        TileVisit[Y][X] = 1
                    else:
                        continue 

                elif Algorithm == "BIDIRECTIONAL":
                    if TileVisit[Y][X] == 0 and TileState[Y][X] != 3 and TileWeight[Y][X] != -1 and (TileConsider[Y][X] == 1):# not obstacle or not visit node
                        PathNotExist = False
                        AccessableNeighbor = GetNeightbor(X,Y)
                        for i in AccessableNeighbor: #####
                            xNB,yNB = i
                            if TileDirection[yNB][xNB] != 0 and TileDirection[Y][X] == Switch_1_2_(TileDirection[yNB][xNB]):
                                if TileWeight[yNB][xNB] == -1:
                                    TileWeight[yNB][xNB] = TileWeight[Y][X] + GetTravelCost(TileState[yNB][xNB])
                                PathFound = True
                                Start_PathFinding = False
                                TileIsShortestPath[yNB][xNB] = 1 # to end
                                TileIsShortestPath[Y][X] = 1 # to start
                                AddWeight = TileWeight[Y][X]
                                AddWeight2 = TileWeight[yNB][xNB]
                                print(str(AddWeight) + " " + str(AddWeight2))
                                TileVisit[yNB][xNB] = 1
                                TileVisit[Y][X] = 1
                                break
                            if TileState[yNB][xNB] != 3 and TileVisit[yNB][xNB] == 0:
                                if TileWeight[yNB][xNB] == -1:
                                    TileWeight[yNB][xNB] = TileWeight[Y][X] + GetTravelCost(TileState[yNB][xNB])
                                TileDirection[yNB][xNB] = TileDirection[Y][X]
                        TileVisit[Y][X] = 1
                    else:
                        continue 
                





            if PathFound:
                if not WeightCorrection and Algorithm == "BIDIRECTIONAL":
                    for Y2 in range(0,Height_Grid):
                        for X2 in range(0,Width_Grid):
                            if TileDirection[Y2][X2] == 2:
                                TileDirection[Y2][X2] = 3
                                TileWeight[Y2][X2] = AddWeight + AddWeight2 - TileWeight[Y2][X2] + 1
                    WeightCorrection = True
                if TileIsShortestPath[Y][X] == 1 and TileAlreadySelectShortestPath[Y][X] == 0:
                    AccessableNeighbor = GetNeightbor(X,Y)
                    for i in AccessableNeighbor: #####
                        xNB,yNB = i
                        if TileState[yNB][xNB] == 3:
                            continue
                        if TileWeight[yNB][xNB] == TileWeight[Y][X] - 1 and TileVisit[yNB][xNB] == 1 and (TileDirection[Y][X] == 1 or TileDirection[Y][X] == 0):
                            TileIsShortestPath[yNB][xNB] = 1
                            TileAlreadySelectShortestPath[Y][X] == 1
                            break
                        elif TileWeight[yNB][xNB] == TileWeight[Y][X] + 1 and TileVisit[yNB][xNB] == 1 and TileDirection[Y][X] == 3:
                            TileIsShortestPath[yNB][xNB] = 1
                            TileAlreadySelectShortestPath[Y][X] == 1
                            break
                else:
                    continue
    ############################################### end of loop

    if Start_PathFinding and Algorithm == "DEPTH_FIRST_SEARCH" and (timer % AnimationDelay) == 0 and not PathNotExist and not PuaseAnimation:
        if TileQueue:
            X,Y = TileQueue.pop()
            TileVisit[Y][X] = 1
            NB = GetNeightbor(X,Y)
            UseableNB = 0
            for i in NB:
                xNB,yNB = i
                if TileState[yNB][xNB] != 3 and TileVisit[yNB][xNB] != 1:
                    UseableNB += 1
            if UseableNB >= 2:
                TileQueue.append((X,Y))
            for i in NB:
                xNB,yNB = i
                if TileState[yNB][xNB] == 1: ####### found IT
                    TileWeight[yNB][xNB] = TileWeight[Y][X] + 1
                    PathFound = True
                    Start_PathFinding = False
                    PathNotExist = False
                    break
                if TileState[yNB][xNB] != 3 and TileVisit[yNB][xNB] != 1:
                    TileWeight[yNB][xNB] = TileWeight[Y][X] + 1
                    TileQueue.append((xNB,yNB))
                    break
        else:
            Start_PathFinding = False
            PathNotExist = True


    if StopGenerateMaze:
        StopGenerateMaze = False
        GenerateMaze = False
        TileState[Y_start][X_start] = 2
        TileState[Y_end][X_end] = 2
        TileState[0][1] = 0
        X_start,Y_start = 1,0
        TileState[19][39] = 1
        X_end,Y_end = 39,19
        User_ResetTileData = True

    if Start_PathFinding and X_consider != -1 and Y_consider != -1 and Algorithm == "A*_SEARCH":
        AccessableNeighbor = GetNeightbor(X_consider,Y_consider)
        for i in AccessableNeighbor: #####
            xNB,yNB = i
            if TileState[yNB][xNB] != 3 and TileVisit[yNB][xNB] == 0: # not obstacle or not visit node
                TileConsider[yNB][xNB] = 1
                if TileWeight[yNB][xNB] == -1 or TileWeight[Y_consider][X_consider] + GetTravelCost(TileState[yNB][xNB]) < TileWeight[yNB][xNB]:
                    TileWeight[yNB][xNB] = TileWeight[Y_consider][X_consider] + GetTravelCost(TileState[yNB][xNB])
        TileConsider[Y_consider][X_consider] = 0
        TileVisit[Y_consider][X_consider] = 1
        #######
        if TileWeight[Y_end][X_end] != -1:
            PathFound = True
            Start_PathFinding = False
        LowestDistanceFromEnd = -1
        X_consider,Y_consider = -1,-1
        LowestPriority = -1

    ##### here
    
    if PathNotExist and Algorithm != "DEPTH_FIRST_SEARCH":
        Start_PathFinding = False


    

    for Y in range(0,Height_Grid):
        for X in range(0,Width_Grid):
            if TileWeight[Y][X] != -1:
                TileConsider[Y][X] = 1

    ClickCoolDown += 1
    timer += 1



    
    


            



    UpdateScreen()
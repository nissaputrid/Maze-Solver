import pygame
from copy import deepcopy

pygame.init()

white = (255,255,255)
black = (0,0,0)
dark_green = (3,105,34)
red = (245,143,149)
green = (0,200,0)
dark_blue = (4,78, 134)
blue = (145,208,255)
dark_red = (154,4,14)
matriks = []
lintasan = []
queue = []
start = False
pilihan = 0
first = True

# Membaca file dengan nama tertentu
def bacafile(nama):
    global matriks
    f = open(nama,"r")
    line = []
    while True:
        temp = f.read(1)
        if not temp:
            matriks.append(line)
            break
        elif temp == '\n' :
            matriks.append(line)
            line = []
        else:
            line.append(int(temp))
    f.close()
    
    

# Mencari jalur masuk maze yang selalu berada di sisi kiri
def searchin():
    for i in range (len(matriks)):
        if (matriks[i][0]==0):
            return i

# Mencari jalur keluar maze yang selalu berada di sisi kanan
def searchout():
    for i in range (len(matriks)):
        if (matriks[i][len(matriks[0])-1]==0):
            return i

# Searching dengan DFS
def DFS(x,y):
    global lintasan, matriks
    found = False
    lintasan.append([x,y])
    matriks[x][y] = 2
    if x==keluar and y==len(matriks[0])-1:
        return
    else:
        if matriks[x][y+1] == 0:
            DFS(x,y+1)
            found = True
        elif matriks[x+1][y] == 0:
            DFS(x+1,y)
            found = True
        elif matriks[x-1][y] == 0:
            DFS(x-1,y)
            found = True
        elif matriks[x][y-1] == 0:
            DFS(x,y-1)
            found = True

        if not found:
            lintasan.pop()
            matriks[x][y] = 3
            last = lintasan.pop()
            DFS(last[0],last[1])

# Mengecek apakah titik x,y berada dalam matriks
def isValid(x,y):
    return x>=0 and y>=0 and x<len(matriks) and y<len(matriks[0])

# Fungsi heuristik
def hn(x,y):
    return abs(x-keluar) + abs(y-(len(matriks[0])-1))

# Mengambil last element list
def takeLast(elem):
    return elem[2]

# Searching dengan A*
def AStar():
    global lintasan, matriks,queue
    found = False
    x = masuk
    y = 0
    while not found:
        lintasan.append([x,y])
        matriks[x][y] = 2
        if x==keluar and y==len(matriks[0])-1:
            found = True
        else:
            gn = len(lintasan)
            if (matriks[x][y+1] == 0 and isValid(x,y+1)):
                queue.append([x,y+1,gn+hn(x,y+1),deepcopy(lintasan)])
            if (matriks[x+1][y] == 0 and isValid(x+1,y)):
                queue.append([x+1,y,gn+hn(x+1,y),deepcopy(lintasan)])
            if (matriks[x-1][y] == 0 and isValid(x-1,y)):
                queue.append([x-1,y,gn+hn(x-1,y),deepcopy(lintasan)])
            if (matriks[x][y-1] == 0 and isValid(x,y-1)):
                queue.append([x,y-1,gn+hn(x,y-1),deepcopy(lintasan)])
            queue.sort(key=takeLast)
            x = queue[0][0]
            y = queue[0][1]
            lintasan = deepcopy(queue[0][3])
            queue.pop(0)
    for i in range (len(matriks)):
        for j in range (len(matriks[0])):
            if matriks[i][j]==2 and [i,j] not in lintasan:
                matriks[i][j] = 3

# Searching dengan BFS
def BFS():
    global lintasan, matriks, queue
    global masuk, keluar
    found = False
    x = masuk
    y = 0
    while not found:
        lintasan.append([x,y])
        matriks[x][y] = 2
        if x==keluar and y==len(matriks[0])-1:
            found = True
        else:
            if (matriks[x][y+1] == 0 and isValid(x,y+1)):
                queue.append([x,y+1,deepcopy(lintasan)])
            if (matriks[x+1][y] == 0 and isValid(x+1,y)):
                queue.append([x+1,y,deepcopy(lintasan)])
            if (matriks[x-1][y] == 0 and isValid(x-1,y)):
                queue.append([x-1,y,deepcopy(lintasan)])
            if (matriks[x][y-1] == 0 and isValid(x,y-1)):
                queue.append([x,y-1,deepcopy(lintasan)])
            x = queue[0][0]
            y = queue[0][1]
            lintasan = deepcopy(queue[0][2])
            queue.pop(0)
    for i in range (len(matriks)):
        for j in range (len(matriks[0])):
            if matriks[i][j]==2 and [i,j] not in lintasan:
                matriks[i][j] = 3
                    
def button(msg,xx,yy,w,h,ic,ac, action=None):
    global pilihan 
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if xx+w > mouse[0] > xx and yy+h > mouse[1] > yy:
        pygame.draw.rect(gameDisplay, ac, (xx,yy,w,h))

        if click[0] == 1 and action != None:
            if mouse[0]>=50 and mouse[0]<=150:
                pilihan = 1
            elif mouse[0]>=250 and mouse[0]<=350:
                pilihan = 2
            elif mouse[0]>=450 and mouse[0]<=550:
                pilihan = 3
            action()
    else:        
        pygame.draw.rect(gameDisplay, ic, (xx,yy,w,h))
        
    smallText = pygame.font.SysFont('Arial', 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((xx+(w/2)), (yy+(h/2)))
    gameDisplay.blit(textSurf, textRect)

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def game_quit():
    pygame.quit()
    quit()
	
def game_intro():
    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisplay.fill(black)
        largeText = pygame.font.SysFont('Century Gothic', 80)
        TextSurf, TextRect = text_objects("MAZE SOLVER", largeText)
        TextRect.center = ((display_width/2), (display_height/2)-30)
        gameDisplay.blit(TextSurf, TextRect)

        text1 = pygame.font.SysFont('Century Gothic', 20)
        text1surf, text1rect = text_objects("Press space to back", text1)
        text1rect.center = ((display_width/2), (display_height/2+30))
        gameDisplay.blit(text1surf, text1rect)
        
        text1 = pygame.font.SysFont('Century Gothic', 20)
        text1surf, text1rect = text_objects("Press enter to see the original maze", text1)
        text1rect.center = ((display_width/2), (display_height/2+50))
        gameDisplay.blit(text1surf, text1rect)

        credit = pygame.font.SysFont('Century Gothic', 20)
        creditsurf, creditrect = text_objects("By: Ajeng (13517085) & Nissa (13517121)", text1)
        creditrect.center = ((display_width/2), (display_height-30))
        gameDisplay.blit(creditsurf, creditrect)

        button("DFS",50,400,100,50,dark_blue,blue, game_loop)
        button("BFS",250,400,100,50,dark_green,green, game_loop)
        button("A*",450,400,100,50,dark_red,red, game_loop)

        pygame.display.update()
        clock.tick(15)

def game_loop():
    exit = False
    global first
    global matriks
    global pilihan
    global lintasan
    global queue

    square_width = float(display_width)/float(len(matriks))
    square_height = float(display_height)/float(len(matriks[0]))
    
    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if pilihan == 1 and first:
                pygame.display.set_caption('Maze Solver: DFS')
                DFS(masuk,0)
                first = False
            elif pilihan == 2 and first:
                pygame.display.set_caption('Maze Solver: BFS')
                BFS()
                first = False
            elif pilihan == 3 and first:
                pygame.display.set_caption('Maze Solver: A*')
                AStar()
                first = False
            gameDisplay.fill(white)
            print(len(lintasan))        
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            for i in range (len(matriks)):
                for j in range (len(matriks[0])):
                    if matriks[i][j] == 1:
                        pygame.draw.rect(gameDisplay, black, (j*square_height,i*square_width,square_height,square_width))
                    elif matriks[i][j] == 2:
                        pygame.draw.rect(gameDisplay, blue, (j*square_height,i*square_width,square_height,square_width))
                    elif matriks[i][j] == 3:
                        pygame.draw.rect(gameDisplay, white, (j*square_height,i*square_width,square_height,square_width))
                    elif matriks[i][j] == 0:
                        pygame.draw.rect(gameDisplay, white, (j*square_height,i*square_width,square_height,square_width))

            font = pygame.font.SysFont('Century Gothic', int(square_height-5))
            text = font.render("Panjang Lintasan: " + str(len(lintasan)), True, white)
            gameDisplay.blit(text, (1,1))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    exit = True
                    pygame.display.set_caption('Maze Solver')
                    lintasan = []
                    queue = []
                    matriks = []
                    bacafile(nama)
                    pilihan = 0
                    first = True
                    game_intro()
                    
                #nampilin maze polos 
                if event.key == pygame.K_RETURN:
                    for i in range (len(matriks)):
                        for j in range (len(matriks[0])):
                            if matriks[i][j] == 1:
                                pygame.draw.rect(gameDisplay, black, (j*square_height,i*square_width,square_height,square_width))
                            elif matriks[i][j] == 2:
                                pygame.draw.rect(gameDisplay, white, (j*square_height,i*square_width,square_height,square_width))
                            elif matriks[i][j] == 3:
                                pygame.draw.rect(gameDisplay, white, (j*square_height,i*square_width,square_height,square_width))
                            elif matriks[i][j] == 0:
                                pygame.draw.rect(gameDisplay, white, (j*square_height,i*square_width,square_height,square_width))

        pygame.display.update()
        clock.tick(30) # to make it faster increase the number

if __name__ == "__main__":
    print("Masukkan nama file:")
    nama = str(input())
    bacafile(nama)
    masuk = searchin()
    keluar = searchout()
    display_width = 600
    display_height = 600
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Maze Solver')
    game_intro()
    pygame.quit()
    quit()

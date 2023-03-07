import pygame
import socket
from cell import Cell
from random import *
import time



# ===================================================================
HEADER_LENGTH = 10

IP = "13mudit.tech"
PORT = 443

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

my_username = input("Username: ")

def connect():

    # Prepare username and header and send them
    # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
    message_initial = my_username + "#(0, 0)"
    username_header = f"{len(message_initial):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + message_initial.encode("utf-8"))
    curr_player = None
    while curr_player is None:
        try:
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            data = client_socket.recv(message_length).decode('utf-8')\
            # 1#Aayu#(127, 543)
            split_data = data.split("#")
            curr_player = int(split_data[0])
            last_played_move = split_data[-1] 
            
            # curr_player = int(client_socket.recv(4).decode("utf-8"))
        except:
            continue
    
    return curr_player, last_played_move
# ====================================================================

pygame.init()
display_width = 600
display_height = 600
count_score_height = 100
cell = 50

gameDisplay = pygame.display.set_mode((display_width,display_height+count_score_height))
pygame.display.set_caption('Game Maybe...')

clock = pygame.time.Clock()

def message_display(text,x,y):
    largetext = pygame.font.Font('freesansbold.ttf',25)
    TextSurf = largetext.render(text, True, (255,255,255))
    TextRect = TextSurf.get_rect()
    TextRect = (x,y)
    gameDisplay.blit(TextSurf,TextRect)



cells = []

for i in range (cell//2, display_height-cell//2, cell):
    cells.append([]) 
    for j in range(cell//2, display_width-cell//2, cell):
        isBorder = False
        if(j == cell//2 or i == cell//2):
            isBorder= True
        new_cell = Cell(j, i, cell, isBorder)
        cells[-1].append(new_cell)



def drawGrid(gameDisplay, color):
    for i in range (cell//2, display_height, cell):
        for j in range(cell//2, display_width, cell):
            pygame.draw.circle(gameDisplay, (255, 255, 255), (j, i), 5)

def countScore():
    score = [0, 0]

    for cell_row in cells:
        for cell in cell_row:
            if cell.player is not None:
                score[cell.player] +=1 
    return score


def gameLoop():
    # curr_player = 0
    curr_player, last_move = connect()
    opponent_name = ""
    # global my_username
    mouse = (0, 0)
    message_header, message = None, None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and curr_player == 0:

                mouse = pygame.mouse.get_pos()
                message = my_username + "#" + str(mouse)
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)
                print(message)
        
        if curr_player == 1:
            # if message is not None:
            #     client_socket.send(message_header + message)
            if last_move != "":
                mouse = eval(last_move)

            try:
                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                data = client_socket.recv(message_length).decode('utf-8')
                print(data)
                received_data = data.split("#")
                opponent_name = received_data[0]
                mouse = eval(received_data[-1])
                
            except:
                pass
        already_changed = 0
        curr_curr_player = curr_player
        for cell_row in cells:
            for cell in cell_row:
                curr_player, already_changed = cell.update(mouse, curr_player, already_changed, curr_curr_player)

        gameDisplay.fill((0, 0, 0))
        drawGrid(gameDisplay, (255, 255, 255))
        for cell_row in cells:
            for cell in cell_row:
                cell.draw(gameDisplay)
        
        message_display(f"{my_username}: {countScore()[0]}", 50, display_height+20)
        message_display(f"{opponent_name}: {countScore()[1]}", 50, display_height+ 50)
        if curr_player ==0:

            message_display(f"Your turn", 300, display_height+50)
        pygame.display.update()
        clock.tick(30)

gameLoop()
pygame.quit()

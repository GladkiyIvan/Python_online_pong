import socket
import time
import pickle
from objects import Player
from objects import Ball
from objects import Game
from _thread import start_new_thread

server = "192.168.0.64"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print('Waiting for connection, Server started')


game = Game([Player(45, 285, 10, 150, (255, 255, 255)),
            Player(945, 285, 10, 150, (255, 255, 255))],
            Ball(465, 330, 25, (255, 255, 255)),
            -1, 0, 0)


def threaded_client(conn, player):
    global playersCount
    conn.send(str.encode(str(player)))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if not data:
                print('Disconnected')
                break
            else:
                if data == 'ready':
                    if player == 0:
                        game.p1_ready = True
                    elif player == 1:
                        game.p2_ready = True
                        game.is_goal = True
                        conn.sendall(pickle.dumps(game))

                reply = game

                print('Received: ', data)
                print('Sending: ', reply)

                conn.sendall(pickle.dumps(reply))

                if game.p1_ready and game.p2_ready and not game.is_finished:
                    game.play_sound = False
                    game.update(data, player)

                if game.is_goal:
                    time.sleep(1)
                    game.is_goal = False


        except Exception as err:
            print(err)
            break

    playersCount = player
    print('Lost connection')
    conn.close()


playersCount = 0
while True:
    if playersCount == 2:
        print('Sorry, server is occupaited now')
        continue
    conn, addr = s.accept()
    print('Connected to: ', addr)
    start_new_thread(threaded_client, (conn, playersCount))

    playersCount += 1
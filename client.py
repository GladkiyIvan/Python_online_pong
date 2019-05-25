import pygame
from network import Network

pygame.font.init()
pygame.mixer.init()
width = 1000
height = 720
win = pygame.display.set_mode((width, height), pygame.GL_DOUBLEBUFFER)
pygame.display.set_caption("Pong")
sound_path = './Sounds/Beep1.wav'


def redrawWindow(win, game, player):

    win.fill((0, 0, 0))

    if game.winner != -1:
        font1 = pygame.font.SysFont('ebrima', 40)
        font2 = pygame.font.SysFont('ebrima', 20)
        final_text = font1.render('You win, take five :)' if game.winner == player else 'You lose :(', 1, (255, 255, 255))
        tip_text = font2.render('To play again restart the client', 1, (255, 255, 255))

        if player == game.winner:
            pos = (340, 310)
        else:
            pos = (420, 310)
        win.blit(final_text, pos)
        win.blit(tip_text, (375, 650))

    elif game.p1_ready and game.p2_ready:
        player_text_pos = (265, 10) if player == 0 else (570, 10)
        opponent_text_pos = (265, 10) if player == 1 else (570, 10)

        player_score = game.p1_scored if player == 0 else game.p2_scored
        opponent_score = game.p1_scored if player == 1 else game.p2_scored
        font = pygame.font.SysFont('ebrima', 25)

        player_text = font.render("You scored: " + str(player_score), 1, (255, 255, 255))
        opponent_text = font.render("Opponent scored: " + str(opponent_score), 1, (255, 255, 255))
        game.draw(win)

        win.blit(player_text, player_text_pos)
        win.blit(opponent_text, opponent_text_pos)
    else:
        font = pygame.font.SysFont('ebrima', 40)
        text = font.render("Waiting for the second player...", 1, (255, 255, 255))
        win.blit(text, (240, 310))

    if game.play_sound:
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(0)

    pygame.display.update()


def main():
    n = Network()

    try:
        player_num = int(n.getP())
    except Exception as err:
        print(err)

    print('You are player ', player_num)
    n.send('ready')

    while True:

        try:
            keys = pygame.key.get_pressed()
            pressed_key = ''

            if keys[pygame.K_UP]:
                pressed_key = 'up'
            if keys[pygame.K_DOWN]:
                pressed_key = 'down'

            if pressed_key != '':
                game = n.send(pressed_key)
            else:
                game = n.send('get')

        except Exception as err:
            print(err)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        redrawWindow(win, game, player_num)


main()

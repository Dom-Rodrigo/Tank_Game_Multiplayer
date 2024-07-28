import sys, pygame
from tank import Tank
from client import Network
import pickle


size = width, height = 900, 700
tank_width, tank_height = 72, 80
grey = 112, 112, 112

screen = pygame.display.set_mode(size)
screen_rect = screen.get_rect()

def drawonscreen(screen, tank, data):
    screen.fill(grey)
    screen.blit(tank.image, tank.rect)
    if data != None:
        for d in data:
                if data[d] != []:
                    screen.blit(tank.image, (data[d][0], data[d][1]))
    pygame.display.update()


data = {0: [], 1: [], 2: [], 3: []}
def main():
    global data
    tank_image = pygame.image.load("tank.png").convert_alpha()
    tank = Tank(image=tank_image, x=0, y=0, speed=3, endurance=60)

    # tanks = pygame.sprite.Group()
    # tanks.add(tank)

    run_game =  True
    n = Network()
    current_id = n.connect("anon")
    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if tank.turn == 4 or tank.turn == -4:  # one cycle
            tank.turn = 0 #this needs to be sent, and considered in the clients

        if tank.speed != 0:
            if keys[pygame.K_UP]:
                tank.move(up=True)
            if keys[pygame.K_DOWN]:
                tank.move(down=True)
            if keys[pygame.K_LEFT]:
                tank.move(turn_left=True)
            if keys[pygame.K_RIGHT]:
                tank.move(turn_right=True)

        # Send tank turn and position to server
        data[current_id] = [tank.rect.x, tank.rect.y]
        n.send_data(data)
        # Receive their positions and draw it
        data = n.receive_data()
        print("id: ", current_id)
        print(data)
        print("\n")

        clock.tick(100)

        drawonscreen(screen, tank, data)
        pygame.display.flip()

if __name__ == "__main__":
    clock = pygame.time.Clock()
    main()

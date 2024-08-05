import sys, pygame
from tank import Tank
from bullet import Bullet
from client import Network
import pickle


size = width, height = 900, 700
tank_width, tank_height = 81, 81
grey = 112, 112, 112

screen = pygame.display.set_mode(size)
screen_rect = screen.get_rect()

tank_image = pygame.image.load("tank_images/tank_red.png").convert_alpha()
bullet_image = pygame.image.load("bullet.png")
tank_image_right  = pygame.transform.rotate(tank_image, -90)
tank_image_left = pygame.transform.rotate(tank_image, -270)
tank_image_down =  pygame.transform.rotate(tank_image, -180)

def drawonscreen(screen, tank, data, bullets):
    screen.fill(grey)
    screen.blit(tank.image, tank.rect)

    if data != None:
        for d in data:
                if data[d] != []:
                    if data[d][2] in [0, 4, -4]: #Tank is poiting to the top
                        screen.blit(tank_image, (data[d][0], data[d][1]))
                    if data[d][2] in [-2, 2]: #Tank is pointing down
                        screen.blit(tank_image_down, (data[d][0], data[d][1]))
                    if data[d][2] in [-1, 3]: #Tank is poiting to the right
                        screen.blit(tank_image_right, (data[d][0], data[d][1]))
                    if data[d][2] in [1, -3]: #Tank is poiting to the left
                        screen.blit(tank_image_left, (data[d][0], data[d][1]))
                    if data[d][3] != None:
                        for b in data[d][3]:
                            screen.blit(bullet_image, (b[0], b[1]))
    bullets.draw(screen)
    pygame.display.update()


data = {0: [], 1: [], 2: [], 3: []}
#[x, y, turn]
def main():
    global data
    tank = Tank(image=tank_image, x=0, y=0, speed=3, endurance=60)
    bullets = pygame.sprite.Group()

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Pressione espaço para atirar
                    bullet = Bullet(bullet_image, tank)
                    bullets.add(bullet)
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


        bullets.update(width, height)
        bullets_rectlist = []
        for b in bullets:
            bullets_rectlist.append((b.rect.x, b.rect.y))

        # Send tank turn and position to server
        data[current_id] = [tank.rect.x, tank.rect.y, tank.turn, bullets_rectlist]
        n.send_data(data)
        # Receive their positions and draw it
        data = n.receive_data()

        # CHECK FOR COLLISIONS
        enemies_bullets = []

        for id in data:
            if data[id] != []:
                if id != current_id:
                    if data[id][3] != None:
                        for i in range(0, len(data[id][3])):
                            enemies_bullets.append(pygame.Rect(data[id][3][i][0], data[id][3][i][1], 8, 8)) #(8, 8) is b_img size

        a = tank.rect.collidelist(enemies_bullets)
        if a != -1: # A coliision happended
            tank.endurance -= 1
            print(f"Tank {current_id} endurance:  {tank.endurance}")
            if tank.endurance == 0:
                print("TANK DESTROYED")
                break

        print("id: ", current_id)
        print(data)
        print("\n")
        clock.tick(30)
        drawonscreen(screen, tank, data, bullets)

        pygame.display.flip()

if __name__ == "__main__":
    clock = pygame.time.Clock()
    main()

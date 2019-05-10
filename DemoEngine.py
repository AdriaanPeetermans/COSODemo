import pygame
import time

class SceneBase:
    def __init__(self, width, height):
        self.next = self
        self.width = width
        self.height = height
    
    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)

def runGame(fps, starting_scene, width, height, pi):
    cnt = 0
    pygame.init()
    pygame.display.set_caption('COSO TRNG Demo')
    if (pi):
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
    else:
        screen = pygame.display.set_mode((width, height))
    dummieScreen = pygame.Surface((starting_scene.width, starting_scene.height))
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while (active_scene != None):
        t1 = time.time()
        pressed_keys = pygame.key.get_pressed()
        # Event filtering 
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if (event.type == pygame.QUIT):
                quit_attempt = True
            elif (event.type == pygame.KEYDOWN):
                alt_pressed = (pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT])
                if (event.key == pygame.K_ESCAPE):
                    quit_attempt = True
                elif ((event.key == pygame.K_F4) and alt_pressed):
                    quit_attempt = True
            if (quit_attempt):
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        t2 = time.time()
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(dummieScreen)
        t3 = time.time()
        pygame.transform.scale(dummieScreen, (width, height), screen)       
        active_scene = active_scene.next
        t4 = time.time()
        pygame.display.flip()
##        pygame.display.update(pygame.Rect(30,230,250,300))
        t5 = time.time()
##        if (cnt%60 == 0):
##            print('Duration1: ' + str((t2-t1)*1000))
##            print('Duration2: ' + str((t3-t2)*1000))
##            print('Duration3: ' + str((t4-t3)*1000))
##            print('Duration4: ' + str((t5-t4)*1000))
##            print('Total: ' + str((t5-t1)*1000))
        cnt += 1
        clock.tick(fps)

# The rest is code where you implement your game using the Scenes model

##class TitleScene(SceneBase):
##    def __init__(self):
##        SceneBase.__init__(self)
##    
##    def ProcessInput(self, events, pressed_keys):
##        for event in events:
##            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
##                # Move to the next scene when the user pressed Enter
##                self.SwitchToScene(GameScene())
##    
##    def Update(self):
##        pass
##    
##    def Render(self, screen):
##        # For the sake of brevity, the title scene is a blank red screen
##        screen.fill((255, 0, 0))
##
##class GameScene(SceneBase):
##    def __init__(self):
##        SceneBase.__init__(self)
##    
##    def ProcessInput(self, events, pressed_keys):
##        pass
##        
##    def Update(self):
##        pass
##    
##    def Render(self, screen):
##        # The game scene is just a blank blue screen 
##        screen.fill((0, 0, 255))

#run_game(400, 300, 60, TitleScene())

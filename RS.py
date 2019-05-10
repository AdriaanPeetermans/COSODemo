import pygame

class RS:

    def __init__(self, screen, FPGAReader, demoScreen):
        self.screen = screen
        self.FPGAReader = FPGAReader
        self.demoScreen = demoScreen
        self.counter = 0

    #Colors:
    white = (255, 255, 255)
    BorderColor = (0, 64, 122)
    Text1Color = (38, 141, 174)
    Text2Color = (0, 0, 0)


    #Positions and sizes:
    BorderWidth = 3
    InternalBorderWidth = 2
    Text1Size = 16
    Text2Size = 20
    Text2RightMar = 5
    Text1LeftMar = 5

    #Others:
    RefreshRate = 60

    def Render(self):
        if (self.counter == 0):
            self.screen.fill(self.white)
            #Draw borders:
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,self.screen.get_height()-self.BorderWidth,self.screen.get_width(),self.BorderWidth))
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.screen.get_width()-self.BorderWidth,0,self.BorderWidth,self.screen.get_height()-self.BorderWidth))
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,0,self.BorderWidth,self.screen.get_height()-self.BorderWidth))
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.BorderWidth,0,self.screen.get_width()-2*self.BorderWidth,self.BorderWidth))
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(int(self.screen.get_width()/2-self.InternalBorderWidth/2+0.5),0,self.InternalBorderWidth,self.screen.get_height()))
            #Print ROSel:
            ROSel = self.FPGAReader.getROSel()
            RS0Text = self.demoScreen.createText(str(int(ROSel[0])), self.demoScreen.preferedFonts, self.Text2Size, self.Text2Color)
            RS1Text = self.demoScreen.createText(str(int(ROSel[1])), self.demoScreen.preferedFonts, self.Text2Size, self.Text2Color)
            self.screen.blit(RS0Text, (int(self.screen.get_width()/2-RS0Text.get_width()-self.Text2RightMar+0.5),int(self.screen.get_height()/2-RS0Text.get_height()/2+0.5)))
            self.screen.blit(RS1Text, (int(self.screen.get_width()-RS1Text.get_width()-self.Text2RightMar+0.5),int(self.screen.get_height()/2-RS1Text.get_height()/2)))
            RS0T = self.demoScreen.createText('RO0Sel:', self.demoScreen.preferedFonts, self.Text1Size, self.Text1Color)
            RS1T = self.demoScreen.createText('RO1Sel:', self.demoScreen.preferedFonts, self.Text1Size, self.Text1Color)
            self.screen.blit(RS0T, (self.Text1LeftMar, int(self.screen.get_height()/2-RS0T.get_height()/2+0.5)))
            self.screen.blit(RS1T, (int(self.screen.get_width()/2+self.Text1LeftMar+0.5),int(self.screen.get_height()/2-RS1T.get_height()/2+0.5)))
        elif (self.counter == self.RefreshRate-1):
            self.counter = -1
        self.counter += 1

    

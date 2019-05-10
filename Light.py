import pygame

class Light:

    def __init__(self, screen, text, fun, demoScreen):
        self.screen = screen
        self.text = text
        self.fun = fun
        self.demoScreen = demoScreen
        self.counter = 0

    #Colors:
    BorderColor = (0, 64, 122)
    TextGreen = (24, 106, 59)
    Green = (88, 214, 141)
    TextRed = (148, 49, 38)
    Red = (236, 112, 99)

    #Positions and sizes:
    BorderWidth = 3
    TextSize = 17

    #Others:
    RefreshRate = 60

    def Render(self):
        if (self.counter == 0):
            #Draw background:
            if (self.fun()):
                color = self.Green
                textColor = self.TextGreen
            else:
                color = self.Red
                textColor = self.TextRed
            self.screen.fill(color)
            #Draw borders:
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,self.screen.get_height()-self.BorderWidth,self.screen.get_width(),self.BorderWidth))
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.screen.get_width()-self.BorderWidth,0,self.BorderWidth,self.screen.get_height()-self.BorderWidth))
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,0,self.BorderWidth,self.screen.get_height()-self.BorderWidth))
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.BorderWidth,0,self.screen.get_width()-2*self.BorderWidth,self.BorderWidth))                      
            #Text:
            labelText = self.demoScreen.createText(self.text, self.demoScreen.preferedFonts, self.TextSize, textColor)
            self.screen.blit(labelText, (int(self.screen.get_width()/2-labelText.get_width()/2+0.5),int(self.screen.get_height()/2-labelText.get_height()/2+0.5)))
        elif (self.counter == self.RefreshRate-1):
            self.counter = -1
        self.counter += 1

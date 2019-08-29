import pygame
import math

class LiveData:

    def __init__(self, screen, FPGAReader, demoScreen):
        self.screen = screen
        self.FPGAReader = FPGAReader
        self.demoScreen = demoScreen
        self.counter = 0
        self.boxHeight = self.screen.get_height()/len(self.Text1s)

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
    Text1LeftMarg = 5
    Text1TopMarg = 3
    Text2Length = 5
    Text2RightMarg = 5
    Text2BotMarg = 3

    #Others:
    RefreshRate = 60
    Text1s = ['CSCnt:', 'Delta:', 'Freq0:', 'Freq1:', 'Throughput:']
    Text2s = ['', 'ps', 'MHz', 'MHz', 'Mbit/s']

    def Render(self):
        if (self.counter == 0):
            self.screen.fill(self.white)
            #Draw borders:
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,self.screen.get_height()-self.BorderWidth,self.screen.get_width(),self.BorderWidth))
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.screen.get_width()-self.BorderWidth,0,self.BorderWidth,self.screen.get_height()-self.BorderWidth))
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,0,self.BorderWidth,self.screen.get_height()-self.BorderWidth))
            pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(self.BorderWidth,0,self.screen.get_width()-2*self.BorderWidth,self.BorderWidth))
            for i in range(len(self.Text1s)-1):
                pygame.draw.rect(self.screen, self.BorderColor, pygame.Rect(0,int((i+1)*self.boxHeight-self.InternalBorderWidth/2+0.5),self.screen.get_width(),self.InternalBorderWidth))
            #Text1s:
            for i in range(len(self.Text1s)):
                text = self.demoScreen.createText(self.Text1s[i], self.demoScreen.preferedFonts, self.Text1Size, self.Text1Color)
                self.screen.blit(text, (self.Text1LeftMarg, int(i*self.boxHeight+self.Text1TopMarg+0.5)))
            data = self.FPGAReader.getLiveData()
            for i in range(len(self.Text1s)):
                text = self.demoScreen.createText(self.stringLength(data[i], self.Text2Length) + ' ' + self.Text2s[i], self.demoScreen.preferedFonts, self.Text2Size, self.Text2Color)
                self.screen.blit(text, (int(self.screen.get_width()-text.get_width()-self.Text2RightMarg+0.5), int((i+1)*self.boxHeight-text.get_height()-self.Text2BotMarg+0.5)))
        elif (self.counter == self.RefreshRate-1):
            self.counter = -1
        self.counter += 1

    @staticmethod
    def stringLength(value, size):
        if (math.isnan(value)):
            return '-'
        if (value%1 == 0):
            return str(value)
        s = str(value)
        while (len(s) < size):
            s += '0'
        while (len(s) > size):
            s = s[0:-1]
        return s

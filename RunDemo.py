import DemoEngine
import DemoScreen
import FPGAReader

#Running on Raspberry Pi?
pi = False

reader = FPGAReader.FPGAReader.init(pi)
reader.start()
reader.sendBounds(50, 150)
reader.initBuffers()
DemoEngine.runGame(60, DemoScreen.DemoScreen(reader), 800, 480, pi)

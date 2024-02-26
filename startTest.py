import main
import Settings


nets = main.createNet(Settings.NS)

for i in range(Settings.testCount):
    X, Y, resX = main.reading()
    nets[i].Train(X, Y, Settings.alpha, Settings.eps, Settings.epochs)
    main.runForBoot(nets[i])

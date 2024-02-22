import main
import Settings

for i in range(Settings.testCount):
    net = main.Network(Settings.NS)
    X, Y, resX = main.reading()
    net.Train(X, Y, Settings.alpha, Settings.eps, Settings.epochs)
    main.runForBoot(net)

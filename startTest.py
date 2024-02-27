import main
import Settings

nets = main.Network(Settings.NS)
X, Y, resX = main.reading()
nets.Train(X, Y, Settings.alpha, Settings.eps, Settings.epochs)
main.runForBoot(nets)

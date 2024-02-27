import main
import Settings

net = main.Network(Settings.NS)
X, Y, resX = main.reading()
main.train(net, X, Y, Settings.alpha, Settings.eps, Settings.epochs)
main.runForBoot(net)

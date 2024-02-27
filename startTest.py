import main
import SettingsTest

net = main.Network(SettingsTest.NS)
X, Y, resX = main.reading()
main.train(net, X, Y, SettingsTest.alpha, SettingsTest.eps, SettingsTest.epochs)
main.testRun(net)

import main
import Settings

n = main.NetworkTrained(Settings.NS)
X, Y, resX = main.reading()

if main.run(1, n, resX)[0] == 1:
    print(2)
    result = f"Болен {main.run(1, n, resX)[1]}"
else:
    print(1)
    result = f"Не болен {main.run(1, n, resX)[1]}"
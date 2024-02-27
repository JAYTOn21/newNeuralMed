config = "[6, 12^50, 1] ActFun = 1 49967322"
# Стартовое название конфига
uniqCode = ""
for i in range(len(config) - 1, 0, -1):
    if config[i] != " ":
        uniqCode += config[i]
    else:
        break
uniqCode = uniqCode[::-1]
folderName = config.replace(f" {uniqCode}", "")
# Разделение на название папки и уникальный код
ActFun = 0
NS = [6]
inType = ""
count = ""
boolCheck = True
for i in range(len(config)):
    if config[i] == " " and boolCheck:
        j = i + 1
        while config[j] != "^":
            inType += config[j]
            j += 1
        boolCheck = False
    elif config[i] == "^":
        j = i + 1
        while config[j] != ",":
            count += config[j]
            j += 1
    elif config[i] == "=":
        ActFun = config[i + 2]
        break
# Алгоритм вычленения типа акт. функции, типа скрытых нейронов и их количества
inType = int(inType)
# Типа скрытых нейронов (6 или 12)
count = int(count)
# Количество скрытых слоев
ActFun = int(ActFun)
# Тип активационной функции
for i in range(count):
    NS.append(inType)
NS.append(1)
# Алгоритм автоматического построения структуры нейронной сети из
alpha = 0.5
# Скорость понижения ошибки
eps = 0.0000000000000000001
# Минимум ошибки
epochs = 10000
# Количество эпох


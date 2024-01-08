import numpy as np
import funct as func

def add_noise_and_decode(signal, standard_deviation):
    signal = np.asarray(signal)
    
    # Добавление шума
    noise = np.random.normal(0, standard_deviation, len(signal))
    signal_with_noise = signal + noise

    # Синхронизация с сигналом и обработка
    golden, G = func.Gold()
    golden = np.repeat(golden, 4)

    autocor = [np.sum(golden * signal_with_noise[i:i + len(golden)]) for i in range(len(signal_with_noise) - len(golden))]
    maximum, pos = max(autocor), np.argmax(autocor)
    
    print("Автокорреляция:", maximum)

    synsig = signal_with_noise[pos: pos + len(signal)]
    func.graphic(synsig, "Синхросигнал")

    # Преобразование временных отсчётов в информацию и избавление от шума
    cipher = [1 if synsig[i * 4] > 0.5 else 0 for i in range(len(synsig) // 4)]

    # Удаление последовательности Голда
    ciphernotgold = cipher[G:]

    # Проверка CRC
    CRC = func.CRC(ciphernotgold)
    print("CRC:", CRC)



    if 1 in CRC:
        print("Ошибка CRC")
    else:
        # Удаление CRC и декодирование битов информации в буквы
        word = []
        for i in range(len(ciphernotgold) - 7):
            word.append(ciphernotgold[i])
        donemas = func.decoder(word)
        done = ""
        for i in donemas:
            if ord(i) > 65 and ord(i) < 90:
                done += " "
            done += i
        print(done[1:])

def generate_signal_and_transmit(name):
    # Кодирование информации
    kod = func.coder(name)
    func.graphic(kod, "Кодирование символов")
    
    # Вычисление CRC
    M = len(kod)
    delet = [1, 1, 1, 1, 1, 0, 1, 1]
    
    for i in range(len(delet) - 1):
        kod.append(0)
    
    CRCnum = func.CRC(kod)
    print("CRC:", CRCnum)
    
    for i in range(M, len(kod)):
        kod[i] = CRCnum[i - M]
    
    # Генерация последовательности Голда
    golden, G = func.Gold()
    
    for i in range(G):
        kod.append(0)
        kod = func.shiftright(kod)  
    
    for i in range(G):
        kod[i] = golden[i]
    
    func.graphic(kod, "Кодирование с голдом и CRC")
    
    # Преобразования битов в временные отсчёты сигналов
    otch = 4
    signal = np.repeat(kod, otch)
    func.graphic(signal, "Отсчёты")
    length = len(signal)
    
    # Внесение массива информации в массив нулей
    bigsignal = [int(0) for i in range(2 * len(signal))]
    key = int(input("Введите число для вставки в массив: "))
    
    while 1 == 1:
        if key > 0 and key < len(signal):
            break
        else:
            print("Недопустимое число, введите ещё раз")
            key = int(input())
    
    for i in range(len(bigsignal)):
        if i >= key and i - key < len(signal):
            bigsignal[i] = signal[i - key]
        else:
            bigsignal[i] = 0
            
    func.graphic(bigsignal, "Сигнал с передатчика")
    
    return bigsignal, length

def main():
    name = input("Введите имя и фамилию: ")
    signal, _ = generate_signal_and_transmit(name)
    add_noise_and_decode(signal, 0.15)

if __name__ == "__main__":
    main()


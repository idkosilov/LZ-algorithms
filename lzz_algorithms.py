import csv
from xlsxwriter.workbook import Workbook


def lz77(src, size_buffer, k):
    with open(f'lz77_{k}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Словарь", "Буфер", "Совпадающая фраза", "Индекс", "Шаги", "Символ"])
    i = 0
    alphabet = ''
    pack = ''
    while alphabet != src:
        flag = True
        buffer = src[i:i + size_buffer]
        for steps in range(size_buffer - 1, 0, -1):
            if alphabet.rfind(buffer[:steps]) != -1:
                pack += f"{i - alphabet.rfind(buffer[:steps]), steps}{buffer[steps]}"
                z = i - alphabet.rfind(buffer[:steps])
                alphabet += src[i:i + steps + 1]
                i += steps + 1
                flag = False
                with open(f'lz77_{k}.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([alphabet, buffer, src[i:i + steps + 1], z, steps, buffer[steps]])
                break
        if flag:
            with open(f'lz77_{k}.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([alphabet, buffer, "-", "1", "0", src[i]])
            pack += src[i]
            alphabet += src[i]
            i += 1
    return pack


def lzss(src, size_buffer, k):
    with open(f'lzss_{k}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Словарь", "Буфер", "Совпадающая фраза", "f", "Индекс", "Шаги", "Символ"])
    i = 0
    alphabet = ''
    pack = ''
    while alphabet != src:
        flag = True
        buffer = src[i:i + size_buffer]
        for steps in range(size_buffer - 1, 1, -1):
            if alphabet.rfind(buffer[:steps]) != -1:
                with open(f'lzss_{k}.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([alphabet, buffer, src[i:i + steps], 1, i - alphabet.rfind(buffer[:steps]), steps, "-"])
                pack += f"{1, i - alphabet.rfind(buffer[:steps]), steps}"
                alphabet += src[i:i + steps]
                i += steps
                flag = False
                break
        if flag:
            with open(f'lzss_{k}.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([alphabet, buffer, "-", "0", "-", "-", src[i]])
            pack += src[i]
            alphabet += src[i]
            i += 1
    return pack


def lz78(src, k):
    i = 0
    alphabet = []
    pack = ''
    with open(f'lz78_{k}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Текст", "Номер", "Совпадающая фраза", "n", "s"])
    while i < len(src):
        flag = False
        for j in range(7, 0, -1):
            if src[i:i + j] in alphabet:
                try:
                    pack += f"({alphabet.index(src[i:i + j]) + 2}){src[i + j]}"
                except Exception:
                    pack += f"{alphabet.index(src[i:i + j]) + 2}"
                with open(f'lz78_{k}.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([src[i:i + j + 1], len(alphabet) + 2,
                                     alphabet[alphabet.index(src[i:i + j])], alphabet.index(src[i:i + j]) + 2,
                                     src[i + j]])
                alphabet.append(src[i:i + j + 1])
                i += len(src[i:i + j + 1])
                flag = True
                break
            else:
                j -= 1
        if flag is False:
            with open(f'lz78_{k}.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([src[i], len(alphabet) + 2, "-", "1", src[i]])
            pack += src[i]
            alphabet.append(src[i])
            i += 1
    return pack


def main():
    with open('text', 'r') as f:
        files = f.readlines()
    for line in files:
        n, tx = line[0:line.find(' ')-1], line[3:]
        print(n)
        print(lz77(tx, 7, n))
        print(lz78(tx, n))
        print(lzss(tx, 7, n))

    workbook = Workbook('lz77.xlsx')
    for csvfile in [f'lz77_{i}.csv' for i in range(1, 101)]:
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
    workbook.close()
    workbook = Workbook('lzss.xlsx')
    for csvfile in [f'lzss_{i}.csv' for i in range(1, 101)]:
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
    workbook.close()
    workbook = Workbook('lz78.xlsx')
    for csvfile in [f'lz78_{i}.csv' for i in range(1, 101)]:
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
    workbook.close()


if __name__ == "__main__":
    main()

from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        global key_first
        global sent
        key_first = request.form['key_first']
        sent = request.form['sent']
        print( 'проверка',key_first, sent)
        context = {
            "answ": playfer(key_first, sent)
        }
        print('Проверка' ,key_first, sent)
        print('Контекст', context['answ'])
        with open('templates/test.html', mode="w", encoding='utf-8') as f:
            f.write(context['answ'])
        return render_template('test.html')
    return render_template('after_button.html')


@app.route('/button', methods = ['POST', 'GET'])
def playfer(key_first, sent):
    print(key_first, sent)
    abc = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я']
    specs = ' ,.:;-!?)('


    sentense = [i.lower() for i in sent]

    for i in specs:
        while sentense.count(i) > 0:
            sentense.pop(sentense.index(i))
    sentense = ''.join(sentense)

    
    addSymbol = 'х'
    preList = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']

    all_key = []    # Проверка повторяющихся символов в коде
    repeat_key = []
    key = ''
    for i in key_first:
        if i in all_key:
            repeat_key.append(i)
        else:
            all_key.append(i)
    key = key.join(repeat_key)


    for i in range(len(key)):
        preList[i] = key[i]

    abcWithoutKey = abc
    for i in key:
        abcWithoutKey.pop(abcWithoutKey.index(i))
    abc = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я']

    for i in range(len(key), len(preList)):
        preList[i] = abcWithoutKey[i - len(key)]

    codeList = [
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','','']
    ]
    tmp = 0
    for i in range(4):
        for j in range(8):
            codeList[i][j] = preList[tmp]
            tmp += 1

    del tmp, abcWithoutKey, specs, preList

    sentenseReacharge = []
    for i in range(0, len(sentense), 2):
        try:
            if sentense[i] != sentense[i + 1]:
                sentenseReacharge.append(sentense[i] + sentense[i + 1])
            else:
                sentense = sentense[:i + 1] + addSymbol + sentense[i + 1:]
                sentenseReacharge.append(sentense[i] + sentense[i + 1])
        except IndexError:
            sentenseReacharge.append(sentense[-1] + addSymbol)

    del sentense

    #for i in range(len(codeList)):
        #print(*codeList[i])
    def takeIndex(code):
        nonlocal codeList
        ans = [[i, _list.index(code)] for i,_list in enumerate(codeList) if code in codeList[i]]
        return ans
        # 1 - столбец
        # 0 - строка

    def Check(indexF, indexS):
        nonlocal codeList
        if indexF[0][1] == indexS[0][1]: #collumn
            #(indexF[0][0] + 3) % 4, (indexS[0][0] + 3) % 4
            pass
        elif indexF[0][0] == indexS[0][0]: #line
            #(indexF[0][1] + 7) % 8, (indexS[0][1] + 7) % 8
            pass
        else: #square
            buf = indexF[0][1]
            indexF[0][1] = indexS[0][1]
            indexS[0][1] = buf
        return indexF, indexS

    codes = []
    for code in sentenseReacharge:
        print('проверка', type(code))
        codes.append(Check(takeIndex(code[0]), takeIndex(code[1])))

    #print(sentenseReacharge)
    #print('строка, столбец')
    AnswerIndex = ''
    #print(codes)
    for i in codes:
        #print(i[0][0][0], i[0][0][1], i[1][0][0], i[1][0][1])
        AnswerIndex += codeList[i[0][0][0]][i[0][0][1]]
        AnswerIndex += codeList[i[1][0][0]][i[1][0][1]]
    print(AnswerIndex)
    return render_template('after_button.html', answer = AnswerIndex)


if __name__ == '__main__':
    app.run(debug=True)
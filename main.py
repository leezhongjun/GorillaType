import random, json
from flask import Flask, render_template, request, url_for, redirect

def get_wordlist():
    with open('wordlist.txt', 'r') as f:
        wordlist = f.read().splitlines()
    wordlist = [x for x in wordlist if x]
    return wordlist, len(wordlist)

def get_potter_wordlist():
    with open('harry_potter.txt', 'r',encoding='utf-8') as f:
        wordlist = f.read().splitlines()
    wordlist = [x for x in wordlist if x]
    return wordlist, len(wordlist)


app = Flask(__name__)

wordlist, wordlist_len = get_potter_wordlist()
# print(wordlist_len,flush=True)
modes = ['10 sec', '15 sec', '20 sec']
hs = {x:0 for x in modes}
stats = {'curr_score':0, 'curr_mode':modes[0]}
wordlist_choice = 0
end_time = 0


@app.route('/', methods=['GET', 'POST'])
def index():
    global stats, wordlist_choice, hs
    wordlist_choice = random.randint(0,wordlist_len-1)
    hs[stats['curr_mode']] = max(hs[stats['curr_mode']], stats['curr_score'])

    if request.method == 'POST':
        keylog = json.loads(request.args.get('data'))
        keylog = [(x, keylog[x]) for x in keylog.keys()]
        keylog = sorted(keylog, key=lambda x: x[1])[::-1]
        return render_template('greet.html', stats = stats, hs=hs,end = True ,keylog=keylog)
    else:
        return render_template('greet.html', stats = stats, hs=hs, end = False)


@app.route('/game', methods=['GET', 'POST'])
def game():
    global stats, wordlist_choice, end_time
    if request.method == 'POST':
        stats['curr_score'] = int(request.form['ss'])
        stats['curr_mode'] = request.form['mode'] + ' sec'
        return redirect(url_for('index', data = request.form['keys']), code=307) # For post
    else:
        return render_template('game.html', light=wordlist[wordlist_choice], score = 0, end_time=int(request.args['secs']))
    

if __name__=='__main__':
    app.run(debug=True)
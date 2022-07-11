#monkeytype but you can put random keypresses
#calculate keypressing stats
#add fake ads
#gorrila typing ui

#timer for typing

#turbo flask for dynamic updating

#import wordlist for typing

#############################################################################################
### pip install flask turbo-flask
import random, json
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


def get_wordlist():
    with open('wordlist.txt', 'r') as f:
        wordlist = f.read().splitlines()
    wordlist = [x for x in wordlist if x]
    return wordlist, len(wordlist)

def get_copypasta():
    with open('copypasta.txt', 'r',encoding='utf-8') as f:
        wordlist = f.read()
    wordlist = [x for x in wordlist.split("""


~~~~~



""") if x and x[0] != '~']
    wordlist = [x.split(')')[1] if ')' in x else x for x in wordlist]
    return wordlist, len(wordlist)




wordlist, wordlist_len = get_copypasta()
stats = {'highscore':0, 'curr_score':0}
wordlist_choice = 0
end_time = 0



@app.route('/', methods=['GET', 'POST'])
def index():
    global stats, wordlist_choice
    
    wordlist_choice = random.randint(0,wordlist_len-1)
    stats['highscore'] = max(stats['highscore'], stats['curr_score'])
    if request.method == 'POST':
        keylog = json.loads(request.args.get('data'))
        keylog = [(x, keylog[x]) for x in keylog.keys()]
        keylog = sorted(keylog, key=lambda x: x[1])[::-1]
        return render_template('greet.html', stats = stats, end = True ,keylog=keylog)
    else:
        return render_template('greet.html', stats = stats, end = False)


@app.route('/game/<sec>', methods=['GET', 'POST'])
def game(sec):
    global stats, wordlist_choice, end_time
    if request.method == 'POST':
        stats['curr_score'] = int(request.form['ss'])
        return redirect(url_for('index', data = request.form['keys']), code=307) #for post
    else:
        return render_template('game.html', light=wordlist[wordlist_choice], score = 0, end_time=int(sec))
if __name__=='__main__':
    app.run(debug=True)
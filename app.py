from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'da'  # Важно для работы сессий

@app.route('/')
def index():

    session['balance'] = 5000000000
    return render_template('index.html', balance=session['balance'])
    

@app.route('/place_bet', methods=['POST'])
def place_bet():
    try:
        bet_amount = int(request.form['bet_amount'])
        if bet_amount <= 0:
            return redirect(url_for('index'))
        if bet_amount > session['balance']:
            return redirect(url_for('index'))
        
        session['bet_amount'] = bet_amount
        session['balance'] -= bet_amount
        return redirect(url_for('select_number'))
    except:
        return redirect(url_for('index'))

@app.route('/select_number')
def select_number():
    return render_template('select_number.html', balance=session['balance'], bet_amount=session['bet_amount'])

@app.route('/play', methods=['POST'])
def play():
    selected_number = int(request.form['number'])
    winning_number = random.randint(1,36)
    
    session['selected_number'] = selected_number
    session['winning_number'] = winning_number
    
    if selected_number == winning_number:
        win_amount = session['bet_amount'] * 36
        session['balance']=session['balance'] + win_amount
        result = 'win'
        message = f"Поздравляем! Вы выиграли {win_amount}$!"
    else:
        result = 'lose'
        message = "К сожалению, вы проиграли."
    
    return render_template('result.html', 
                         balance=session['balance'],
                         message=message,
                         result=result,
                         selected_number=selected_number,
                         winning_number=winning_number,
                         bet_amount=session['bet_amount'])
@app.route('/gg', methods=['POST'])
def index1():

    session['balance1'] = session['balance']
    return render_template('index1.html', balance=session['balance1'])

if __name__ == '__main__':
    app.run(debug=True)
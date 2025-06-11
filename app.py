from flask import Flask, render_template, url_for, request, jsonify, session
import sqlite3
import shutil
import secrets

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)
command = """CREATE TABLE IF NOT EXISTS feedback(Type TEXT, user TEXT, game TEXT, feedback TEXT)"""
cursor.execute(command)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT * FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchone()

        if result:
            session['type'] = 'user'
            session['name'] = result[0]
            session['user'] = result[0]

            connection = sqlite3.connect(session['user']+'.db')
            cursor = connection.cursor()

            command = """CREATE TABLE IF NOT EXISTS pattern(score TEXT, timer TEXT, level TEXT, average TEXT, date TEXT, time TEXT)"""
            cursor.execute(command)
            command = """CREATE TABLE IF NOT EXISTS sudoku(score TEXT, timer TEXT, mistake TEXT, date TEXT, time TEXT)"""
            cursor.execute(command)
            command = """CREATE TABLE IF NOT EXISTS tetris(score TEXT, level TEXT, line TEXT, date TEXT, time TEXT)"""
            cursor.execute(command)
            command = """CREATE TABLE IF NOT EXISTS ticktack(timer TEXT, wins TEXT, losses TEXT, ties TEXT, date TEXT, time TEXT)"""
            cursor.execute(command)
            command = """CREATE TABLE IF NOT EXISTS hanoi(moves TEXT, timer TEXT, date TEXT, time TEXT)"""
            cursor.execute(command)
            command = """CREATE TABLE IF NOT EXISTS whackhole(score TEXT, accuracy TEXT, reactionTime TEXT, duration TEXT, date TEXT, time TEXT)"""
            cursor.execute(command)
            return render_template('allgames.html')
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
    return render_template('index.html')


@app.route('/adminlog', methods=['GET', 'POST'])
def adminlog():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        if name == 'admin@gmail.com' and password == 'admin123':
            session['type'] = 'admin'
            session['name'] = 'admin'
            return render_template('patterngraph.html')
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/home')
def home():
    if session['type'] == 'user':
        return render_template('allgames.html')
    else:
        return render_template('patterngraph.html')

@app.route('/feedbackpage')
def feedbackpage():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    if session['type'] == 'user':
        Type = 'admin'
        cursor.execute("select * from feedback where Type = '"+Type+"'")
        result = cursor.fetchall()
        return render_template('feedbacks.html', result=result, title="Admin Feedbacks")
    else:
        Type = 'user'
        cursor.execute("select * from feedback where Type = '"+Type+"'")
        result = cursor.fetchall()
        return render_template('feedbacks.html', result=result, title="User Feedbacks")

@app.route('/feedbacks', methods=['POST', 'GET'])
def feedbacks():
    if request.method == 'POST':
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()
        game = request.form['game']
        feed = request.form['feed']
        cursor.execute("insert into feedback values(?,?,?,?)", [session['type'], session['name'], game, feed])
        connection.commit()
        if session['type'] == 'user':  
            return render_template('allgames.html')
        else:
            return render_template('patterngraph.html')
    return render_template('index.html')

@app.route('/graphs')
def graphs():
    return render_template('patterngraph.html')

@app.route('/allgames')
def allgames():
    return render_template('allgames.html')

@app.route('/pattern')
def pattern():
    return render_template('pattern.html')

@app.route('/sudoku')
def sudoku():
    return render_template('sudoku.html')

@app.route('/tetris')
def tetris():
    return render_template('tetris.html')

@app.route('/ticktack')
def tickack():
    return render_template('ticktack.html')

@app.route('/hanoi')
def hanoi():
    return render_template('hanoi.html')

@app.route('/whackmole')
def whackmole():
    return render_template('whackmole.html')

@app.route('/patterngraph', methods=['POST', 'GET'])
def patterngraph():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute("select * from user")
    result = cursor.fetchall()
    names = []
    for row in result:
        names.append(row[0])

    if request.method == 'POST':
        session['user'] = request.form['name']
        return render_template('patterngraph.html', names=names, Type = session['type'], name=session['user'])

    return render_template('patterngraph.html', Type = session['type'], names=names)

@app.route('/sudokugraph', methods=['POST', 'GET'])
def sudokugraph():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute("select * from user")
    result = cursor.fetchall()
    names = []
    for row in result:
        names.append(row[0])

    if request.method == 'POST':
        session['user'] = request.form['name']
        return render_template('sudokugraph.html', names=names, Type = session['type'], name=session['user'])

    return render_template('sudokugraph.html', Type = session['type'], names=names)

@app.route('/tetrisgraph', methods=['POST', 'GET'])
def tetrisgraph():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute("select * from user")
    result = cursor.fetchall()
    names = []
    for row in result:
        names.append(row[0])

    if request.method == 'POST':
        session['user'] = request.form['name']
        return render_template('tetrisgraph.html', names=names, Type = session['type'], name=session['user'])

    return render_template('tetrisgraph.html', Type = session['type'], names=names)

@app.route('/ticktackgraph', methods=['POST', 'GET'])
def tickackgraph():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute("select * from user")
    result = cursor.fetchall()
    names = []
    for row in result:
        names.append(row[0])

    if request.method == 'POST':
        session['user'] = request.form['name']
        return render_template('ticktackgraph.html', names=names, Type = session['type'], name=session['user'])

    return render_template('ticktackgraph.html', Type = session['type'], names=names)

@app.route('/hanoigraph', methods=['POST', 'GET'])
def hanoigraph():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute("select * from user")
    result = cursor.fetchall()
    names = []
    for row in result:
        names.append(row[0])

    if request.method == 'POST':
        session['user'] = request.form['name']
        return render_template('hanoigraph.html', names=names, Type = session['type'], name=session['user'])

    return render_template('hanoigraph.html', Type = session['type'], names=names)

@app.route('/whackmolegraph', methods=['POST', 'GET'])
def whackmolegraph():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute("select * from user")
    result = cursor.fetchall()
    names = []
    for row in result:
        names.append(row[0])

    if request.method == 'POST':
        session['user'] = request.form['name']
        return render_template('whackmolegraph.html', names=names, Type = session['type'], name=session['user'])

    return render_template('whackmolegraph.html', Type = session['type'], names=names)

@app.route('/update_pattern', methods=['POST'])
def update_pattern():
    data = request.json
    score = data['score']
    score = score.replace('Score: ', '')
    timer = data['timer']
    timer = timer.replace('Time: ', '')
    averageRecallTimeValue = data['averageRecallTimeValue']
    level = data['level']
    
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()

    import datetime
    Date = datetime.date.today().strftime('%Y-%m-%d')
    Time = datetime.datetime.now().time().strftime('%H:%M:%S')
    print(score, timer, Date, Time)

    cursor.execute("select * from pattern where date = '"+Date+"'")
    result = cursor.fetchall()
    print(result)
    # if result:
    #     cursor.execute("update pattern set score = ?, timer = ?, time = ? , level = ?, average = ? where date = ?", [score, timer, Time, level, averageRecallTimeValue, Date])
    #     connection.commit()
    # else:
    cursor.execute("insert into pattern values(?,?,?,?,?,?)", [score, timer, level, averageRecallTimeValue, Date, Time])
    connection.commit()
    return jsonify({'message': 'score and timer received'})

@app.route('/update_sudoku', methods=['POST'])
def update_sudoku():
    data = request.json
    timer = data['timer']
    score = data['progress']
    Mistakes = data['Mistakes']
    Mistakes = Mistakes.replace('Mistakes: ', '')
    score = score.replace('Progress: ', '')
    score = score.replace('%', '')
    print(timer, score, Mistakes)

    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()

    import datetime
    Date = datetime.date.today().strftime('%Y-%m-%d')
    Time = datetime.datetime.now().time().strftime('%H:%M:%S')
    print(score, timer, Date, Time)

    cursor.execute("select * from sudoku where date = '"+Date+"'")
    result = cursor.fetchall()
    # print(result)
    # if result:
        # cursor.execute("update sudoku set score = ?, timer = ?, mistake = ?, time = ? where date = ?", [score, timer, Mistakes, Time, Date])
        # connection.commit()
    # else:
    cursor.execute("insert into sudoku values(?,?,?,?,?)", [score, timer, Mistakes, Date, Time])
    connection.commit()

    return jsonify({'message': 'Score and Mistakes received'})

@app.route('/update_tetris', methods=['POST'])
def update_tetris():
    data = request.json
    score = data['score']
    level = data['level']
    lines = data['lines']
    print(score, level, lines)
    
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()

    import datetime
    Date = datetime.date.today().strftime('%Y-%m-%d')
    Time = datetime.datetime.now().time().strftime('%H:%M:%S')
    print(score, level, lines, Date, Time)

    cursor.execute("select * from tetris where date = '"+Date+"'")
    result = cursor.fetchall()
    print(result)
    # if result:
    #     cursor.execute("update tetris set score = ?, level = ?, time = ?, line = ? where date = ?", [score, level, Time, lines, Date])
    #     connection.commit()
    # else:
    cursor.execute("insert into tetris values(?,?,?,?,?)", [score, level, lines, Date, Time])
    connection.commit()

    return jsonify({'message': 'Score and level received'})

@app.route('/update_ticktack', methods=['POST'])
def update_ticktack():
    data = request.json
    timer = data['timer']
    wins = data['wins']
    wins = wins.replace('Wins: ', '')
    losses = data['losses']
    losses = losses.replace('Losses: ', '')
    ties = data['ties']
    ties = ties.replace('Ties: ', '')

    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()

    import datetime
    Date = datetime.date.today().strftime('%Y-%m-%d')
    Time = datetime.datetime.now().time().strftime('%H:%M:%S')
    print(timer, wins, losses, ties, Date, Time)

    cursor.execute("select * from ticktack where date = '"+Date+"'")
    result = cursor.fetchall()
    print(result)
    # if result:
    #     cursor.execute("update ticktack set timer = ?, wins = ?, losses = ?, ties = ?, time = ? where date = ?", [timer, wins, losses, ties, Time, Date])
    #     connection.commit()
    # else:
    cursor.execute("insert into ticktack values(?,?,?,?,?,?)", [timer, wins, losses, ties, Date, Time])
    connection.commit()

    return jsonify({'message': 'timer, wins, losses and ties received'})

@app.route('/update_hanoi', methods=['POST'])
def update_hanoi():
    data = request.json
    moves = data['moves']
    moves = moves.replace('Moves: ', '')
    timer = data['timer']
    timer = timer.replace('Time: ', '')
    
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()

    import datetime
    Date = datetime.date.today().strftime('%Y-%m-%d')
    Time = datetime.datetime.now().time().strftime('%H:%M:%S')
    print(moves, timer, Date, Time)

    cursor.execute("select * from hanoi where date = '"+Date+"'")
    result = cursor.fetchall()
    print(result)
    # if result:
    #     cursor.execute("update hanoi set moves = ?, timer = ?, time = ? where date = ?", [moves, timer, Time, Date])
    #     connection.commit()
    # else:
    cursor.execute("insert into hanoi values(?,?,?,?)", [moves, timer, Date, Time])
    connection.commit()

    return jsonify({'message': 'moves and timer received'})

@app.route('/update_whackmole', methods=['POST'])
def update_whackmole():
    data = request.json
    score = data['score']
    accuracy = data['accuracy']
    accuracy = accuracy.replace('%', '')
    reactionTime = data['reactionTime']
    reactionTime = reactionTime.replace('s', '')
    duration = data['duration']
    duration = duration.replace('DURATION: ', '')

    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()

    import datetime
    Date = datetime.date.today().strftime('%Y-%m-%d')
    Time = datetime.datetime.now().time().strftime('%H:%M:%S')
    
    print(score, accuracy, reactionTime, duration, Date, Time)

    cursor.execute("select * from whackhole where date = '"+Date+"'")
    result = cursor.fetchall()
    print(result)
    # if result:
    #     cursor.execute("update whackhole set score = ?, accuracy = ?, reactionTime = ?, duration = ?, time = ? where date = ?", [score, accuracy, reactionTime, duration, Time, Date])
    #     connection.commit()
    # else:
    cursor.execute("insert into whackhole values(?,?,?,?,?,?)", [score, accuracy, reactionTime, duration, Date, Time])
    connection.commit()

    return jsonify({'message': 'data received'})

@app.route('/logout')
def logout():
    return render_template('index.html')

@app.route('/get_pattern_graph1')
def get_pattern_graph1():
    print(session['user'])
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from pattern')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[0])))
    return jsonify([labels1, data1])

@app.route('/get_pattern_graph2')
def get_pattern_graph2():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from pattern')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[1].replace(':',''))))
    return jsonify([labels1, data1])

@app.route('/get_pattern_graph3')
def get_pattern_graph3():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from pattern')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[2].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_pattern_graph4')
def get_pattern_graph4():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from pattern')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[3].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_pattern_graph5')
def get_pattern_graph5():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from pattern')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[5])
        data1.append(int(float(i[0])))
    return jsonify([labels1, data1])

@app.route('/get_pattern_graph6')
def get_pattern_graph6():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from pattern')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[5])
        data1.append(int(float(i[1].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_pattern_graph7')
def get_pattern_graph7():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from pattern')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[5])
        data1.append(int(float(i[2].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_pattern_graph8')
def get_pattern_graph8():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from pattern')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[5])
        data1.append(int(float(i[3].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_hanoi_graph1')
def get_hanoi_graph1():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from hanoi')
    result = cursor.fetchall()
    print(result)
    for i in result:
        labels1.append(i[2])
        data1.append(int(float(i[0])))
    return jsonify([labels1, data1])

@app.route('/get_hanoi_graph2')
def get_hanoi_graph2():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from hanoi')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[2])
        data1.append(int(float(i[1].replace(':',''))))
    return jsonify([labels1, data1])

@app.route('/get_hanoi_graph3')
def get_hanoi_graph3():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from hanoi')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[3])
        data1.append(int(float(i[0])))
    return jsonify([labels1, data1])

@app.route('/get_hanoi_graph4')
def get_hanoi_graph4():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from hanoi')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[3])
        data1.append(int(float(i[1].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_tetris_graph1')
def get_tetris_graph1():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from tetris')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[3])
        data1.append(int(float(i[0])))
    return jsonify([labels1, data1])

@app.route('/get_tetris_graph2')
def get_tetris_graph2():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from tetris')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[3])
        data1.append(int(float(i[1])))
    return jsonify([labels1, data1])

@app.route('/get_tetris_graph3')
def get_tetris_graph3():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from tetris')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[3])
        data1.append(int(float(i[2].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_tetris_graph4')
def get_tetris_graph4():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from tetris')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[0].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_tetris_graph5')
def get_tetris_graph5():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from tetris')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[1].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_tetris_graph6')
def get_tetris_graph6():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from tetris')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[2].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_sudoku_graph1')
def get_sudoku_graph1():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from sudoku')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[3])
        data1.append(int(float(i[0])))
    return jsonify([labels1, data1])

@app.route('/get_sudoku_graph2')
def get_sudoku_graph2():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from sudoku')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[3])
        data1.append(int(float(i[1].replace(':',''))))
    return jsonify([labels1, data1])

@app.route('/get_sudoku_graph3')
def get_sudoku_graph3():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from sudoku')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[3])
        data1.append(int(float(i[2].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_sudoku_graph4')
def get_sudoku_graph4():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from sudoku')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[0].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_sudoku_graph5')
def get_sudoku_graph5():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from sudoku')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[1].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_sudoku_graph6')
def get_sudoku_graph6():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from sudoku')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[2].replace(':', ''))))
    return jsonify([labels1, data1])


@app.route('/get_ticktack_graph1')
def get_ticktack_graph1():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from ticktack')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[0].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_ticktack_graph2')
def get_ticktack_graph2():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from ticktack')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[1])))
    return jsonify([labels1, data1])

@app.route('/get_ticktack_graph3')
def get_ticktack_graph3():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from ticktack')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[2].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_ticktack_graph4')
def get_ticktack_graph4():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from ticktack')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[3].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_ticktack_graph5')
def get_ticktack_graph5():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from ticktack')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[5])
        data1.append(int(float(i[0].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_ticktack_graph6')
def get_ticktack_graph6():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from ticktack')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[5])
        data1.append(int(float(i[1].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_ticktack_graph7')
def get_ticktack_graph7():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from ticktack')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[5])
        data1.append(int(float(i[2].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_ticktack_graph8')
def get_ticktack_graph8():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from ticktack')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[5])
        data1.append(int(float(i[3].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_whackhole_graph1')
def get_whackhole_graph1():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from whackhole')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[0])))
    return jsonify([labels1, data1])

@app.route('/get_whackhole_graph2')
def get_whackhole_graph2():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from whackhole')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[1])))
    return jsonify([labels1, data1])

@app.route('/get_whackhole_graph3')
def get_whackhole_graph3():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from whackhole')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[2].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_whackhole_graph4')
def get_whackhole_graph4():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from whackhole')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[4])
        data1.append(int(float(i[3].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_whackhole_graph5')
def get_whackhole_graph5():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from whackhole')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[5])
        data1.append(int(float(i[0].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_whackhole_graph6')
def get_whackhole_graph6():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from whackhole')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[5])
        data1.append(int(float(i[1].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_whackhole_graph7')
def get_whackhole_graph7():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from whackhole')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[5])
        data1.append(int(float(i[2].replace(':', ''))))
    return jsonify([labels1, data1])

@app.route('/get_whackhole_graph8')
def get_whackhole_graph8():
    connection = sqlite3.connect(session['user']+'.db')
    cursor = connection.cursor()
    labels1 = []
    data1 = []
    cursor.execute('select * from whackhole')
    result = cursor.fetchall()
    for i in result:
        labels1.append(i[5])
        data1.append(int(float(i[3].replace(':', ''))))
    return jsonify([labels1, data1])

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

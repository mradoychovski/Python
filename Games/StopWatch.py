import simplegui

# template for "Stopwatch: The Game"
# http://www.codeskulptor.org/#user23_NTjIwI79CX_1.py

# define global variables
height = 200
width = 200
t = 0
tenths = 0
triger = "0:00.0"
stops = 0
wins = 0
score = "0/0"
percent = "0%"
switch = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global triger, tenths, percent, score
    minutes = t / 600
    seconds = t / 10 - minutes * 600
    tenths = t - (minutes * 600 + seconds * 10)
    triger = "%d:%02d.%d" %(minutes, seconds, tenths)
    score = "%d/%d" %(wins, stops)
    if stops != 0:
        percent = str(int((1.0*wins / stops)*100)) + "%"
       
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global switch
    timer.start()
    switch = True

def stop():
    global stops, wins, switch
    if tenths == 0 and switch:
        stops += 1
        wins += 1
    elif switch:
        stops += 1
    timer.stop()
    switch = False
    format(t)
    
def reset():
    global t, wins, stops, percent
    timer.stop()
    t = 0
    wins = 0
    stops = 0
    percent = "0%"
    score = "%d / %d" %(wins, stops)
    switch = False
    format(t)

# define event handler for timer with 0.1 sec interval
def update():
    global t
    t += 1
    format(t)
    if t == 6000:
        timer.stop()
    
# define draw handler
def draw(canvas):
    canvas.draw_text(percent, (height/20, (height+width)/15), (height+width)/22, 'Green')
    canvas.draw_text(score, (height/1.25, (height+width)/15), (height+width)/22, 'Green')
    canvas.draw_text(triger, (height/4, (height+width)/4), (height+width)/10, 'Red')
    
# create frame
frame = simplegui.create_frame('Stopwatch', height, width)

# register event handlers
frame.set_draw_handler(draw)
button1 = frame.add_button('Start', start, 200)
button2 = frame.add_button('Stop', stop, 200)
button3 = frame.add_button('Reset', reset, 200)
timer = simplegui.create_timer(100, update)

# start frame
frame.start()

# Please remember to review the grading rubric

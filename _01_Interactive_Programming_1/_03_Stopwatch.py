""" STOPWATCH: Our mini-project for this week will focus on combining text drawing in the canvas with timers to build a simple digital stopwatch that keeps track of the time in tenths of a second. """
# use following link to test the program in 'codeskulptor': http://www.codeskulptor.org/#user45_rFwBq1QGls_4.py

try:
    import simplegui  # access to drawing operations for interactive applications
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui  # CodeSkulptor GUI module stand alone version


# define global variables
game_running = False  # this VARIABLE is just to avoid false counter updates when we press the 'stop' button
count = 0
count_hits = 0
count_total = 0


# define helper function format that converts time in tenths of seconds into formatted string A:BC.D
def format(t):  # some testing code can be found here: http://www.codeskulptor.org/#user44_3D4nahojKF_0.py
    global count_hits
    A = t // 600
    B = (t % 600) // 100
    C = (t % 100) // 10
    D = t % 10
    return str(A) + ":" +str(B) + str(C) + "." + str(D)  # the whole stopwatch has to be split to a single DIGITS, because the stopwatch display is of a fixed size


# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global game_running
    timer.start()
    game_running = True

def stop():
    global game_running, count_hits,  count_total
    if game_running == True:
        timer.stop()
        game_running = False
        count_total += 1
        if count % 10 == 0:
            count_hits += 1

def reset():
    global game_running, count, count_hits, count_total
    timer.stop()
    game_running = False
    count = 0; count_hits = 0; count_total = 0


# define event handler for timer with 0.1 sec interval
def tick():
    global count
    count += 1


# define draw handler
def draw(canvas):
    canvas.draw_text(str(format(count)), [100, 110], 44, 'White')
    canvas.draw_text(str(count_hits) + "/" + str(count_total), [220, 40], 30, 'Green')


# create frame and timer
frame = simplegui.create_frame("Stopwatch: The Game", 300, 200)
timer = simplegui.create_timer(100, tick)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button("Start", start, 150)
frame.add_button("Stop", stop, 150)
frame.add_button("Reset", reset, 150)

# start frame
frame.start()

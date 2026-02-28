from flask import Flask, render_template
from flask_socketio import SocketIO
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)

def minütliche_erinnerungen(e):
    while e > 0:
        time.sleep(60)
        e -= 60
        if e > 0:
            socketio.emit("erinnerung", {"nachricht": f"Noch {int(e // 60)} Minuten übrig"})
        else:
            socketio.emit("erinnerung", {"nachricht": "Zeit ist um, du musst raus!"})

def timer_logik(ges_dauer_min):
    t0 = ges_dauer_min * 60
    x = t0

    delta1 = round(t0 - (t0 * 0.75))
    time.sleep(delta1)
    a = x - delta1
    socketio.emit("erinnerung", {"nachricht": f"Noch {int(t0*0.75 // 60)} Minuten übrig"})

    if a <= 600:
        minütliche_erinnerungen(a)
        return

    delta2 = round((a) - (a * 0.666))
    time.sleep(delta2)
    b = a - delta2
    socketio.emit("erinnerung", {"nachricht": f"Noch {int(b // 60)} Minuten übrig"})

    if b <= 600:
        minütliche_erinnerungen(b)
        return

    delta3 = round(b - (b * 0.666))
    time.sleep(delta3)
    c = b - delta3
    socketio.emit("erinnerung", {"nachricht": f"Noch {int(c // 60)} Minuten übrig"})

    if c <= 600:
        minütliche_erinnerungen(c)
        return

    delta4 = round(c - (c * 0.75))
    time.sleep(delta4)
    d = c - delta4
    socketio.emit("erinnerung", {"nachricht": f"Noch {int(d // 60)} Minuten übrig"})

    if d <= 600:
        minütliche_erinnerungen(d)
        return

    delta5 = round(d - (d * 0.666))
    time.sleep(delta5)
    e = round(d - delta5)
    socketio.emit("erinnerung", {"nachricht": f"Noch {int(e // 60)} Minuten übrig"})

    if e <= 600:
        minütliche_erinnerungen(e)
        return

    while e > 600:
        time.sleep(60)
        e -= 60

    while e > 0:
        time.sleep(60)
        e -= 60
        if e > 0:
            socketio.emit("erinnerung", {"nachricht": f"Noch {int(e // 60)} Minuten übrig"})
        else:
            socketio.emit("erinnerung", {"nachricht": "Zeit ist um, du musst raus!"})

@socketio.on("start_timer")
def handle_start(data):
    minuten = int(data["minuten"])
    thread = threading.Thread(target=timer_logik, args=(minuten,))
    thread.start()

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000, allow_unsafe_werkzeug=True)
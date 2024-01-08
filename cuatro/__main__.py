import frontend as UI
import frontend.gameplay as gameplay
import frontend.gamepause as gamepause
import frontend.gameover as gameover
import frontend.mainmenu as mainmenu
import engine

evb = engine.EventBus()
ui = UI.Core(evb)
game = None


class Game:
    _fend = None
    _fend_pause = None
    _engine = None
    _uint = None
    _ev_bus = None
    _paces = [500, 400, 350, 320, 290, 275, 250, 235, 210, 180, 150]
    _pace = 0

    def __init__(self, ev_bus, ui):
        self._ev_bus = ev_bus
        self._uint = ui
        self._engine = engine.Core(self._ev_bus)
        UI.set_timer(engine.EV_TIMER1, self._paces[self._pace])
        self._fend = gameplay.Screen(ui.display)
        self._fend.connect(ev_bus)
        self.play()

    def set_pace(self, score):
        sco, ln, lvl = score
        if lvl != self._pace:
            self._pace = lvl if lvl < 10 else 10
            UI.set_timer(engine.EV_TIMER1, self._paces[self._pace])

    def play(self):
        if self._fend_pause is not None:
            self._fend_pause.restore()
        self._ev_bus.subscribe(engine.EV_TIMER1, self._engine.step)
        self._ev_bus.subscribe(engine.EV_SCORE_CHANGE, self.set_pace)
        self._uint.key_map({
            UI.K_UP: self._engine.rot_right,
            UI.K_LEFT: self._engine.left,
            UI.K_RIGHT: self._engine.right,
            UI.K_DOWN: self._engine.step,
            UI.K_P: self.pause,
            UI.K_ESCAPE: lambda: self._ev_bus.publish(engine.EV_GAME_ABORT)
        })

    def pause(self):
        self._ev_bus.unsubscribe(engine.EV_TIMER1, self._engine.step)
        self._fend_pause = gamepause.Screen(ui.display)
        self._uint.key_map({
            UI.K_P: self.play
        })

    def end(self):
        self._ev_bus.unsubscribe(engine.EV_SCORE_CHANGE, self.set_pace)
        self._ev_bus.unsubscribe(engine.EV_TIMER1, self._engine.step)
        self._fend.disconnect(self._ev_bus)
        self._uint.key_map({})


def main_menu():
    mainmenu.Screen(ui.display)
    ui.key_map({
        UI.K_N: game_play,
        UI.K_Q: lambda: ui.exit(0)
    })


def game_play():
    global game
    game = Game(evb, ui)


def game_abort():
    global game
    game.end()
    main_menu()


def game_won(score):
    global game
    game.end()
    sco, ln, lvl = score
    print(f"Game won! score: {sco}")
    ui.exit(0)


def game_over(score):
    global game
    game.end()
    gameover.Screen(ui.display)
    sco, ln, lvl = score
    print(f"Game over! score: {sco}, lines: {ln}")
    main_menu()


evb.subscribe(engine.EV_GAME_ABORT, game_abort)
evb.subscribe(engine.EV_GAME_OVER, game_over)
main_menu()

ui.loop()

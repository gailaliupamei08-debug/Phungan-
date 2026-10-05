from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line
from kivy.clock import Clock
from math import sin, cos, radians, hypot
from random import randint


class Galaxy(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.angle = 0
        self.zoom = 1.0
        self.move_x = 0
        self.move_y = 0
        self.touches = {}
        self.old_distance = None
        self.stars = [
            (randint(-600, 600), randint(-1000, 1000), randint(2, 5))
            for _ in range(140)
        ]

        Clock.schedule_interval(self.update, 1 / 30)

    def screen_pos(self, x, y):
        return (
            self.width / 2 + (x + self.move_x) * self.zoom,
            self.height / 2 + (y + self.move_y) * self.zoom
        )

    def update(self, dt):
        self.canvas.clear()

        with self.canvas:
            # Stars
            Color(1, 1, 1, 1)
            for x, y, size in self.stars:
                sx, sy = self.screen_pos(x, y)
                Ellipse(pos=(sx, sy), size=(size, size))

            cx, cy = self.screen_pos(0, 0)

            # Sun
            sun_size = 90 * self.zoom
            Color(1, 0.55, 0.05, 1)
            Ellipse(
                pos=(cx - sun_size / 2, cy - sun_size / 2),
                size=(sun_size, sun_size)
            )

            # Orbits
            Color(0.25, 0.25, 0.25, 1)
            for orbit in (100, 160, 220, 290, 370):
                Line(circle=(cx, cy, orbit * self.zoom), width=1)

            # Mercury
            a = radians(self.angle * 1.5)
            self.draw_planet(cx + cos(a) * 100 * self.zoom,
                             cy + sin(a) * 100 * self.zoom,
                             16 * self.zoom, (0.65, 0.65, 0.65))

            # Earth
            a = radians(self.angle)
            self.draw_planet(cx + cos(a) * 160 * self.zoom,
                             cy + sin(a) * 160 * self.zoom,
                             30 * self.zoom, (0.1, 0.4, 1))

            # Mars
            a = radians(self.angle * 0.7)
            self.draw_planet(cx + cos(a) * 220 * self.zoom,
                             cy + sin(a) * 220 * self.zoom,
                             24 * self.zoom, (0.9, 0.2, 0.1))

            # Jupiter
            a = radians(self.angle * 0.35)
            self.draw_planet(cx + cos(a) * 290 * self.zoom,
                             cy + sin(a) * 290 * self.zoom,
                             50 * self.zoom, (0.8, 0.55, 0.3))

            # Saturn
            a = radians(self.angle * 0.22)
            sx = cx + cos(a) * 370 * self.zoom
            sy = cy + sin(a) * 370 * self.zoom
            self.draw_planet(sx, sy, 44 * self.zoom, (0.85, 0.7, 0.45))
            Color(0.8, 0.7, 0.5, 1)
            Line(
                ellipse=(sx - 38 * self.zoom, sy - 12 * self.zoom,
                         76 * self.zoom, 24 * self.zoom),
                width=3
            )

        self.angle = (self.angle + 1) % 360

    def draw_planet(self, x, y, size, color):
        Color(*color, 1)
        Ellipse(pos=(x - size / 2, y - size / 2),
                size=(size, size))

    def on_touch_down(self, touch):
        self.touches[touch.uid] = touch.pos

        if len(self.touches) == 2:
            points = list(self.touches.values())
            self.old_distance = hypot(
                points[0][0] - points[1][0],
                points[0][1] - points[1][1]
            )

        return True

    def on_touch_move(self, touch):
        old = self.touches.get(touch.uid, touch.pos)

        # Two fingers = zoom
        if len(self.touches) >= 2:
            self.touches[touch.uid] = touch.pos
            points = list(self.touches.values())[:2]
            distance = hypot(
                points[0][0] - points[1][0],
                points[0][1] - points[1][1]
            )

            if self.old_distance and self.old_distance > 0:
                self.zoom *= distance / self.old_distance
                self.zoom = max(0.5, min(self.zoom, 3.0))

            self.old_distance = distance
            return True

        # One finger = move
        dx = touch.x - old[0]
        dy = touch.y - old[1]
        self.move_x += dx / self.zoom
        self.move_y += dy / self.zoom
        self.touches[touch.uid] = touch.pos
        return True

    def on_touch_up(self, touch):
        if touch.uid in self.touches:
            del self.touches[touch.uid]

        if len(self.touches) < 2:
            self.old_distance = None

        return True


class GalaxyApp(App):
    def build(self):
        return Galaxy()


GalaxyApp().run()

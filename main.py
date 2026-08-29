from kivy.clock import Clock
import random
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle


class MyApp(App):
    def build(self):
        self.body = []
        self.tail_widgets = []
        self.direction = "right"
        self.game_running = True

        self.layout = FloatLayout()

        # --- GAME WORLD OUTER WALLS (White) ---

        self.grid1 = Widget(
            size_hint=(None, None),
            size=(20, 820),
            pos=(50, 600)
        )
        with self.grid1.canvas:
            Color(1, 1, 1, 1)
            Rectangle(size=self.grid1.size, pos=self.grid1.pos)

        self.grid2 = Widget(
            size_hint=(None, None),
            size=(20, 820),
            pos=(630, 600)
        )
        with self.grid2.canvas:
            Color(1, 1, 1, 1)
            Rectangle(size=self.grid2.size, pos=self.grid2.pos)

        self.grid3 = Widget(
            size_hint=(None, None),
            size=(600, 20),
            pos=(50, 1420)
        )
        with self.grid3.canvas:
            Color(1, 1, 1, 1)
            Rectangle(size=self.grid3.size, pos=self.grid3.pos)

        self.grid4 = Widget(
            size_hint=(None, None),
            size=(600, 20),
            pos=(50, 600)
        )
        with self.grid4.canvas:
            Color(1, 1, 1, 1)
            Rectangle(size=self.grid4.size, pos=self.grid4.pos)

        # --- CONTROLS AREA BORDERS (Yellow) ---

        self.grid5 = Widget(
            size_hint=(None, None),
            size=(20, 550),
            pos=(50, 50)
        )
        with self.grid5.canvas:
            Color(1, 1, 0, 1)
            Rectangle(size=self.grid5.size, pos=self.grid5.pos)

        self.grid6 = Widget(
            size_hint=(None, None),
            size=(20, 550),
            pos=(630, 50)
        )
        with self.grid6.canvas:
            Color(1, 1, 0, 1)
            Rectangle(size=self.grid6.size, pos=self.grid6.pos)

        self.grid7 = Widget(
            size_hint=(None, None),
            size=(600, 20),
            pos=(50, 50)
        )
        with self.grid7.canvas:
            Color(1, 1, 0, 1)
            Rectangle(size=self.grid7.size, pos=self.grid7.pos)

        # --- PLAYABLE OBJECTS ---

        self.box = Widget(
            size_hint=(None, None),
            size=(40, 40),
            pos=(190, 700)
        )

        with self.box.canvas:
            Color(0, 1, 1, 1)
            self.box_rect = Rectangle(
                size=self.box.size,
                pos=self.box.pos
            )

        self.box.bind(pos=self.update_box_rect)
        
        self.player = Widget(
            size_hint=(None, None),
            size=(40, 40),
            pos=(70, 620)
        )

        with self.player.canvas:
            Color(0, 1, 0, 1)
            self.rect = Rectangle(
                size=self.player.size,
                pos=self.player.pos
            )

        self.player.bind(pos=self.update_rect)

        # --- CONTROLLER BUTTONS ---

        bnt1 = Button(
            text="right",
            size_hint=(None, None),
            size=(100, 100),
            pos=(420, 280)
        )

        bnt2 = Button(
            text="left",
            size_hint=(None, None),
            size=(100, 100),
            pos=(180, 280)
        )

        bnt3 = Button(
            text="up",
            size_hint=(None, None),
            size=(100, 100),
            pos=(300, 390)
        )

        bnt4 = Button(
            text="down",
            size_hint=(None, None),
            size=(100, 100),
            pos=(300, 170)
        )

        bnt1.bind(on_press=lambda instance: self.change_direction("right"))
        bnt2.bind(on_press=lambda instance: self.change_direction("left"))
        bnt3.bind(on_press=lambda instance: self.change_direction("up"))
        bnt4.bind(on_press=lambda instance: self.change_direction("down"))

        # Adding components

        self.layout.add_widget(self.box)
        self.layout.add_widget(self.player)

        self.layout.add_widget(bnt1)
        self.layout.add_widget(bnt2)
        self.layout.add_widget(bnt3)
        self.layout.add_widget(bnt4)

        self.layout.add_widget(self.grid1)
        self.layout.add_widget(self.grid2)
        self.layout.add_widget(self.grid3)
        self.layout.add_widget(self.grid4)
        self.layout.add_widget(self.grid5)
        self.layout.add_widget(self.grid6)
        self.layout.add_widget(self.grid7)

        Clock.schedule_interval(self.auto_move, 0.2)

        return self.layout
        
    def update_box_rect(self, instance, value):
        self.box_rect.pos = value
        
    def change_direction(self, direction):
        self.direction = direction

    def auto_move(self, dt):
        if self.game_running:
            self.move(self.direction)
    
    def update_rect(self, instance, value):
        self.rect.pos = value

    def reset_game(self):
        self.player.pos = (70, 620)
        self.box.pos = (190, 700)
        self.direction = "right"
        self.game_running = True

        for widget in self.tail_widgets:
            self.layout.remove_widget(widget)

        self.tail_widgets.clear()
        self.body.clear()

    def reset_from_popup(self, popup):
        popup.dismiss()
        self.reset_game()

    def move(self, direction):

        # Store positions BEFORE anything moves
        pre_pos = [list(self.player.pos)]

        for w in self.body:
            pre_pos.append(list(w.pos))

        # Calculate player's next position
        next_x = self.player.x
        next_y = self.player.y

        if direction == "right":
            next_x += 40
        elif direction == "left":
            next_x -= 40
        elif direction == "up":
            next_y += 40
        elif direction == "down":
            next_y -= 40

        # Boundary collision
        if (
            next_x < 70
            or next_x > 590
            or next_y < 620
            or next_y > 1380
        ):
            self.game_over()
            return
            
      
        # Self-collision
        for segment in self.body:
            if next_x == segment.x and next_y == segment.y:
                self.game_over()
                return

        # Move player
        self.player.pos = (next_x, next_y)

        # Move body segments
        for i in range(len(self.body)):
            self.body[i].pos = pre_pos[i]

        # Collect box
        if self.player.pos == self.box.pos:

            if self.body:
                position = pre_pos[-1]
            else:
                position = pre_pos[0]

            tail = Widget(
                size_hint=(None, None),
                size=(40, 40),
                pos=position
            )

            with tail.canvas:
                Color(0, 0, 1, 1)
                tract = Rectangle(
                    size=tail.size,
                    pos=tail.pos
                )

            # Bind position updates to the canvas rectangle
            tail.bind(pos=lambda inst, val: setattr(tract, "pos", val))

            self.layout.add_widget(tail)
            self.tail_widgets.append(tail)
            self.body.append(tail)
            
            x = random.randint(0, 13) * 40 + 70
            y = random.randint(0, 19) * 40 + 620
            self.box.pos = (x, y)

    def game_over(self):
        self.game_running = False

        content = FloatLayout()

        message = Label(
            text="YOU LOSE!",
            font_size=40,
            size_hint=(1, None),
            height=100,
            pos_hint={"x": 0, "top": 1}
        )

        reset_button = Button(
            text="Game Reset",
            size_hint=(0.6, 0.25),
            pos_hint={"center_x": 0.5, "y": 0.15}
        )

        content.add_widget(message)
        content.add_widget(reset_button)

        popup = Popup(
            title="Game Over",
            content=content,
            size_hint=(0.7, 0.4),
            auto_dismiss=False
        )

        reset_button.bind(
            on_press=lambda instance: self.reset_from_popup(popup)
        )

        popup.open()


if __name__ == '__main__':
    MyApp().run()
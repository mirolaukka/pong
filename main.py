import tkinter as tk
import random


class Ball:
    def __init__(self, canvas_size, canvas, size):
        self.canvas = canvas
        self.size = size
        self.canvas_width, self.canvas_height = canvas_size
        canvas_center_x = self.canvas_width // 2
        canvas_center_y = self.canvas_height // 2
        self.id = canvas.create_oval(canvas_center_x - size // 2, canvas_center_y - size //
                                     2, canvas_center_x + size // 2, canvas_center_y + size // 2, fill="white")
        self.speed_x = 3
        self.speed_y = 3

    def reset(self):
        # returns -> 0 | self.canvas.winfo_width() returns 1
        canvas_center_x = self.canvas_width // 2
        # returns -> 0 | self.canvas.winfo_height() returns 1
        canvas_center_y = self.canvas_height // 2
        self.canvas.coords(self.id, canvas_center_x - self.size // 2, canvas_center_y - self.size // 2,
                           canvas_center_x + self.size // 2, canvas_center_y + self.size // 2)
        self.speed_x = 3
        self.speed_y = 3

    def move(self):
        self.canvas.move(self.id, self.speed_x, self.speed_y)
        pos = self.canvas.coords(self.id)

        if pos[0] <= 0 or pos[2] >= self.canvas.winfo_width():
            self.speed_x *= -1
        if pos[1] <= 0 or pos[3] >= self.canvas.winfo_height():
            self.speed_y *= -1

    def set_speed_x(self, speed):
        self.speed_x = speed

    def set_speed_y(self, speed):
        self.speed_y = speed

    def get_bbox(self):
        return self.canvas.coords(self.id)


class Paddle:
    def __init__(self, canvas, x, y, width, height):
        self.canvas = canvas
        self.id = canvas.create_rectangle(
            x, y, x + width, y + height, fill="white")
        self.speed = 0

    def move(self):
        self.canvas.move(self.id, 0, self.speed)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0 or pos[3] >= self.canvas.winfo_height():
            self.speed = 0

    def set_speed(self, speed):
        self.speed = speed

    def get_bbox(self):
        return self.canvas.coords(self.id)


class Score:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.score = 0
        self.id = canvas.create_text(
            x, y, text=f"Score: {self.score}", fill="white", font=("Arial", 18))

    def update(self):
        self.canvas.itemconfig(self.id, text=f"Score: {self.score}")

    def reset(self):
        self.score = 0
        self.update()


class GameController:
    def __init__(self, canvas, paddle_a, paddle_b, ball, score_a, score_b, canvas_size):
        self.canvas = canvas
        self.paddle_a = paddle_a
        self.paddle_b = paddle_b
        self.ball = ball
        self.score_a = score_a
        self.score_b = score_b
        self.PADDLE_SPEED = 2.75

        self.canvas_width, self.canvas_height = canvas_size

        self.paddle_a_speed = 0
        self.paddle_b_speed = 0

        # Reset both scores to 0 before starting the game
        self.score_a.reset()
        self.score_b.reset()

        self.canvas.bind(
            "<KeyPress-w>", lambda event: self.paddle_a.set_speed(-self.PADDLE_SPEED))
        self.canvas.bind(
            "<KeyPress-s>", lambda event: self.paddle_a.set_speed(self.PADDLE_SPEED))
        self.canvas.bind("<KeyRelease-w>",
                         lambda event: self.paddle_a.set_speed(0))
        self.canvas.bind("<KeyRelease-s>",
                         lambda event: self.paddle_a.set_speed(0))
        self.canvas.bind(
            "<KeyPress-Up>", lambda event: self.paddle_b.set_speed(-self.PADDLE_SPEED))
        self.canvas.bind(
            "<KeyPress-Down>", lambda event: self.paddle_b.set_speed(self.PADDLE_SPEED))
        self.canvas.bind("<KeyRelease-Up>",
                         lambda event: self.paddle_b.set_speed(0))
        self.canvas.bind("<KeyRelease-Down>",
                         lambda event: self.paddle_b.set_speed(0))

    def check_ball_paddle_collision(self):
        if self.intersect(self.ball.get_bbox(), self.paddle_a.get_bbox()):
            self.ball.set_speed_x(abs(self.ball.speed_x))
        elif self.intersect(self.ball.get_bbox(), self.paddle_b.get_bbox()):
            self.ball.set_speed_x(-abs(self.ball.speed_x))

    def check_ball_out_of_bounds(self):
        pos = self.ball.get_bbox()
        if pos[0] <= 0:
            self.score_b.score += 1
            self.score_b.update()
            self.reset_ball()
        elif pos[2] >= self.canvas_width:
            self.score_a.score += 1
            self.score_a.update()
            self.reset_ball()

    def reset_ball(self):
        self.ball.reset()
        # Randomize initial direction
        self.ball.set_speed_x(random.choice([3, -3]))
        # Randomize initial direction
        self.ball.set_speed_y(random.choice([3, -3]))

    def move_ball(self):
        self.ball.move()
        self.check_ball_paddle_collision()
        self.check_ball_out_of_bounds()

    def update(self):
        self.move_ball()
        self.move_paddles()
        self.canvas.after(16, self.update)

    def intersect(self, box1, box2):
        x1, y1, x2, y2 = box1
        x3, y3, x4, y4 = box2
        return not (x2 < x3 or x1 > x4 or y2 < y3 or y1 > y4)

    def move_paddles(self):
        self.paddle_a.move()
        self.paddle_b.move()


class PongGame:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.PADDLE_WIDTH = 10
        self.PADDLE_HEIGHT = 80
        self.BALL_SIZE = 15

        self.root = tk.Tk()
        self.root.title("Pong Game")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.canvas = tk.Canvas(
            self.root, width=self.WIDTH, height=self.HEIGHT, bg="black")
        self.canvas.pack()

        self.paddle_a = Paddle(self.canvas, 50, self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2,
                               self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.paddle_b = Paddle(self.canvas, self.WIDTH - 50 - self.PADDLE_WIDTH, self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2,
                               self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.ball = Ball((self.WIDTH, self.HEIGHT), self.canvas,
                         self.BALL_SIZE)  # Corrected argument

        self.score_a = Score(self.canvas, 100, 50)
        self.score_b = Score(self.canvas, self.WIDTH - 100, 50)

        self.game_controller = GameController(
            self.canvas, self.paddle_a, self.paddle_b, self.ball, self.score_a, self.score_b, (self.WIDTH, self.HEIGHT))

        # Bind key presses to paddle movements
        self.root.bind(
            "<KeyPress-w>", lambda event: self.paddle_a.set_speed(-self.game_controller.PADDLE_SPEED))
        self.root.bind(
            "<KeyPress-s>", lambda event: self.paddle_a.set_speed(self.game_controller.PADDLE_SPEED))
        self.root.bind("<KeyRelease-w>",
                       lambda event: self.paddle_a.set_speed(0))
        self.root.bind("<KeyRelease-s>",
                       lambda event: self.paddle_a.set_speed(0))
        self.root.bind(
            "<KeyPress-Up>", lambda event: self.paddle_b.set_speed(-self.game_controller.PADDLE_SPEED))
        self.root.bind(
            "<KeyPress-Down>", lambda event: self.paddle_b.set_speed(self.game_controller.PADDLE_SPEED))
        self.root.bind("<KeyRelease-Up>",
                       lambda event: self.paddle_b.set_speed(0))
        self.root.bind("<KeyRelease-Down>",
                       lambda event: self.paddle_b.set_speed(0))

    def start_game(self):
        self.canvas.pack()  # Pack the canvas first
        self.ball.reset()   # Call reset() after the canvas is displayed
        self.game_controller.update()
        self.root.mainloop()


if __name__ == "__main__":
    # Constants
    WIDTH = 600
    HEIGHT = 400

    game = PongGame(WIDTH, HEIGHT)
    game.start_game()

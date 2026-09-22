import random
import tkinter as tk


class SnakeGame:
	def __init__(self, root):
		self.root = root
		self.root.title("Snake")
		self.root.resizable(False, False)

		self.cell_size = 20
		self.columns = 30
		self.rows = 20
		self.width = self.columns * self.cell_size
		self.height = self.rows * self.cell_size

		self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 14))
		self.score_label.pack(pady=5)

		self.canvas = tk.Canvas(
			root, width=self.width, height=self.height, bg="#111111", highlightthickness=0
		)
		self.canvas.pack()
		self.root.bind("<KeyPress>", self.change_direction)

		self.start_game()

	def start_game(self):
		self.snake = [(10, 10), (9, 10), (8, 10)]
		self.direction = (1, 0)
		self.next_direction = self.direction
		self.score = 0
		self.game_over = False
		self.food = self.new_food()
		self.score_label.config(text="Score: 0")
		self.update()

	def new_food(self):
		available = [
			(x, y)
			for x in range(self.columns)
			for y in range(self.rows)
			if (x, y) not in self.snake
		]
		return random.choice(available)

	def change_direction(self, event):
		if self.game_over:
			if event.keysym.lower() == "r":
				self.start_game()
			return

		directions = {
			"up": (0, -1), "w": (0, -1),
			"down": (0, 1), "s": (0, 1),
			"left": (-1, 0), "a": (-1, 0),
			"right": (1, 0), "d": (1, 0),
		}
		new_direction = directions.get(event.keysym.lower())
		if new_direction and new_direction != (-self.direction[0], -self.direction[1]):
			self.next_direction = new_direction

	def update(self):
		if self.game_over:
			self.draw()
			self.canvas.create_text(
				self.width // 2,
				self.height // 2,
				text=f"Game Over\nScore: {self.score}\nPress R to restart",
				fill="white",
				font=("Arial", 20, "bold"),
				justify="center",
			)
			return

		self.direction = self.next_direction
		head_x, head_y = self.snake[0]
		new_head = (head_x + self.direction[0], head_y + self.direction[1])

		hit_wall = not (0 <= new_head[0] < self.columns and 0 <= new_head[1] < self.rows)
		hit_self = new_head in self.snake[:-1]
		if hit_wall or hit_self:
			self.game_over = True
			self.update()
			return

		self.snake.insert(0, new_head)
		if new_head == self.food:
			self.score += 1
			self.score_label.config(text=f"Score: {self.score}")
			self.food = self.new_food()
		else:
			self.snake.pop()

		self.draw()
		self.root.after(max(50, 140 - self.score * 3), self.update)

	def draw(self):
		self.canvas.delete("all")
		x, y = self.food
		self.canvas.create_oval(
			x * self.cell_size + 2, y * self.cell_size + 2,
			(x + 1) * self.cell_size - 2, (y + 1) * self.cell_size - 2,
			fill="#e74c3c", outline=""
		)
		for index, (x, y) in enumerate(self.snake):
			color = "#2ecc71" if index == 0 else "#27ae60"
			self.canvas.create_rectangle(
				x * self.cell_size + 1, y * self.cell_size + 1,
				(x + 1) * self.cell_size - 1, (y + 1) * self.cell_size - 1,
				fill=color, outline="#111111"
			)


if __name__ == "__main__":
	root = tk.Tk()
	SnakeGame(root)
	root.mainloop()
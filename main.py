import pygubu, time
import tkinter as tk
from PIL import Image, ImageTk
from BotPresensi import BotPresensi

class App:
	def __init__(self):
		self.builder = pygubu.Builder()
		self.builder.add_from_file("App.ui")

		self.mainwindow = self.builder.get_object('mainwindow')
		self.tklabel = self.builder.get_object('label_3')

		self.Eusername = self.builder.get_object('e_username')
		self.Epassword = self.builder.get_object('e_password')

		width    = 320
		height   = 480
		scx      = (self.mainwindow.winfo_screenwidth() // 2 ) - (width // 2)
		scy      = (self.mainwindow.winfo_screenheight() // 2 ) - (height // 2)
		self.mainwindow.geometry('{}x{}+{}+{}'.format(width, height, scx, scy))
		self.mainwindow.iconbitmap(r'icon.ico')
		self.builder.connect_callbacks(self)

		self.default_label = ""
		self.tklabel.configure(text=self.default_label)

		canvas  = self.builder.get_object('canvas_1')
		self.img = ImageTk.PhotoImage(Image.open("logo.png"))
		canvas.create_image(0,0, image=self.img, anchor='nw')

	def on_quit_click(self):
		self.bot_run = False
		self.mainwindow.quit()
	def frame_mapped(self,e):
		self.mainwindow.update_idletasks()
		self.mainwindow.overrideredirect(1)
		self.mainwindow.state('normal')
	def do_minimize(self):
		self.mainwindow.update_idletasks()
		self.mainwindow.overrideredirect(0)
		self.mainwindow.state('iconic')

	def on_start_click(self):
		self.username = self.Eusername.get()
		self.password = self.Epassword.get()
		bot_run = True
		bot 	= BotPresensi(self.username, self.password)

		if bot.doLogin():
			output = "Login Success."
			self.updateLabel(output)

			bot.getEvents()
			self.updateLabel("Grabbing Events ...")
			for i in bot.events:
				now 	= bot.getDateTime()
				i_url 	= i[0]
				i_time	= i[1]
				while bot_run:
					if now >= i_time:
						bot.doLogin()
						bot.doPresensi(i_url)

						self.updateLabel("{}:{} submitted.".format(i_time.hour, i_time.minute))
						break
					else:
						self.updateLabel("Waiting for submit {}:{} != {}:{}".format(now.hour, now.minute, i_time.hour, i_time.minute))
			self.updateLabel("Task for today is done.")
		else:
			output = "Failed User/Pass."
			self.updateLabel(output)
	def on_stop_click(self):
		self.bot_run = False
		self.updateLabel("Bot Stopped.")

	def updateLabel(self, newtext):
		self.tklabel.configure(text = newtext)
		self.mainwindow.update()

	def on_info_button(self):
		about = 'Coded by FilthyRoot\nInstagram : @gtx666ti\nJogjakarta Hacker Link (c) 2020'
		self.tklabel.configure(text=about)
		self.mainwindow.update_idletasks()
		time.sleep(1)
		self.tklabel.configure(text=self.default_label)
		self.mainwindow.update()

	def start_move(self, event):
		self.x = event.x
		self.y = event.y

	def stop_move(self, event):
		self.x = None
		self.y = None

	def do_move(self, event):
		deltax = event.x - self.x
		deltay = event.y - self.y

		x = self.mainwindow.winfo_x() + deltax
		y = self.mainwindow.winfo_y() + deltay

		self.mainwindow.geometry(f"+{x}+{y}")

	def run(self):
		self.mainwindow.mainloop()


if __name__ == '__main__':
	app  = App()
	app.run()

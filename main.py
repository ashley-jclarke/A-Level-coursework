# main.py

from CreatureBuildTool.window import MainWindow
from WindowManager.main import Main
from WindowManager.window import Window

def main():
	runner = Main()
	w = MainWindow()
	runner.add_window(w)
	runner.run()
	

if __name__=="__main__":
	main()

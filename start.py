from main import *
from preference import *


config = Config()
main = MainWindow(config=config.get_config())
main.run()

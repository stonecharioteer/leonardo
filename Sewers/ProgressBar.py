from PyQt4.QtGui import QProgressBar

class ProgressBar(QProgressBar):
	def __init__(self):
		super(ProgressBar,self).__init__()
		progress_bar_style = """
            QProgressBar {
                 border: 0.5px solid black;
                 border-radius: 5px;
                 text-align: center;
             }

            QProgressBar::chunk {
                 background-color: #0088D6;
                 width: 20px;
             }""" #05B8CC
		self.setStyleSheet(progress_bar_style)

		pass
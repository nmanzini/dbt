

import get_urls
import image_downloader
import set_image


import sys, os
from PyQt5.QtWidgets import QSlider, QFrame, QMessageBox, QVBoxLayout, QLabel, QWidget, QToolTip, QPushButton, QApplication, QLineEdit
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QFont, QIcon, QPixmap



# pictures folder path in current working directory (cwd)
FOLDER_PATH = os.getcwd() + "\\pictures\\"

# number of pages to go through (up to 25 pictures per page)
PAGES = 2

# determines method of sorting
SORTING = "top"


# time period for links
TIME_PERIOD = "all"

image_downloader.check_folder(FOLDER_PATH)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Desktop Background Tool 0.1')
        self.setWindowIcon(QIcon('icon.png'))

        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        # Separator definition
        self.separator = QFrame()
        self.separator.setFrameStyle(QFrame.HLine)


        # SUBREDDIT AREA --------------------------------------------------------------
        self.subreddit_label = QLabel('Subreddit(s)')
        self.subreddit_input = QLineEdit('EarthPorn+wallpapers')
        self.subreddit_download = QPushButton('Download')
        self.subreddit_download.setToolTip('Click here to download the <b>subreddit</b> images to your pc')
        self.subreddit_input.setToolTip('Write the <b>subreddit</b> you want to download from. Concatenate with a +')

        # button action



        self.subreddit_download.clicked.connect(lambda: download(self.subreddit_input.text()))

        # Vertical Layout for the subreddit part
        vl_subreddit = QVBoxLayout()
        vl_subreddit.addWidget(self.subreddit_label)
        vl_subreddit.addWidget(self.subreddit_input)
        vl_subreddit.addWidget(self.subreddit_download)

        # PERIOD AREA------------------------------------------------------------------
        self.period = 2

        self.period_label = QLabel('Change image every '+str(self.period)+' seconds.')

        self.period_slider = QSlider(Qt.Horizontal)
        self.period_slider.setMinimum(1)
        self.period_slider.setMaximum(60)
        self.period_slider.setTickPosition(10)
        self.period_slider.setTickInterval(20)
        self.period_slider.setValue(self.period)
        self.period_slider.setToolTip('Time that pass between a background to the next')

        self.period_set = QPushButton('Set')


        # control if slider changes value
        self.period_slider.valueChanged.connect(self.v_change)

        images_list = [file for file in os.listdir(FOLDER_PATH)]
        self.period_set.clicked.connect(self.set_background, 2)



        # Vertical Layout for the period part
        vl_period = QVBoxLayout()
        vl_period.addWidget(self.period_label)
        vl_period.addWidget(self.period_slider)
        vl_period.addWidget(self.period_set)

        # BOTTOM IMAGE AREA-------------------------------------------------------------
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap('icon.png'))
        self.logo.setGeometry(50, 50, 50, 50)

        # MAIN LAYOUT ------------------------------------------------------------------
        vl_main = QVBoxLayout()
        vl_main.addLayout(vl_subreddit)
        vl_main.addWidget(self.separator)
        vl_main.addLayout(vl_period)
        vl_main.addStretch(1)
        vl_main.addWidget(self.logo)

        self.setLayout(vl_main)

        self.show()


    def v_change(self):
        '''
        change values of label based on slider
        '''
        self.period = str(self.period_slider.value())
        self.period_label.setText('Change image every ' + self.period + ' seconds.')


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit Confirmation', "Are you sure to quit?\nThe desktop will stop updating.",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def set_background(self):
        '''
        takes the value of the slider 'period_slider'
        starts a thread with that variable         
        '''
        # gets period straight from slider
        period = self.period_slider.value()
        # debugging text
        print('set cliked','Period = ',period)
        # creates the thread
        self.get_thread = BackgroundThread(period)
        # starts this thread
        self.get_thread.start()


class BackgroundThread(QThread):

    def __init__(self, period):
        QThread.__init__(self)
        self.period = period

    def __del__(self):
        self.wait()

    def run(self):
        self.images = [file for file in os.listdir(FOLDER_PATH)]
        for image in self.images:
            set_image.set_image(FOLDER_PATH + image)
            self.sleep(self.period)


def download(subreddits):
    """
    Gets reddit pic URLs from input subreddit
    Downloads the pictures
    """
    print(subreddits)
    pic_urls = get_urls.reddit_pics(subreddits, PAGES, SORTING, TIME_PERIOD)
    print('pic_urls', pic_urls)
    image_downloader.check_folder(FOLDER_PATH)
    image_downloader.download_pics(pic_urls, FOLDER_PATH)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())
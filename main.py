import sys,threading,time,random,os
import cv2
import pyautogui
from PIL import ImageGrab
import pygetwindow
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QSpinBox


class Window(QWidget):
    counter = 0
    i = True

    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        # Start Button
        start = QPushButton("Start", self)
        start.setGeometry(30, 290, 141, 41)
        start.clicked.connect(self.loop)

        # End Button
        end = QPushButton("End", self)
        end.setGeometry(220, 290, 141, 41)
        end.clicked.connect(self.loopex)

        # Exit Button
        close = QPushButton("Close", self)
        close.setGeometry(410, 290, 141, 41)
        close.clicked.connect(self.clos)

        # Headline, Version, Replay Label, Status Label, ConfigLabel
        head = QLabel("Raid: Shadow Legends Bot", self)
        head.setGeometry(50, 30, 501, 71)
        head.setFont(QFont("Stencil", 26))
        version = QLabel("Version 1.0", self)
        version.setGeometry(10, 0, 61, 16)
        state = QLabel("Status", self)
        state.setGeometry(40, 210, 71, 31)
        state.setFont(QFont("Dubai Medium", 16))
        confl = QLabel("Replay", self)
        confl.setGeometry(450, 160, 61, 21)
        confl.setFont(QFont("Dubai Medium", 16))
        

        self.confn = QLabel(str(self.counter), self)
        self.confn.setGeometry(530, 160, 61, 21)
        self.confn.setFont(QFont("Dubai Medium", 16))

        # Button Label, Check
        #replayl = QLabel("Replay Button:", self)
        #replayl.setGeometry(40, 140, 141, 31)
        #replayl.setFont(QFont("Dubai Medium", 16))
        #replayd = QLabel("Button not found", self)
        #replayd.setGeometry(210, 140, 155, 31)
        #replayd.setFont(QFont("Dubai Medium", 16))
        #replayd.setStyleSheet("color: red")

        # Bot-status
        self.stater = QLabel("Not running", self)
        self.stater.setGeometry(210, 210, 141, 31)
        self.stater.setFont(QFont("Dubai Medium", 16))
        self.stater.setStyleSheet("color: red")

        # Replay Spinner
        self.spinco = QSpinBox(self)
        self.spinco.setGeometry(480, 190, 61, 22)

        # Submit Button for ReplaySpinner
        submit = QPushButton("Submit", self)
        submit.setGeometry(480, 222, 61, 23)
        submit.clicked.connect(self.submit)

        # Game detection 
        #status = QLabel("Status:", self)
        #status.setGeometry(430, 356, 41, 16)
        #self.statusg = QLabel("Game not detected", self)
        #self.statusg.setGeometry(475, 356, 100, 16)
        #self.statusg.setStyleSheet("color: red")
       

        # Window
        self.setGeometry(600, 300, 584, 374)
        self.setWindowTitle("Raid Bot")
        self.setWindowIcon(QIcon("image\\icon.png"))
        self.show()
    def clos(self):
        try:
            os.remove("image\\img.jpg")
            self.close()
        except:
            self.close()

    def submit(self):
        self.counter = self.spinco.value()
        self.spinco.setValue(0)
        self.confn.setText(str(self.counter))

    def printy(self):
        print(self.counter)

    def loop(self):
        win = pygetwindow.getWindowsWithTitle('Raid: Shadow Legends')[0]
        win.size = (1280, 720)
        if self.counter == 0:
            self.i = True
            self.stater.setText("Is running")
            self.stater.setStyleSheet("color:green")

            def lopp():
                while self.i:
                    self.checkup()
                    time.sleep(1)
                self.stater.setText("Not running")
                self.stater.setStyleSheet("color:red")

            thread = threading.Thread(target=lopp)
            thread.start()
        else:
            def lopp():
                self.stater.setText("Is running")
                self.stater.setStyleSheet("color:green")
                while self.counter > 0:
                    self.checkup()
                    time.sleep(1)
                    self.counter -= 1
                    self.confn.setText(str(self.counter))
                self.stater.setText("Not running")
                self.stater.setStyleSheet("color:red")

            thread = threading.Thread(target=lopp)
            thread.start()

    def loopex(self):
        self.i = False
        #self.stater.setText("Is terminated")

    def checkup(self):
        while self.i:
            img = ImageGrab.grab()
            img.save("image\\img.jpg")

            img_main = cv2.imread("image\\img.jpg", cv2.COLOR_BGR2GRAY)
            temp = cv2.imread("temp\\temp3.jpg", cv2.COLOR_BGR2GRAY)

            result = cv2.matchTemplate(img_main, temp, cv2.TM_CCOEFF_NORMED)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            a, b = max_loc
            max_loc = a + 50, b + 30
            if max_val > 0.75:
                time.sleep(random.randint(1, 5))
                pyautogui.click(max_loc)
                break

    def resizewindow(self):
        tab = pygetwindow.getWindowsWithTitle('Raid: Shadow Legends')[0]
        tab.size = (1280,720)
        tab.moveTo(400,100)

app = QApplication(sys.argv)

window = Window()

sys.exit(app.exec_())


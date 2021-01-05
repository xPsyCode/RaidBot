import sys,threading,time,random,os, re
import cv2
import pyautogui
from capture import win_cap
from PIL import ImageGrab
import pygetwindow
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pytesseract as pyt
import shutil

pyt.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
count = 0

class Window(QWidget):
    
    i = True

    def __init__(self):
        super().__init__()
        # Window
        self.setGeometry(600, 300, 600, 400)
        self.setFixedSize(600,400)
        self.setWindowTitle("Raid Bot")
        self.setWindowIcon(QIcon("image\\icon.png"))
        self.show()

        #Create the tabs
        tab = QTabWidget()
        tab.addTab(StartTab(),"Start")
        tab.addTab(Config(),"Config")

        #Create the Layout
        vbox = QVBoxLayout()
        vbox.addWidget(tab)
        self.setLayout(vbox)
        self.show()

class StartTab(QWidget):
    
    counter = 0
    i = True
    def __init__(self):
        super().__init__()
        self.default()
        self.status()

    def default(self):
    
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
        version = QLabel("Version 2.0", self)
        version.setGeometry(10, 0, 61, 16)
      

    def status(self):
        # Bot-status
        state = QLabel("Status:", self)
        state.setGeometry(140, 120, 71, 31)
        state.setFont(QFont("Dubai Medium", 16))

        self.stater = QLabel("Not running", self)
        self.stater.setGeometry(300, 120, 141, 31)
        self.stater.setFont(QFont("Dubai Medium", 16))
        self.stater.setStyleSheet("color: red")

        #Replay-status
        rpleft = QLabel("Replays still left:", self)
        rpleft.setGeometry(60,180,151,31)
        rpleft.setFont(QFont("Dubai Medium", 16))

        self.repl = QLabel("",self)
        self.repl.setGeometry(310,185,40,21)
        self.repl.setFont(QFont("Dubai Medium", 16))

        self.progress = QProgressBar(self)
        self.progress.setGeometry(140,240,291,23)
        self.timer = QBasicTimer()
        self.progressval = 100

    ##Methods for running process##

    #Close the App and remove __pycache__ and img.jpg
    def clos(self):
        shutil.rmtree("__pycache__")
        try:
            os.remove("image\\img.jpg")
            self.close()
        except:
            self.close()

    def progressB(self):
        self.progressval -= 100/self.progress_count
        self.progress.setValue(int(self.progressval))

    #Mainloop for programm
    def loop(self):
        global count        
        self.repl.setText(str(count))
        self.resizewindow()
        self.progress.setValue(100)
        self.progress_count = count
        if count == 0:
            self.i = True
            self.stater.setText("Is running")
            self.stater.setStyleSheet("color:green")
           
            #Infinity replay loop
            def lopp():
                while self.i:
                    self.checkup()
                    time.sleep(1)
    
                self.stater.setText("Not running")
                self.stater.setStyleSheet("color:red")
                self.progress.setValue(0)
            thread = threading.Thread(target=lopp)
            thread.start()
        else:

            #Counter replay loop
            def lopp():
                global count
                self.stater.setText("Is running")
                self.stater.setStyleSheet("color:green")
                while count > 0:
                    self.checkup()
                    time.sleep(1)
                    self.progressB()
                    count -= 1
                    self.repl.setText(str(count))
                self.stater.setText("Not running")
                self.stater.setStyleSheet("color:red")

            thread = threading.Thread(target=lopp)
            thread.start()

    def loopex(self):
        self.i = False
        #self.stater.setText("Is terminated")


    #Search for replaybutton and click if find
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
    
    #Resize the game
    def resizewindow(self):
        tab = pygetwindow.getWindowsWithTitle('Raid: Shadow Legends')[0]
        tab.size = (1280,720)
        tab.moveTo(400,100)

    #Convert the image of energy to int
    def energy(self):
        self.resizewindow()
        cv2.imwrite("imgt.jpg",win_cap('Raid: Shadow Legends'))
        img = cv2.imread("imgt.jpg", cv2.IMREAD_GRAYSCALE)
        img2 = img[70:110,1110:1250]
        img3 = img[600:650,710:780]
        current_energy = pyt.image_to_string(img2)
        needed_energy = pyt.image_to_string(img3)
        current_energy = re.findall('([0-9]*)',current_energy)
        needed_energy = re.findall('([0-9]*)',needed_energy)
        current_energy = [i for i in current_energy if i !=""]
        needed_energy = [i for i in needed_energy if i !=""]
        os.remove("imgt.jpg")
        return current_energy[0], needed_energy[0]

#The configurationtab
class Config(QWidget):
    def __init__(self):
        super().__init__()
        #Headline
        headline = QLabel("Configuration",self)
        headline.setGeometry(150, 10, 501, 71)
        headline.setFont(QFont("Stencil", 26))

        self.replay()
        self.cal()
        self.replay()
        self.setreplay()


    def replay(self):
        # Replay Label
        confl = QLabel("Set Replay", self)
        confl.setGeometry(20, 110, 110, 30)
        confl.setFont(QFont("Dubai Medium", 16))
        confl.setStyleSheet("border: 2px solid black;") 

        #Replay Spinner
        self.spinco = QSpinBox(self)
        self.spinco.setGeometry(40, 170, 65, 25)

        # Submit Button for ReplaySpinner
        submit = QPushButton("Submit", self)
        submit.setGeometry(38, 220, 68, 25)
        submit.clicked.connect(self.submit)

        
    def cal(self):
        #Headline
        energy_cal = QLabel("Energy Calculater", self)
        energy_cal.setFont(QFont("Dubai Medium", 16))
        energy_cal.setGeometry(400,110,165,30)
        energy_cal.setStyleSheet("border: 2px solid black;") 

        energy_current = QLabel("Current:", self)
        energy_current.setFont(QFont("Dubai Medium", 14))
        energy_current.setGeometry(420,180,70,30)

        energy_needed= QLabel("Needed:", self)
        energy_needed.setFont(QFont("Dubai Medium", 14))
        energy_needed.setGeometry(420,220,70,30)

        self.current = QLabel("0", self)
        self.current.setFont(QFont("Dubai Medium", 14))
        self.current.setGeometry(520,180,50,30)

        self.needed= QLabel("0", self)
        self.needed.setFont(QFont("Dubai Medium", 14))
        self.needed.setGeometry(520,220,50,30)
        

        #Calculate Button

        self.calbutton = QPushButton("Calculate", self)
        self.calbutton.setGeometry(440,270,80,25)
        self.calbutton.clicked.connect(self.calculate)
        self.calbutton.setDisabled(True)
        self.timer = QBasicTimer()
        self.timer.start(1, self)
        self.timevar = 1
    
    def setreplay(self):
        select = QLabel("Selected Replays:", self)
        select.setGeometry(180,170,200,50)
        select.setFont(QFont("Dubai Medium", 18))


        self.replay = QLabel(u"\u221E", self)
        self.replay.setGeometry(250,220,100,50)
        self.replay.setFont(QFont("Dubai Medium", 16))

    #Method for Submit-Button
    def submit(self):
        global count
        count = self.spinco.value()
        self.spinco.setValue(0)
        self.replay.setText(str(count))

    def timerEvent(self, e):
        def timerloop():
            
            while self.timevar >= 0:
                try:
                    cal = StartTab()
                    cur, need = cal.energy()
                    self.current.setText(cur)
                    self.needed.setText(need)
                    self.timevar -= 1
                    self.calbutton.setDisabled(False)
                except:
                    self.current.setText("N.A.")
                    self.needed.setText("N.A.")
        theard = threading.Thread(target=timerloop)
        theard.start()
        self.timer.stop()

    """def actuell(self):
        if self.timer.isActive():
            time.sleep(2)
        else:
            self.timer.start(1,self)"""

    #Method for calculate-button
    def calculate(self):
        cal = StartTab()
        def calloop():
            global count
            while True:
                try:
                    cur, need = cal.energy()
                    count = int(int(cur)/int(need))
                    self.replay.setText(str(count))
                    self.current.setText(cur)
                    self.needed.setText(need)
                    break
                except:
                    self.current.setText("N.A.")
                    self.needed.setText("N.A.")
                    b = ""
                    for x in ".....":
                        b += x
                        self.replay.setText("Wait" + b)
                        time.sleep(1)
        theard = threading.Thread(target=calloop)
        theard.start()
app = QApplication(sys.argv)

window = Window()

sys.exit(app.exec_())


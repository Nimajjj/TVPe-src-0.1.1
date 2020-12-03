from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QKeyEvent
import random
import os.path
import json, time

"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>

    Copyright 2020 Benjamin Borello

    Threshold of visual perception Experiment [TVPe]
    version: 0.1.1
    date: 03/12/2020

"""

app = QApplication([])

TT, DELTA = 0.0375, 0.00075
T, delta = 0.0375, 0.00075
tours = 50
current_S = 0
current_mask = 'XXXXX'
word = [
'TABLE', 'CHAISE', 'CARTE', 'VERRE', 'CACTUS', 'FRAISE', 'TONGUE', 'CRAYON', 'CORDE', 'CISEAU', 'CARTON',
'PHOTO', 'PORTE', 'FILTRE', 'COUSIN', 'MARCHE', 'ARBRE', 'COUETTE', 'SOUPE', 'DOUCHE', 'VACHE', 'MENTHE'
]

class MainWindow(QWidget):
    def __init__(self, title):
        QWidget.__init__(self)
        self.setWindowTitle(title)

        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()

        self.h_layout.addStretch()
        self.h_layout.addLayout(self.v_layout)
        self.h_layout.addStretch()

        self.set_button("Paramètres experience", self.exp_settings)
        self.set_button("Start", self.start_exp)

        self.setLayout(self.h_layout)
        self.showMaximized()

    def set_button(self, title, action):
        self.button = QPushButton(title)
        self.button.setFont(QFont('Arial', 16))
        self.button.clicked.connect(action)

        self.v_layout.addWidget(self.button)

    def exp_settings(self):
        self.settings_windows = ExpSettings()

    def start_exp(self):
        self.new_s_window = NewS()

    def start(self):
        self.exp = ExpStart()
        self.exp.show()

    def rules(self):
        self.rule = Rules()
        self.rule.show()

    def reset(self):
        del self.exp

class NewS(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        global current_S
        self.setWindowTitle("TVPe - Nouveau sujet")
        self.resize(300, 75)

        self.numero_edit = QLineEdit()

        self.numero_edit.setText(str(current_S))

        self.form_layout = QFormLayout()
        self.form_layout.addRow("Sujet", self.numero_edit)

        self.ok_bt = QPushButton("OK")
        self.ok_bt.clicked.connect(self.ok_button)

        self.v_layout = QVBoxLayout()
        self.v_layout.addLayout(self.form_layout)
        self.v_layout.addWidget(self.ok_bt)

        self.setLayout(self.v_layout)
        self.show()

    def ok_button(self):
        global current_S

        current_S = int(self.numero_edit.text())
        save(current_S, {'Sujet': current_S})
        rules()
        self.close()

class ExpSettings(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("TVPe - Paramètres")
        self.resize(350, 100)

        self.round_edit = QLineEdit()
        self.round_edit.setText(str(tours))

        self.reload_bt = QPushButton('Recharger liste mots')
        self.reload_bt.clicked.connect(set_word)

        self.ok_bt = QPushButton("OK")
        self.ok_bt.clicked.connect(self.ok_button)

        self.form = QFormLayout()
        self.form.addRow('Nombre de tours', self.round_edit)

        self.v_layout = QVBoxLayout()
        self.v_layout.addLayout(self.form)
        self.v_layout.addWidget(self.reload_bt)
        self.v_layout.addWidget(self.ok_bt)

        self.setLayout(self.v_layout)
        self.show()

    """
    def mask(self):
        self.res = ''
        for i in range(len(self.word_edit.text())):
            self.res = self.res + 'X'
        self.mask_edit.setText(self.res)
    """

    def ok_button(self):
        global tours
        tours = int(self.round_edit.text())
        self.close()

class Rules(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        global current_S
        self.setWindowTitle("TVPe - Explications")
        self.resize(400, 400)

        rules = 'Une croix va apparaitre quelques instants à l\'endroit où vous devrez regarder.\
        \nAprès ceci un mot va apparaitre pendant un très court instant.\
        \nVous devrez simplement dire à l\'experimentateur si vous avez réussi à le lire.\
        \nSi c\'est le cas, vous appuyerez sur la touche <n>. Si vous n\'avez pas réussi, \
        \nappuyez sur la touche <c>.'

        self.label = QLabel(rules)
        self.label.setFont(QFont('Arial', 16))

        self.start_bt = QPushButton('Commencer')
        self.start_bt.setFont(QFont('Arial', 16))
        self.start_bt.clicked.connect(self.start)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.start_bt)

        self.setLayout(self.layout)

    def start(self):
        start()
        self.close()

class ExpStart(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.state, self.i, self.x = 0, 0, 1
        self.resultats = []
        #print('\nExpStart\ntours: {}\nT: {}\ndelta: {}\nstate: {}\ni: {}\nx: {}\n'.format(tours, T, delta, self.state, self.i, self.x))

        self.setWindowTitle('TVPe - Test')

        self.word = QLabel('                      ', self)
        self.word.setFont(QFont('Arial', 32))
        self.pos_x = 500
        self.pos_y = 300
        self.word.move(self.pos_x, self.pos_y)

        self.start_bt = QPushButton('Commencer', self)
        self.start_bt.setFont(QFont('Arial', 16))
        self.start_bt.move(500,500)

        self.start_bt.clicked.connect(self.main_exp)

        self.showMaximized()

        # n = 78; c = 67; r = 82
    def keyPressEvent(self, event):
        if self.state == 2:
            if event.key() == 78:   # trouvé
                self.data_manager(1)
            elif event.key() == 67:   # raté
                self.data_manager(0)
            elif event.key() == 82: # 'r' : reset
                self.data_manager(-1)

    def hide_layout(self):
        self.start_bt.setParent(None)

    def main_exp(self):
        wait(1)

        self.state = 1

        self.hide_layout()

        self.set_word('+', 1)
        self.set_word('', 1)

        self.set_word(current_mask, T)  # forward masking
        self.set_word('', T/2)    # isi
        self.set_word(word[self.i], T)
        self.set_word('', T/2)   # isi
        self.set_word(current_mask, T) # backward masking

        self.word.setText('')

        self.state = 2

    def set_word(self, word, t=0):
        self.word.setText(word)
        QApplication.processEvents()
        wait(t)

    def data_manager(self, res):
        global T, delta

        if res != -1:   # if not reset
            self.resultats.append({'n': self.x, 'Mot': word[self.i], 'Correct': res, 'T': T, 'delta': delta})
            if res == 1:
                T = round((T-delta), 4)
            elif res == 0:  T = round((T+delta), 4)

            #if self.i < (len(word)-1):  self.i += 1
            #else:   self.i = 0

            self.i = random.randint(0,len(word)-1)

            if self.x >= tours:
                save(current_S, {'Resultats': self.resultats})
                #print('\nExpEnd\ntours: {}\nT: {}\ndelta: {}\nstate: {}\ni: {}\nx: {}\n'.format(tours, T, delta, self.state, self.i, self.x))
                reset()
                self.close()

            self.x += 1
        self.main_exp()

def start():
    MainWindow.start(main)

def rules():
    MainWindow.rules(main)

def wait(s):
    t0 = time.time_ns()
    while ((time.time_ns() - t0)  / (10 ** 9)) < s:
        QApplication.processEvents()

def save(n=int(), data={}):
    title = "{}.json".format(n)
    complete_name = os.path.join('./subjects_infos/', title)
    res = {}
    if os.path.exists('./subjects_infos/{}.json'.format(n)):
        with open(complete_name, "r") as file:
            json_file = json.load(file)
            for clé, val, in data.items():
                json_file[clé] = val
            res = json_file
        with open(complete_name, "w") as file:
            json.dump(res, file, indent=4)
    else:
        with open(complete_name, "w") as file:
            json.dump(data, file, indent=1)

def set_word():
    global word
    word = [line.rstrip('\n') for line in open('words.txt')]

def reset():
    global T, delta, current_S

    current_S += 1
    T = TT
    delta = DELTA

    MainWindow.reset(main)

def main():
    main = MainWindow("TVPe - MENU")
    set_word()

    main.show()
    app.exec_()

if __name__ == '__main__':
    main()

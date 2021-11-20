import sqlite3
import sys
from PyQt5 import Qt
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5 import uic
from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
import datetime as dt

SUMM = 0
COUNT_SPECIAL = 0
COUNT_CHEESE = 0
COUNT_MINI = 0
COUNT_DAN = 0
COUNT_CHIL = 0
COUNT_VEG = 0
COUNT_BBQ = 0
FLAG_CHECK = False
FLAG_SALE = False


class Receipt(QMainWindow):
    # Данный виджет отвечает за последнее окно чека
    def __init__(self):
        super().__init__()
        uic.loadUi('Bill.ui', self)
        self.setWindowTitle('Чек')
        self.receipt.setDisabled(True)
        # self.style_choice.insertItems(1, 'classic')
        # self.style_choice.insertItem(2, 'retro')
        # self.style_choice.insertItem(3, 'unusual'
        global COUNT_DAN, COUNT_BBQ, COUNT_MINI, COUNT_CHIL, COUNT_VEG, COUNT_CHEESE, COUNT_SPECIAL, SUMM, FLAG_SALE
        # тут я беру глобальные переменные с количество заказанных хот дого
        self.receipt.setStyleSheet('background-color: black;'
                                   'color: yellow')
        if COUNT_CHEESE != 0:
            # здесь и в последующих уловиях происходит проверка на количество заказанных хот догов того или иного
            # названия в случае если значение переменной не нулевое, то в виджет PlainTextEdit добавляется строка с
            # количеством этого хотдога и ценой
            self.receipt.insertPlainText(f'CHEESE-  дог     *     {COUNT_CHEESE}     =     {COUNT_CHEESE * 199}')
            self.receipt.insertPlainText(f'\n')
        if COUNT_VEG != 0:
            self.receipt.insertPlainText(f'VEG-дог     *     {COUNT_VEG}     =     {COUNT_VEG * 170}')
            self.receipt.insertPlainText(f'\n')
        if COUNT_SPECIAL != 0:
            self.receipt.insertPlainText(f'Классический-дог     *     {COUNT_SPECIAL}     =     {COUNT_SPECIAL * 149}')
            self.receipt.insertPlainText(f'\n')
        if COUNT_MINI != 0:
            self.receipt.insertPlainText(f'Мини-дог     *     {COUNT_MINI}     =     {COUNT_MINI * 99}')
            self.receipt.insertPlainText(f'\n')
        if COUNT_BBQ != 0:
            self.receipt.insertPlainText(f'Барбекю-дог     *     {COUNT_BBQ}     =     {COUNT_BBQ * 149}')
            self.receipt.insertPlainText(f'\n')
        if COUNT_CHIL != 0:
            self.receipt.insertPlainText(f'Chil-дог     *     {COUNT_CHIL}     =     {COUNT_CHIL * 199}')
            self.receipt.insertPlainText(f'\n')
        if COUNT_DAN != 0:
            self.receipt.insertPlainText(f'Датский-дог     *     {COUNT_DAN}     =     {COUNT_DAN * 149}')
            self.receipt.insertPlainText(f'\n')
        if FLAG_SALE:
            self.receipt.insertPlainText(f'ИТОГО     :     {SUMM * 0.91}')
            self.receipt.insertPlainText(f'\n')
            self.receipt.insertPlainText('СКИДКА ЗА ПОКУПКУ 9%')
        else:
            self.receipt.insertPlainText(f'ИТОГО     :     {SUMM}')

        self.style_choice.currentTextChanged.connect(self.style_change)
        with open('чек.txt', 'w') as f:
            # здесь происходит добавление текущей даты в чек и введение самого чека
            date = dt.datetime.now().date()
            time = dt.datetime.now().time()
            f.write(f'Дата покупки:     {str(date.day)}.{str(date.month)}.{str(date.year)}')
            f.write('\n')
            f.write(f'Время покупки:    {str(time.hour)}:{str(time.minute)}:{str(round(time.second))}')
            f.write('\n')
            list_receipt = self.receipt.toPlainText()
            f.write(list_receipt)
        # ниже пользователю сообщается о том где посмотреть текстовый чек
        self.statusBar().showMessage('Информация о вашей покупке сохранена в файле чек.txt в директории приложения')
        self.statusBar().setStyleSheet('background-color: black;'
                                       'color: yellow;')

    def style_change(self):
        # так как в моём приложении есть несколько стилей чека, данный метод берёт значение из ComboBox и сравнивает со
        # всеми стилями, при нахождении совпадения чек получает соответствующий стиль шрифта и заднего фона
        if self.style_choice.currentText() == 'retro':
            self.receipt.setStyleSheet('background-color: #4FA7F9;'
                                       'color: #E21A00;')
            self.statusBar().setStyleSheet('background-color: #4FA7F9;'
                                       'color: #E21A00;')
        elif self.style_choice.currentText() == 'classic':
            self.receipt.setStyleSheet('background-color: black;'
                                       'color: yellow;')
            self.statusBar().setStyleSheet('background-color: black;'
                                       'color: yellow;')
        elif self.style_choice.currentText() == 'unusual':
            self.receipt.setStyleSheet('background-color: #00FFFF;'
                                       'color: #660099;')
            self.statusBar().setStyleSheet('background-color: #00FFFF;'
                                       'color: #660099;')

class PasswordError(Exception):
    # этот класс необходим, если пользователь ввёл соответствующий критериям пароль и используется в Registration
    pass


class LengthError(PasswordError):
    # этот класс описывает, которая возникает при введении короткого пароля
    pass


class LetterError(PasswordError):
    # данный класс описывает ошибку, возникающую при отстутствии букв в пароле покупателя
    pass


class DigitError(PasswordError):
    # этот класс вызывается при отсутсвии цифр в пароле пользователя
    pass


class Registration(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('registration.ui', self)
        self.setWindowTitle('Регистрация и вход')

        self.passwordEdit.textChanged.connect(self.sale)
        self.continue_btn.clicked.connect(self.sale_btn)

    def sale(self):
        name = self.nameEdit.text()
        password = self.passwordEdit.text()
        flag_digit = False  # флаг если есть цифр в пароле
        flag_string = False  # флаг если нет букв
        flag_length = False  # флаг если длина пароля меньше 8 символов
        try:
            for item in password:
                if item.isdigit():
                    flag_digit = True
                elif item.isalpha():
                    flag_string = True
            if len(password) >= 8:
                flag_length = True
            if not flag_digit and flag_length:
                raise DigitError
            elif not flag_string and flag_length:
                raise LetterError
            elif flag_string and flag_digit and flag_length:
                raise PasswordError
            elif not flag_length:
                raise LengthError
        except DigitError:
            # Сообщение которое выведется в StatusBar при недостатке цифр
            self.statusBar().showMessage('В вашем пароле нет цифр')
            self.statusBar().setStyleSheet('background-color:red;')
        except LetterError:
            # Сообщение которое выведется в StatusBar при недостатке букв
            self.statusBar().showMessage('В вашем пароле нет букв')
            self.statusBar().setStyleSheet('background-color:red;')
        except LengthError:
            # Сообщение которое выведется в StatusBar, если пароль слишком короткий
            self.statusBar().showMessage('Ваш пароль слишком короткий')
            self.statusBar().setStyleSheet('background-color:red;')
        except PasswordError:
            # Сообщение которое выведется в StatusBar если пароль надёжный
            global FLAG_CHECK
            FLAG_CHECK = True
            self.statusBar().showMessage('Вы придумали надёжный пароль')
            self.statusBar().setStyleSheet('background-color:green;')

    def sale_btn(self):
        # метод описывающий работу БД
        name = self.nameEdit.text()
        password = self.passwordEdit.text()
        if FLAG_CHECK:
            con = sqlite3.connect('MyDB.db')
            cur = con.cursor()
            result = cur.execute("""SELECT Costumer, Password FROM Costumer LEFT JOIN Passwords ON
                 Costumer.id = Passwords.id;""").fetchall()  # тут я совмещаю две таблицы по общему id и на выходе
            # получаю список кортежей в каждом из которых первый элемент имя пользователя, а второй соответствующий ему
            # пароль
            flag = False
            for elem in result:
                if elem[0] == name and elem[1] == password:
                    flag = True
                    break
            if flag:
                global FLAG_SALE
                FLAG_SALE = True
            else:
                cur.execute("""INSERT INTO Costumer(Costumer) VALUES(?)""", (name,))  # добавление имени покупателя
                cur.execute("""INSERT INTO Passwords(password) VALUES(?)""", (password,))  # добавление пароля
                con.commit()
            con.close()
            self.hide()
            self.window_bill = Receipt()
            self.window_bill.show()


class Special(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Special_dog.ui', self)
        self.setWindowTitle('Классический-дог')


class Cheese(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Cheese_dog.ui', self)
        self.setWindowTitle('Cheese-дог')


class Mini(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Mini_dog.ui', self)
        self.setWindowTitle('Мини-дог')


class Vegan(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Vegan_dog.ui', self)
        self.setWindowTitle('Веганский-дог')


class BBQ(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('BBQ_dog.ui', self)
        self.setWindowTitle('Барбекю-дог')


class Dan(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Dan_dog.ui', self)
        self.setWindowTitle('Датский-дог')


class Chil(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Chil_dog.ui', self)
        self.setWindowTitle('Chil-дог')


class Price_list_widget(QMainWindow):
    def __init__(self):
        # этот класс описывает меню, предлагаемое покупателю, здесь доступны голосовые подсказки, в которых
        # рассказывается об ингредиенте каждого хот дога, также здесь хот доги разделены на три категории(в меру острые,
        # острые и очень острые), помимо этого каждая группа имеет свой личный цвет. Именно в этом окне покупатель может
        # увидеть фотографии каждого из хот догов при нажатии на соответствующую кнопку.
        # Помимо этого данный класс не будет закрываться автоматически, так как после получения чека покупатель может
        # захотеть сверить цены на хот доге в чеке и в меню
        super().__init__()
        uic.loadUi('Price_list.ui', self)
        self.setWindowTitle('Меню')
        self.hotdog_special = QLabel(self)
        self.hotdog_special.resize(150, 30)
        self.hotdog_special.setText("Классический хот-дог - 149 ₽")
        self.hotdog_special.move(50, 250)
        self.hotdog_special.setStyleSheet('color:yellow;')

        self.hotdog_chil = QLabel(self)
        self.hotdog_chil.resize(150, 30)
        self.hotdog_chil.setText("Chill дог - 199 ₽")
        self.hotdog_chil.move(680, 250)
        self.hotdog_chil.setStyleSheet('color:red;')

        self.hotdog_veg = QLabel(self)
        self.hotdog_veg.resize(150, 30)
        self.hotdog_veg.setText("Веган-дог - 170 ₽")
        self.hotdog_veg.move(340, 250)
        self.hotdog_veg.setStyleSheet('color:orange;')

        self.cheese_dog = QLabel(self)
        self.cheese_dog.resize(150, 30)
        self.cheese_dog.setText("Cheese-дог - 199 ₽")
        self.cheese_dog.move(50, 350)
        self.cheese_dog.setStyleSheet('color:yellow;')

        self.bbq_dog = QLabel(self)
        self.bbq_dog.resize(150, 30)
        self.bbq_dog.setText("Барбекю-дог - 149 ₽")
        self.bbq_dog.move(340, 350)
        self.bbq_dog.setStyleSheet('color:orange;')

        self.mini_dog = QLabel(self)
        self.mini_dog.resize(150, 30)
        self.mini_dog.setText("Мини-дог - 99 ₽")
        self.mini_dog.move(50, 450)
        self.mini_dog.setStyleSheet('color:yellow;')

        self.dan_dog = QLabel(self)
        self.dan_dog.resize(150, 30)
        self.dan_dog.setText("Датский-дог - 149 ₽")
        self.dan_dog.move(340, 450)
        self.dan_dog.setStyleSheet('color:orange;')

        self.voice_special_dog = QPushButton(self)
        self.voice_special_dog.resize(20, 20)
        self.voice_special_dog.setText('🔊')
        self.voice_special_dog.move(210, 255)
        self.voice_special_dog.setStyleSheet('background-color: yellow')
        self.voice_special_dog.clicked.connect(self.load_mp3)
        self.voice_special_dog.setCheckable(True)

        self.voice_chil_dog = QPushButton(self)
        self.voice_chil_dog.resize(20, 20)
        self.voice_chil_dog.setText('🔊')
        self.voice_chil_dog.move(800, 255)
        self.voice_chil_dog.setStyleSheet('background-color: red')
        self.voice_chil_dog.clicked.connect(self.load_mp3)
        self.voice_chil_dog.setCheckable(True)

        self.voice_veg_dog = QPushButton(self)
        self.voice_veg_dog.resize(20, 20)
        self.voice_veg_dog.setText('🔊')
        self.voice_veg_dog.move(500, 255)
        self.voice_veg_dog.setStyleSheet('background-color: orange')
        self.voice_veg_dog.clicked.connect(self.load_mp3)
        self.voice_veg_dog.setCheckable(True)

        self.voice_cheese_dog = QPushButton(self)
        self.voice_cheese_dog.resize(20, 20)
        self.voice_cheese_dog.setText('🔊')
        self.voice_cheese_dog.move(210, 355)
        self.voice_cheese_dog.setStyleSheet('background-color: yellow')
        self.voice_cheese_dog.clicked.connect(self.load_mp3)
        self.voice_cheese_dog.setCheckable(True)

        self.voice_bbq_dog = QPushButton(self)
        self.voice_bbq_dog.resize(20, 20)
        self.voice_bbq_dog.setText('🔊')
        self.voice_bbq_dog.move(500, 355)
        self.voice_bbq_dog.setStyleSheet('background-color: orange')
        self.voice_bbq_dog.clicked.connect(self.load_mp3)
        self.voice_bbq_dog.setCheckable(True)

        self.voice_mini_dog = QPushButton(self)
        self.voice_mini_dog.resize(20, 20)
        self.voice_mini_dog.setText('🔊')
        self.voice_mini_dog.move(210, 455)
        self.voice_mini_dog.setStyleSheet('background-color: yellow')
        self.voice_mini_dog.clicked.connect(self.load_mp3)
        self.voice_mini_dog.setCheckable(True)

        self.voice_dan_dog = QPushButton(self)
        self.voice_dan_dog.resize(20, 20)
        self.voice_dan_dog.setText('🔊')
        self.voice_dan_dog.move(500, 455)
        self.voice_dan_dog.setStyleSheet('background-color: orange;')
        self.voice_dan_dog.clicked.connect(self.load_mp3)
        self.voice_dan_dog.setCheckable(True)

        self.inf_btn_special_dog = QPushButton(self)
        self.inf_btn_special_dog.resize(20, 20)
        self.inf_btn_special_dog.setText('❓')
        self.inf_btn_special_dog.move(20, 255)
        self.inf_btn_special_dog.setStyleSheet('background-color: yellow;')
        self.inf_btn_special_dog.clicked.connect(self.information)
        self.inf_btn_special_dog.setCheckable(True)

        self.inf_btn_cheese_dog = QPushButton(self)
        self.inf_btn_cheese_dog.resize(20, 20)
        self.inf_btn_cheese_dog.setText('❓')
        self.inf_btn_cheese_dog.move(20, 355)
        self.inf_btn_cheese_dog.setStyleSheet('background-color: yellow;')
        self.inf_btn_cheese_dog.clicked.connect(self.information)
        self.inf_btn_cheese_dog.setCheckable(True)

        self.inf_btn_mini_dog = QPushButton(self)
        self.inf_btn_mini_dog.resize(20, 20)
        self.inf_btn_mini_dog.setText('❓')
        self.inf_btn_mini_dog.move(20, 455)
        self.inf_btn_mini_dog.setStyleSheet('background-color: yellow;')
        self.inf_btn_mini_dog.clicked.connect(self.information)
        self.inf_btn_mini_dog.setCheckable(True)

        self.inf_btn_vegan_dog = QPushButton(self)
        self.inf_btn_vegan_dog.resize(20, 20)
        self.inf_btn_vegan_dog.setText('❓')
        self.inf_btn_vegan_dog.move(310, 255)
        self.inf_btn_vegan_dog.setStyleSheet('background-color: orange;')
        self.inf_btn_vegan_dog.clicked.connect(self.information)
        self.inf_btn_vegan_dog.setCheckable(True)

        self.inf_btn_bbq_dog = QPushButton(self)
        self.inf_btn_bbq_dog.resize(20, 20)
        self.inf_btn_bbq_dog.setText('❓')
        self.inf_btn_bbq_dog.move(310, 355)
        self.inf_btn_bbq_dog.setStyleSheet('background-color: orange;')
        self.inf_btn_bbq_dog.clicked.connect(self.information)
        self.inf_btn_bbq_dog.setCheckable(True)

        self.inf_btn_dan_dog = QPushButton(self)
        self.inf_btn_dan_dog.resize(20, 20)
        self.inf_btn_dan_dog.setText('❓')
        self.inf_btn_dan_dog.move(310, 455)
        self.inf_btn_dan_dog.setStyleSheet('background-color: orange;')
        self.inf_btn_dan_dog.clicked.connect(self.information)
        self.inf_btn_dan_dog.setCheckable(True)

        self.inf_btn_chil_dog = QPushButton(self)
        self.inf_btn_chil_dog.resize(20, 20)
        self.inf_btn_chil_dog.setText('❓')
        self.inf_btn_chil_dog.move(650, 255)
        self.inf_btn_chil_dog.setStyleSheet('background-color: red;')
        self.inf_btn_chil_dog.clicked.connect(self.information)
        self.inf_btn_chil_dog.setCheckable(True)

    def load_mp3(self):
        # в этом методе подгружаются голосовые подсказки о хот догах
        button_voice_send = QApplication.instance().sender()
        # переменная button_voice_send получает имя нажатой кнопки, затем это имя сравнивается с именем каждой кнопки,
        # чтобы запустить соответствующую ей голосовую подсказку.
        if self.voice_special_dog == button_voice_send:
            media = QtCore.QUrl.fromLocalFile('Voices/classic_hotdog.mp3')
            content = QtMultimedia.QMediaContent(media)
            self.player = QtMultimedia.QMediaPlayer()
            self.player.setMedia(content)
            self.player.play()
        elif self.voice_veg_dog == button_voice_send:
            media = QtCore.QUrl.fromLocalFile('Voices/vegan_dog.mp3')
            content = QtMultimedia.QMediaContent(media)
            self.player = QtMultimedia.QMediaPlayer()
            self.player.setMedia(content)
            self.player.play()
        elif self.voice_cheese_dog == button_voice_send:
            media = QtCore.QUrl.fromLocalFile('Voices/cheese_dog.mp3')
            content = QtMultimedia.QMediaContent(media)
            self.player = QtMultimedia.QMediaPlayer()
            self.player.setMedia(content)
            self.player.play()
        elif self.voice_chil_dog == button_voice_send:
            media = QtCore.QUrl.fromLocalFile('Voices/chil_dog.mp3')
            content = QtMultimedia.QMediaContent(media)
            self.player = QtMultimedia.QMediaPlayer()
            self.player.setMedia(content)
            self.player.play()
        elif self.voice_bbq_dog == button_voice_send:
            media = QtCore.QUrl.fromLocalFile('Voices/bbq_dog.mp3')
            content = QtMultimedia.QMediaContent(media)
            self.player = QtMultimedia.QMediaPlayer()
            self.player.setMedia(content)
            self.player.play()
        elif self.voice_mini_dog == button_voice_send:
            media = QtCore.QUrl.fromLocalFile('Voices/mini_dog.mp3')
            content = QtMultimedia.QMediaContent(media)
            self.player = QtMultimedia.QMediaPlayer()
            self.player.setMedia(content)
            self.player.play()
        elif self.voice_dan_dog == button_voice_send:
            media = QtCore.QUrl.fromLocalFile('Voices/dan_dog.mp3')
            content = QtMultimedia.QMediaContent(media)
            self.player = QtMultimedia.QMediaPlayer()
            self.player.setMedia(content)
            self.player.play()

    def information(self):
        # метод information выдаёт информацию и фотографии хот догов и работает схоже с методом load_mp3
        button_send = QApplication.instance().sender()
        if button_send == self.inf_btn_special_dog:
            self.window_special = Special()
            self.window_special.show()
        if button_send == self.inf_btn_cheese_dog:
            self.window_cheese = Cheese()
            self.window_cheese.show()
        if button_send == self.inf_btn_mini_dog:
            self.window_mini = Mini()
            self.window_mini.show()
        if button_send == self.inf_btn_vegan_dog:
            self.window_vegan = Vegan()
            self.window_vegan.show()
        if button_send == self.inf_btn_bbq_dog:
            self.window_bbq = BBQ()
            self.window_bbq.show()
        if button_send == self.inf_btn_dan_dog:
            self.window_dan = Dan()
            self.window_dan.show()
        if button_send == self.inf_btn_chil_dog:
            self.window_chil = Chil()
            self.window_chil.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_1:
            self.window_special = Special()
            self.window_special.show()
        elif event.key() == Qt.Key_2:
            self.window_cheese = Cheese()
            self.window_cheese.show()
        elif event.key() == Qt.Key_3:
            self.window_mini = Mini()
            self.window_mini.show()
        elif event.key() == Qt.Key_4:
            self.window_vegan = Vegan()
            self.window_vegan.show()
        elif event.key() == Qt.Key_5:
            self.window_bbq = BBQ()
            self.window_bbq.show()
        elif event.key() == Qt.Key_6:
            self.window_dan = Dan()
            self.window_dan.show()
        elif event.key() == Qt.Key_7:
            self.window_chil = Chil()
            self.window_chil.show()


class Menu(QMainWindow):
    # этот класс отвечает за выбор пользователем хот догов
    def __init__(self):
        super().__init__()
        uic.loadUi('Menu_main.ui', self)
        self.setWindowTitle('Окно заказа')
        self.initUI()

    def initUI(self):
        # Тут я меняю цвета у некоторых виджетов чтобы они соответствовали дизайну
        self.heading = QLabel(self)
        self.heading.resize(50, 30)
        self.heading.setText("Меню")
        self.heading.move(450, 20)
        self.heading.setStyleSheet('"font-weight:bold";')
        self.heading.setStyleSheet('color:yellow;')

        self.hotdog_1.setStyleSheet('color:yellow;')
        self.hotdog_2.setStyleSheet('color:yellow;')
        self.hotdog_3.setStyleSheet('color:yellow;')
        self.hotdog_4.setStyleSheet('color:yellow;')
        self.hotdog_5.setStyleSheet('color:yellow;')
        self.hotdog_6.setStyleSheet('color:yellow;')
        self.hotdog_7.setStyleSheet('color:yellow;')

        self.spinBox.setStyleSheet('color:red;')
        self.spinBox_2.setStyleSheet('color:red;')
        self.spinBox_3.setStyleSheet('color:red;')
        self.spinBox_4.setStyleSheet('color:red;')
        self.spinBox_5.setStyleSheet('color:red;')
        self.spinBox_6.setStyleSheet('color:red;')
        self.spinBox_7.setStyleSheet('color:red;')

        self.intermediate_sum.setStyleSheet('color:red;'
                                            'border-color:yellow;')
        self.intermediate_sum.setDigitCount(6)  # данная строка увеличивает количество символов в lcdNumber
        self.sum_label.setStyleSheet('background-color:red;'
                                     'color:yellow;')

        self.hotdog_1.stateChanged.connect(self.change)
        self.hotdog_2.stateChanged.connect(self.change)
        self.hotdog_3.stateChanged.connect(self.change)
        self.hotdog_4.stateChanged.connect(self.change)
        self.hotdog_5.stateChanged.connect(self.change)
        self.hotdog_6.stateChanged.connect(self.change)
        self.hotdog_7.stateChanged.connect(self.change)

        # ниже я делаю виджеты SpinBox недоступными для корректировок покупателя
        self.spinBox.setDisabled(True)
        self.spinBox_2.setDisabled(True)
        self.spinBox_3.setDisabled(True)
        self.spinBox_4.setDisabled(True)
        self.spinBox_4.setDisabled(True)
        self.spinBox_5.setDisabled(True)
        self.spinBox_6.setDisabled(True)
        self.spinBox_7.setDisabled(True)

        self.spinBox.textChanged.connect(self.change_sum)
        self.spinBox_2.textChanged.connect(self.change_sum)
        self.spinBox_3.textChanged.connect(self.change_sum)
        self.spinBox_4.textChanged.connect(self.change_sum)
        self.spinBox_5.textChanged.connect(self.change_sum)
        self.spinBox_6.textChanged.connect(self.change_sum)
        self.spinBox_7.textChanged.connect(self.change_sum)

        self.order_btn.clicked.connect(self.order)

    def change(self):  # при помощи функции change я меняю состояния виджетов SpinBox и CheckBox
        if self.hotdog_1.isChecked():
            # например, тут я проверяю, если пользователь нажал на CheckBox
            # соответствующий первому хот догу(Классический-дог), то мы позволяем пользователю вносить изменения
            # в SpinBox и ставим значение по умолчанию 1
            if not self.spinBox.value() > 1:
                self.spinBox.setDisabled(False)
                self.spinBox.setValue(1)
        elif not self.hotdog_1.isChecked():
            # в случаем если с CheckBox была снята галочка, то SpinBox становится недоступным для корректировок
            # пользователя и устанавливается значение равное 0
            # ниже я делаю схожие операции, но для других CheckBox и SpinBox
            self.spinBox.setDisabled(True)
            self.spinBox.setValue(0)
        if self.hotdog_2.isChecked():
            if not self.spinBox_2.value() > 1:
                self.spinBox_2.setDisabled(False)
                self.spinBox_2.setValue(1)
        elif not self.hotdog_2.isChecked():
            self.spinBox_2.setDisabled(True)
            self.spinBox_2.setValue(0)
        if self.hotdog_3.isChecked():
            if not self.spinBox_3.value() > 1:
                self.spinBox_3.setDisabled(False)
                self.spinBox_3.setValue(1)
        elif not self.hotdog_3.isChecked():
            self.spinBox_3.setDisabled(True)
            self.spinBox_3.setValue(0)
        if self.hotdog_4.isChecked():
            if not self.spinBox_4.value() > 1:
                self.spinBox_4.setDisabled(False)
                self.spinBox_4.setValue(1)
        elif not self.hotdog_4.isChecked():
            self.spinBox_4.setDisabled(True)
            self.spinBox_4.setValue(0)
        if self.hotdog_5.isChecked():
            if not self.spinBox_5.value() > 1:
                self.spinBox_5.setDisabled(False)
                self.spinBox_5.setValue(1)
        elif not self.hotdog_5.isChecked():
            self.spinBox_5.setDisabled(True)
            self.spinBox_5.setValue(0)
        if self.hotdog_6.isChecked():
            if not self.spinBox_6.value() > 1:
                self.spinBox_6.setDisabled(False)
                self.spinBox_6.setValue(1)
        elif not self.hotdog_6.isChecked():
            self.spinBox_6.setDisabled(True)
            self.spinBox_6.setValue(0)
        if self.hotdog_7.isChecked():
            if not self.spinBox_7.value() > 1:
                self.spinBox_7.setDisabled(False)
                self.spinBox_7.setValue(1)
        elif not self.hotdog_7.isChecked():
            self.spinBox_7.setDisabled(True)
            self.spinBox_7.setValue(0)

    def change_sum(self):
        # с помощью данной функции я меняю сумму заказа покупателя, как можно заметить функция активируется при любом
        # изменении виджетов SpinBox, таким образом, сумма, выдаваемая в LCDNumber всегда актуальна.
        if self.spinBox.value() == 0:
            self.spinBox.setDisabled(True)
            self.hotdog_1.setChecked(False)
        if self.spinBox_2.value() == 0:
            self.spinBox_2.setDisabled(True)
            self.hotdog_2.setChecked(False)
        if self.spinBox_3.value() == 0:
            self.spinBox_3.setDisabled(True)
            self.hotdog_3.setChecked(False)
        if self.spinBox_4.value() == 0:
            self.spinBox_4.setDisabled(True)
            self.hotdog_4.setChecked(False)
        if self.spinBox_5.value() == 0:
            self.spinBox_5.setDisabled(True)
            self.hotdog_5.setChecked(False)
        if self.spinBox_6.value() == 0:
            self.spinBox_6.setDisabled(True)
            self.hotdog_6.setChecked(False)
        if self.spinBox_7.value() == 0:
            self.spinBox_7.setDisabled(True)
            self.hotdog_7.setChecked(False)
        global SUMM
        SUMM = 0
        SUMM += int(self.spinBox.value()) * 149
        SUMM += int(self.spinBox_2.value()) * 199
        SUMM += int(self.spinBox_3.value()) * 170
        SUMM += int(self.spinBox_4.value()) * 149
        SUMM += int(self.spinBox_5.value()) * 199
        SUMM += int(self.spinBox_6.value()) * 99
        SUMM += int(self.spinBox_7.value()) * 149
        self.intermediate_sum.display(SUMM)

    def order(self):
        global COUNT_DAN, COUNT_CHIL, COUNT_VEG, COUNT_CHEESE, COUNT_SPECIAL, COUNT_MINI, COUNT_BBQ
        # данная функция необходима для записи количества заказанных пользователем хот догов в константы для
        # последующего использования в чеке
        COUNT_SPECIAL = self.spinBox.value()
        COUNT_CHIL = self.spinBox_2.value()
        COUNT_VEG = self.spinBox_3.value()
        COUNT_BBQ = self.spinBox_4.value()
        COUNT_CHEESE = self.spinBox_5.value()
        COUNT_MINI = self.spinBox_6.value()
        COUNT_DAN = self.spinBox_7.value()
        if COUNT_SPECIAL != 0 or COUNT_BBQ != 0 or COUNT_CHEESE != 0 or COUNT_MINI != 0 or COUNT_CHIL != 0 or \
            COUNT_VEG != 0 or COUNT_DAN != 0:
            self.hide()
            # здесь мы открываем окно
            self.window_bd = Registration()
            self.window_bd.show()
        else:
            self.statusBar().showMessage('Сначала закажите что-нибудь')
            self.statusBar().setStyleSheet('background-color: red')


class Starting_window(QMainWindow):
    # Тут я создал класс с краткой информацией о моей хотдожной
    def __init__(self):
        super().__init__()
        # Здесь мы подгружаем наш интерфейс
        uic.loadUi('Starting_window.ui', self)
        self.setWindowTitle('Приветствие')
        self.load_mp3_greeting('Voices/Greeting_voice.mp3')
        self.voice_btn_start.clicked.connect(self.player.play)
        self.voice_btn_end.clicked.connect(self.player.stop)
        self.start_btn.clicked.connect(self.run)
        self.start_btn.setStyleSheet('background-color:white;')
        self.voice_btn_start.setStyleSheet('background-color:white;')
        self.voice_btn_end.setStyleSheet('background-color:white;')
        # тут делаем кнопки в одной стилистике цвета

    def load_mp3_greeting(self, filename):
        # это файл для загрузки нашей голосовой подсказки
        media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)

    def run(self):
        # с помощью нажатия кнопки пользователь открывает другие окна с меню
        self.window2 = Menu()
        self.window2.show()
        self.window3 = Price_list_widget()
        self.window3.show()
        self.hide()

    def keyPressEvent(self, event):
        # это дополнительная опция, по которой пользователь может нажать на пробел
        # и открыть меню и список хот догов с подробной информацией о них
        if event.key() == Qt.Key_Space:
            self.window_menu = Menu()
            self.window_menu.show()
            self.window_price_list = Price_list_widget()
            self.window_price_list.show()
            self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Starting_window()
    ex.show()
    sys.exit(app.exec_())
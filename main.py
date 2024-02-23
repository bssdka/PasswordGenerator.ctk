# !usr\bin\activate
# :using "utf-8":

import customtkinter as ctk

import random as rnd
import colorama as cm
from PIL import Image
import pyperclip
import ctypes
import time
import sys
import os
cm.init()

import assets.messegespy as msgpy
import assets.inputtext as inptxt
import assets.debugerros as debug
import config.settings as settings


#__Author__: Zhilyaev Arseniy
#__Mail__: ay.zhiliaev@outlook.com
#__GitHub__: https://github.com/1nonlySeny
VERSION = "w1.30R"


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(VERSION)
        self.geometry("400x280")
        self.resizable(False, False)

        try:
            # $Set Windows titlebar icon$
            if sys.platform.startswith('win'):
                self.customtkinter_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                self.after(200, lambda: self.iconbitmap(os.path.join(self.customtkinter_directory, "assets", "icons", "logo.ico")))

                # $Set the taskbar icon$
                myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass 


        # $Create dependent variables$
        self.digits = ['1', '2', '3', '4', '5','6', '7', '8', '9', '0']

        self.uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                        'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        
        self.lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                        'u', 'v', 'w', 'x', 'y', 'z']
        
        self.punctuation = ['%', '*', ')', '?', '@', '#', '$', '~']

        # $Set images for buttons$
        self.copyImg = ctk.CTkImage(light_image=Image.open(os.path.join(self.customtkinter_directory, "assets", "icons", "copy.png")))
        self.settingsImg = ctk.CTkImage(light_image=Image.open(os.path.join(self.customtkinter_directory, "assets", "icons", "settings.png")))

        self.build()

    def build(self):
        # $Build widgets$
        self.mainEntry = ctk.CTkEntry(self, width=290, height=50, placeholder_text="Enter the number of characters in the password")
        self.mainEntry.place(x=25, y=20)

        self.opensettingsButton = ctk.CTkButton(self, image=self.settingsImg, width=50, height=50, text="", fg_color="#906DDE", hover_color="#B56DDE", command=self.open_settings)
        self.opensettingsButton.place(x=320, y=20)

        self.digitsBox = ctk.CTkCheckBox(self, width=20, height=20, fg_color="#906DDE", hover_color="#B56DDE", text="Should I use numbers when generating a password?")
        self.digitsBox.place(x=25, y=80)

        self.uppercaseBox = ctk.CTkCheckBox(self, width=20, height=20, fg_color="#906DDE", hover_color="#B56DDE", text="Should I use capital letters \n when generating a password?")
        self.uppercaseBox.place(x=25, y=110)

        self.lowercaseBox = ctk.CTkCheckBox(self, width=20, height=20, fg_color="#906DDE", hover_color="#B56DDE", text="Should I use lowercase letters \n when generating a password?")
        self.lowercaseBox.place(x=25, y=145)

        self.punctuationBox = ctk.CTkCheckBox(self, width=20, height=20, fg_color="#906DDE", hover_color="#B56DDE",  text="Should I use special characters \n when generating a password?")
        self.punctuationBox.place(x=25, y=180)

        self.createBtn = ctk.CTkButton(self, width=105, height=40, text="Generate", fg_color="#906DDE", hover_color="#B56DDE", command=self.generate )
        self.createBtn.place(x=270, y=220)

        self.copyBtn = ctk.CTkButton(self, image=self.copyImg, text="", fg_color="#906DDE", hover_color="#B56DDE", width=40, height=40, command=lambda: pyperclip.copy(self.textresult.get()))
        self.copyBtn.place(x=225, y=220)

        self.textresult = ctk.CTkEntry(self, width=195, height=40, placeholder_text="This will be your password", text_color="GREEN", state="disabled")
        self.textresult.place(x=25, y=220)

        # Загрузка сохранённых настроек
        self.load_settings()


    def generate(self):
        # $Create dependent variables$
        digitsList = []
        uppercaseList = []
        lowercaseList = []
        punctuationList = []
    
        # $Destroy and set the widget to display the result (I can't do it any other way)$
        self.textresult.destroy()
        self.textresult = ctk.CTkEntry(self, width=195, height=40, placeholder_text="This will be your password", text_color="green")
        self.textresult.place(x=25, y=220)
        self.textresult.configure(state="normal")

        # $Translate the string into int. If there is an error, output$
        symbols = int(self.mainEntry.get())

        # $Character count check$
        if symbols < 6:
            self.textresult.insert(0, msgpy.MinimalNumbersSymbolsEN) 
            self.textresult.configure(state="disabled", text_color="RED")
        # $Checking for selected categories$
        if self.digitsBox.get() == 0 and self.uppercaseBox.get() == 0 and self.lowercaseBox.get() == 0 and self.punctuationBox.get() == 0:
            self.textresult.insert(0, msgpy.NoGenerationCategoriesSelectedEN) 
            self.textresult.configure(state="disabled", text_color="RED")
            return 
       
        # $Check already selected categories and randomize values from their lists$
        if self.digitsBox.get():
            _listlong = len(self.digits)
            for i in range(symbols):
                rndIndex = rnd.randint(0, _listlong - 1)
                digitsList.append(self.digits[rndIndex])
        if self.uppercaseBox.get():
            _listlong = len(self.uppercase)
            for i in range(symbols):
                rndIndex = rnd.randint(0, _listlong - 1)
                uppercaseList.append(self.uppercase[rndIndex])
        if self.lowercaseBox.get():
            _listlong = len(self.lowercase)
            for i in range(symbols):
                rndIndex = rnd.randint(0, _listlong - 1)
                lowercaseList.append(self.lowercase[rndIndex])
        if self.punctuationBox.get():
            _listlong = len(self.punctuation)
            for i in range(symbols):
                rndIndex = rnd.randint(0, _listlong - 1)
                punctuationList.append(self.punctuation[rndIndex])

        # $Combine the randoms in the litas into one and mix it up$
        output = digitsList + uppercaseList + lowercaseList + punctuationList
        rnd.shuffle(output)

        # $Basic password creation cycle$ 
        while len(output) != symbols:
            _listlong = len(output)
            index = rnd.randint(0, _listlong)
            try:
                output.pop(index)
            except IndexError:
                try:
                    output.pop(index - 1)
                except IndexError:
                    pass

        else:
            rnd.shuffle(output)
            _result = ''.join(output)
            self.textresult.insert(0, _result)
            self.textresult.configure(state="disabled", text_color="GREEN")

    
    def load_settings(self):
        try:
            # $Загрузка языка$
            if settings.language == 'English':
                self.mainEntry.configure(placeholder_text=inptxt.InputFieldEN)
                self.digitsBox.configure(text=inptxt.CheckBoxNumbersEN)
                self.uppercaseBox.configure(text=inptxt.CheckboxCapitalLettersEN)
                self.lowercaseBox.configure(text=inptxt.CheckBoxLowercaseLettersEN)
                self.punctuationBox.configure(text=inptxt.CheckboxSpecialCharastersEN)
                self.createBtn.configure(text=inptxt.GenerateButtonEN)
                self.applyButton.configure(text=inptxt.ApplyButtonEN)
                self.changeFGCcolor.configure(placeholder_text=inptxt.ChangeFGCcolorEN)
                self.changeHCcolor.configure(placeholder_text=inptxt.ChangeHCcolorEN)
                self.changecolorButton.configure(text=inptxt.ChangeColorButtonEN)

            if settings.language == 'Russian':
                self.mainEntry.configure(placeholder_text=inptxt.InputFieldRU)
                self.digitsBox.configure(text=inptxt.CheckBoxNumbersRU)
                self.uppercaseBox.configure(text=inptxt.CheckboxCapitalLettersRU)
                self.lowercaseBox.configure(text=inptxt.CheckBoxLowercaseLettersRU)
                self.punctuationBox.configure(text=inptxt.CheckboxSpecialCharastersRU)
                self.createBtn.configure(text=inptxt.GenerateButtonRU)
                self.applyButton.configure(text=inptxt.ApplyButtonRU)
                self.changeFGCcolor.configure(placeholder_text=inptxt.ChangeFGCcolorRU)
                self.changeHCcolor.configure(placeholder_text=inptxt.ChangeHCcolorRU)
                self.changecolorButton.configure(text=inptxt.ChangeColorButtonRU)

            if settings.language == 'Chinese':
                self.mainEntry.configure(placeholder_text=inptxt.InputFieldZH)
                self.digitsBox.configure(text=inptxt.CheckBoxNumbersZH)
                self.uppercaseBox.configure(text=inptxt.CheckboxCapitalLettersZH)
                self.lowercaseBox.configure(text=inptxt.CheckBoxLowercaseLettersZH)
                self.punctuationBox.configure(text=inptxt.CheckboxSpecialCharastersZH)
                self.createBtn.configure(text=inptxt.GenerateButtonZH)
                self.applyButton.configure(text=inptxt.ApplyButtonZH)
                self.changeFGCcolor.configure(placeholder_text=inptxt.ChangeFGCcolorZH)
                self.changeHCcolor.configure(placeholder_text=inptxt.ChangeHCcolorZH)
                self.changecolorButton.configure(text=inptxt.ChangeColorButtonZH)

            if settings.language == 'Spanish':
                self.mainEntry.configure(placeholder_text=inptxt.InputFieldES)
                self.digitsBox.configure(text=inptxt.CheckBoxNumbersES)
                self.uppercaseBox.configure(text=inptxt.CheckboxCapitalLettersES)
                self.lowercaseBox.configure(text=inptxt.CheckBoxLowercaseLettersES)
                self.punctuationBox.configure(text=inptxt.CheckboxSpecialCharastersES)
                self.createBtn.configure(text=inptxt.GenerateButtonES)
                self.applyButton.configure(text=inptxt.ApplyButtonES)
                self.changeFGCcolor.configure(placeholder_text=inptxt.ChangeFGCcolorES)
                self.changeHCcolor.configure(placeholder_text=inptxt.ChangeHCcolorES)
                self.changecolorButton.configure(text=inptxt.ChangeColorButtonES)
        except AttributeError:
            pass

    
    def save_settings(self):
        # $Собираем и обновляем настройки языка$
        settings.language = self.changelangMenu.get()
        self.load_settings()

        self.geometry('400x280')
        self.applyButton.destroy()
        self.changelangMenu.destroy()
        self.changeFGCcolor.destroy()
        self.changeHCcolor.destroy()
        self.fgcolorexample.destroy()
        self.hcolorexample.destroy()
        self.changecolorButton.destroy()

        self.opensettingsButton.configure(state="normal")


    def open_settings(self):
        self.geometry('400x455')

        # $Выстраиваем виджеты настроек$
        self.applyButton = ctk.CTkButton(self, width=105, height=40, text="Apply", fg_color="#906DDE", hover_color="#B56DDE", command=self.save_settings )
        self.applyButton.place(x=270, y=270)

        self.opensettingsButton.configure(state="disabled")

        # $Изменения языка приложения$
        self.changelangMenu = ctk.CTkOptionMenu(self, values=['English', 'Russian', 'Chinese', 'Spanish'], width=240, height=40, fg_color="#906DDE", button_hover_color="#B56DDE", button_color="#906DDE")
        self.changelangMenu.set(settings.language)
        self.changelangMenu.place(x=25, y=270)

        self.changecolorButton = ctk.CTkButton(self, width=105, height=40, text="Preview", fg_color="#906DDE", hover_color="#D56DDE", command=self.changecolorama)
        self.changecolorButton.place(x=270, y=315)

        # $Лейбл размером в 30px по вертикали$
        # $Изменения цветов приложения$
        self.changeFGCcolor = ctk.CTkEntry(self, width=195, height=40, placeholder_text="Foreground-color (#906DDE)")
        self.changeFGCcolor.place(x=25, y=315)

        self.changeHCcolor = ctk.CTkEntry(self, width=195, height=40, placeholder_text="Hover-color (#B56DDE)")
        self.load_settings()
        self.changeHCcolor.place(x=25, y=360)

        # $Цветовые аргументы. Показ цветов, которые выбрал пользователь$
        self.fgcolorexample = ctk.CTkFrame(self, width=40, height=40, fg_color="#906DDE")
        self.fgcolorexample.place(x=225, y=315)

        self.hcolorexample = ctk.CTkFrame(self, width=40, height=40, fg_color="#B56DDE")
        self.hcolorexample.place(x=225, y=360)


    def changecolorama(self):
        fgcustomcolor = self.changeFGCcolor.get()
        hcustomcolor = self.changeHCcolor.get()
        self.textresult.configure(state="normal")
        if len(fgcustomcolor) != 7 or fgcustomcolor[0] != "#" :
            self.textresult.insert(0, "Invalid HEX")

        self.textresult.configure(state="disabled", text_color="GREEN")
        

        

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()


'''

1) Кастомные символы
2) Меню настроек языка и цвета
3) Анимации
4) Кастомный виджет (выбор цвета интерфейса, выбор языка)

'''
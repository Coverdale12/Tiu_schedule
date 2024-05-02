import requests
from bs4 import BeautifulSoup as bs
import tkinter as tk

def filter_data_schedule(lessons): #Функция для фильтрации данных
    lister = [] 
    new_lessons = []
    for ii in range(len(lessons)):
        element = []
        for i in lessons[ii]:
            item = str(i.get_text(' '))
            element.append(item)
        lister.append(element)
    new_lessons.append(lister[0])

    for ii in range(1, 49, 7):
        new_lessons.append(lister[ii])
        
    lessons = new_lessons 
    return lessons

def get_schedule(): #функция обращения к сайту
    URL = "https://temnomor.ru/api/groups?group=ИСПт-22-(9)-1" #Ссылка на расписание
    try:
        r = requests.get(URL) #Подключение к серверу
        soup = bs(r.text, "html.parser")#курсор для запросов для сайта
        lessons = soup.findAll('tr') #обращение к большим массивам данных по тегу html
        if lessons == []:
            lessons = 'Проблема на стороне серверов МПК ТИУ\n:('
        else:
            lessons = filter_data_schedule(lessons) #фильтрация данных 
    except requests.exceptions.ConnectionError: #ослеживание ошибки на отсутвие интернета
        lessons = 'Нет доступа в интернет!'
    return lessons

def gapper(item): #Удаление '\t' из данных
    if '\t' in item:
        item = item[1:]
    return item

def place_date(data): #функция установки нумерации №1234567
    for i in data[0]:
        i = i.split(' ')
        if len(i) != 1:
            value = ""
            for ii in range(len(i)):
                i[ii] += '\n'
                value += i[ii]
            value = value[:-1]
            tk.Label(win, text=value, bg='white', font=('Arial', 10,'bold'),relief='solid',width=14, height=3).pack(side='left',anchor='nw')
        else:
            tk.Label(win, text=i, bg='white', font=('Arial', 10,'bold'),relief='solid',width=6, height=3).pack(side='left',anchor='nw')
    
    data.pop(0) 
    return data #Возврат данных без нумерации

def plate_numbers_time(data): # функция установки времени пар 8:00 - 9:35
    num = 52
    for i in range(len(data)):
        tk.Label(win, text=data[i][0],height=4, width=6, relief='solid', bg='white', font=("Arial", 10)).place(x=0,y=num)
        string = data[i][1]
        lister = []
        for el in string:
            lister.append(el)
        lister[7]='\n'
        string= ''.join(lister)
        tk.Label(win, text=string,height=4, width=6, relief='solid', bg='white', font=("Arial", 10)).place(x=54,y=num)
        num += 60
        del data[i][:2]
    return data #Возврат данных без времени 

def plate_lessons(data): #функция отрисовки всех пар
    num = 52
    for i in range(len(data)):
        num1 = 107
        for ii in range(len(data[i])):#конкретный цвет для каждого случая
            if 'снято' in data[i][ii].lower(): #пара снята
                color = '#adb0b2'
                data[i][ii] = '                       Снято'
            elif 'Практика' in data[i][ii]: #Производственная практика
                color = '#5fffc2'
            elif 'самостоятельная' in data[i][ii].lower(): #Самостоятельная работа
                color = '#e1e264'
            elif 'замена' in data[i][ii].lower(): #Пара была заменена
                color = '#6cdcff' 
            elif '(' not in data[i][ii] and len(data[i][ii]) > 1: #праздники
                color = '#ff5f5f'
            else: #остальные случаи
                color = 'white'
            tk.Label(win, text=gapper(data[i][ii]),height=6, font=("Arial", 6, 'bold'), bg=color, relief='solid', width=23,anchor='nw', wraplength=120).place(x=num1,y=num) #размещение лейбла с парой
            num1 +=118  
        num +=60        

def place_schedule(): #функция отрисовки расписания в окне
    data = get_schedule()# Получение данных в переменную data
    if data != 'Нет доступа в интернет!' and data != 'Проблема на стороне серверов МПК ТИУ\n:(': #Проверка считываемости данных
        data = plate_lessons(plate_numbers_time(place_date(data))) #распределение данных по функции, финальная фильтрация
    else:
        tk.Label(win, text = data, font=("Arial",30), bg='white', justify='center', fg='blue').pack() #Вывод окна с ошибкой подключения
    
def main(): #функция создания окна
    global win
    win = tk.Tk()
    win.title('ИСПт 22-(9)-1')
    win.geometry('933x480')
    win.configure(bg= 'white')
    win.resizable(False, False)
    win.iconbitmap('./icon.ico') #Установка иконки
    place_schedule() # Обращение у установке расписания в окне
    win.mainloop()

if __name__ == '__main__': #запуск программы
    main()
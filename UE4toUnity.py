import pyperclip
import time
import pyautogui

def parsing(i):
    start = i.find('(')+1
    end = i.find(')')
    pars = i[start:end].split(',')
    for j in range(len(pars)):
        start = pars[j].find('=')+1
        pars[j] = float(pars[j][start:])
    return pars

while True:    
    text = pyperclip.paste().split('\n')

    while True:
        pyautogui.click(x=900, y=320)
        aim = pyautogui.confirm(text='Курсор наведён на копируемый объект?',
                                title='Выбор объекта копирования',
                                buttons=['Да, начать копирование',
                                         'Нет, повторить центрирование',
                                         'Закончить выполнение'])
        if aim == 'Да, начать копирование': break
        if aim == 'Закончить выполнение':
            text = ''
            break

    starttime = time.time()
    quantity  = 0
    flag = 0
    for i in text:
        
        if i.find('RelativeLocation')  != -1:
            location = parsing(i)
            location[1], location[2] = location[2], location[1]
            location[0] = round(location[0]*(-0.01), 5)
            location[1] = round(location[1]*(0.01), 5)
            location[2] = round(location[2]*(0.01), 5)
            flag += 1

        if i.find('RelativeRotation')  != -1:
            rotation = parsing(i)
            rotation[0] -= 90
            flag += 1

        if i.find('ActorLabel')  != -1:
            start = i.find('"')+1
            end = i.find('"', start)
            name = i[start:end]
            flag += 1

        if flag == 3:
            pyautogui.click(x=900, y=320)
            pyautogui.keyDown('ctrl')
            pyautogui.press('d')
            pyautogui.keyUp('ctrl')
            print('Object name:', name)        
            transform = [location, rotation]
            transformname = ('location', 'rotation')
            axis = ('X', 'Y', 'Z')
            onscreen = [[1710, 1800, 1882], [186, 203]]
            for i in range(len(transform)):
                print(str(transformname[i]).title(), 'in Unity')
                for j in range(len(axis)):
                    print(axis[j]+': '+str(transform[i][j]))
                    pyperclip.copy(transform[i][j])
                    pyautogui.click(x=onscreen[0][j], y=onscreen[1][i])
                    pyautogui.hotkey('ctrl', 'v')
            quantity += 1
            flag = 0
            print()

    extime = round((time.time()-starttime)/60, 2)
    if aim != 'Закончить выполнение':
        end = pyautogui.confirm(text='Создан {} объект(ов)\nВремя выполнения {} мин'.format(quantity, extime),
                                title='Статистика выполнения',
                                buttons=['Вставить новые координаты',
                                         'Закончить выполнение'])
    end = 'Закончить выполнение' if aim == 'Закончить выполнение' else end
    if end == 'Закончить выполнение': break

    print('Objects quantity: {}'.format(quantity))
    print('Execution time: {} min'.format(round((time.time()-starttime)/60, 2)))

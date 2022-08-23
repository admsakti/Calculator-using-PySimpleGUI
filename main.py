import PySimpleGUI as sg


def create_window(theme='dark'):
    sg.theme(theme)
    sg.set_options(font='Franklin 14', button_element_size=(6, 3))
    button_size = (6, 3)

    layout = [
        [sg.Text('', key='-POPUP-', expand_x=True, font='Franklin 16'),
            sg.Text('', key='-OUTPUT-', font='Franklin 22', justification='right',
                    expand_x=True, pad=(10, 20), right_click_menu=theme_Menu)
        ],
        [sg.Button('Clear', size=button_size, key='-CLEAR-'),
            sg.Button('Delete', size=button_size, key='-DELETE-'),
            sg.Button('Enter', expand_x=True, key='-ENTER-')
        ],
        [sg.Button('7', size=button_size),
            sg.Button('8', size=button_size),
            sg.Button('9', size=button_size),
            sg.Button('/', size=button_size)
        ],
        [sg.Button('4', size=button_size),
            sg.Button('5', size=button_size),
            sg.Button('6', size=button_size),
            sg.Button('*', size=button_size)
        ],
        [sg.Button('1', size=button_size),
            sg.Button('2', size=button_size),
            sg.Button('3', size=button_size),
            sg.Button('-', size=button_size)
        ],
        [sg.Button('0', expand_x=True),
            sg.Button('.', size=button_size),
            sg.Button('+', size=button_size)
        ]
    ]
    return sg.Window('Calculator', layout, size=(355, 500))


def full_operation(event_key):
    global num_string

    currentNum.append(event_key)
    num_string = ''.join(currentNum)
    window['-OUTPUT-'].update(num_string)


def delete():
    global num_string

    try:
        currentNum.pop(-1)
        num_string = ''.join(currentNum)
        window['-OUTPUT-'].update(num_string)
    except IndexError:
        pass


def clear():
    global currentNum
    global num_string
    global result

    result = ''
    num_string = ''
    currentNum = []
    window['-OUTPUT-'].update('')
    window['-POPUP-'].update('')


def count_popup(popup):
    try:
        popup = cut_zeroes(popup)
    except ValueError:
        popup = popup

    try:
        popup_show = round(eval(popup), 3)
    except SyntaxError:
        popup_show = ''
        window['-OUTPUT-'].update('ERROR')

    window['-POPUP-'].update(popup_show)


def cut_zeroes(zeroes):
    i, res = 0, []
    n = len(zeroes)

    while i < n:
        j = i
        while i < n and zeroes[i] not in '+-/*.':
            i += 1
        res.append(int(zeroes[j:i]))

        if i < n:
            res.append(zeroes[i])

        i += 1

    return ''.join(map(str, res))


def count_eval(output):
    result_eval = eval(output)
    window['-OUTPUT-'].update(result_eval)


result = ''
num_string = ''
currentNum = []

theme_Menu = ['Theme', ['LightGrey1', 'DarkBrown2', 'BrightColors', 'GreenTan', 'Random']]
window = create_window()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event in theme_Menu[1]:
        window.close()
        window = create_window(event)

    if event in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
        full_operation(event)
        count_popup(num_string)

    if event in ('.', '+', '-', '*', '/'):
        full_operation(event)

    if event == '-CLEAR-':
        clear()

    if event == '-DELETE-':
        delete()

    if event == '-ENTER-':
        try:
            result = cut_zeroes(num_string)
        except ValueError:
            result = num_string

        try:
            count_eval(result)
        except SyntaxError:
            # window['-POPUP-'].update('')
            # window['-OUTPUT-'].update('ERROR')
            clear()
        else:
            window['-POPUP-'].update('')


window.close()

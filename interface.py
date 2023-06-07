import PySimpleGUI as sg


def interface():

    sg.theme('Reddit')

    layout = [
        [sg.Text('Digite o cnpj da empresa: ')],
        [sg.Input(key='Cnpj')],
        [sg.Button('Consultar')],
        [sg.Text('Carregando...', key='loading_text', visible=False)],
        [sg.Text('⣾', key='spinner', visible=False)]
    ]

    window = sg.Window('Tela de consulta', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Consultar':
            window['Consultar'].update(disabled=True)
            window['loading_text'].update(visible=True)
            window['spinner'].update(visible=True)
            window.Refresh()
            return values['Cnpj']

    window.Close()

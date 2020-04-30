import requests
import json

try:
    import tkinter
    from tkinter import filedialog
except ImportError:
    import Tkinter as tkinter
    from tkinter import filedialog


# def example():
#     root = tkinter.Tk()
#
#     name_label = tkinter.Label(text="Имя:").grid(row=0, column=0, sticky="W", pady=10, padx=10)
#     table_name = tkinter.Entry(width=30)
#     table_name.grid(row=0, column=1, columnspan=3, sticky='WE', padx=10)
#
#     name_label_2 = tkinter.Label(text="Столбцов:").grid(row=1, column=0, sticky='W', padx=10, pady=10)
#     table_column = tkinter.Spinbox(width=7, from_=1, to=50)
#     table_column.grid(row=1, column=1, padx=10)
#     tkinter.Label(text="Строк:").grid(row=1, column=2, sticky='E')
#     table_row = tkinter.Spinbox(width=7, from_=1, to=100)
#     table_row.grid(row=1, column=3, sticky='E', padx=10)
#
#     info_button = tkinter.Button(text="Справка").grid(row=2, column=0, pady=10, padx=10)
#     tkinter.Button(text="Вставить").grid(row=2, column=2)
#     tkinter.Button(text="Отменить").grid(row=2, column=3, padx=10)
#
#     # root.minsize(300,300)
#     # root.maxsize(300,300)
#     root.mainloop()

def get_statuses_by_barcodes(lang, barcodes):
    parameters = {'lang': lang}
    headers = {'Authorization': 'Bearer d88371da-60c7-3651-8609-35d93c29a05a',
               'Content-Type': 'application/json'}

    url = 'https://www.ukrposhta.ua/status-tracking/0.0.1/statuses/with-not-found'

    status_data = requests.post(url, params=parameters, headers=headers, data=json.dumps(barcodes))
    print(status_data.url)
    return status_data


def label_info_updater(label, text_var, text, error_flag):
    if error_flag:
        label.config(background="#f15b60")
        text_var.set(text)
    else:
        label.config(background="#8bc63f")
        text_var.set(text)


def status_label_info(data):
    print(data.status_code)
    if data.status_code == 200:
        text = '200 OK'
        label_info_updater(status_code_label, status_code_text, text, False)
    elif data.status_code == 404:
        text = 'ШКІ не знайдено'
        label_info_updater(status_code_label, status_code_text, text, True)
    elif data.status_code == 500:
        text = 'Помилка сервера'
        label_info_updater(status_code_label, status_code_text, text, True)
    # else:
    #     text = 'Невідома помилка. Код: ' + str(data.status_code)
    #     label_info_updater(status_code_label, status_code_text, text, True)


def default_color():
    status_code_label.configure(background='#ffce2f')
    status_code_text.set("")


def get_entry_text(entry):
    forbidden_symbols = set('[~!@#$%^&*()_+{}":;\']+$')
    # forbidden_letters = set('asdfghjjklqwertyuiopzxcvbnmQWERTYUIIIOPASDFGHJKLZXCVBNM')
    raw_barcodes = entry.get(1.0, tkinter.END).split()
    incorrect_barcodes = list()
    barcodes = list()
    for barcode in raw_barcodes:
        if forbidden_symbols.intersection(barcode):
            incorrect_barcodes.append(barcode)
        elif len(barcode) != 13:
            incorrect_barcodes.append(barcode)
        else:
            barcodes.append(barcode)
    # if forbidden_symbols.intersection(barcode):
    #     barcode = "ШКІ не має міститі спецсимволи."
    #     label_info_updater(barcode_label, barcode_text, barcode, True)
    #     default_color()
    # elif forbidden_letters.intersection(text):
    #     barcode = "ШКІ не має міститі букви."
    #     label_info_updater(barcode_label, barcode_text, barcode, True)
    #     default_color()
    # elif len(text) != 13:
    #     barcode = "ШКІ має складатися з 13 символів."
    #     label_info_updater(barcode_label, barcode_text, barcode, True)
    #     default_color()
    # else:
    #     barcode = text
    #     label_info_updater(barcode_label, barcode_text, barcode, False)

    return barcodes, incorrect_barcodes


def save_file(data, barcode, incorrect_barcodes):
    if data.status_code == requests.codes.ok:
        status_label_info(data)
        mainWindow.filename = filedialog.asksaveasfilename(initialdir="C:/",
                                                           title="Выберете папку",
                                                           initialfile='Statuses',
                                                           filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        with open(mainWindow.filename + ".txt", "w") as file:
            statuses = data.json()
            file.write(json.dumps(statuses, sort_keys=True, indent=4))
            file.write('\n' + str(incorrect_barcodes))
    else:
        status_label_info(data)


def button_get_text():
    barcodes, incorrect_barcodes = get_entry_text(text_field)
    data = get_statuses_by_barcodes(r_val.get(), barcodes)
    save_file(data, barcodes, incorrect_barcodes)


width = 500
height = 300

mainWindow = tkinter.Tk()

mainWindow.title("Status Downloader")

mainWindow.geometry("{}x{}".format(width, height))
mainWindow.configure(background='#ffce2f')

info_label = tkinter.Label(text="Получить статусы отправлений", background='#ffce2f')
info_label.pack(side='top', fill='x')

barcode_text = tkinter.StringVar()
barcode_text.set("Введите ШКИ отправлений")

barcode_label = tkinter.Label(textvariable=barcode_text, background='#ffce2f')
barcode_label.pack(side='top', fill='x')

status_code_text = tkinter.StringVar()
status_code_label = tkinter.Label(textvariable=status_code_text, background='#ffce2f')
status_code_label.pack(side='top', fill='x')

text_frame = tkinter.Frame(mainWindow)
text_frame.pack(side='left')

text_field = tkinter.Text(text_frame, width=50, height=10)
text_field.pack(side='top')

button_go = tkinter.Button(text_frame, text="Получить", relief="raised", command=button_get_text)
button_go.pack(side='right')

radio_frame = tkinter.Frame(text_frame)
r_val = tkinter.StringVar()
r_val.set('en')
r1 = tkinter.Radiobutton(radio_frame, text='en', variable=r_val, value='en')
r2 = tkinter.Radiobutton(radio_frame, text='ua', variable=r_val, value='ua')
r1.pack(side='left')
r2.pack(side='right')

radio_frame.pack(side='left')

mainWindow.mainloop()

# data = get_statuses_by_barcodes('en', ["SF015183061EE"])
# statuses = data.json()
#
# with open("statuses.txt", "w") as file:
#     file.write(json.dumps(statuses, sort_keys=True, indent=4))
#
# print(json.dumps(statuses, sort_keys=True, indent=4))

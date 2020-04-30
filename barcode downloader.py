import requests

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
    forbidden_letters = set('asdfghjjklqwertyuiopzxcvbnmQWERTYUIIIOPASDFGHJKLZXCVBNM')
    text = entry.get()

    if forbidden_symbols.intersection(text):
        barcode = "ШКІ не має міститі спецсимволи."
        label_info_updater(barcode_label, barcode_text, barcode, True)
        default_color()
    elif forbidden_letters.intersection(text):
        barcode = "ШКІ не має міститі букви."
        label_info_updater(barcode_label, barcode_text, barcode, True)
        default_color()
    elif len(text) != 13:
        barcode = "ШКІ має складатися з 13 символів."
        label_info_updater(barcode_label, barcode_text, barcode, True)
        default_color()
    else:
        barcode = text
        label_info_updater(barcode_label, barcode_text, barcode, False)

    return barcode


def get_sticker_by_barcode(barcode):
    parameters = {'token': '5ad3833f-083f-2867-e053-6d28310abbf5'}
    headers = {'Authorization': 'Bearer 998e005e-accb-35ed-adde-abf4480f18dc'}

    url = 'https://ukrposhta.ua//ecom//0.0.1//shipments//{}//sticker'.format(barcode)

    data = requests.get(url, parameters, headers=headers)
    return data


# def save_sticker(data):
#     if data.status_code == requests.codes.ok:
#         save_file(data, barcode)
#     else:
#         print("error") # error message


def save_file(data, barcode):
    if data.status_code == requests.codes.ok:
        status_label_info(data)
        mainWindow.filename = filedialog.asksaveasfilename(initialdir="C:/",
                                                           title="Оберіть папку",
                                                           initialfile=barcode,
                                                           filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
        with open(mainWindow.filename + ".pdf", "wb") as file:
            file.write(data.content)

    else:
        status_label_info(data)


def button_get_text():
    barcode = get_entry_text(entry_field)
    if len(barcode) == 13:
        data = get_sticker_by_barcode(barcode)
        save_file(data, barcode)


width = 300
height = 100

mainWindow = tkinter.Tk()

info_text = "StickerGet"

mainWindow.title("Barcode Downloader")

mainWindow.geometry("{}x{}".format(width, height))
mainWindow.configure(background='#ffce2f')

info_label = tkinter.Label(text="Отримати стікер за ШКІ", background='#ffce2f')
# info_label.grid(row=0, column=0, columnspan=3)
info_label.pack(side='top', fill='x')

barcode_text = tkinter.StringVar()
barcode_text.set("Введіть ШКІ відпровлення")

barcode_label = tkinter.Label(textvariable=barcode_text, background='#ffce2f')
# barcode_label.grid(row=5, column=0, sticky='nsew')
barcode_label.pack(side='top', fill='x')

status_code_text = tkinter.StringVar()
status_code_label = tkinter.Label(textvariable=status_code_text, background='#ffce2f')
status_code_label.pack(side='top', fill='x')

entry_frame = tkinter.Frame(mainWindow)

entry_field = tkinter.Entry(entry_frame, width=26)
# table_name.grid(row=1, column=0, columnspan=3, sticky='nsew')
# table_name.grid(row=1, column=0, columnspan=3, rowspan=2, sticky='nsew', padx=10)
entry_field.pack(side='left')

button_go = tkinter.Button(entry_frame, text="Отримати", relief="raised", command=button_get_text)
# button_go.grid(row=1, column=3, rowspan=2, sticky="nsew")
button_go.pack(side='left')

entry_frame.pack(side='left')

mainWindow.minsize(width, height)
mainWindow.maxsize(width, height)

mainWindow.mainloop()
# example()

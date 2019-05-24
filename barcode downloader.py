import requests

try:
    import tkinter
except ImportError:
    import Tkinter as tkinter


info_text = "Привет косолапые из отдела поддержки юр лиц"

mainWindow = tkinter.Tk()

mainWindow.title("Black Jack Game")
mainWindow.geometry("640x480")
mainWindow.configure(background='#ffce2f')

info_label = tkinter.Label(mainWindow, text=info_text, fg='black')
info_label.grid(row=0,column=0)

'''
barcode = input('Enter a barcode: ')
token = '5cd620e2-eaf5-49f6-aff0-4be03211f2fc'

url = 'http://10.255.102.215:8080/UkrPostAPI/shipments/{}/sticker?token={}'.format(barcode, token)

r = requests.get(url)

#file_name = '{}.pdf'.format(barcode)
root.filename =  filedialog.asksaveasfilename(initialdir = "C:/",
                                              title = "Оберіть папку", initialfile=barcode,
                                              filetypes = (("pdf files","*.pdf"), ("all files","*.*")))
print (root.filename)


with open(root.filename + ".pdf", "wb") as code:
    code.write(r.content)

print("Your file downloaded")
'''

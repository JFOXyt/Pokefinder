import tkinter.messagebox
import requests,tkinter,time
from tkinter import messagebox
from tkinter.messagebox import showerror
from tkinter import PhotoImage

root=tkinter.Tk()
root.geometry('500x300')
root.resizable(False,False)

result_labels = []

def clearlabel():
    pokeentry.delete(0,tkinter.END)

def pokefinder():

    for label in result_labels:
        label.destroy()
    result_labels.clear()

    op = pokeentry.get().lower().strip()

    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{op}')
    

    if response.status_code==200 and op!='':

        url = response.json()

        idpoke = url['id']
        responsedescript=requests.get(f'https://pokeapi.co/api/v2/characteristic/{idpoke}/')

        urldescript=responsedescript.json()

        namepoke = url['name']
        namepoket = tkinter.Label(root, text=f'Name: {namepoke.capitalize()}')
        namepoket.place(x=25, y=150)
        result_labels.append(namepoket)

        for i in range(3):
            stats = url['stats'][i]
            basestat = stats['base_stat']
            stat = stats['stat']
            namestat = stat['name']

            statt = tkinter.Label(root, text=f'{namestat.capitalize()}: {basestat}')
            statt.place(x=25, y=(175 + 25 * i))
            result_labels.append(statt)

        
        idpoket = tkinter.Label(root, text=f'ID: {idpoke}')
        idpoket.place(x=175, y=150)
        result_labels.append(idpoket)

        heightpoke = url['height']
        heightpoket = tkinter.Label(root, text=f'Height: {heightpoke}')
        heightpoket.place(x=175, y=175)
        result_labels.append(heightpoket)

        weightpoke = url['weight']
        weightpoket = tkinter.Label(root, text=f'Weight: {weightpoke}')
        weightpoket.place(x=175, y=200)
        result_labels.append(weightpoket)

        if responsedescript.status_code==200:
            descripteng=urldescript['descriptions'][7]
            tedescripteng=descripteng['description']
            langeng=descripteng['language']['name']

            descriptja=urldescript['descriptions'][8]
            tedescriptja=descriptja['description']
            langja=descriptja['language']['name']

            descriptt=tkinter.Label(root,text=f'{langeng}: {tedescripteng}\n{langja}: {tedescriptja}')
            descriptt.place(x=300,y=250)

    else:
        tkinter.messagebox.showerror(title='ERROR',message='Check if your connected to wifi or if you entered a name of a real pokemon')

frametop=tkinter.Frame(root,background='gray',height=75,width=1000)
frametop.place(x=0,y=0)

poketexto=tkinter.Label(root,text='POKEFINDER',font=('Comic Sans MS',18),fg='yellow',bg='blue')
poketexto.place(x=167,y=15)

pokeentry=tkinter.Entry(root)
pokeentry.place(x=25,y=100,height=30,width=170)

pesquisarbuton=tkinter.Button(root,text='Search',command=lambda: [pokefinder(),clearlabel()] )
pesquisarbuton.place(x=210,y=100,height=30,width=150)

root.config(bg='white')
root.mainloop()
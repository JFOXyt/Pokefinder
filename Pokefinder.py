import requests,tkinter,tkinter.messagebox
from tkinter import PhotoImage,ttk

root=tkinter.Tk()
root.geometry('500x400')
root.resizable(False,False)
root.title('Pokefinder')
icon=tkinter.PhotoImage(file='C:\\Users\\Administrator\\Desktop\scripts py\\pokefinder\\icon.png')
icons=root.iconphoto(False,icon)


result_labels = []

def clearentry():
    namepokeentry.delete(0,tkinter.END)
    idpokeentry.delete(0,tkinter.END)

def pokefinder():

    for label in result_labels:
        label.destroy()
    result_labels.clear()


    opname = namepokeentry.get().lower().strip()
    opid=idpokeentry.get().lower().strip()

    if opname!='':
        op=opname
    elif opid!='':
        op=opid
    else:
        op=''
    

    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{op}')

    if response.status_code==200 and op!='':

        url = response.json()

        idpoke = url['id']
        responsedescript=requests.get(f'https://pokeapi.co/api/v2/characteristic/{idpoke}/')

        urlimg = "https://github.com/PokeAPI/sprites/blob/ca5a7886c10753144e6fae3b69d45a4d42a449b4/sprites/pokemon/{id}.png?raw=true"

        urldamagerelations=requests.get(f"https://pokeapi.co/api/v2/type/{idpoke}/")

        urllocation=requests.get(f'https://pokeapi.co/api/v2/pokemon/{idpoke}/encounters')
        
        urlhabitat=requests.get('https://pokeapi.co/api/v2/pokemon-habitat/1/')



        species_url = url['species']['url']
        species_response = requests.get(species_url)

        if species_response.status_code == 200:
            evolution_chain_url = species_response.json()['evolution_chain']['url']
            urlevolution = requests.get(evolution_chain_url)
        else:
            urlevolution = None

        try:
            urldescript=responsedescript.json()
        except:
            pass

        try:
            responsedamagerelations=urldamagerelations.json()
        except:
            pass

        try:
            responseevolution=urlevolution.json()
        except:
            pass

        try:
            responselocation=urllocation.json()
        except:
            pass

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
        idpoket.place(x=150, y=150)
        result_labels.append(idpoket)

        heightpoke = url['height']
        heightpoket = tkinter.Label(root, text=f'Height: {heightpoke}')
        heightpoket.place(x=150, y=175)
        result_labels.append(heightpoket)

        weightpoke = url['weight']
        weightpoket = tkinter.Label(root, text=f'Weight: {weightpoke}')
        weightpoket.place(x=150, y=200)
        result_labels.append(weightpoket)

        if responsedescript.status_code==200:

            descripteng=urldescript['descriptions'][7]
            tedescripteng=descripteng['description']
            langeng=descripteng['language']['name']

            descriptja=urldescript['descriptions'][8]
            tedescriptja=descriptja['description']
            langja=descriptja['language']['name']

            descriptt=tkinter.Label(root,text=f'{langeng}: {tedescripteng}\n{langja}: {tedescriptja}')
            result_labels.append(descriptt)
            descriptt.place(x=300,y=250)

        elif responsedescript.status_code==404:
            try:
                descriptt=tkinter.Label(root,text='Description not found')
                result_labels.append(descriptt)
                descriptt.place(x=315,y=250)
            except:
                pass

        responseimg = requests.get(urlimg.format(id=idpoke))

        if responseimg.status_code==200:

            with open("pokemon.png", "wb") as f:
                f.write(responseimg.content)

            image = PhotoImage(file="pokemon.png")

            image_label = tkinter.Label(root, image=image)
            image_label.image = image
            image_label.place(x=325,y=140)
            result_labels.append(image_label)

        else:
            image_label.config(image='')

        if urldamagerelations.status_code==200:
            try:
                weakness=responsedamagerelations['damage_relations']['double_damage_from'][0]['name']
            except:
                weakness="Not found"

            try:
                resistance=responsedamagerelations['damage_relations']['double_damage_to'][0]['name']
            except:
                resistance="Not found"

            weaknesst=tkinter.Label(root,text=f'Weakness: {weakness}')
            weaknesst.place(x=150,y=225)
            result_labels.append(weaknesst)

            resistancet=tkinter.Label(root,text=f'Resistance: {resistance}')
            resistancet.place(x=150,y=250)
            result_labels.append(resistancet)
        else:
            weaknesst=tkinter.Label(root,text="Weakness: Not found")
            weaknesst.place(x=150,y=225)
            result_labels.append(weaknesst)

            resistancet=tkinter.Label(root,text="Resistance: Not found")
            resistancet.place(x=150,y=250)
            result_labels.append(resistancet)

        if urlevolution.status_code==200:
            chain = responseevolution['chain']
            names=[chain['species']['name']]

            to_process = chain['evolves_to']

            while to_process:
                current_evolution = to_process.pop(0)
                names.append(current_evolution['species']['name'])
                to_process.extend(current_evolution['evolves_to'])

                evot=tkinter.Label(root,text='Evoluções: ' + ' -> '.join(names),wraplength=175)
                evot.place(x=300,y=300)
                result_labels.append(evot)

        elif urlevolution.status_code!=200:
            evot=tkinter.Label(root,text="Evoluções: Doesn't exist")
            evot.place(x=300,y=300)
            result_labels.append(evot)

        if urllocation.status_code==200:
            locall=[]
            if responselocation!=[]:
                n=0
                local=responselocation[n]['location_area']['name']

                while n<13:
                    try:
                        local=responselocation[n]['location_area']['name']
                        locall.append(local)
                        n+=1
                        
                    except:
                        n=101

                loaclln=len(locall)
                locall.pop(loaclln-1)
                locallj=','.join(locall)
                localljr=locallj.replace('-',' ')
                if n==13:
                    amais=', ...'
                    localt=tkinter.Label(root,text=f'Location area: {localljr}{amais}',wraplength=265,justify='left')
                    localt.place(x=25,y=280)
                    result_labels.append(localt)

                else:

                    if localljr!='':
                        localt=tkinter.Label(root,text=f'Location area: {localljr}',wraplength=265,justify='left')
                        localt.place(x=25,y=280)
                        result_labels.append(localt)
                    else:
                        localt=tkinter.Label(root,text=f'Location area: Not found',wraplength=265,justify='left')
                        localt.place(x=25,y=280)
                        result_labels.append(localt)
                        
            else:
                localt=tkinter.Label(root,text=f'Location area: Not found',wraplength=265,justify='left')
                localt.place(x=25,y=280)
                result_labels.append(localt)

        

        elif urllocation!=200:
            pass
        
        if urlhabitat.status_code==200:
            habitatpoke='Not found'
            for i in range(1,15):
                urlhabitat=requests.get(f'https://pokeapi.co/api/v2/pokemon-habitat/{i}/')

                try:
                    responsehabitat=urlhabitat.json()
                except:
                    pass
                    

                qnt=len(responsehabitat['pokemon_species'])

                for c in range(1,qnt+1):
                    pokes=responsehabitat['pokemon_species'][c-1]['name']
                    if pokes==namepoke:
                        habitatpoke=responsehabitat['name'].replace('-',' ')
                         
            habitatt=tkinter.Label(root,text=f'Habitat: {habitatpoke}')
            habitatt.place(x=25,y=250)
            result_labels.append(habitatt)
                    
        elif urlhabitat.status_code!=200:
            pass

        else:
            pass
            
    else:
        tkinter.messagebox.showerror(title='ERROR',message='Check if your connected to wifi or if you entered a name of a real pokemon')

style=ttk.Style()
style.theme_use('vista')

frametop=tkinter.Frame(root,background='gray',height=75,width=1000)
frametop.place(x=0,y=0)

imagepoke = PhotoImage(file="C:\\Users\\Administrator\\Desktop\\scripts py\\pokefinder\\pokemonimage.png")

image_labelpoke = tkinter.Label(root, image=imagepoke,bg='gray')
image_labelpoke.imagepoke = imagepoke
image_labelpoke.place(x=25,y=10)

finder=tkinter.Label(root,text='FINDER',bg='gray',font=('Pokemon Solid',18,'bold'),fg='yellow')
finder.place(x=235,y=0)

namepokeentry=ttk.Entry(root)
namepokeentry.place(x=25,y=100,height=30,width=140)

idpokeentry=ttk.Entry(root)
idpokeentry.place(x=175,y=100,height=30,width=140)

img_button=tkinter.PhotoImage(file='C:\\Users\\Administrator\\Desktop\\scripts py\\pokefinder\\butao.gif').subsample(11,11)

pesquisarbuton=tkinter.Button(root,image=img_button,command=lambda: [pokefinder(),clearentry()],cursor='hand2',border=0,bg='white')
pesquisarbuton.place(x=320,y=95)

namet=tkinter.Label(root,text='Name:',bg='white')
namet.place(x=25,y=75)

idt=tkinter.Label(root,text='Id:',bg='white')
idt.place(x=175,y=75)

root.config(bg='white')
root.mainloop()

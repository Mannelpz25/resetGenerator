from tkinter.font import ITALIC
import requests
from tkinter.filedialog import  asksaveasfilename
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
from threading import Thread



# API Siliant
def apiOnline(id):
  url = "https://wso.resser.com/api/producthistoryfilter"
  params = dict(_dc="1665315187835")
  headers = {
  "Accept":"*/*",
  "Accept-Encoding":"gzip, deflate, br",
  "Accept-Language":"es-ES,es;q=0.9",
  "Authorization":"Basic bWFudWVsbDpVMkZzZEdWa1gxK05talNweGVQejM2c2hxYVpOc25QQlJSTzlhSTVMd0RVPQ==",
  "Connection":"keep-alive",
  "Content-Length":"721",
  "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
  "Host":"wso.resser.com",
  "Origin":"http://onlineresser.azurewebsites.net",
  "Referer":"http://onlineresser.azurewebsites.net/",
  "sec-ch-ua":'"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
  "sec-ch-ua-mobile":"?0",
  "sec-ch-ua-platform":'"Windows"',
  "Sec-Fetch-Dest":"empty",
  "Sec-Fetch-Mode":"cors",
  "Sec-Fetch-Site":"cross-site",
  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
  "X-Requested-With":"XMLHttpRequest",
  }
  datos = {
    'activo':'',
    'antiguo':'false',
    'incluirAntiguos':'',
    'cuentaParaNuevo':'',
    'lugar':'0',
    'fechaCreacionL':"01/01/2000",
    'fechaCreacionH':"01/01/2025",
    'fechaActL':'',
    'fechaActH':'',
    'simSerial':'',
    'carrier':'',
    'idResser':id,
    'idFabricante':'',
    'equipo':'',
    'idCliente':'',
    'sustituto':'',
    'numeroOrden':'',
    'firmware':'',
    'plan':'',
    'producto':'',
    'folio':'',
    'centroDistribucion':'',
    'fechaEntradaAlmL':'',
    'fechaEntradaAlmH':'',
    'fechaInstalacionL':'',
    'fechaInstalacionH':'',
    'instalador':'',
    'marca':'',
    'subMarca':'',
    'numeroSerie':'',
    'numEconomico':'',
    'placas':'',
    'fechaDesmonteL':'',
    'fechaDesmonteH':'',
    'instaladorDesmonto':'',
    'desmontoStatus':'',
    'fechaReparacionL':'',
    'fechaReparacionH':'',
    'idArrendadora':'',
    'contratoArrendadora':'',
    'arrendadoraVigente':'',
    'contratoVigencia':'',
    'vigenciaVigente':'',
    'contratoGarantia':'',
    'garantiaVigente':'',
    'contratoMonitoreo':'',
    'monitoreoVigente':'',
    'page':'1',
    'start':'0',
    'limit':'400'
  } # <- El json que enviamos
  respuesta = requests.post(url, params=params, headers=headers, data=datos)
  # Ahora decodificamos la respuesta como json
  cjson = respuesta.json()  
  return cjson


class ResetGenerator:
    def __init__(self, master):
        self.master = master
        master.title("ResetGenerator")
        self.labelEntry = Label(master, text="Id's:")
        self.labelEntry.place(relx=0.05, rely=0.05,relwidth=.05, relheight=0.05)
        self.textIds = Entry(master)
        self.textIds.place(relx=0.1, rely=0.05,relwidth=0.85, relheight=0.05)      
        self.labelEntryPlaceHolder = Label(master, text="Separa los id's con comas", font=("Arial", 10, ITALIC), fg='#808080')
        self.labelEntryPlaceHolder.place(relx=0.1, rely=0.1,relwidth=.85, relheight=0.05)
        self.buttonStart = ttk.Button(master , text='Generar',command=self.generator)
        self.buttonStart.place(relx=0.15, rely=0.2,relwidth=0.3, relheight=0.05)
        self.buttonDownloadFile = ttk.Button(master , text='Descargar Resultados', command=self.toFile, state=DISABLED)
        self.buttonDownloadFile.place(relx=0.55, rely=0.2,relwidth=0.3, relheight=0.05)
        self.labelProgress = Label(master, text="En espera...")
        self.labelProgress.place(relx=0.3, rely=0.25,relwidth=0.4, relheight=0.05)
        self.progressbar = ttk.Progressbar( master,orient='horizontal', mode='indeterminate')
        self.progressbar.place(relx=0.05, rely=0.3,relwidth=0.9, relheight=0.05) 
        self.labelResult = Label(master, text="Resultados:")
        self.labelResult.place(relx=0.3, rely=0.4,relwidth=0.4, relheight=0.05)
        self.textResult = scrolledtext.ScrolledText(master, font=("Arial", 11))
        
        self.textResult.config(state=DISABLED)
        self.textResult.place(relx=0.05, rely=0.45,relwidth=.9, relheight=0.5)  

    def hilo(self):   
              
        self.generatorResets()
        self.progressbar.stop()
        self.imprimirResultados()
        
        self.buttonStart['state'] = NORMAL
        self.buttonDownloadFile['state'] = NORMAL
        self.textIds['state'] = NORMAL
        self.labelProgress['text'] = "Resets generados..."

    def generator(self):
        if(self.textIds.get() == ""):
            messagebox.showerror(title='Error', message="Favor de ingresar id's para generar resets")
        else:
            self.textIds['state'] = DISABLED
            self.buttonStart['state'] = DISABLED
            self.buttonDownloadFile['state'] = DISABLED
            self.crearDiccionario()
            self.progressbar.start()
            self.labelProgress['text'] = "Generando resets..."
            Thread(target=self.hilo).start()
    
    def crearDiccionario(self):
        global dataIn
        data = self.textIds.get()
        data = data.split(',')
        dataIn['id'] = []
        for item in data:
            dataIn['id'].append(item.strip())

    def generatorResets(self):    
        global generetedResets, dataIn, como_json
        generetedResets = {}
        for item in dataIn['id']:
            id=item    
            print(id)
            if(id=="" or not id):
                continue
            como_json=apiOnline(id)            
            if(como_json['count']!=0):
                modelo=como_json['history'][0]['produccion']['producto'].upper()
                telefono=como_json['history'][0]['telefono']
                imei=como_json['history'][0]['produccion']['idFabricante']
                msg=''
                msg2=''
                generetedResets[id] ={}
                generetedResets[id]['modelo']=modelo
                generetedResets[id]['telefono']=telefono
                generetedResets[id]['imei']=imei

                if('3340' in modelo or '4310' in modelo or '4315' in modelo or '3300' in modelo or '4305' in modelo or '4330' in modelo or '4335' in modelo or '4340' in modelo or '4345' in modelo):
                    if(len(imei)==10):
                        msg="CMD;"+imei+";03;03"
                    else:
                        msg="CMD;0"+imei+";03;03"
                elif('640' in modelo or '600' in modelo):
                    if(len(imei)==5):
                        msg="ST600CMD;0080"+imei+";02;Reboot"
                        msg2="ST600CMD;0100"+imei+";02;Reboot"
                    else:
                        msg="ST600CMD;008"+imei+";02;Reboot"
                        msg2="ST600CMD;010"+imei+";02;Reboot"
                elif("340" in modelo or '300' in modelo or '330' in modelo):
                    if(len(imei)==5):
                        msg="ST300CMD;2050"+imei+";02;Reboot"
                        msg2="ST300CMD;9070"+imei+";02;Reboot"
                    else:
                        msg="ST300CMD;205"+imei+";02;Reboot"
                        msg2="ST300CMD;907"+imei+";02;Reboot"
                elif("940" in modelo):
                    if(len(imei)==5):
                        msg="ST910;Reboot;0080"+imei
                        msg2="ST910;Reboot;0100"+imei
                    else:
                        msg="ST910;Reboot;008"+imei
                        msg2="ST910;Reboot;010"+imei
                elif("IQ" in modelo or "BOX" in modelo):
                    msg="CELLO"
                elif('3940' in modelo):
                    msg="ST600CMD;"+imei+";02;Reboot"
                    msg2="ST600CMD;"+imei+";02;Reboot"
                elif('215' in modelo):
                    msg="ST600CMD;"+imei+";02;Reboot"
                    msg2="ST600CMD;"+imei+";02;Reboot"
                else:
                    msg="CMD;0"+imei+";03;03"
                generetedResets[id]['msg1']=msg
                generetedResets[id]['msg2']=msg2
            else:
                modelo="***** Id no encontrado *****"
                telefono=""
                imei=""
                msg=''
                msg2=''
                generetedResets[id] ={}
                generetedResets[id]['modelo']=modelo
                generetedResets[id]['telefono']=telefono
                generetedResets[id]['imei']=imei
                generetedResets[id]['msg1']=msg
                generetedResets[id]['msg2']=msg2

    def toFile(self):      
        filename = asksaveasfilename(defaultextension=".txt")
        if(filename):
            fichero = open(filename, "w") 
            for equipo in generetedResets.items():
                id=equipo[0]
                cadena="--------------------------------\n"+equipo[0] + "\n\n"
                for item in equipo[1].items():
                    cadena=cadena+item[0]+": "+ item[1]+"\n"
                cadena=cadena+"\n\n\n"
                fichero.write(cadena)
            fichero.close()
    def imprimirResultados(self):  
        global generetedResets   
        cadena=""
        for equipo in generetedResets.items():
            cadena=cadena+"--------------------------------\n"+equipo[0] + "\n\n"
            for item in equipo[1].items():
                cadena=cadena+item[0]+": "+ item[1]+"\n"
            cadena=cadena+"\n\n\n"
        self.textResult['state'] = NORMAL
        self.textResult.delete("1.0","end")
        self.textResult.insert(END, cadena)
        self.textResult['state'] = DISABLED

#Variables globales
como_json=None
dataIn = dict()
generetedResets = {}

root = Tk()
root.geometry('600x500')
evaluador = ResetGenerator(root)
root.mainloop()

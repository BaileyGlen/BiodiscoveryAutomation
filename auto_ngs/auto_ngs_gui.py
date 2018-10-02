import tkinter as tk
from tkinter import filedialog
import pandas as pd
#import auto_microarray
import auto_ngs
import os
import logging
#from auto_ngs import auto_ngs
from auto_microarray import auto_microarray

class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""
    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            self.text.yview(tk.END)
        self.text.after(0, append)

logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.INFO)
class Application(tk.Frame):
    def __init__(self, master=None):
        self.panel = tk.StringVar(master)
        self.panel.set("Solid Tumor")
        self.autoBool = tk.IntVar(master)
        self.dir_opt = options = {}
        options['initialdir'] = os.getcwd
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'
        self.curdir = os.getcwd()
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.Filedirectory = ""
        self.getExcelFile = ""
        self.log= ["",""]
    def createWidgets(self):
        self.getExcelFile = tk.Button(self)
        self.getExcelFile["text"] = "Get File Directory"
        self.getExcelFile["command"] = self.askFiledirectory
        self.getgetExcelFile = tk.Button(self)
        self.getgetExcelFile["text"] = "Get Excel File"
        self.getgetExcelFile["command"] = self.askgetExcelFile

        self.cleanvcf = tk.Button(self)
        self.cleanvcf["text"] = "Clean VCF"
        self.cleanvcf["command"] = self.cleenvcf

        self.QUIT = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.oK = tk.Button(self, text="OK")
        self.oK["command"] = self.oKSave
        self.directoryFileText = tk.Text(self, height=2, width=100)
        self.directorygetFileText = tk.Text(self, height=2, width=100)

        self.panelMenu = tk.OptionMenu(self, self.panel, "Solid Tumor", "Hematological")

        self.logtext=tk.Text(self,height=15,width=200)
        self.text_handler=TextHandler(self.logtext)
        self.logger = logging.getLogger()
        self.logger.addHandler(self.text_handler)

        self.getExcelFile.pack()
        self.directoryFileText.pack()
        self.getgetExcelFile.pack()
        self.directorygetFileText.pack()
        self.cleanvcf.pack()
        self.panelMenu.pack()
        self.logtext.pack()
        self.QUIT.pack(side='left')
        self.oK.pack(side='right')

    def askFiledirectory(self):
        self.Filedirectory = os.path.normpath(filedialog.askdirectory(initialdir = os.path.normpath('Z:\\\\MicroArray\\Archived data\\GS projects\\GS PROJECTS 2018\\'), parent=root))
        self.logger.info('Obtained File Directory')
        self.directoryFileText.delete('1.0', tk.END)
        self.directoryFileText.insert(tk.END, self.Filedirectory)
    def askgetExcelFile(self):
        self.getExcelFile=(str)(filedialog.askopenfilename(initialdir="Z:\\\\MicroArray\\Archived data\\Microarray Tracking Lab Worksheets\\"))
        self.logger.info('Obtained Excel File')
        self.directorygetFileText.delete('1.0', tk.END)
        self.directorygetFileText.insert(tk.END, self.getExcelFile)
    def cleenvcf(self):
        vcf=filedialog.askopenfilename(initialdir="Z:\\\\BaileyGlen\\MultiOmics\\")
        vsf=(str)(vcf).split("/")
        loc=auto_ngs.readingvcf(vcf,vsf[-1])
        return loc
    def oKSave(self):
        panel=self.panel.get()
        df = pd.read_excel((str)(self.getExcelFile),sheet_name="MUSC",converters={'MRN':str},index=False)
        self.logger.info('Read Excel File In')
        df = df[df['Project']==(str)(panel)]
        path=(str)(self.Filedirectory)
        fileslist=os.listdir(path)
        filelist = [files for files in fileslist if files.endswith('.vcf.gz')]
        for sample in df["AccessionNumber"]:
            for files in filelist:
                names=files.split(" ")
                name=names[2]
                if "nextgene" not in name and "_cleaned" not in name:
                    if name[0:-7].upper()==sample:
                        try:
                            files=auto_ngs.readingvcf(path,files)
                            df.loc[df['AccessionNumber']==sample, "FileName"]= path+"\\"+files
                        except:
                            self.logger.info("This file had an error: "+files)
                            raise
        df=df.drop(["Well","AccessionNumber","PatientName","Gender","MRN","DOB","Import Notes"],axis=1)
        df=df.rename({"SampleID":"Sample Name","Project":"Sample Type","FileName":"Seq Var File"}, axis=1)
        df["Sample Type"]="Illumina "+df["Sample Type"]
        df["Seq Var Setting"]="VCF Settings"
        #pathh="Z:\\\\MicroArray\\Archived data\\GS projects\\GS PROJECTS 2018"
        col=list(df.columns)
        self.logger.info("We processed:")
        self.logger.info('\n'.join(df.loc[~df["Seq Var File"].isna(),"Sample Name"].values))
        self.logger.info("We skipped:")
        self.logger.info('\n'.join(df.loc[df["Seq Var File"].isna(),"Sample Name"].values))
        df.to_csv(path+"_"+panel, sep='\t', columns=col,index=False)
root=tk.Tk()
app = Application(master=root)
app.mainloop()
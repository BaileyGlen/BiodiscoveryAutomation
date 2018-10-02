import os
import tkinter as tk
from tkinter import filedialog
#import auto_microarray
import logging
from auto_microarray import auto_microarray#validateAscessionNumber, validatePatientName, validateMRN, readExcel, cleanDF, writeTSV, setFilename

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
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)

logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.INFO)
class Application(tk.Frame):
    def __init__(self, master=None):
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

        self.QUIT = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.oK = tk.Button(self, text="OK")
        self.oK["command"] = self.oKSave
        self.directoryFileText = tk.Text(self, height=2, width=100)
        self.directorygetFileText = tk.Text(self, height=2, width=100)
        self.scrollbar = tk.Scrollbar(self)
        self.logtext=tk.Text(self,height=15,width=200,yscrollcommand=self.scrollbar.set)
        self.text_handler=TextHandler(self.logtext)
        self.logger = logging.getLogger()
        self.logger.addHandler(self.text_handler)

        self.getExcelFile.pack()
        self.directoryFileText.pack()
        self.getgetExcelFile.pack()
        self.directorygetFileText.pack()
        self.logtext.pack()
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.QUIT.pack(side='left')
        self.oK.pack(side='right')

    def askFiledirectory(self):
        """Returns a selected directoryname."""
        #self.dir_opt.initialdir = os.path.abspath('Y:\runs')
        #print(self.dir_opt)
        self.Filedirectory = os.path.normpath(filedialog.askdirectory(initialdir = os.path.normpath('Z:\\\\MicroArray\\Archived data\\GS projects\\GS PROJECTS 2018\\'), parent=root))
        self.logger.info('Obtained File Directory')
        self.directoryFileText.delete('1.0', tk.END)
        self.directoryFileText.insert(tk.END, self.Filedirectory)
    def askgetExcelFile(self):
        #initialdir = os.path.normpath('Z:\\Sequencer\\Clinical\\ThunderBolts Tumor Runs\\2017 Cancer Panel')
        #self.getExcelFile = os.path.normpath(filedialog.askdirectory(initialdir = initialdir, parent=root))
        self.getExcelFile=(str)(filedialog.askopenfilename(initialdir="Z:\\\\MicroArray\\Archived data\\Microarray Tracking Lab Worksheets\\"))
        self.logger.info('Obtained Excel file')
        #excel=self.getExcelFile.split('/')
        #self.getExcelFile=str(excel[-1])
        self.directorygetFileText.delete('1.0', tk.END)
        self.directorygetFileText.insert(tk.END, self.getExcelFile)
    def oKSave(self):
        path=(str)(self.Filedirectory)
        #path="Z:\\\\MicroArray\\Archived data\\GS projects\\GS PROJECTS 2018\\6-5-2018 32PAT"
        file_name=(str)(self.getExcelFile)
        #file_name="D:\\\\grego\\Documents\\Pathology\\Projects\\biodiscovery\\files\\excelsheet\\musc_sample_sheet.xlsm"
        inputfile = file_name
        #filepath="D:\\\\grego\\Documents\\Pathology\\Projects\\biodiscovery\\output\\"

        #outputfile = "Sample_Sheet.tsv"
        self.logtext.delete('0', tk.END)
        df = auto_microarray.readExcel(inputfile)
        self.logger.info('Reading in Excel file'+"\n")
        #df.apply(lambda x: auto_microarray.loggertest(x, logger=self.logger),axis=1)
        #df.apply(auto_microarray.loggertest, logger=self.logger, axis=1)
        self.logger.info('Possible Issues below:')
        df=df.dropna(subset=['Project']).transform(auto_microarray.cleanRow, logger=self.logger, axis=1).dropna(how='all')
        self.logger.info('\n')
        #df,df2 = auto_microarray.cleanDF(df)
        self.logger.info('Cleaning up file')
        df = auto_microarray.setFilename(df,path)
        self.logger.info('Adding appropriate information')
        auto_microarray.writeTSV(df,path)
        self.logger.info('Wrote file to location')
        #samplelist=df2["Sample Name"]
        #self.logger.info("\n"+"The samples below are not going to be sent to biodiscovery. Make sure these do not need to be sent to biodiscovery.")
        #self.logger.info(samplelist)
        #self.logtext.insert(tk.END,"The samples below are not going to be sent to biodiscovery. Make sure these do not need to be sent to biodiscovery.\n")
        #self.logtext.insert(tk.END, self.log)
root = tk.Tk()
app = Application(master=root)
app.mainloop()
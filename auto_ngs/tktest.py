import os
import tkinter as tk
from tkinter import filedialog
from auto import completioncheck, createproject, fastqtemptransfer


class Application(tk.Frame):
    def __init__(self, master=None):
        self.panel = tk.StringVar(master)
        self.panel.set("Solid")
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
        self.miseqdirectory = ""
        self.datadirectory = ""
        self.autorundirectory = ""
        


    def createWidgets(self):
        self.getMiseqDirectory = tk.Button(self)
        self.getMiseqDirectory["text"] = "Get Miseq Directory"
        self.getMiseqDirectory["command"] = self.askmiseqdirectory #tk.filedialog.askdirectory(
            #parent=root, initialdir=self.curdir, title='Please select a directory')
        self.getDataDirectory = tk.Button(self)
        self.getDataDirectory["text"] = "Get Data Directory"
        self.getDataDirectory["command"] = self.askdatadirectory

        self.getAutorunDirectory = tk.Button(self)
        self.getAutorunDirectory["text"] = "Get Autorun Directory"
        self.getAutorunDirectory["command"] = self.askAutorundirectory

        self.QUIT = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.Run = tk.Button(self, text="Run")
        self.Run["command"] = self.runAuto
        self.directoryMiseqText = tk.Text(self, height=2, width=100)
        self.directoryDataText = tk.Text(self, height=2, width=100)
        self.directoryAutorunText = tk.Text(self, height=2, width=100)

        self.panelMenu = tk.OptionMenu(self, self.panel, "Solid", "Myeloid")

        self.autoCheckBox = tk.Checkbutton(self, text="Auto Detect", variable=self.autoBool)

        self.panelMenu.pack()
        self.autoCheckBox.pack()
        self.getMiseqDirectory.pack()
        self.directoryMiseqText.pack()
        self.getDataDirectory.pack()
        self.directoryDataText.pack()
        self.getAutorunDirectory.pack()
        self.directoryAutorunText.pack()
        self.QUIT.pack(side='left')
        self.Run.pack(side='right')


    def say_hi(self):
        print("hi there, everyone!")


    def askmiseqdirectory(self):
        """Returns a selected directoryname."""
        #self.dir_opt.initialdir = os.path.abspath('Y:\runs')
        #print(self.dir_opt)
        self.miseqdirectory = os.path.normpath(filedialog.askdirectory(initialdir = os.path.normpath('Y:\\runs'), parent=root))
        self.directoryMiseqText.delete('1.0', tk.END)
        self.directoryMiseqText.insert(tk.END, self.miseqdirectory)


    def askdatadirectory(self):
        """Returns a selected directoryname."""
        if self.panel.get() == "Solid":
            initialdir = os.path.normpath('Z:\\Sequencer\\Clinical\\ThunderBolts Tumor Runs\\2017 Cancer Panel')
        elif self.panel.get() == "Myeloid":
            initialdir = os.path.normpath('Z:\\Sequencer\\Clinical\\Myeloid Hub\\2017')
        self.datadirectory = os.path.normpath(filedialog.askdirectory(initialdir = initialdir, parent=root))
        self.directoryDataText.delete('1.0', tk.END)
        #self.dir_opt.initialdir = dir
        self.directoryDataText.insert(tk.END, self.datadirectory)

    def askAutorundirectory(self):
        """Returns a selected directoryname."""
        print(self.panel.get())
        #self.autorundirectory = filedialog.askdirectory((initialdir = os.path.abspath('Y:\\runs'), parent=root)
        self.autorundirectory = os.path.normpath('Z:\\Sequencer\\Clinical\\ThunderBolts Tumor Runs\\2017 Cancer Panel\\autorun')
        
        self.directoryAutorunText.delete('1.0', tk.END)
        #self.dir_opt.initialdir = dir
        self.directoryAutorunText.insert(tk.END, self.autorundirectory)


    def runAuto(self):
        print("startingcheck")
        print(self.miseqdirectory)
        completioncheck(self.miseqdirectory, self.autoBool)
        print("startingtransfer")
        fastqtemptransfer(self.miseqdirectory, self.datadirectory)
        print("creating project")
        createproject(self.datadirectory, self.autorundirectory, self.panel.get())
        print("done")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
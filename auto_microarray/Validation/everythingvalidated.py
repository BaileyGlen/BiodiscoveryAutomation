import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
import csv
import logging
import gzip
#from Biodiscovery.auto_ngs import auto_ngs
import shutil
def readingvcf2(path,vcf,path2):
    outputvcf=vcf[0:-7]+"_cleaned"+vcf[-7:-3]
    with gzip.open(path+"/"+vcf, mode='rt') as csvfile, open(path2+"\\"+outputvcf, mode='wt') as outputfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        writer= csv.writer(outputfile, delimiter='\t',lineterminator="\n", quotechar='|')

        samples=next(getSamples(reader,writer))
        for row in reader:
            columns=row[8].split(":")
            data=["",""]
            for sampleidx, sampledata in enumerate(row[9:]):
                data[sampleidx]={}
                for dataidx, datapoint in enumerate(sampledata.split(":")):
                    data[sampleidx][columns[dataidx]] = datapoint
            if data[0]["AF2"]=='.':
                if row[7]=="":
                    row[7]="."
                writer.writerow(row[0:9]+[row[10]])
            elif data[1]["AF2"]=='.':
                if row[7]=="":
                    row[7]="."
                writer.writerow(row[0:10])
            elif(float(data[0]["AF2"])<3 and float(data[1]["AF2"])>3):
                if row[7]=="":
                    row[7]="."
                writer.writerow(row[0:9]+[row[10]])
            else:
                if row[7]=="":
                    row[7]="."
                writer.writerow(row[0:10])
        return outputvcf
def getSamples(reader, writer):
    for row in reader:
        
        if(row[0]==("#CHROM")):
            writer.writerow(row[0:10])
            yield row[9:]
        else:
            writer.writerow(row)
def validate():
    settings = {"Solid":"Illumina Solid Tumor","Hem":"Illumina Hematological"}
    panel="Solid"
    excels=[pd.read_excel("Z:\\\\BaileyGlen\\List of clinical cases for validation.xlsx",sheet_name="Solid tumors"),pd.read_excel("Z:\\\\BaileyGlen\\List of clinical cases for validation.xlsx",sheet_name="Hematological")]
    MicroarraySolRawpath="Z:\\\\BaileyGlen\\autovalidation\\Validation1\\Microarray\\Solid\\Raw"
    MicroarrayHemRawpath="Z:\\\\BaileyGlen\\autovalidation\\Validation1\\Microarray\\Hematological\\Raw"
    MicroarraySolCleanpath="Z:\\\\BaileyGlen\\autovalidation\\Validation1\\Microarray\\Solid\\Clean"
    MicroarrayHemCleanpath="Z:\\\\BaileyGlen\\autovalidation\\Validation1\\Microarray\\Hematological\\Clean"
    yearlist=["Z:\\\\MicroArray\\Archived data\\GS projects\\GS projects 2017","Z:\\\\MicroArray\\Archived data\\GS projects\\GS PROJECTS 2018"]
    '''for year in yearlist:
        dirlist=os.listdir(year)
        for curdir in dirlist:
            if '.' not in curdir:# and "07-12" not in curdir:
                filelist=os.listdir(year+"\\"+curdir)
                filelist = [files for files in filelist if files.endswith('.txt')]
                for files in filelist:
                    names=files.split("_")
                    name=names[-1].replace(".txt","")
                    for x, excel in enumerate(excels):
                        if(x==0):
                            for sol in excel['Case #']:
                                if name.upper()==sol.upper():
                                    shutil.copy2(year+"\\"+curdir+"\\"+files,MicroarraySolRawpath)
                        else:
                            for hem in excel['Case #']:
                                if name.upper()==hem.upper():
                                    shutil.copy2(year+"\\"+curdir+"\\"+files,MicroarrayHemRawpath)'''
    pathlis=["Z:\\\\Sequencer\\Clinical\\Myeloid hub\\2017","Z:\\\\Sequencer\\Clinical\\Myeloid hub\\2018","Z:\\\\Sequencer\\Clinical\\ThunderBolts Tumor Runs\\2017 Cancer Panel","Z:\\\\Sequencer\\Clinical\\ThunderBolts Tumor Runs\\2018 Cancer Panel Runs"]
    NGSSolRawRawpath="Z:\\\\BaileyGlen\\autovalidation\\Validation1\\NGS\\Solid\\RawRaw"
    NGSHemRawRawpath="Z:\\\\BaileyGlen\\autovalidation\\Validation1\\NGS\\Hematological\\RawRaw"
    NGSSolRawpath="Z:\\\\BaileyGlen\\autovalidation\\Validation1\\NGS\\Solid\\Raw"
    NGSHemRawpath="Z:\\\\BaileyGlen\\autovalidation\\Validation1\\NGS\\Hematological\\Raw"
    for pat in pathlis:
        dirlist=os.listdir(pat)
        for curdir in dirlist:
            if '.' not in curdir and "07-26" not in curdir and "autorun" not in curdir and "08-02" not in curdir and "08-09" not in curdir:
                filelists=os.listdir(pat+"\\"+curdir+"\\miseq")
                filelists = [filess for filess in filelists if filess.endswith('.vcf')]
                for filess in filelists:
                    names=filess.split("_")
                    name=names[0]
                    for x, excel in enumerate(excels):
                        if(x==0):
                            for sol in excel['Case #']:
                                if name.upper()==sol.upper():
                                    shutil.copy2(pat+"\\"+curdir+"\\miseq\\"+filess,NGSSolRawRawpath)
                                    os.chdir("Z:\\\\BaileyGlen\\autovalidation\\Validation1\\NGS\\Solid\\RawRaw")
                                    f=open("NGS_Solid_Val1 Locations","a+")
                                    f.write(pat+"\\"+curdir+"\\miseq\\"+filess+"\r\n")
                                    NGSlist=os.listdir(NGSSolRawpath)
                                    for files in NGSlist:
                                        #vcfs=files.split(" ")
                                        #vcf=vcfs[2]
                                        newvcf=readingvcf2(NGSSolRawpath,files,"Z:\\\\BaileyGlen\\autovalidation\\Validation1\\NGS\\Solid\\Clean")
                        else:
                            for hem in excel['Case #']:
                                if name.upper()==hem.upper():
                                    shutil.copy2(pat+"\\"+curdir+"\\miseq\\"+filess,NGSHemRawRawpath) 
                                    os.chdir("Z:\\\\BaileyGlen\\autovalidation\\Validation1\\NGS\\Hematological\\RawRaw")
                                    f=open("NGS_Hem_Val1 Locations","a+")
                                    f.write(pat+"\\"+curdir+"\\miseq\\"+filess+"\r\n") 
                                    NGSlist2=os.listdir(kindaNGSHemRawRawpath)
                                    for files in NGSlist2:
                                        #vcfs=files.split(" ")
                                        #vcf=vcfs[2]
                                        newvcf=readingvcf2(NGSHemRawpath,files,"Z:\\\\BaileyGlen\\autovalidation\\Validation1\\NGS\\Hematological\\Clean")                      
    '''solidlist=os.listdir(MicroarraySolRawpath)
    for files in solidlist:
        names=files.split("_")
        name=names[-1].replace(".txt","")
        print(name)
        with open(MicroarraySolRawpath+"\\"+files, mode='rt') as csvfile, open(MicroarraySolCleanpath+"\\"+name.upper()+"_Val1.txt", mode='wt') as outputfile:
            for line in csvfile:
                line=line.replace(name,name.upper()+"_Val1")
                outputfile.write(line)
    hemlist=os.listdir(MicroarrayHemRawpath)
    for files in hemlist:
        names=files.split("_")
        name=names[-1].replace(".txt","")
        with open(MicroarrayHemRawpath+"\\"+files, mode='rt') as csvfile, open(MicroarrayHemCleanpath+"\\"+name.upper()+"_Val1.txt", mode='wt') as outputfile:
            for line in csvfile:
                line=line.replace(name,name.upper()+"_Val1")
                outputfile.write(line)'''
    
    '''os.chdir("Z:\\\\BaileyGlen\\autovalidation\\Validation1\\Microarray\\Solid")
    batchdir="Z:\\\\BaileyGlen\\autovalidation\\Validation1\\Microarray\\Solid"
    #CHANGE BASED OFF HEM OR SOLID
    data={}
    cleanlist=os.listdir(MicroarraySolCleanpath)
    for files in cleanlist:
        names=files.split("_")
        name=names[0]
        data[name]=[]
        data[name].append(name+"_Val1") #df.loc["Sample Name"]=name+"_Val1"
        data[name].append(name)#df["Accession Number"]=name
        data[name].append(settings[panel])#df["Sample Type"]=settings[panel]
        data[name].append("CytoSNP-850K Cancer")#df["Processing Setting"]="CytoSNP-850K Cancer"
        data[name].append(batchdir+"\\Clean\\"+files)
    df=pd.DataFrame.from_dict(data, columns=["Sample Name","Accession Number","Sample Type","Processing Setting","Filename"],orient="index")
    df.to_csv(batchdir+"\\Solid_Microarray_Val1_batch.txt",sep="\t",index=False)

    os.chdir("Z:\\\\BaileyGlen\\autovalidation\\Validation1\\Microarray\\Hematological")
    batchhemdir="Z:\\\\BaileyGlen\\autovalidation\\Validation1\\Microarray\\Hematological"
    #CHANGE BASED OFF HEM OR SOLID
    data={}
    cleanhemlist=os.listdir(MicroarrayHemCleanpath)
    panel="Hem"
    for files in cleanhemlist:
        names=files.split("_")
        name=names[0]
        data[name]=[]
        data[name].append(name+"_Val1") #df.loc["Sample Name"]=name+"_Val1"
        data[name].append(name)#df["Accession Number"]=name
        data[name].append(settings[panel])#df["Sample Type"]=settings[panel]
        data[name].append("CytoSNP-850K Cancer")#df["Processing Setting"]="CytoSNP-850K Cancer"
        data[name].append(batchhemdir+"\\Clean\\"+files)
    df=pd.DataFrame.from_dict(data, columns=["Sample Name","Accession Number","Sample Type","Processing Setting","Filename"],orient="index")
    df.to_csv(batchhemdir+"\\Hem_Microarray_Val1_batch.txt",sep="\t",index=False)'''

    os.chdir("Z:\\\\BaileyGlen\\autovalidation\\Validation1\\NGS\\Solid")
    batchsoldir="Z:\\\\BaileyGlen\\autovalidation\\Validation1\\NGS\\Solid"
    #CHANGE BASED OFF HEM OR SOLID
    data={}
    cleansollist=os.listdir("Z:\\\\BaileyGlen\\autovalidation\\Validation1\\NGS\\Solid\\Clean")
    panel="Solid"
    for files in cleansollist:
        names=files.split(" ")
        name=names[2]
        name=name[0:-12]
        data[name]=[]
        data[name].append(name+"_Val1")
        data[name].append(name)
        data[name].append(settings[panel])
        data[name].append("VCF Settings")
        data[name].append(batchsoldir+"\\Clean\\"+files)
    df=pd.DataFrame.from_dict(data, columns=["Sample Name","Accession Number","Sample Type","Seq Var Setting","Seq Var File"],orient="index")
    df.to_csv(batchsoldir+"\\Solid_NGS_Val1_batch.txt",sep="\t",index=False)
    
    os.chdir("Z:\\\\BaileyGlen\\autovalidation\\Validation1\\NGS\\Hematological")
    batchhemdir="Z:\\\\BaileyGlen\\autovalidation\\Validation1\\NGS\\Hematological"
    #CHANGE BASED OFF HEM OR SOLID
    data={}
    cleanhemlist=os.listdir("Z:\\\\BaileyGlen\\autovalidation\\Validation1\\NGS\\Hematological\\Clean")
    panel="Hem"
    for files in cleanhemlist:
        names=files.split(" ")
        name=names[2]
        name=name[0:-12]
        data[name]=[]
        data[name].append(name+"_Val1")
        data[name].append(name)
        data[name].append(settings[panel])
        data[name].append("VCF Settings")
        data[name].append(batchhemdir+"\\Clean\\"+files)
    df=pd.DataFrame.from_dict(data, columns=["Sample Name","Accession Number","Sample Type","Seq Var Setting","Seq Var File"],orient="index")
    df.to_csv(batchhemdir+"\\Hem_NGS_Val1_batch.txt",sep="\t",index=False)
validate()
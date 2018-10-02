import pandas as pd
import numpy as np
import os
def validateAscessionNumber(ANstr):
    fullnumber=ANstr.split("-")
    if(len(fullnumber)==2):
        if(not fullnumber[1].isnumeric()):
            return False
        if(len(fullnumber[0])<4):
            return False
        number=fullnumber[0]
        first=number[0:-2]
        second=number[-2:]
        if(not first.isalpha()):
            return False
        if(not second.isnumeric()):
            return False
        else:
            return True
    else:
        return False
def validatePatientName(name):
    fullname=name.split(",")
    if(len(fullname)==2):
        for name in fullname:
            for x in range(10):
                if str(x) in name:
                    return False
        else:
            return True
    else:
        return False
def validateMRN(mrn):
    if(not mrn.isdigit()):
        return False
    else:
        return True
def readExcel(filepath):
    df=pd.read_excel(filepath,sheet_name="MUSC",converters={'MRN':str})
    return df
def cleanRow(row,logger=None):
    if row['Project'].startswith('_'):
        logger.info("skipped: " + row['SampleID'])
        return None
    else:
        row=row.rename({"SampleID": "Sample Name", "Project": "Sample Type","PatientName":"Patient's Name","AccessionNumber": "Accession Number"})
        #row=row.dropna(subset=['Sample Type'])
        if pd.isna(row["Accession Number"]):
            row["Accession Number"]=row["Sample Name"]
        if not validateAscessionNumber(row["Accession Number"]):
            logger.info("bad accession number for: " + row['Sample Name'])
            return None
        row=row.drop(["Well"])
        #df = df.assign(ProcessingType=pd.Series())
        genderconv = {"M":"Male","F":"Female","U":"Unspecified"}
        row['Gender']=genderconv[row['Gender']]
        processdict = {"Constitutional": "CytoSNP-850K Constitutional","Hematological": "CytoSNP-850K Cancer","Solid Tumor":"CytoSNP-850K Cancer"}
        row["Processing Setting"] = processdict[row["Sample Type"]]
        row["Sample Type"] = "Illumina " + row["Sample Type"]
        print(type(row["DOB"]))
        if type(row["DOB"])==pd.Timestamp:
            row["DOB"]=row["DOB"].strftime('%m/%d/%Y')
        else:
            pass
        row=row.fillna("")
    return row
def matchFiles(samplename,filelist):
    filep=""
    for files in filelist:
        stringlist=files.split("_")
        for string in stringlist:
            #print(string.upper()[0:-4]+" - "+samplename)
            if(string.upper()[0:-4]==samplename.upper()):
                filep=files   
    return filep
def setFilename(df,path):
    filelist=[os.path.join(path, files) for files in os.listdir(path)]
    for samplename in df["Sample Name"]:  
        df.loc[df["Sample Name"]==samplename, 'Filename'] = matchFiles(samplename,filelist)
    return df
def writeTSV(df, filepath):
    #if df["DOB"]=="":
        #pass
    #else:
    #df["DOB"]=df["DOB"].dt.strftime('%m/%d/%y')
    col=list(df.columns)
    outlist=filepath.split("\\")
    output=outlist[-1]+"_batch.txt"
    df.to_csv(filepath+"\\"+output, sep='\t', columns=col,index=False)
def loggertest(row,logger=None):
    logger.info(row)

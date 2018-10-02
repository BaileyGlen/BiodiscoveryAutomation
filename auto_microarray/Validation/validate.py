import os
import pandas as pd
import shutil

filepath="Z:\\\\BaileyGlen\\List of clinical cases for validation.xlsx"
df2=pd.read_excel(filepath,sheet_name="Solid tumors")
df2['Case #']=df2['Case #'].str.upper()
linking = pd.DataFrame(index=list(df2['Case #'])+list(df2['Case #']+'.pjt'))
def get2017Hem():
    path="Z:\\\\Sequencer\\Clinical\\Myeloid hub\\2017"
    dirlist=os.listdir(path)
    badpath="Z:/BaileyGlen/autovalidation/Validation1/Microarray/Raw"
    for curdir in dirlist:
        if '.' not in curdir:
            filelist=os.listdir(path+"\\"+curdir+"\\miseq")
            filelist = [files for files in filelist if files.endswith('.vcf')]
            for files in filelist:
                name=files.split("_")
                for hem in df2['Case #']:
                    if name[0].upper()==hem:
                        shutil.copy2(path+"\\"+curdir+"\\miseq\\"+files,badpath)
                        linking.loc[name[0], 'OriginalSampleName']=name[0]
                        linking.loc[name[0], 'NewSampleName']=name[0]
                        linking.loc[name[0], 'TumorStatus']="Tumor"
                        linking.loc[name[0], 'MatchedNormal']=name[0]+"_nextgene"
                        linking.loc[name[0], 'SampleSourceFileName']=path+"\\"+curdir+'\\miseq\\'+files
            filelist=filelist=os.listdir(path+"\\"+curdir+"\\nextgene")
            filelist = [files for files in filelist if files.endswith('.vcf')]
            for files in filelist:
                name=files.split("_")
                for hem in df2['Case #']:
                    if name[0].upper()==hem:
                        shutil.copy2(path+"\\"+curdir+"\\nextgene\\"+files,badpath)
                        linking.loc[name[0]+".pjt", 'OriginalSampleName']=name[0]+".pjt"
                        linking.loc[name[0]+".pjt", 'NewSampleName']=name[0]+"_nextgene"
                        linking.loc[name[0]+".pjt", 'TumorStatus']="Normal"
                        linking.loc[name[0]+".pjt", 'MatchedNormal']=""
                        linking.loc[name[0]+".pjt", 'SampleSourceFileName']=path+"\\"+curdir+'\\nextgene\\'+files
    #for sample in linking[sample]:
        #newsamples=sample+".pjt"
    #df=linking[sample]+newsamples
get2017Hem()

def get2018Hem():
    path="Z:\\\\Sequencer\\Clinical\\Myeloid hub\\2018"
    dirlist=os.listdir(path)
    badpath="Z:/BaileyGlen/autovalidation/Validation1/Microarray/Raw"
    for curdir in dirlist:
        if '.' not in curdir and "07-12" not in curdir:
            filelist=os.listdir(path+"\\"+curdir+"\\miseq")
            filelist = [files for files in filelist if files.endswith('.vcf')]
            for files in filelist:
                name=files.split("_")
                for hem in df2['Case #']:
                    if name[0].upper()==hem:
                        shutil.copy2(path+"\\"+curdir+"\\miseq\\"+files,badpath)
                        linking.loc[name[0], 'OriginalSampleName']=name[0]
                        linking.loc[name[0], 'NewSampleName']=name[0]
                        linking.loc[name[0], 'TumorStatus']="Tumor"
                        linking.loc[name[0], 'MatchedNormal']=name[0]+"_nextgene"
                        linking.loc[name[0], 'SampleSourceFileName']=path+"\\"+curdir+'\\miseq\\'+files
            filelist=filelist=os.listdir(path+"\\"+curdir+"\\nextgene")
            filelist = [files for files in filelist if files.endswith('.vcf')]
            for files in filelist:
                name=files.split("_")
                for hem in df2['Case #']:
                    if name[0].upper()==hem:
                        shutil.copy2(path+"\\"+curdir+"\\nextgene\\"+files,badpath)
                        linking.loc[name[0]+".pjt", 'OriginalSampleName']=name[0]+".pjt"
                        linking.loc[name[0]+".pjt", 'NewSampleName']=name[0]+"_nextgene"
                        linking.loc[name[0]+".pjt", 'TumorStatus']="Normal"
                        linking.loc[name[0]+".pjt", 'MatchedNormal']=""
                        linking.loc[name[0]+".pjt", 'SampleSourceFileName']=path+"\\"+curdir+'\\nextgene\\'+files
get2018Hem()
col=list(linking.columns)
linking.to_csv(os.getcwd()+"\\auto_microarray\\Validation\\"+"vcf list", sep='\t',index=False)
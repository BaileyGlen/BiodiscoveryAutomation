from collections import OrderedDict
import gzip
import csv
import os

def readingvcf(path,vcf):
    outputvcf=vcf[0:-7]+"_cleaned"+vcf[-7:-3]
    with gzip.open(path+"\\"+vcf, mode='rt') as csvfile, open(path+"\\"+outputvcf, mode='wt') as outputfile:
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
#readingvcf()
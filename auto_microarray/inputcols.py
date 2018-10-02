collist = ['=INDEX(SampleID,{})&IF(INDEX(SampleID,{})="0"," ",)'.format(x+1, x+1) for x in range(64)]
print("\n".join(collist))

#collist=[]
#for x in range...:
#    collist.append(str(x+1))
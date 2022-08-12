sols = []

def findCombs(arx,tmpa):
	global sols
	if len(tmpa)==len(arx):
		sols.append(tmpa.copy())
	else:
		for ii in range(len(arx)):
			if arx[ii]!=0:
				tmpa.append(arx[ii])
				tmpval=arx[ii]
				arx[ii]=0
				findCombs(arx,tmpa)
				arx[ii]=tmpval
				del tmpa[len(tmpa)-1]

def insertVal(grp,val):
	ins = False
	if len(grp)>0:
		for i in range(len(grp)):
			if val<grp[i]:
				ins = True
				grp.insert(i,val)
				break
		if ins==False:
			grp.append(val)
	else:
		grp.append(val)
	return grp

def removeDups(grps):
	kk = len(grps)
	ii = 0
	rFlag = False
	while ii<kk:
		jj=ii+1
		tmpa = grps[ii]
		while jj<kk:
			tmpb = grps[jj]
			rFlag=delVal(tmpa,tmpb)
			if rFlag==True:
				del grps[jj]
				jj=jj-1
				kk=kk-1
			jj=jj+1
		ii=ii+1
	return grps

def delVal(tmpa,tmpb):
	bFound = False
	aFound = True
	for i in range(len(tmpa)):
		bFound = False
		for j in range(len(tmpb)):
			if tmpa[i]==tmpb[j]:
				bFound=True
				break
		if bFound==False:
			aFound = False
			break
		
	return aFound

def main():
	#arr=[1,2,3,4]
	arr=[4,2,1,1]
	tmp=[]
	findCombs(arr,tmp)
	limit =5
	solgrp=[]
	for i in range(len(sols)):
		grp=[]
		sumx=0
		grp1=[]
		if len(solgrp)==7:
			aaa=1
		for j in range(len(sols[i])):
			sumx=sumx+int(sols[i][j])
			if sumx>limit:
				if sumx==0:
					grp1=insertVal(grp1,int(sols[i][j]))
					grp1=[]
				else:
					grp.append(grp1)
					grp1=[]
					sumx=int(sols[i][j])
					grp1=insertVal(grp1,int(sols[i][j]))				
			elif sumx==limit:
				grp1=insertVal(grp1,int(sols[i][j]))
				grp.append(grp1)
				grp1=[]
				sumx=0
			else:
				grp1=insertVal(grp1,int(sols[i][j]))
			if j==len(sols[i])-1 and len(grp1)!=0:
				grp.append(grp1)
		solgrp.append(grp)

	min=len(arr)

	for i in range(len(solgrp)):
		tmin=len(solgrp[i])
		if tmin<min:
		    min=tmin

	ii=0
	kk=len(solgrp)
	while ii<kk:
		if len(solgrp[ii]) > min:
			del solgrp[ii]
			kk=kk-1
			ii=ii-1
		ii=ii+1

	solgrp = removeDups(solgrp)

	for sl in solgrp:
		print(sl)

main()
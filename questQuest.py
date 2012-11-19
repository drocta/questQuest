"""
todo:

use
custom functions (mostly done)
triggers

"""

from random import *
#start utility code:
def echo(arg):
    print arg
    return True
def defaultoption(given,default,f=lambda x:x):
        if given:
                return f(given)
        else:
                return default
switch=lambda value,casedict:casedict[value]()#defines a function that takes an argument that the switch statement is based off of,
#and a dictionary with functions as the values, and then calls the resultant function.
#example usage:
#switch(number,{val1:function1,val2:lambda:something})
#for readibility put it on multiple lines:
#switch(number,{
#   1:lambda:echo("bob"),
#   "orange":lambda:echo(23),
#   })
#start entity item etc class:
class withstats:
        def __init__(self, stats={}, hiddenstats={},name='bugerror',desc='It seems there is a bug'):
                self.stats=stats
                self.name=name
                self.hiddenstats=hiddenstats
                #self.visible=visible
                self.hiddenstats['items']=[]
                self.items=self.hiddenstats['items']
                if(desc):
                    self.desc=desc
                else:
                    self.desc="it is a "+name
                return self
        def takedamage(self,stat='hp',damage=1.0,lethaldamage=True,visibleout=True):
                #if the damage is not lethal damage, the entity cannot die as a result of the attack,
                #even if the stat reaches zero)
                self.stats[stat]-=damage
                if self.stats[stat]<=0 and lethaldamage:
                        thisentity=self
                        global entities
                        global entitiesInRoom
                        entityindex=entities.index(thisentity)
                        if visibleout:print "the",self.names ,"has been destroyed."
                        entities.remove(thisentity)
                        entitiesInRoom.remove(thisentity)
                        return False
                else:
                        if visibleout:print self.stats[stat]
                        return self.stats[stat]
        def additem(self,itemobj):
                self.items.append(itemobj)
        def remitem(self,itemobj):
                self.items.remove(itemobj)
                    
#end
#start beings code
class entity(withstats):
        def __init__(self, stats={}, hiddenstats={},name='person',desc='',visible=True):
                withstats.__init__(self, stats=stats, hiddenstats=hiddenstats,name=name,desc=desc)
        def takedamage(self,stat='hp',damage=1.0,lethaldamage=True,visibleout=True):
                #if the damage is not lethal damage, the entity cannot die as a result of the attack, even if the stat reaches zero)
                self.stats[stat]-=damage
                calltrigger("entityAttacked",self.name)
                if self.stats[stat]<=0 and lethaldamage:
                        thisentity=self
                        if visibleout:print "the",self.name ,"has died"
                        curRm.entities.remove(thisentity)
                        return False
                else:
                        return self.stats[stat]
        def varystat(self,stat,changeinstat):
                self.stats[stat]+=changeinstat
                return getentity(entityarg).stats[stat]
        def setstat(self,stat,newvalue):
                self.stats[stat]=newvalue
                return newvalue

class item(withstats):
    def __init__(self, name='ball', desc='It is a ball', stats={}, hiddenstats={},visible=True):
        withstats.__init__(self, stats=stats, hiddenstats=hiddenstats,name=name,desc=desc)


class newRoom(withstats):
    def __init__(self, name='testingroom', desc='It is another testingroom', stats={}, hiddenstats={}):
        withstats.__init__(self, stats=stats, hiddenstats=hiddenstats,name=name,desc=desc)
        self.hiddenstats['paths']=[]
        self.paths=self.hiddenstats['paths']
        self.hiddenstats['objects']=[]
        self.objects=self.hiddenstats['objects']
        self.hiddenstats['entities']=[]
        self.entities=self.hiddenstats['entities']
        roomObjs.append(self)

    def addpath(self,name,roomobj):
        self.paths.append(roomobj)
##        if not isinstance(names,str):
##            try:
##                for name in names:
##                    self.paths[name]=roomobj
##            except:
##                self.paths[names]=roomobj
##        else:
##            self.paths[names]=roomobj
    def additem(self,itemobj):
        self.items.append(itemobj)
    def remitem(self,itemobj):
        self.items.remove(itemobj)
    def addobj(self,objobj):
        self.objects.append(objobj)
    def remobj(self,objobj):
        self.objects.remove(objobj)

def varystat(stat,changeinstat,entityarg=0):
	getentity(entityarg).stats[stat]+=changeinstat
	return getentity(entityarg).stats[stat]
def setstat(stat,newvalue,entityarg=0):#self has entitynum 0
	getentity(entityarg).stats[stat]=newvalue
	return newvalue

def getentity(arg):
    return getgameobject(arg,curRm.entities)


def getgameobject(arg,haystack):#haystack is the array in which to search
    if(isinstance(arg,withstats)):
        return arg
    elif(arg.isdigit()):
        return haystack[int(arg)]
    else:
        didnotfind=True
        for thing in haystack:
            if (didnotfind and (arg in thing.name)):
                didnotfind=False
                outthing=thing
            elif arg==thing.name:
                outthing=thing
        if didnotfind:
            return False
        else:
            return outthing

def go(roomName,visibleout=True):
    global curRm
    nxtRm=getgameobject(roomName,curRm.paths)
    if(nxtRm):
        curRm.entities.remove(player)
        curRm=nxtRm
        curRm.entities.append(player)
        if visibleout:
            print "you enter",nxtRm.name
            look()
        return nxtRm
    elif(curRm.name==roomName):
        print "how can you go there, when YOU'RE ALREADY HERE"
        return False
    else:
        print "you can't move there right now"
        return False

def unsafego(roomName):
    global curRm
    nxtRm=getgameobject(roomName,roomObjs)
    if(nxtRm):
        curRm.entities.remove(player)
        curRm=nxtRm
        curRm.entities.append(player)
        return nxtRm
    elif(curRm.name==roomName):
        return False
    else:
        return False

def takeItem(itemName,visibleout=True):
    itemobj=getgameobject(itemName,curRm.items)
    if(itemobj and (itemName!='pumpkin')):
        curRm.remitem(itemobj)
        player.additem(itemobj)
        if visibleout:print('you take the '+itemName+' from the room')
        return curRm.items
    elif(getgameobject(itemName,curRm.objects)):
        if visibleout:print "you can't get the", itemName
        return False
    else:
        #What pumpkin?
        if visibleout:print('what '+itemName+'?')
        return False

def placeItem(itemName,visibleout=True):
    itemobj=getgameobject(itemName,player.items)
    if(itemobj):
        curRm.additem(itemobj)
        player.remitem(itemobj)
        if visibleout:print('you put the '+itemName+' in the room')
        return curRm.items
    else:
        #What pumpkin?
        if visibleout:print('what '+itemName+'?')
        return False
# viewInv was superfluous, so I removed it

def getDesc(Descs,thingy,visibleout=True):
	"""getDesc is how the program gets the description of either a room or an item
	so like if you entered a room, or said 'look', or said 'look itemname'
	getDesc is not the same as look
	to look something first it needs to check that you can look at the thing.
	"""
	resultantdescription=Descs[thingy]
	if visibleout:print resultantdescription
	return resultantdescription
			
def look(thing=""):
    if(thing in ["",'room',curRm.name]):
        print curRm.desc
        print "the items in the room are:"
        for item in curRm.items:
            print item.name
        for item in curRm.objects:
            print item.name
        print "here there is:"
        for being in curRm.entities:
            print "a",being.name
        print "the paths from here are:"
        for place in curRm.paths:
            print place.name
    else:
        thingobj= (getgameobject(thing,curRm.items) or
               getgameobject(thing,player.items) or
               getgameobject(thing,curRm.objects) or
               getgameobject(thing,curRm.entities)
               )
        if(thingobj):
            print thingobj.desc
        else:
            print("what "+thing+'?')

def splitquotes(instr):
    res1=instr.split('"')
    res2=[]
    for part in res1:
        if(res2[-1][-1]=='\\'):
            res2[-1]+='"'+part
        else:
            res2.append(part)
    inquote=False
    res3=[]
    for part in res2:
        if not inquote:
            words=part.split(' ')
            for word in words:
                res3.append(word)
        else:
            res3.append(part)
    return res3

def calltrigger(triggername,args=''):
    if(triggername in customcmds):
        evalcmbdcmd(triggername,args)
        return True
    else:
        return False
    

def ignoreWords(vinput,ignWords):
	splitIn=vinput.split(' ')
	result=''	
	for word in splitIn:
		if(not (word in ignWords)):
			result=result+word+' '
	result=result.rstrip()
	return result
def evalcmd(cmd,arg,visibleout=False,unsafe=True):
	global room
	global cont
	if(cmd in ['look','inspect','see','check']):
		#do the looky thing	
		look(arg)#Descs,arg,room)
	elif(cmd in ['take','get','grab']):
		takeItem(arg)
	elif(cmd in ['inv','inventory']):
		for item in player.items:
			print(item.name)
	elif(cmd in ['use','interact','activate','utilize']):
		pass#not implemented
	elif(cmd in ['leave','put','place']):
		placeItem(arg,visibleout=visibleout)
	elif(cmd in ['go','enter','travel','ride']):
		#room=go(arg,visibleout)
		#return room
		go(arg,visibleout)#return something maybe?
	elif(cmd=='help'):
		print(intro)
	elif(cmd in ['quit','exit','bye','close','adios']):
		cont=False
	elif(cmd in ['die']):
		print youdied
		cont=False
	elif(cmd in ['stats','health','stamina']):
		being=getentity(arg)
		if(being):
			for stat in being.stats:
				print stat,":",being.stats[stat]
			return being.stats
		else:
			print "I do not see a",arg
			return False
	elif(cmd in ['spawn','summon']):
		args=arg.split(' ',1)
		tempobj=entity({'hp':float(args[0])},name=args[1])
		curRm.entities.append(tempobj)
		#entitiesInRoom.append(tempobj)
		print "you have spawned a",args[1], "with an hp of",args[0]
	elif(cmd in ['strike','hit','attack','hurt','injure','stab','strife','aggrieve']):
		if(calltrigger("strike",arg)):
			return ""
		damagedentity=getentity(arg)
		if(damagedentity):
			healthleft=damagedentity.takedamage(damage=randint(1,3))
			if healthleft: print "the", damagedentity.name ,"has", healthleft,"health left"
			del damagedentity
		else:
			print 'what',arg+'?'
	elif(cmd in ['dealdamage']):
		args=arg.split(' ');
		damagedentity=getentity(args[0])
		if(damagedentity):
			healthleft=damagedentity.takedamage(damage=float(args[1]))
			#if healthleft: print "the", damagedentity.name ,"has", healthleft,"health left"
			del damagedentity
		#else:
			#print 'what',arg+'?'
	elif(cmd == "unsafego"):
		unsafego(arg)
	elif(cmd in ['debug','bug','d']):
		print(eval(raw_input('>>>')))
	elif(cmd in ['print','echo','output']):
		print arg
		return arg
	elif(cmd == "add"):
		return str(sum(map(int,arg.split(' '))))
	elif(cmd == "sub"):
		nums=map(int,arg.split(' '))
		return nums[0]-nums[1]
	elif(cmd == "concat"):
		#print arg
		#print arg.split(' ')
		#print ''.join(arg.split(' '))
		return ''.join(arg.split(' '))
	elif(cmd == "set"):
		return setuservar(arg)
	elif(cmd =="return"):
		return arg
	elif(cmd == "evalif"):
		[val,line]=prepline(arg)#arg.split(' ',1)
		try:
			val=float(val)
		except:
			if(val==""):
				val=False
		if(val):
			[condcmd,condarg]=prepline(line)#changethis
			return evalcmd(condcmd,condarg)
	elif(cmd == "prompt"):
		return raw_input(arg)
	elif(cmd in ['comp','==','equal','equals']):
		parts=prepline(arg)#arg.split(' ')
		if(parts[0]==parts[1]):
			return '1'
		else:
			return '0'
	elif(cmd in ["defined","defined?", "isdefined", "isdefined?",  "isset"]):
		if ((arg in uservars) and (uservars[arg]!="")):
			return '1'
		else:
			return '0'
	elif(cmd in customcmds):
		return evalcmbdcmd(cmd,arg)
	else:
		print "not a recognized command",cmd
	return None
def getval(val):
    if(val[0]=='>'):
        return uservars[getval(val[1:])]
    elif(val.isdigit()):
        return float(val)
    elif(val[:7]=="player."):
        return player.stats[val[7:]]
    elif(val[:6]=="curRm."):
        return curRm.stats[val[6:]]
    elif(val in uservars):
        #print val
        return uservars[val]
    else:
        return ""

def getval2(val):
    parts=val.split('.')
    
        
def setuservar(arg):
    [vartoset,val]=prepline(arg)#arg.split(' ',1)
    if(vartoset[:7]=='player.'):
        player.stats[vartoset[7:]]=val
    else:
        uservars[vartoset]=val
    return val

def setuservar2(arg):
    pass

def evalcmbdcmd(cmd,arg):
    #my apologies to anyone trying to read this.
    #You can figure it out, but it would take longer than if I had use better variable names
    if(cmd in customcmds):
        cmdcode=customcmds[cmd]
        cmdlines=cmdcode.split('\n')
        argnames=cmdlines.pop(0).split(' ')
        argnum=len(argnames)
        args=arg.split(' ',argnum)
        argdict={}
        for i in range(argnum):
            argsinlen=len(args)
            if(i<argsinlen):
                argdict[argnames[i]]=args[i]
            else:
                argdict[argnames[i]]=""
        ii=0
        numberOfLines=len(cmdlines)
        while(ii<numberOfLines):
        #for line in cmdlines:
            #print line
            line=cmdlines[ii]
            ii+=1
            if((len(line)==0) or (line[0]=='#')):
                continue
            if((len(line)>=4)and line.split(' ')[0]=='a'):
                pass
            [linecmd,argraw]=prepline(line)
            if(linecmd == 'goto'):
                if(argraw.isdigit()):
                    ii=int(argraw)
                elif((":"+argraw+";") in cmdlines):
                    ii=cmdlines.index((":"+argraw+";"))
                else:
                    ii=0
                continue
            elif(linecmd in ['isset', 'isdefined']):
                if((('>'+argraw) in argdict) and (argdict[('>'+argraw)]!="")):
                    returnvalue="1"
                else:
                    returnvalue=evalcmd('isset', argraw)
                    #print "argraw:",argraw
                    #print "returnvalue:",returnvalue
                    #print 'returnvalue=="":',returnvalue=="0"
                    if(returnvalue=="0"):
                        returnvalue="0"
                    else:
                        returnvalue="1"
                continue
            
            argarrout=argraw.split(' ')
            #print argarrout
            newargarr=[]
            for i in range(len(argarrout)):
                if argarrout[i][0]=='>':
                    if argarrout[i] in argnames:
                        #functionargindex=argnames.index(argarrout[i])
                        #correspondingvalue=args[functionargindex]
                        correspondingvalue=argdict[argarrout[i]]
                        newargarr.append(correspondingvalue)
                    else:
                        #print "arg to getval:", argarrout[i][1:]
                        argfromgetvalue=getval(argarrout[i][1:])
                        #print "argfromgetvalue",argfromgetvalue
                        newargarr.append(argfromgetvalue)
                elif argarrout[i]=="_":
                    newargarr.append(str(returnvalue))
                else:
                    newargarr.append(argarrout[i])
            newargstr=' '.join(newargarr)
            returnvalue=evalcmd(linecmd,newargstr)
    else:
        print "shouldn't happen"
        returnvalue=None
    return returnvalue
    
def addcmd(functiondata):
    cmdlines=functiondata.split('\n')
    fname=cmdlines.pop(0)
    #fname=fname[1:][:-1]
    customcmds[fname]='\n'.join(cmdlines)

def addcmds(filecontents):
    cmds=filecontents.split("defun\n")
    cmds.pop(0)
    #print cmds
    for cmd in cmds:
        #print cmd
        addcmd(cmd)

def prepline(line):
    command=ignoreWords(line.lower(),ignWords)
    temparr=command.split(' ',1)
    if(len(temparr)==2):
        return temparr
    elif(len(temparr)==1):
        return [temparr[0],""]
    else:
        return ["",""]


uservars={}
#start variables to change
#introduction and stuff
intro="Welcome to questQuest\n\
currently accepted commands are look take inventory and quit\n\
certain synonypes also work, such as inspect, grap, inv etc.\n\
commands in development are use, go, propably others later.\n\
enter help to see this message again"
youdied="You have died. Better luck next time!"
##Descs={
##        'ball':'it is an ordinary ball',
##        'duck':'it is a duck',
##        'bull':'it is a dangerous bull. good thing it is only a model',
##        'dent':'there is a dent in the wall',
##        'testing room':'it is a simple testing room for the purpose of testing a program',
##        'box':'it is a very large card board box'
##        }

player=entity(
    {
        'hp':5.0,
        'atk':1.0,
        'def':1.0
        }
    ,name='person(yourself)',desc='You are a brave and heroic adventurer, or so you like to think')



##rooms={
##        "testing room":[["ball"],["duck"],["box"],[]],
##        "box":[["bull"],["dent"],["testing room"],[]],
##        }

roomObjs=[]
curRm=newRoom("testing room",desc="it is a room for testing games")
curRm.entities.append(player)
curRm.addpath("box",newRoom("box",desc="it is a very large box"))
curRm.additem(item(name='ball', desc='It is a ball'))
curRm.addobj(item(name='square', desc='It is a small sqyare'))
roomObjs[1].addpath("testing room",curRm)
newRoom("home",desc="""this is your home.
Due to the disaster, you cannot exit your house through the normal methods.
Its a nice place to rest and store your stuff though.
It has a lot of sentimental value.""")
#end
#safecmds=['look','inspect','see','check','take','get','grab','inv','inventory','leave','put','place',
#              'go','enter','travel','ride','help','quit','exit','bye','close','adios','die',
#              'stats','health','stamina','strike','hit','attack','hurt','injure','print','echo','output']
ignWords=['at','the','please','stupid','to','in','of']
unsafecmds=['debug','d','spawn','summon','eval','set','dealdamage']
customcmds={
    'e':
""">x
go >x""",
    'dig':
""">a >b
print >b >a
print >a""",
"make0":
""">var
set >var 0""",
"set2":
""">var >val
set >var >val""",
"++":
""">var
set junk >var
add >>junk 1
set >var _""",
"antspawn":
""">hp
spawn >hp ant"""

    }


filelink=open('qqf.txt','r')
filecontents=filelink.read(-1)
#print "contents:",filecontents
addcmds(filecontents)
print "file succesfully read!"
calltrigger("initQuest")
print intro
cont=True #cont stores whether we should continue the loop 
testing=True

while(cont):
	eachloop=lambda:True
	userIn=raw_input(":").lower()
	[cmd,arg]=prepline(userIn)
	if((cmd not in unsafecmds)or testing):
		evalcmd(cmd,arg,visibleout=True,unsafe=True)
	else:print "unsafe command"




	    
		

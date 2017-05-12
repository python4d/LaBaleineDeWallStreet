import requests
import os
import json
import getopt
import discord

client = discord.Client()

token = "MzAyODMyMTY4NzY4MzcyNzM2.C9PR-A.89-GgiT9TbphCPgIgGTFgYVlEsk"

class switch(object):

    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))



def traitement(boo): #ICI

    d = 0

    print("Contrôle mot 1")
    if(len(boo.split())>1):
        while switch((boo.split()[0]).lower()):
            if case('prix'):
                d = price(boo.split())
                break
            if case('price'):
                d = price(boo.split())
                break
            if case('conv'):
                d = conv(boo.split())
                break
            if case('volume'):
                print("soon")
                break
            break

    return d

def price(boo2):

    print("Choix du market")

    if(len(boo2)>=2):
        while switch(boo2[1]):
            if case('polo'):            #polo
                boo2.remove("polo")
                t = poloniex(boo2)
                break
            if case('trex'):            #trex
                boo2.remove("trex")
                t = bittrex(boo2)
                break
            if case('poloniex'):        #polo
                boo2.remove("poloniex")
                t = poloniex(boo2)
                break
            if case('bittrex'):         #trex
                boo2.remove("bittrex")
                t = bittrex(boo2)
                break
            if case('p'):           #polo
                boo2.remove("p")
                t = poloniex(boo2)

                break
            if case('b'):               #trex
                boo2.remove("b")
                t = bittrex(boo2)
                break
            t = lost(boo2)                    # Si market pas indiqué
            break

    return t

def conv(boo2):

    print("CONV")

    
    boo2.remove("conv")

    print(boo2)
    
    valBtc = btcrecup(1)
    print(valBtc)
    try:
        float(boo2[0])
        final=polorecup(boo2[1],0)

        if(final==0):
            final=bittrecup(boo2[1],0)

        final=float(final)*float(boo2[0])
        final = "```"+str(boo2[0])+" "+str(boo2[1]).upper()+" valent "+ str("%.2f" %final)+"$```"

    except :
        float(boo2[1])
        final=polorecup(boo2[0],0)
        if(final==0):
            final=bittrecup(boo2[0],0)
        
        final=float(final)*float(boo2[1])
        final ="```"+str(boo2[1])+" "+str(boo2[0]).upper()+" valent "+  str("%.2f" %final)+"$```"

    return final



def bittrex(boo3):

    print("Trex Selector")

    i = 0
    final = ["","","","","",""]
    boo3.remove("price")

    nbreCase = len(boo3)

    offset = 0

    while nbreCase > i :

        final[offset]=bittrecup(boo3[i],1)

        if(final[offset]!=0):
            offset+=1

        i = 1 + i

    return final

def poloniex(boo3):

    print("Polo Selector")

    i = 0
    final = ["","","","","",""]

    boo3.remove("price")


    nbreCase = len(boo3)

    offset=0

    while nbreCase > i :

        final[offset]=polorecup(boo3[i],1)

        if(final[offset]!=0):
            offset+=1

        i = 1 + i
    return final

def lost(boo3):

    print("Mot 2 inconnu")

    i = 0
    final = ["","","","","",""]
    boo3.remove("price")

    nbreCase = len(boo3)



    while nbreCase > i :

        final[i]=polorecup(boo3[i],1)

        if(final[i]==0):
            final[i]=bittrecup(boo3[i],1)

        i = 1 + i


    return final

def polorecup(boo4,all):

    url="https://poloniex.com/public?command=returnTicker"
    print("Poloniex Récup")

    content=requests.get(url)
    data=content.json()
    market="BTC_"+boo4.upper()

    valBtc = btcrecup(0)

    print(market)
    if(market in data):
        if(all):
            return("```"+boo4.upper()+"   "+data[market]["last"]+" ("+str("%.2f" %(float(data[market]["percentChange"])*100))+"%) $"+(str("%.5f" %(float(data[market]["last"])*(float(valBtc)))))+"   (Poloniex)"+"```")
        else:
            return(float(data[market]["last"])*valBtc)
    else:
        return 0




def bittrecup(boo4,all):

    print("Bittrex Recup")

    url="https://bittrex.com/api/v1.1/public/getmarketsummary?market="
    valBtc = btcrecup(0)
    market="btc-"+boo4
    print(market)
    content=requests.get(url+market)
    data=content.json()

    print(data["success"])
    
    if(data["success"]):

        if(all):
            print("all")
            percent1=((data["result"][0]["Last"])-(data["result"][0]["PrevDay"]))
            percent2=(percent1/float(data["result"][0]["PrevDay"]))*100

            

            return("```"+boo4.upper()+"   "+str(data["result"][0]["Last"])+" ("+str("%.2f" %percent2)+"%) $"+str("%.5f" %(data["result"][0]["Last"]*float(valBtc)))+"   (Bittrex)"+"```")
        else:
            return(data["result"][0]["Last"]*valBtc)
    else:
        return 0

def btcrecup(euro):

    print("Bitcoin Recup")

    if(euro):
        url="https://www.bitstamp.net/api/v2/ticker/btceur/"
    else:
        url="https://www.bitstamp.net/api/v2/ticker/btcusd/"

    content=requests.get(url)
    data=content.json()
    if( "last" in data):
        return (float(data["last"]))

    else:
        return(0)


def renvoie(boo5):

    print("Fonction de renvoie")
    client = discord.Client()
    boucle = len(boo5)

    i=0

    print(boo5[:])
    while boucle > i :

        i += 1





@client.event
async def on_message(message):

    if message.content.startswith('price btc'):


        boo = "```1 BTC vaut "+str(btcrecup(0))+"$"+" ou "+str(btcrecup(1))+"€```"
        
        await client.send_message(message.channel, boo)    

    if message.content.startswith('price'):

        retour=traitement(message.content)
        print("retour ok")

        boucle = len(retour)

        i=0

        print(retour[0])
        print(retour[1])


        while boucle > i :

            if(retour[i]!=0):
                await client.send_message(message.channel, retour[i])

            i += 1


    if message.content.startswith('prix'):
        
        retour=traitement(message.content)
        print("retour ok")

        boucle = len(retour)

        i=0

        print(retour[0])
        print(retour[1])


        while boucle > i :

            if(retour[i]!=0):
                await client.send_message(message.channel, retour[i])

            i += 1

    if message.content.startswith('conv'):

        retour=traitement(message.content)
        print("retour ok")


        await client.send_message(message.channel, retour)



@client.event
async def on_ready():
    
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    

try:
    client.run(token)
except:
    print("No internet Connection")
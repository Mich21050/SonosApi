import soco
from soco import SoCo
from flask import Flask,request
import json
import os.path
from os import path
app = Flask(__name__)
app.config["DEBUG"] = True

if path.exists("tokens.txt") == False:
    print("ERROR: No auth tokens found. Run tokenGen atleast once.")
    print("If you want to use the discover function just enter a random ip Adress.")
    exit()

def chkAuth(authHeader, ipA):
    f = open("tokens.txt","r")
    tmpTk = f.readlines()
    f.close()
    if isinstance(authHeader,str) == False:
        return False
    for el in tmpTk:
        tmpS = el.strip().split(":")
        if tmpS[0] == ipA and tmpS[1] == authHeader:
            return True
        else:
            return False


@app.route('/api/volume', methods=['GET','POST'])
def Volume():
    if chkAuth(request.headers.get('authToken'), request.args.get('ip')):
        def volResp():
            resp = {}
            resp['Sonos_IP'] = device
            resp['volume'] = sonos.volume 
            return resp

        device = request.args.get('ip')
        sonos = SoCo(device)
        if request.method == 'GET':
            return volResp()
        if request.method == 'POST':
            content = request.json
            sonos.volume = content['SetVolume']
            return volResp()
    else:
        return "Invalid auth Token",404

@app.route('/api/state', methods=['GET','POST'])
def State():
    if chkAuth(request.headers.get('authToken'),request.args.get('ip')):
        def stateResp():
            resp = {}
            resp['Sonos_IP'] = devIP
            resp['Transp_State'] = sonos.get_current_transport_info()['current_transport_state']
            return resp
        
        devIP = request.args.get('ip')
        sonos = SoCo(devIP)
        if request.method == 'GET':
            return stateResp()
        
        if request.method == 'POST':
            content = request.json
            if content['SetState'] == 'Play':
                sonos.play()
                return stateResp()
            elif content['SetState'] == 'Pause':
                sonos.pause()
                return stateResp()
            else:
                return "Not Found",404
    else:
        return "Invalid auth Token",404

@app.route('/api/track', methods=['GET'])
def Track():
    if chkAuth(request.headers.get('authToken'),request.args.get('ip')):
        devIP = request.args.get('ip')
        sonos = SoCo(devIP)
        trackInf = sonos.get_current_track_info()
        resp = {}
        resp['title'] = trackInf['title']
        resp['artist'] = trackInf['artist']
        resp['album_art'] = trackInf['album_art']
        return resp
    return "Invalid auth Token",404

@app.route('/api/device', methods=['GET'])
def device():
    zoneList = list(soco.discover())
    resp = {}
    for i in range(len(zoneList)):
        resp[zoneList[i].player_name] = zoneList[i].ip_address
    return resp

app.run(host='0.0.0.0')

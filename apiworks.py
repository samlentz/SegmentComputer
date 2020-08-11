class api:
    import webbrowser
    import requests
    import time
    import polyline
    import os.path as path
    import json
    cid = '51681'
    com = '5e638b979122678ce91820fc6083aa02e6850f89'
    actoken = ''
    retoken = ''
    athid = 0
    exptime = 0
    def __init__(self,nologin = False):
        if nologin:
            return
        if self.path.exists("/home/pi/gps3/codes.txt"):
            file1 = open("/home/pi/gps3/codes.txt","r") 
            self.actoken, self.retoken, self.athid,self.exptime =file1.read().split(',')

        else:
            self.webbrowser.open('http://www.strava.com/oauth/authorize?client_id='+self.cid+'&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read',new = 0)
            print('http://www.strava.com/oauth/authorize?client_id='+self.cid+'&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read')
            code = input()
            data1 =dict(client_id=self.cid,client_secret=self.com,code=code,grant_type='authorization_code')
            r = self.requests.post('https://www.strava.com/api/v3/oauth/token',data = data1)
            re = r.json()
            self.actoken = re['access_token']
            self.exptime =str( re['expires_at'])
            self.retoken = re['refresh_token']
            self.athid = str(re['athlete']['id'])

    def refresh(self):

        if(int(self.exptime)-self.time.time()<0 or True):
            print('Refreshing Miles')
            data =dict(client_id=self.cid,client_secret=self.com,refresh_token=self.retoken,grant_type='refresh_token')
            response = self.requests.post('https://www.strava.com/api/v3/oauth/token',data = data)
            js = response.json()
            #print(js)
            self.actoken = js['access_token']
            self.exptime = js['expires_at']
            self.retoken = js['refresh_token']
        else:
            print('no refresh needed')
        file1 = open("codes.txt","w")
        L = self.actoken+','+self.retoken+','+(self.athid)+','+str(self.exptime)
        file1.write(L)  
        file1.close() 

    def getMiles(self):
        data = {'Authorization':'Bearer '+self.actoken}
        r = self.requests.get('https://www.strava.com/api/v3/segments/'+(self.athid)+'/stats',headers=data)
        js = r.json()
        return(int(js['all_ride_totals']['distance']/1609) + 3*int(js['all_run_totals']['distance']/1609))
    
    def getSegment(self,segmentID):     
        data = {'Authorization':'Bearer '+self.actoken}
        r = self.requests.get('https://www.strava.com/api/v3/segments/'+str(segmentID),headers=data)
        js = r.json()
        #print(type(js['map']['polyline']))
        array = self.polyline.decode(js['map']['polyline'])
        #print(type(array))
        return array
    def findSegments(self,xy):
        x,y = xy
        region = 0.01
        x1,y1,x2,y2 = [x-region, y-region,x+region,y+region]
        data = {'Authorization':'Bearer '+self.actoken}
        r = self.requests.get('https://www.strava.com/api/v3/segments/explore?bounds='+str(x1)+","+str(y1)+","+str(x2)+","+str(y2)+","+'&activity_type=riding&min_cat=&max_cat=',headers=data)

        #r = self.requests.get('https://www.strava.com/api/v3/segments/explore?bounds=['+str([x1,y1,x2,y2])+'&activity_type=riding&min_cat=&max_cat=',headers=data)
        #print(r)
        #print(type(r))
        #print(r.json())
        output = []
        for i in r.json()['segments']:
            output.append([i['id'],i['start_latlng'],i['points'], i['name']])
       # print(output)
        return output
    def exportStar(self):
        data = {'Authorization':'Bearer '+self.actoken}
        r = self.requests.get('https://www.strava.com/api/v3/segments/starred?page=1&per_page=100',headers=data)
        output = []
        for i in r.json():
            output.append([i['id'],i['start_latlng'],self.getSegment(i['id']), i['name']])
        #with open('thestuff.json','w') as file:
        #    self.json.dump(r.json(),file)
        with open('data.json', 'w') as f:
            self.json.dump(output, f, indent=4)
    def importStar(self):
        with open('/home/pi/gps3/data.json') as f:
            data = self.json.load(f)
        return data
            
                

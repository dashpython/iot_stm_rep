import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import sqlite3
from dash.dependencies import Input, Output, State
import paho.mqtt.client as mqtt
import time
import pandas as pd
import sqlite3
import os
import base64
from six.moves.urllib.parse import quote
from sqlalchemy import create_engine
from datetime import datetime,timedelta
import unicodedata
from flask_mqtt import Mqtt
#import socketio
from flask_socketio import SocketIO
FA ="https://use.fontawesome.com/releases/v5.8.1/css/all.css"

server = Flask(__name__)
#server.config['DEBUG'] = True
server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///test.db')

#server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)
db_URI = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
engine = create_engine(db_URI)



class User(db.Model):
    __tablename__ = 'datatable'

    id = db.Column(db.Integer, primary_key=True)
    stamp = db.Column(db.String(26))
    devId = db.Column(db.String(15))
    SPA = db.Column(db.String(10))
    TA = db.Column(db.String(10))

    def __repr__(self):
        return '<User %r %r  %r %r>' % (self.stamp, self.devId, self.SPA, self.TA)

class smb(db.Model):
    __tablename__ = 'smbtable'

    id = db.Column(db.Integer, primary_key=True)
    stamp = db.Column(db.String(26))
    devId = db.Column(db.String(15))
    str1 = db.Column(db.String(10))
    str2 = db.Column(db.String(10))
    str3 = db.Column(db.String(10))
    str4 = db.Column(db.String(10))
    str5 = db.Column(db.String(10))
    str6 = db.Column(db.String(10))
    str7 = db.Column(db.String(10))
    str8 = db.Column(db.String(10))
    str9 = db.Column(db.String(10))
    str10 = db.Column(db.String(10))
    str11 = db.Column(db.String(10))
    str12 = db.Column(db.String(10))
    str13 = db.Column(db.String(10))

    vol1 = db.Column(db.String(10))
    vol2 = db.Column(db.String(10))
    vol3 = db.Column(db.String(10))
    vol4 = db.Column(db.String(10))
    vol5 = db.Column(db.String(10))
    vol6 = db.Column(db.String(10))
    vol7 = db.Column(db.String(10))
    vol8 = db.Column(db.String(10))
    vol9 = db.Column(db.String(10))
    vol10 = db.Column(db.String(10))
    vol11 = db.Column(db.String(10))
    vol12 = db.Column(db.String(10))
    vol13 = db.Column(db.String(10))
   
    temp = db.Column(db.String(10))
    
    stravg=db.Column(db.Float)
    volavg=db.Column(db.Float)
    poweravg =db.Column(db.Float)

    def __repr__(self):
        return '<User %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r %r>' % (self.stamp, self.devId, self.str1, self.str2, self.str3, self.str4, self.str5, self.str6, self.str7, self.str8, self.str9, 
                self.str10, self.str11, self.str12, self.str13, self.vol1, self.vol2, self.vol3, self.vol4, self.vol5, self.vol6, self.vol7, self.vol8, self.vol9, self.vol10, self.vol11, self.vol12, self.vol13, self.temp, self.stravg, self.volavg, self.poweravg)

db.create_all()

def on_connect(client, userdata, flags, rc):
    print("Connected!", rc)
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))

def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))

def on_publish(client, userdata, mid):
    print("Publish:", client)

def on_log(client, userdata, level, buf):
    print("log:", buf)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
messagelist=[]
messagelist2=[]
smbdict={}
teststr=""
devicetime=[]

#@mqtt2.on_message()
#@socketio.on('welcome')
def on_message(client, userdata, message):
    data={}
    data1={}
    payload = str(message.payload.decode("utf-8"))#+" "
    print("payload=",payload,len(payload))
    print("payload[:4]",payload[:4],len(payload))
    #messagelist=
    if payload[:4]=="Dev:":# and len(payload)!=45:
        ind=payload.index(",Time")
        #ind=ind+25
        print("index devid=",ind)
        print("payload[ind+25:]",payload[ind+25:],len(payload))
    #messagelist=
        #print("hi37")
        teststr=payload[:ind]+payload[ind+25:]
       # print("index=",payload.index('Time:'))
        #devicetime[0]=payload[7:11]
        
        #devicetime[1]=payload[12:31]
        #print(devicetime)
        messagelist.append(payload)
        if len(messagelist)>4:
        #for i in (0,3):
            messagelist.remove(messagelist[0])
        print("smbmessagelist=",messagelist)
        data = dict(x.split(":") for x in teststr.split(","))
        #print(payload[12:31])
        data['Time']=payload[ind+21:ind+25]+"-"+payload[ind+18:ind+20]+"-"+payload[ind+15:ind+17]+"T"+payload[ind+6:ind+14]+".000000"#+payload[ind+15:ind+25]#devicetime[1]
        print("smb data=",data)

    print("pay data1=",payload[:6])

    if payload[:6]=="DevId:":        
        print("hi data1")
        data1 = dict(x.split(":") for x in payload.split(","))
        messagelist2.append(payload)
        if len(messagelist2)>4:
        #for i in (0,3):
            messagelist2.remove(messagelist2[0])
        print("messagelist2=",messagelist2)
        #data1 = dict(x.split(":") for x in payload.split(","))
    #data = dict(x.split(":") for x in teststr.split(","))
    #data = dict(x.split(":") for x in teststr.split(","))
    #data['Time']=devicetime[1]
#    print("smb dict=",smbdict)
    print("data=",data1)
    print("smb data=",data)
    print("len dataa=",len(data))
    if (len(data1)==3):
        print("len",len(data1))
        admin = User(stamp=str(datetime.now()+timedelta(minutes=330)),devId=data1['DevId'],SPA=data1['SPA'],TA=data1['TA'])
        db.session.add(admin)
        db.session.commit()


    #elif (len(payload)==45 and (len(smbdict)==28)):
    elif len(smbdict)==28:

    #elif ((len(data)==3) and (len(smbdict)==28) and (data['temp'] is not None)):
        print("smb dict=",smbdict)
        stravg=0
        #for i in (1,14):
        #    print("stravg=",float(smbdict['str%s'%(i)]))
        #    stravg=stravg+float(smbdict['str%s'%(i)])
        stravg=float(smbdict['str1'])+float(smbdict['str2'])+float(smbdict['str3'])+float(smbdict['str4'])+float(smbdict['str5'])+float(smbdict['str6'])+float(smbdict['str7'])+float(smbdict['str8'])+float(smbdict['str9'])+float(smbdict['str10'])+float(smbdict['str11'])+float(smbdict['str12'])+float(smbdict['str13'])
        stravg=float(stravg/13)
        smbdict['stravg']=stravg 
        print("smb dict=",smbdict)
        volavg=0

        #for i in (1,14):
        #    print("volavg",float(smbdict['vol%s'%(i)]))
        volavg=float(smbdict['vol1'])+float(smbdict['vol2'])+float(smbdict['vol3'])+float(smbdict['vol4'])+float(smbdict['vol5'])+float(smbdict['vol6'])+float(smbdict['vol7'])+float(smbdict['vol8'])+float(smbdict['vol9'])+float(smbdict['vol10'])+float(smbdict['vol11'])+float(smbdict['vol12'])+float(smbdict['vol13'])
        volavg=float(volavg/13)
        smbdict['volavg']=volavg
        print("smb dict=",smbdict)
        poweravg=0 
        poweravg=float((volavg*stravg)/1000)
        
        smbdict['poweravg']=poweravg

        #smbdict['temp']=data['temp']
        smbdict['temp']=data['temp']
        print("smb dict=",smbdict)
        
        smbdata = smb(stamp=smbdict['Time'],devId=smbdict['Dev'],temp=smbdict['temp'],str1=smbdict['str1'],vol1=smbdict['vol1'],str2=smbdict['str2'],vol2=smbdict['vol2'],str3=smbdict['str3'],vol3=smbdict['vol3'],str4=smbdict['str4'],vol4=smbdict['vol4'],str5=smbdict['str5'],vol5=smbdict['vol5'],str6=smbdict['str6'],vol6=smbdict['vol6'],str7=smbdict['str7'],vol7=smbdict['vol7'],
                str8=smbdict['str8'],vol8=smbdict['vol8'],str9=smbdict['str9'],vol9=smbdict['vol9'],str10=smbdict['str10'],vol10=smbdict['vol10'],str11=smbdict['str11'],vol11=smbdict['vol11'],str12=smbdict['str12'],vol12=smbdict['vol12'],str13=smbdict['str13'],vol13=smbdict['vol13'],stravg=smbdict['stravg'],volavg=smbdict['volavg'],poweravg=smbdict['poweravg'])
        db.session.add(smbdata)
        db.session.commit()
        smbdict.clear()
    
    #print("len dataa=",len(data))
    #elif payload:
    #    print("pay=",payload)
    #    messageli=messagelist+list(payload)
    #    print("messagelist=",messageli)
    elif len(data)==4:
    #elif ((len(payload)>37) and (len(payload)!=45)):
   #     print("hi dict")
  #      print(len(smbdict))
        if len(smbdict)==0:
            smbdict.update(data)
    #        print(len(smbdict))
        #else:# len(smbdict)==4
        #if 'str2' not in smbdict:
        elif (('str2' not in smbdict) and ('str2' in data)):
     #       print("str2")
            smbdict['str2']=data['str2']
            smbdict['vol2']=data['vol2']
        #elif 'str3' not in smbdict:
        elif (('str3' not in smbdict) and ('str3' in data)):
      #      print("str3")
            smbdict['str3']=data['str3']
            smbdict['vol3']=data['vol3']
        #elif 'str4' not in smbdict:
        elif (('str4' not in smbdict) and ('str4' in data)):
       #     print("str4")
            smbdict['str4']=data['str4']
            smbdict['vol4']=data['vol4']
        #elif 'str5' not in smbdict:
        elif (('str5' not in smbdict) and ('str5' in data)):
        #    print("str5")
            smbdict['str5']=data['str5']
            smbdict['vol5']=data['vol5']
        #elif 'str6' not in smbdict:
        elif (('str6' not in smbdict) and ('str6' in data)):
         #   print("str6")
            smbdict['str6']=data['str6']
            smbdict['vol6']=data['vol6']
        #elif 'str7' not in smbdict:
        elif (('str7' not in smbdict) and ('str7' in data)):
          #  print("str7")
            smbdict['str7']=data['str7']
            smbdict['vol7']=data['vol7']
        #elif 'str8' not in smbdict:
        elif (('str8' not in smbdict) and ('str8' in data)):
          #  print("str8")
            smbdict['str8']=data['str8']
            smbdict['vol8']=data['vol8']
        elif (('str9' not in smbdict) and ('str9' in data)):
         #   print("str9")
            smbdict['str9']=data['str9']
            smbdict['vol9']=data['vol9']
        elif (('str10' not in smbdict) and ('str10' in data)):
          #  print("str10")
            smbdict['str10']=data['str10']
            smbdict['vol10']=data['vol10']
        elif (('str11' not in smbdict) and ('str11' in data)):
           # print("str11")
            smbdict['str11']=data['str11']
            smbdict['vol11']=data['vol11']
        elif (('str12' not in smbdict) and ('str12' in data)):
            #print("str12")
            smbdict['str12']=data['str12']
            smbdict['vol12']=data['vol12']
        elif (('str13' not in smbdict) and ('str13' in data)):
          #  print("str13")
            smbdict['str13']=data['str13']
            smbdict['vol13']=data['vol13']
        #print(smbdict)
#mqtt.Client.connected_flag=False#create flag in class
client = mqtt.Client()
#print("client=",client)

client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe
client.on_connect = on_connect
client.on_message = on_message
time.sleep(1)

subtop="tracker/device/sub"
pubtop="tracker/device/pub"
client.username_pw_set("cbocdpsu", "3_UFu7oaad-8")
client.connect('soldier.cloudmqtt.com', 14035,60)
client.loop_start()
client.subscribe(subtop)
client.loop()
 
app = dash.Dash(__name__,server=server,external_stylesheets=[dbc.themes.BOOTSTRAP, FA])


CONTENT_STYLE = {
    "bottom": "0rem",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding-right": "10rem",
}



PLOTLY_LOGO = "https://i2.wp.com/corecommunique.com/wp-content/uploads/2015/09/smarttrak1.png"

dropdown = dbc.DropdownMenu(
        children=[dbc.DropdownMenu(nav=True,in_navbar=True,label="Layout",
                    children=[
                        dbc.DropdownMenuItem(dbc.NavLink("Layout",href="/page-0"))]),
            dbc.DropdownMenu(nav=True,in_navbar=True,label="Trackers",
                    children=[
                        dbc.DropdownMenuItem(dbc.NavLink("Table",href="/page-1")),
                        dbc.DropdownMenuItem(dbc.NavLink("Graph", href='/page-2',style={'backgroundColor':'purple','fontSize':'bold','fontWeight':"10px"})),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem(dbc.NavLink("Read", href='/page-3',style={'backgroundColor':'brown'})),
                        dbc.DropdownMenuItem(dbc.NavLink("Write", href='/page-4',style={'backgroundColor':'black'}))]),
                    dbc.DropdownMenu(nav=True,in_navbar=True,label="SMB's",
                    children=[
                        dbc.DropdownMenuItem(dbc.NavLink("Table",href="/page-5")),
                        dbc.DropdownMenuItem(dbc.NavLink("Graph", href='/page-6')),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem(dbc.NavLink("Read", href='/')),
                        dbc.DropdownMenuItem(dbc.NavLink("Write", href='/'))])],
                    nav=True,in_navbar=True,label="DashBoard",style={'color':'black'})



navbar = dbc.Navbar(html.Div(
    # Use row and col to control vertical alignment of logo / brand
            dbc.Row([dbc.Col(html.Img(src=PLOTLY_LOGO, height="50px")),
                     dbc.Col(dbc.NavbarBrand( html.H2("DASHBOARD",style={"align":"center",'padding-right':'30rem','fontSize':'40px','align':'center','font-style': 'Georgia', 'font-weight': 'bold','color':'#610572'}))),],), ),color="#C3C489")


content = html.Div(id="page-content",style=CONTENT_STYLE)



card_1 =  html.Div([ dbc.Button(html.A("Trackers", id="tracker-button",href="/page-1"),outline=True),html.Br(),html.Br(),

            dbc.Card([dbc.CardBody([html.H4("Tracker Devices", className="card-title"),
            dbc.Button(html.A("R1", id="button",href="/page-2"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("R2", href="/page-2"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("B1", href="/page-2"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("B2", href="/page-2"),className="mr-1",color="warning"),html.Br(),html.Br(),
            dbc.Button(dbc.CardLink("C1", href="/page-2"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("C2", href="/page-2"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("E1", href="/page-2"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("E2", href="/page-2"),className="mr-1",color="warning"),html.Br(),html.Br(),
            dbc.Button(dbc.CardLink("F1", href="/page-2"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("F2", href="/page-2"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("G1", href="/page-2"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("G2", href="/page-2"),className="mr-1",color="warning"),html.Br(),html.Br(),
            dbc.Button(dbc.CardLink("H1", href="/page-2"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("H2", href="/page-2"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("I1", href="/page-2"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("I2", href="/page-2"),className="mr-1",color="warning"),

            ])],style={"border":"2px darkblue solid",'width':'18rem'},className="mr-2")])




card_2 =  html.Div([ dbc.Button(html.A("SMB's", id="tracker-button",href="/page-5"),outline=True),html.Br(),html.Br(),
            dbc.Card([dbc.CardBody([ html.H4("SMB's Devices", className="card-title"),
            dbc.Button(dbc.CardLink("R1", href="/page-6"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("R2", href="/page-6"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("B1", href="/page-6"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("B2", href="/page-6"),className="mr-1",color="warning"),html.Br(),html.Br(),
            dbc.Button(dbc.CardLink("C1", href="/page-6"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("C2", href="/page-6"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("E1", href="/page-6"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("E2", href="/page-6"),className="mr-1",color="warning"),html.Br(),html.Br(),
            dbc.Button(dbc.CardLink("F1", href="/page-6"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("F2", href="/page-6"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("G1", href="/page-6"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("G2", href="/page-6"),className="mr-1",color="warning"),html.Br(),html.Br(),
            dbc.Button(dbc.CardLink("H1", href="/page-6"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("H2", href="/page-6"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("I1", href="/page-6"),className="mr-1",color="warning"),
            dbc.Button(dbc.CardLink("I2", href="/page-6"),className="mr-1",color="warning"),

            ])],style={"border":"2px darkblue solid",'width':'18rem'},className="ml-2")])






app.config['suppress_callback_exceptions']=True

app.layout = html.Div([navbar,dropdown,dcc.Location(id='url', refresh=False),content])    


@app.callback(
    Output("navbar-collapse2", "is_open"),
    [Input("navbar-toggler2", "n_clicks")],
    [State("navbar-collapse2", "is_open")],
)
def toggle_navbar(n,is_open):
    if n:
        return not is_open
    return is_open



page_0_layout =html.Div([dbc.Row([dbc.Col(card_1),dbc.Col(card_2)]), dcc.Link(href='/page-0')])

page_2_graph =html.Div([dbc.Button(html.A("Home", href="/page-2"),outline=True,className="mr-4"),
    dbc.Button(html.A("Status", href="/"),outline=True,className="mr-4"),
    dbc.Button(html.A("Location SetUp", href="/page-4"),outline=True,className="mr-4"), 
    dbc.Button(html.A("Control",href="/"),outline=True,className="mr-4"),
    dbc.Jumbotron([
        dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H3('Graph'),
                    dcc.Dropdown(id='devices',
                options=[{'label': 'R1', 'value': 'R1'},{'label': 'G2', 'value': 'G2'},{'label': 'R2', 'value': 'R2'}],
                value='R1', style={"width":"auto","height":"auto"}),
            dcc.DatePickerRange(id='my-date-picker-range',
                min_date_allowed=datetime(1995, 8, 5,1,1,1,1),
                max_date_allowed=datetime.now(),
                initial_visible_month=datetime.now(),
                end_date=datetime.now(),
                start_date=datetime.now()-timedelta(days=1)),
            html.Div(id='output-container-date-picker-range'),
            html.Div(id='dd-output-container'),
            dcc.Graph(id='graph-with-slider',style={"width":"auto","height":"300px"}),
            dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),dcc.Link(href='/page-2'),
],style={'maxHeight':"470px","overflowY":"scroll"})),
    ]),], style={"border":"2px black solid"}),])])


page_6_graph = dbc.Jumbotron([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H3('SMB Graph'),
                    dcc.Dropdown(id='devicessmb',
                options=[{'label': 'G1', 'value': 'G1'},{'label': 'G2', 'value': 'G2'},{'label': 'R2', 'value': 'R2'}],
                value='G1', style={"width":"auto","height":"auto"}),
            dcc.DatePickerRange(id='my-date-picker-rangesmb',
                min_date_allowed=datetime(1995, 8, 5,1,1,1,1),
                max_date_allowed=datetime.now(),
                initial_visible_month=datetime.now(),
                end_date=datetime.now(),
                start_date=datetime.now()-timedelta(days=1)),
            html.Div(id='output-container-date-picker-rangesmb'),
            html.Div(id='dd-output-containersmb'),
            dcc.Graph(id='graph-with-slidersmb',style={"width":"auto","height":"300px"}), 
            dcc.Graph(id='graph-with-slidersmb2',style={"width":"auto","height":"300px"}),

            dcc.Link(href='/page-6'),
],style={'maxHeight':"470px","overflowY":"scroll"})),
    ]),], style={"border":"2px black solid"}),])


page_1_table = dbc.Jumbotron([
    dbc.Container(html.Div([html.H3('Table Data'),
          html.Br(),
          html.Div([ dbc.Button(html.A(
        "Download CSV",
        id='download-link',
        download="rawtable.csv",href="",target="_blank"),style={'color':'#C0C0C0'})
]),
          html.Br(),
          dcc.DatePickerRange(
            id='my-date-picker-range2',
            min_date_allowed=datetime(1995, 8, 5,1,1,1,1),
            max_date_allowed=datetime.now(),
            initial_visible_month=datetime.now(),
            end_date=datetime.now(),
            start_date=datetime.now()-timedelta(days=1)),
    html.Div(id='output-container-date-picker-range2'),
      

            dcc.Link(href='/page-1'),
            html.Br(),

            html.Div([html.Table(id="live-update-text")],style={'maxHeight':"380px","overflowY":"scroll"}),
]),style={"border":"2px black solid","padding":"0 rem"}),])

   
page_5_smbtable = dbc.Jumbotron([
    dbc.Container(html.Div([html.H3('Table Data'),
          html.Br(),
          html.Div([ dbc.Button(html.A(
        "Download CSV",
        id='download-linksmb',
        download="rawtable.csv",href="",target="_blank"),style={'color':'#C0C0C0'})
]), html.Br(),
          dcc.DatePickerRange(
            id='my-date-picker-range2smb',
            min_date_allowed=datetime(1995, 8, 5,1,1,1,1),
            max_date_allowed=datetime.now(),
            initial_visible_month=datetime.now(),
            end_date=datetime.now(),
            start_date=datetime.now()-timedelta(days=1)),
    html.Div(id='output-container-date-picker-range2smb'),
            dcc.Link(href='/page-5'),
            html.Br(),

            html.Div([html.Table(id="live-update-text-smb")],style={'maxHeight':"380px","overflowY":"scroll"}),
]),style={"border":"2px black solid","padding":"0 rem"}),])

   

page_3_read = html.Div([
    html.H4('You can read the data using these dropdown buttons'),
    dcc.Dropdown(
        id='devices1',
        options=[
            {'label': 'R1', 'value': 'R1'},
            {'label': 'G2', 'value': 'G2'},
            {'label': 'R2', 'value': 'R2'}
        ],
        value='', style={"width":"auto"}),
    dcc.Dropdown(
        id='options1',
        options=[
            {'label': 'ELIM', 'value': 'ELIM'},
            {'label': 'LAT', 'value': 'LAT'},
            {'label': 'LON', 'value': 'LON'},
            {'label': 'TA', 'value': 'TA'},
            {'label': 'WLIM', 'value': 'WLIM'},
            {'label': 'SPA', 'value': 'SPA'},
            {'label': 'MOTOR', 'value': 'MOTOR'},
            {'label': 'ZONE', 'value': 'ZONE'},
            {'label': 'MODE', 'value': 'MODE'},
            {'label': 'HR', 'value': 'HR'},
            {'label': 'MIN', 'value': 'MIN'},
            {'label': 'SEC', 'value': 'SEC'},
            {'label': 'DATE', 'value': 'DATE'},
            {'label': 'MONTH', 'value': 'MONTH'},
            {'label': 'YEAR', 'value': 'YEAR'},
            {'label': 'DAY', 'value': 'DAY'},
                    ],
        value='', style={"width":"auto"}),
    #inline=True,
    dbc.Button("Read", id="buttons1"),

html.Div(id='display'),
dcc.Link(href='/page-3'),html.H5("Tracker Data:"),
html.Div(messagelist2),html.H5("SMB Data:"),html.Div(messagelist)],style={'minHeight':"500px","overflowY":"scroll",'backgroundColor':'info'})


page_4_write=html.Div([
    html.H4('Using these you can write the commands for setting the values in the device'),
        dcc.Dropdown(id='device',
        options=[{'label': 'R1', 'value': 'R1'},{'label': 'R2', 'value': 'R2'},{'label': 'R3', 'value': 'R3'}],
        value='',style={"width":"auto"}    ),  html.Div(id="output"),
        dbc.Row([dbc.Col([html.H4("TimeStamp"),
            dbc.Row([html.H6("Seconds",className="mr-1",style={'color':'darkblue'}), dcc.Input(id="input SEC", type="text",className="mr-1"),
                dbc.Button("Send", id="SEC button",color='primary',outline=True)]),html.Br(),
       dbc.Row([ html.H6("Minute",className="mr-3",style={'color':'darkblue'}),dcc.Input(id="input MIN", type="text",className="mr-1"),
           dbc.Button("Send", id="MIN button",color='primary',outline=True)]),html.Br(),
       dbc.Row([html.H6("Hour",className="mr-4",style={'color':'darkblue'}),dcc.Input(id="input HOUR", type="text",className="mr-1"),
           dbc.Button("Send", id="HOUR button",color='primary',outline=True)]),html.Br(),
      dbc.Row([html.H6("Date",className="mr-4",style={'color':'darkblue'}),dcc.Input(id="input DATE", type="text",className="mr-1"),
          dbc.Button("Send", id="DATE button",color='primary',outline=True)]),html.Br(),
      dbc.Row([html.H6("Month",className="mr-3",style={'color':'darkblue'}),dcc.Input(id="input MONTH", type="text",className="mr-1"),
          dbc.Button("Send", id="MONTH button",color='primary',outline=True)]),html.Br(),
     dbc.Row([html.H6("Year",className="mr-4",style={'color':'darkblue'}),dcc.Input(id="input YEAR", type="text",className="mr-1"),
         dbc.Button("Send", id="YEAR button",color='primary',outline=True)]),html.Br(),
     dbc.Row([dbc.Button("AUTOMODE", id="AUTOMODE button",color='success',outline=True,className="mr-1"),
         dbc.Button("MANUALMODE", id="MANUALMODE button",color='primary',outline=True,className="mr-1"),
         dbc.Button("STOP", id="STOP button",color='danger',className="mr-1",outline=True)]),html.Br(),]),
    dbc.Col([
        dbc.Row([html.H4("Location")]),
        dbc.Row([html.H6("Latitude",className="mr-3",style={'color':'darkblue'}),dcc.Input(id="input LAT", type="text",className="mr-1"),
            dbc.Button("Send", id="LAT button",color='primary',outline=True,)]),html.Br(),
        dbc.Row([html.H6("Longitude",className="mr-2",style={'color':'darkblue'}),dcc.Input(id="input LONGITUDE", type="text",className="mr-1"),
            dbc.Button("Send", id="LONGITUDE button",color='primary',outline=True)]),html.Br(),
        dbc.Row([html.H6("Timezone",className="mr-2",style={'color':'darkblue'}), dcc.Input(id="input TIMEZONE", type="text",className="mr-1"),
            dbc.Button("Send", id="TIMEZONE button",color='primary',outline=True)]),html.Br(),
        dbc.Row([html.H4("Tracker Limits")]),html.Br(),
      dbc.Row([html.H6("East Limit",className="mr-1",style={'color':'darkblue'}),  dcc.Input(id="input ELIM", type="text",className="mr-1"),
          dbc.Button("Send", id="ELIM button",color='primary',outline=True,)]),html.Br(),
       dbc.Row([html.H6("West Limit",className="mr-1",style={'color':'darkblue'}), dcc.Input(id="input WLIM", type="text",className="mr-1"),
           dbc.Button("Send", id="WLIM button",color='primary',outline=True)]),html.Br(),
       dbc.Row([dbc.Button("EAST", id="EAST button",color='primary',outline=True,className="mr-1"),
           dbc.Button("WEST", id="WEST button",color='primary',outline=True,)])]),
     ]),
dcc.Link(href='/page-4')
])

@app.callback( Output('SEC button', 'value'),[Input('device', 'value'),Input('input SEC', 'value'),Input('SEC button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:SEC_{}".format(valueDEV,value2))
        #return 'You have published "{} SEC write {}"'.format(valueDEV,value2)
@app.callback( Output('MIN button', 'value'),[Input('device', 'value'),Input('input MIN', 'value'),Input('MIN button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:MIN_{}".format(valueDEV,value2))
        return 'You have published "{} MIN write {}"'.format(valueDEV,value2)
@app.callback( Output('HOUR button', 'value'),[Input('device', 'value'),Input('input HOUR', 'value'),Input('HOUR button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:HOUR_{}".format(valueDEV,value2))
        return 'You have published "{} HOUR write {}"'.format(valueDEV,value2)
@app.callback( Output('DATE button', 'value'),[Input('device', 'value'),Input('input DATE', 'value'),Input('DATE button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:DATE_{}".format(valueDEV,value2))
        return 'You have published "{} DATE write {}"'.format(valueDEV,value2)
@app.callback( Output('MONTH button', 'value'),[Input('device', 'value'),Input('input MONTH', 'value'),Input('MONTH button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:MONTH_{}".format(valueDEV,value2))
        return 'You have published "{} MONTH write {}"'.format(valueDEV,value2)
@app.callback( Output('YEAR button', 'value'),[Input('device', 'value'),Input('input YEAR', 'value'),Input('YEAR button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:YEAR_{}".format(valueDEV,value2))
        return 'You have published "{} YEAR write {}"'.format(valueDEV,value2)


@app.callback( Output('LAT button', 'value'),[Input('device', 'value'),Input('input LAT', 'value'),Input('LAT button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:LAT_{}".format(valueDEV,value2))
        return 'You have published "{} LAT write {}"'.format(valueDEV,value2)
@app.callback( Output('LONGITUDE button', 'value'),[Input('device', 'value'),Input('input LONGITUDE', 'value'),Input('LONGITUDE button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:LONGITUDE_{}".format(valueDEV,value2))
        return 'You have published "{} LONGITUDE write {}"'.format(valueDEV,value2)

@app.callback( Output('ELIM button', 'value'),[Input('device', 'value'),Input('input ELIM', 'value'),Input('ELIM button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:ELIM_{}".format(valueDEV,value2))
        return 'You have published "{} ELIM write {}"'.format(valueDEV,value2)
@app.callback( Output('WLIM button', 'value'),[Input('device', 'value'),Input('input WLIM', 'value'),Input('WLIM button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:WLIM_{}".format(valueDEV,value2))
        return 'You have published "{} WLIM write {}"'.format(valueDEV,value2)
@app.callback( Output('TIMEZONE button', 'value'),[Input('device', 'value'),Input('input TIMEZONE', 'value'),Input('TIMEZONE button', 'n_clicks')])
def update_output(valueDEV,value2,x):
    if((value2 != None) and (x is not None)):
        client.publish(pubtop,"{} WRITE:TIMEZONE_{}".format(valueDEV,value2))
        return 'You have published "{} TIMEZONE write {}"'.format(valueDEV,value2)

@app.callback( Output('EAST button', 'value'),[Input('device', 'value'),Input('EAST button', 'n_clicks')])
def update_output(valueDEV,x):
    if(x is not None):
        client.publish(pubtop,"{} WRITE:EAST".format(valueDEV))
        return 'You have published "{} write EAST"'.format(valueDEV)
@app.callback( Output('WEST button', 'value'),[Input('device', 'value'),Input('WEST button', 'n_clicks')])
def update_output(valueDEV,x):
    if(x is not None):
        client.publish(pubtop,"{} WRITE:WEST".format(valueDEV))
        return 'You have published "{} write WEST"'.format(valueDEV)

@app.callback( Output('AUTOMODE button', 'value'),[Input('device', 'value'),Input('AUTOMODE button', 'n_clicks')])
def update_output(valueDEV,x):
    if(x is not None):
        client.publish(pubtop,"{} WRITE:AUTOMODE".format(valueDEV))
        return 'You have published "{} write AUTOMODE"'.format(valueDEV)
@app.callback( Output('MANUALMODE button', 'value'),[Input('device', 'value'),Input('MANUALMODE button', 'n_clicks')])
def update_output(valueDEV,x):
    if(x is not None):
        client.publish(pubtop,"{} WRITE:MANUALMODE".format(valueDEV))
        return 'You have published "{} write MANUALMODE"'.format(valueDEV)
@app.callback( Output('STOP button', 'value'),[Input('device', 'value'),Input('STOP button', 'n_clicks')])
def update_output(valueDEV,x):
    if(x is not None):
        client.publish(pubtop,"{} WRITE:STOP".format(valueDEV))
        return 'You have published "{} write STOP"'.format(valueDEV)




def conv(x):
    val=unicodedata.normalize('NFKD', x).encode('ascii','ignore')
    print("val=",val)
    return val
def table(filtered_df):
    table_header=[html.Thead(html.Tr([html.Th('Id'),html.Th('stamp'),html.Th('devId'),html.Th('sun angle') ,html.Th('tracker angle')]))]
    table_body=[html.Tbody(html.Tr([html.Td(dev[0]),html.Td(dev[1]),html.A(html.Td(dev[2]),href="/page-2"),html.Td(dev[3]),html.Td(dev[4])]))for dev in filtered_df]
    table=dbc.Table(table_header+table_body,bordered=True,striped=True,hover=True,style={"backgroundColor":"white"})
    return table


def tablesmb(filtered_df):
    
    table_header=[html.Thead(html.Tr([html.Th('Id'),html.Th('stamp'),html.Th('devId'),html.Th('str1') ,html.Th('str2'),html.Th('str3') ,html.Th('str4'),html.Th('str5') ,html.Th('str6'),html.Th('str7') ,html.Th('str8'),html.Th('str9') ,html.Th('str10'),html.Th('str11') ,html.Th('str12'),html.Th('str13'),html.Th('vol1'),html.Th('vol2'),html.Th('vol3'),html.Th('vol4'),html.Th('vol5'),html.Th('vol6'),html.Th('vol7'),html.Th('vol8'),html.Th('vol9'),html.Th('vol10'),html.Th('vol11'),html.Th('vol12'),html.Th('vol13'),html.Th('temp')
         ]))]
    table_body=[html.Tbody(html.Tr([html.Td(dev[0]),html.Td(dev[1]),html.A(html.Td(dev[2]),href="/page-6"),html.Td(dev[3]),html.Td(dev[4]),html.Td(dev[5]),html.Td(dev[6]),html.Td(dev[7]),html.Td(dev[8]),html.Td(dev[9]),html.Td(dev[10]),html.Td(dev[11]),html.Td(dev[12]),html.Td(dev[13]),html.Td(dev[14]),html.Td(dev[15]),html.Td(dev[16]),html.Td(dev[17]),html.Td(dev[18]),html.Td(dev[19]),html.Td(dev[20]),html.Td(dev[21]),html.Td(dev[22]),html.Td(dev[23]),html.Td(dev[24]),html.Td(dev[25]),html.Td(dev[26]),html.Td(dev[27]),html.Td(dev[28]),html.Td(dev[29])]))for dev in filtered_df]
    table=dbc.Table(table_header+table_body,bordered=True,striped=True,hover=True,style={"backgroundColor":"white"})
    return table


@app.callback(
        Output('display', 'children'),
        [Input('devices1', 'value'),Input('options1', 'value'),Input('buttons1','n_clicks')])

def output(val1,val2,n):
    if n:
        client.publish(pubtop,"{} READ:{}".format(val1,val2))
        return "published for getting {}".format(val2)

    
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('devices', 'value'),Input('my-date-picker-range', 'start_date'),Input('my-date-picker-range', 'end_date')])
def update_figure(selected_device,start,end):
    connection1 = engine
    print("start=",start,"end=",end,"dt.now=",datetime.now())
    df=pd.read_sql("select * from datatable",connection1)
    filtered_d = df[df.devId == selected_device]
    filtered_df = filtered_d.loc[(filtered_d['stamp'] > start) & (filtered_d['stamp'] <= end)]
    print("filtered df=",filtered_df)
    client.publish(pubtop,"{} READ:GETALL".format(selected_device))
    return {
                                'data': [
                                    {'x': filtered_df.stamp, 'y':filtered_df.SPA
                                    #.where(df.devname=='dev_01')
                                    , 'name': 'SPA'},
                                    {'x': filtered_df.stamp, 'y':filtered_df.TA
                                                                  , 'name': 'TA'}, ],
            'layout': {
                'title': '(SPA and TA)  vs Time'
                }}

@app.callback(
    Output('graph-with-slidersmb', 'figure'),
    [Input('devicessmb', 'value'),Input('my-date-picker-rangesmb', 'start_date'),Input('my-date-picker-rangesmb', 'end_date')])
def update_figure(selected_device,start,end):
    connection1 = engine#.connnect()
    print("start=",start,"end=",end,"dt.now=",datetime.now())
    df=pd.read_sql("select * from smbtable",connection1)
    filtered_d = df[df.devId == selected_device]# and ([df.stamp == i] for i in (start,end,timedelta(microseconds=1)))]
    filtered_df = filtered_d.loc[(filtered_d['stamp'] > start) & (filtered_d['stamp'] <= end)]
    print("filtered df=",filtered_df)
    
    return {
                                'data': [
                                    {'x': filtered_df.stamp, 'y':filtered_df.poweravg, 'name': 'Power(avg) in KW'},],
            'layout': {
                'title': 'Power in KW(avg) vs Time'
                }}


@app.callback(
    Output('graph-with-slidersmb2', 'figure'),
    [Input('devicessmb', 'value'),Input('my-date-picker-rangesmb', 'start_date'),Input('my-date-picker-rangesmb', 'end_date')])
def update_figure(selected_device,start,end):
    connection1 = engine#.connnect()
    print("start=",start,"end=",end,"dt.now=",datetime.now())
    df=pd.read_sql("select * from smbtable",connection1)
    filtered_d = df[df.devId == selected_device]# and ([df.stamp == i] for i in (start,end,timedelta(microseconds=1)))]
    filtered_df = filtered_d.loc[(filtered_d['stamp'] > start) & (filtered_d['stamp'] <= end)]
    print("filtered df=",filtered_df)
    return {
                                'data': [{'x': filtered_df.stamp, 'y':filtered_df.volavg, 'name': 'Voltage(avg) in Volts'},
                                    {'x': filtered_df.stamp, 'y':filtered_df.stravg, 'name': 'String Current(avg) in Amps'}, ],
            'layout': {
                'title': '(Voltage(avg) and String Current(avg))  vs Time'
 }}




@app.callback(Output("live-update-text", "children"),
              [Input("live-update-text", "className"),Input('my-date-picker-range2', 'start_date'),Input('my-date-picker-range2', 'end_date')])
def update_output_div(input_value,start,end):
    connection1 = engine#.connnect()
    df=pd.read_sql("select * from datatable",connection1)
    filtered_df = df.loc[(df['stamp'] > start) & (df['stamp'] <= end)]
    print("table filtereddf=",filtered_df.stamp)
    print("table filtereddf=",filtered_df.all)
    filtered_df=filtered_df.values.tolist()
    return [html.Table(table(filtered_df)
        )]


def timeconvert(dftime):
    print("dftime=",dftime[0])
    print("dftime=",len(dftime))
    #x=dftime[:8]+".00000"+dftime[9:]
    for i in dftime:
        dftime[i]=datetime.strptime(dftime[i],"%d/%m/%Y %H:%M:%S.%f")
    return dftime

@app.callback(Output("live-update-text-smb", "children"),
              [Input("live-update-text-smb", "className"),Input('my-date-picker-range2smb', 'start_date'),Input('my-date-picker-range2smb', 'end_date')])
def update_output_div(input_value,start,end):
    connection1 = engine#.connnect()
    df=pd.read_sql("select * from smbtable",connection1)
    print("smb table=",df)
    print("smb table df time=",df['stamp'])
    print("smb start=",str(start),"smb end",end)
    filtered_df = df.loc[(start < df['stamp']) & (end >= df['stamp'])]
    filtered_df=filtered_df.values.tolist()
    return [html.Table(tablesmb(filtered_df))]



@app.callback(Output("download-link", "href"),
              [Input("download-link", "className"),Input('my-date-picker-range2', 'start_date'),
                  Input('my-date-picker-range2', 'end_date')])
def update_download_link(input_value,start,end):
    print("executing")
    connection1 = engine
    df=pd.read_sql("select * from datatable",connection1)
    filtered_df = df.loc[(df['stamp'] > start) & (df['stamp'] <= end)]
    filtered_df=filtered_df.values.tolist()
    con_df = pd.DataFrame(filtered_df, columns=['id','stamp','devId','SPA','TA'])
    print("con_df=",con_df)

    cv = con_df.to_csv(index=False, encoding='utf-8')
    cv = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(cv)
    return cv

@app.callback(Output("download-linksmb", "href"),
              [Input("download-linksmb", "className"),Input('my-date-picker-range2smb', 'start_date'),
                  Input('my-date-picker-range2smb', 'end_date')])
def update_download_link(input_value,start,end):
    print("executing")
    connection1 = engine
    df=pd.read_sql("select * from smbtable",connection1)
    filtered_df = df.loc[(df['stamp'] > start) & (df['stamp'] <= end)]
    filtered_df=filtered_df.values.tolist()
    con_df = pd.DataFrame(filtered_df, columns=['id','stamp','devId','str1','str2','str3','str4','str5','str6','str7','str8','str9','str10','str11','str12','str13','vol1','vol2','vol3','vol4','vol5','vol6','vol7','vol8','vol9','vol10','vol11','vol12','vol13','temp','stravg','volavg','poweravg'])
    print("con_df=",con_df)

    cv = con_df.to_csv(index=False, encoding='utf-8')
    cv = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(cv)
    return cv


@app.callback(dash.dependencies.Output('url', 'pathname'),
              [dash.dependencies.Input('tabs', 'value')])
def tab_updates_url(value):
    return value
    
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')],
              )
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_table
    elif pathname == '/page-2':
        return page_2_graph
    elif pathname == '/page-3':
        return page_3_read
    elif pathname =='/page-4':
        return page_4_write
    elif pathname =='/page-5':
     #   pathname == '/page-1'
        return page_5_smbtable
    elif pathname =='/page-6':
        return page_6_graph
    elif pathname =='/page-0':
        return page_0_layout
    return page_0_layout

        

if __name__ == '__main__':
    app.run_server(debug=True,threaded=True, use_reloader=True)

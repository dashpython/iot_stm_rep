import os 
import pathlib
import requests
import flask
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import sqlite3
from flask import Flask, request,render_template
from flask_restful import Api
from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
#from models import User
import paho.mqtt.client as mqtt
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
#import argparse
from datetime import timedelta 
num=0

FA ="https://use.fontawesome.com/releases/v5.8.1/css/all.css"
LOGO ="https://www.tirumala.org/NewImages/TTD-Logo.png"
LOGO1="https://www.tirumala.org/NewImages/HD-TXT.png"
#client = mqtt.Client()



server = flask.Flask(__name__)

server.config['DEBUG'] = True

server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

server.secret_key = 'smarttrak'

#db_URI = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
#engine = create_engine(db_URI)

api = Api(server)
db = SQLAlchemy(server)


@server.before_first_request
def create_tables():
    db.create_all()

class DeviceModel(db.Model):
    __tablename__ = 'data'

    devId  = db.Column(db.String(15),primary_key=True)
    deviceId = db.Column(db.String(15))
    SPA = db.Column(db.Float(precision=2))
    TA= db.Column(db.Float(precision=2))

    def __init__(self,devId,deviceId,SPA,TA):
        self.deviceId=devId
        self.SPA= SPA
        self.TA= TA


def on_connect(client, userdata, flags, rc):
    print("Connected!", rc)

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

connection = sqlite3.connect('data.db',check_same_thread=False)
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY,stamp VARCHAR(15), devId VARCHAR(15), SPA VARCHAR(15),TA VARCHAR(15) )")

n=0
def on_message(client, userdata, message):
  #global num
  #global n
  #if num!=n:  
    print("on_message=",message)
    if str(message.topic) != pubtop:
        print(str(message.topic), str(message.payload.decode("utf-8")))
    payload = str(message.payload.decode("utf-8"))
    print("payload=",payload)
    data = dict(x.split(": ") for x in payload.split(" , "))
    x=["stamp"]
    y=[str(datetime.now()+ timedelta(minutes=330))]
    for columns,placeholders in data.items():
          x.append(columns)
          y.append(placeholders)
          print(x)
          print(y)
    
    if  len(data)>2:
        sql = "INSERT INTO data ('%s','%s','%s','%s') VALUES ('%s','%s','%s','%s')" % (x[0],x[1],x[2],x[3],y[0],y[1],y[2],y[3])

        try:
            print("try block")
            cursor.execute(sql)
        except sqlite3.Error as error:
            print("Error: {}".format(error))
        connection.commit()

n=n+1
print("n=",n)
client = mqtt.Client()
print("client=",client)

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
print("in loop")
client.subscribe(subtop)
client.loop()


#api.add_resource(Device, '/device/<string:devId>')
#api.add_resource(DeviceList, '/devices')

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "15rem",
    "padding": "2rem 2rem",
    "fontSize":"30rem"
}

collapse = html.Div(
    [
        dbc.Button("Menu",id="collapse-button",className="mb-4",color="primary"),
        dbc.Container(dbc.Collapse(
            children=[dbc.DropdownMenu(nav=True,in_navbar=True,label="Substations",
            children=[
                dbc.DropdownMenu(nav=True,in_navbar=True,label="SUB 1",
                    children=[
                        dbc.DropdownMenuItem(dbc.NavLink("Dev 1",href="/Dev-1",id="dev-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("Dev 2",href="/Dev-2",id="dev-2")),dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem(dbc.NavLink("Dev 3",href="/Dev-3",id="dev-3"))]),
                           dbc.DropdownMenu(nav=True,in_navbar=True,label="SUB 2",
                               children=[
                                   dbc.DropdownMenuItem(dbc.NavLink("SVM 1",href="/SVM-1",id="svm-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("SVM 2",href="/SVM 2",id="svm-2")),dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem(dbc.NavLink("SVM 3",href="/SVM-3",id="svm-3"))])]),
                    dbc.DropdownMenu(nav=True,in_navbar=True,label="Streetlights",
                        children=[
                dbc.DropdownMenu(nav=True,in_navbar=True,label="SL 1",
                    children=[
                        dbc.DropdownMenuItem(dbc.NavLink("JEO 1",href="/jeo-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("JEO 2",href="/jeo 2")),dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem(dbc.NavLink("JEO 3",href="/jeo 3"))]),
                           dbc.DropdownMenu(nav=True,in_navbar=True,label="SL 2",
                               children=[
                                   dbc.DropdownMenuItem(dbc.NavLink("SVSD 1",href="/SVSD-1")),dbc.DropdownMenuItem(divider=True),dbc.DropdownMenuItem(dbc.NavLink("SVSD 2",href="/SVSD 2")),dbc.DropdownMenuItem(divider=True)])])],                                                                  
                                
    id="collapse"),style={"backgroundColor":"grey","width":"auto"})])     

sidebar = html.Div(
        [
       dbc.Row(
            html.Img(src=LOGO,height="100px",width="auto"),style={"padding-left":0}),
                
            dbc.Nav(collapse, vertical=True)
  ] ,

style={
    "position": "absolute",
    "top": 0,
    "left":"2rem",
    "bottom": 0,
    "width": "12rem",
    "padding": "1rem 0rem",
    "backgroundColor":"light"},
     id="sidebar",
)

button =html.Div(
           dbc.Row(
              [
                  dbc.Col(dbc.Button("Login",color="primary",className="mb-3",href="#"),style={"padding-left":"20rem","width":"15rem"})]))
navbar = dbc.Navbar(
           html.Div(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.NavbarBrand(
                                html.H2((html.Img(src=LOGO1,height="60px",width="auto"))),style={"fontSize":"50px","padding-left":"10rem"})),
                        dbc.NavbarToggler(id="navbar-toggler"),
                         dbc.Collapse(sidebar,id="sidebar-collapse",navbar=True),
                         dbc.Collapse(button,id="button-collapse",navbar=True)
                        ],
                    align="center",
                    no_gutters=True,
                ),
             ),
          )

content = html.Div(id="page-content", style=CONTENT_STYLE)

buttons=html.Div([html.Button('longitude', id='button1'),html.Button('latitude', id='button2'),html.Button('rtc', id='button3'),html.Button('sun', id='button4')])


data1= html.Div([
        html.H4('Substation Data Live Feed'),
        html.Table(id="live-update-text"),],style={"overflowX":"scroll"}) 

app = dash.Dash(__name__,server=server,external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

app.config['suppress_callback_exceptions']=True

def table(rows):
    #global reading
    print("table rows=",rows)
    #reading=reading+1
    table_header=[
        html.Thead(html.Tr([html.Th('id'),html.Th('stamp'),html.Th('devId'),html.Th('SPA') ,html.Th('TA')#, html.Th('motor status') ,
         ]))]
    table_body=[
        html.Tbody(html.Tr([html.Td(dev[0]),html.Td(dev[1]),html.Td(dev[2]),html.Td(dev[3]),html.Td(dev[4])]))for dev in rows]
    table=dbc.Table(table_header+table_body,bordered=True,striped=True,hover=True,style={"backgroundColor":"white"})
    return table

#df=pd.read_sql("select * from data",connection)
select=html.Div([
    dcc.Dropdown(
        id='device',
        options=[
            {'label': 'R1 ', 'value': 'R1 '},
            {'label': 'G2 ', 'value': 'G2 '},
            {'label': 'R2 ', 'value': 'R2 '}
        ],
        value='R1 '
    ),
    html.Div(id='dd-output-container1'),],)
    
select2=html.Div(  [  dcc.Dropdown(
        id='options',
        options=[
            {'label': 'LAT', 'value': 'LAT'},
            {'label': 'LONGITUDE', 'value': 'LONGITUDE'},
            {'label': 'SUN', 'value': 'SUN'},
            {'label': 'RTC', 'value': 'RTC'}

        ],
        value='LAT'
    ),
    html.Div(id='dd-output-container2')

])

items = [
    dbc.DropdownMenuItem("R1"),
    dbc.DropdownMenuItem("R2"),
    dbc.DropdownMenuItem("G2"),
]
items2 = [
    dbc.DropdownMenuItem("LAT"),
    dbc.DropdownMenuItem("LONGITUDE"),
    dbc.DropdownMenuItem("SUN"),
    dbc.DropdownMenuItem("RTC"),
    dbc.DropdownMenuItem("TA"),
]
app.layout = html.Div([navbar,content,data1,dcc.Location(id="url",refresh=True)])
def update_output(valueDEV,valueOP):
    if client.publish(pubtop,"'{a}' WRITE:'{b}'_'{c}'".format(a=valueDEV,b=valueOP,c=value2)):
        return html.Div(['You have selected "{}"'.format(value)])

@app.callback(
    dash.dependencies.Output('button1', 'children'),
    [dash.dependencies.Input('button1', 'n_clicks')])
def update_output(n_clicks):
    if client.publish(pubtop, "R1 Read:longitude"):
        return html.Div("longitude")

@app.callback(
    dash.dependencies.Output('button2', 'children'),
    [dash.dependencies.Input('button2', 'n_clicks')])
def update_output(n_clicks):
    if client.publish(pubtop, "R1 Read:latitude"):
        return html.Div("latitude")

@app.callback(
    dash.dependencies.Output('button3', 'children'),
    [dash.dependencies.Input('button3', 'n_clicks')])
def update_output(n_clicks):
    if client.publish(pubtop, "R1 Read:rtc"):
        return html.Div("rtc")

@app.callback(
    dash.dependencies.Output('button4', 'children'),
    [dash.dependencies.Input('button4', 'n_clicks')])
def update_output(n_clicks):
    if client.publish(pubtop, "R1 Read:sun"):
        return html.Div("sun")
   
@app.callback(Output("live-update-text", "children"),
              [Input("live-update-text", "className")])


def update_output_div(input_value):
    connection = sqlite3.connect('data.db',check_same_thread=False)
    cursor.execute("SELECT * FROM data")
    rows = cursor.fetchall()
    return [html.Table(table(rows)
        )]
    
                  
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],)

def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in range(1,4):
    @app.callback(
         Output("dev-{%d}"%i, "active"),
         [Input("url", "pathname")],
         )
    def toggle_active_links(pathname):
        if pathname == "/":
        # Treat page 1 as the homepage / index
            return True, False, False
        return [pathname == "/Dev-{%d}"%i]

@app.callback([Output("page-content", "children")],
        [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname in ["/", "/Dev-1"]:
        return [
                html.H4("Displays Device 1 Graph")]

    elif pathname in ["/", "/Dev-2"]:
        return [
                html.H4("Displays Device 2 Graph")]

    elif pathname in ["/", "/Dev-3"]:
        return [
                html.H4("Displays Device 3 Graph")]
    
   # If the user tries to reach a different page, return a 404 message
    return [404]

if __name__=="__main__":
    print("main starts")
    db.create_all()
    app.run_server(debug=True,port=449)
    #mqtt1()
    #app1.run(debug=True)
    print("main end")

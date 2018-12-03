import paho.mqtt.client as paho
import pandas as pd
import time

broker="10.42.0.1"
port=1883


def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def getData():    

    data = pd.read_csv('../../Fuel_Dataset/testing.csv')

    '''
        Using random values from individual columns
    '''
    '''
    K = data.iloc[:,0].sample(n=1).item()
    Psi = data.iloc[:,1].sample(n=1).item()
    Th = data.iloc[:,2].sample(n=1).item()
    SV = data.iloc[:,3].sample(n=1).item()
    
    retData = str([K, Psi, Th, SV])
    print(retData)
    '''


    '''
        Using random rows
    '''    
    retData = str(data.sample(n=1).values.tolist())
    print(retData)


    return retData


client1= paho.Client("iot_client")                           #create client object

client1.on_publish = on_publish                          #assign function to callback



client1.connect(broker,port,60)                                 #establish connection



NoError = True

while(NoError):
    data = getData()

    x,y= client1.publish("sensor/fuel_data", data)
    NoError = x == 0
    time.sleep(1)


print("Fuel data Publishing stopped due to some reason..disconnecting")

client1.disconnect()
print("Disconnected")

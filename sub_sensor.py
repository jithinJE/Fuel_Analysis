import paho.mqtt.client as mqtt
from sklearn.externals import joblib
from sklearn.preprocessing import PolynomialFeatures

broker="localhost"
port=1883
keepalive = 60

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensor/fuel_data")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = msg.payload
    message = message.translate(None, '[],')

    # parse columns from the string message
    list_of_columns = [[float(i) for i in message.split()]]
    

    # Separate X & Y from the column
    actual_Y = list_of_columns[0][4]
    sensor_X = [list_of_columns[0][:4]]
    print("\n\nSensor X : {0}".format(sensor_X))
    print("Actual Y : {0}".format(actual_Y))

    
    
    # Predict Y
    pred_value = linear_regressor_poly.predict(poly_regressor.fit_transform(sensor_X))    
    print("Predicted Y : {0}".format(pred_value[0][0]))


# Load model
linear_regressor_poly = joblib.load('nonlinear_order8_model.pkl')

poly_regressor = PolynomialFeatures(degree = 8)




# MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, keepalive)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

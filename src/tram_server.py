#!/usr/bin/env python
import os
import rospy
import threading

from waitress import serve
from flask import Flask
from flask_ask import Ask, question, statement
from std_msgs.msg import String,Bool
start_flag =False
e_stop_flag =False
app = Flask(__name__)
ask = Ask(app, "/")
NEWCODE="rostopic pub /test_flag std_msgs/Bool false --once"
#waypoint="roslaunch waypoint_maker waypoint_loader.launch multi_lane_csv:=/home/usrg/waypoint/ki_to_presi_si4.csv"
# ROS node, publisher, and parameter.
# The node is started in a separate thread to avoid conflicts with Flask.
# The parameter *disable_signals* must be set if node is not initialized
# in the main thread.

threading.Thread(target=lambda: rospy.init_node('test_node', disable_signals=True)).start()
start_pub = rospy.Publisher('start_pub', Bool, queue_size=1)
e_stop_pub = rospy.Publisher('e_stop_pub', Bool, queue_size=1)
NGROK = rospy.get_param('/ngrok', None)

def test_cb(msg):

    print("hi")

@ask.launch
def launch():
    welcome_sentence = 'Welcome to U s r g Tram. where do you want to go?'
    return question(welcome_sentence)
   
@ask.intent('TestIntent', default={'goal': 'Main building'})
def test_intent_function(goal):
    

    start_flag=True
    start_pub.publish(start_flag)
    #os.system(waypoint) 
    return statement('Hello Everyone. Thank you for riding!. \
    U s r g Tram is leaving soon. Fasten your seat belt please!.\
    It will take 6minutes to go to : {0}.'.format(goal))

@ask.intent('EmergencyIntent')
def Emergency_intent_function():

    e_stop_flag=True
    e_stop_pub.publish(e_stop_flag)
    return statement('Emergecy stop')



@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if NGROK:
        print 'NGROK mode'
    #app.run(host=os.environ['ROS_IP'], port=5002)
	#serve(app)
	#serve(app, host=os.environ['ROS_IP'], port=5002)
	#serve(app, host='0.0.0.0', port=5002)
	#serve(app, host='127.0.0.1', port=8080)
	serve(app, host='127.0.0.1', port=5050)
    else:
        print 'Manual tunneling mode'
        dirpath = os.path.dirname(__file__)
        cert_file = os.path.join(dirpath, '../config/ssl_keys/certificate.pem')
        pkey_file = os.path.join(dirpath, '../config/ssl_keys/private-key.pem')
        app.run(host=os.environ['ROS_IP'], port=5000,
                ssl_context=(cert_file, pkey_file))
    rospy.Subscriber("/test_flag",Bool,test_cb)
    rospy.spin()
    

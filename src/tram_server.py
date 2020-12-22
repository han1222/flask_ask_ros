#!/usr/bin/env python
import os
import rospy
import threading

from waitress import serve
from flask import Flask
from flask_ask import Ask, question, statement
from std_msgs.msg import String,Bool
from sensor_msgs.msg import NavSatFix
start_flag =False
e_stop_flag =False
app = Flask(__name__)
ask = Ask(app, "/")
#NEWCODE="rostopic pub /test_flag std_msgs/Bool false --once"
#waypoint="roslaunch waypoint_maker waypoint_loader.launch multi_lane_csv:=/home/usrg/waypoint/ki_to_presi_si4.csv"
# ROS node, publisher, and parameter.
# The node is started in a separate thread to avoid conflicts with Flask.
# The parameter *disable_signals* must be set if node is not initialized
# in the main thread.

threading.Thread(target=lambda: rospy.init_node('test_node', disable_signals=True)).start()
start_pub = rospy.Publisher('/Bool/start_pub', Bool, queue_size=1)
e_stop_pub = rospy.Publisher('/Bool/e_stop_pub', Bool, queue_size=1)
nav_pub = rospy.Publisher('/Goal/latlon', NavSatFix, queue_size=1)
NGROK = rospy.get_param('/ngrok', None)


@ask.launch
def launch():
    welcome_sentence = 'Welcome to U s r g Tram. where do you want to go?'
    return question(welcome_sentence)
   
@ask.intent('TestIntent', default={'goal': 'Main building'})
def test_intent_function(goal):
    
    navsat=NavSatFix()
    if goal =="Main building" or goal=="Maine building" or goal=="Maine" or goal =="main building":
        start_flag=True
        start_pub.publish(start_flag)
        navsat.latitude=36.3708332
        navsat.longitude=127.3615032
        nav_pub.publish(navsat)
        print(goal)
        return statement('Hello Everyone. Thank you for riding!. \
        U s r g Tram is leaving soon. Fasten your seat belt please!.\
        It will take 6minutes to go to : {0}.'.format("Main building"))
        
    if goal =="library" or goal=="raebareli" or goal=="rewari" or goal=="rajouri":
        start_flag=True
        start_pub.publish(start_flag)
        navsat.latitude= 36.3694411
        navsat.longitude=127.3621108
        nav_pub.publish(navsat)
        print(goal)
        return statement('Hello Everyone. Thank you for riding!. \
        U s r g Tram is leaving soon. Fasten your seat belt please!.\
        It will take 4minutes to go to : {0}.'.format("library"))

         
    if goal =="subway":
        start_flag=True
        start_pub.publish(start_flag)
        navsat.latitude=36.371122
        navsat.longitude=127.362080
        nav_pub.publish(navsat)
        print(goal)
        return statement('Hello Everyone. Thank you for riding!. \
        U s r g Tram is leaving soon. Fasten your seat belt please!.\
        It will take 4minutes to go to : {0}.'.format("subway"))
    
    if goal =="K. I building" or goal =="K. caerphilly building" or goal =="caerphilly" or goal == "KI building" or goal =="Thai binh":
        start_flag=True
        start_pub.publish(start_flag)
        navsat.latitude=36.3685642
        navsat.longitude=127.3636356
        nav_pub.publish(navsat)
        print(goal)
        return statement('Hello Everyone. Thank you for riding!. \
        U s r g Tram is leaving soon. Fasten your seat belt please!.\
        It will take 6minutes to go to : {0}.'.format("K. I building"))
    print(goal)
    #os.system(waypoint) 
   

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
    #rospy.spin()
    

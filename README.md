# flask_ask_ros
A locally hosted web service + ROS node for custom Alexa skills based on [Flask-Ask](https://github.com/johnwheeler/flask-ask).

## Table of Contents

* [Description](README.md#description)
* [Requirements](README.md#requirements)
* [Maintainers](README.md#maintainers)
* [Installation](README.md#installation)
* [Usage](README.md#usage)
* [TO DO](README.md#todo)

## Description
This package combines a Flask server and ROS node into a script that serves as an endpoint for a custom Alexa Skill. This enables information sent by voice to the Amazon Alexa to be processed by other ROS nodes and services.

In this package we provide a simple Alexa skill that parses a single slot (word/argument) from an utterance (spoken function call) and publishes it to a ROS topic. 


## Requirements

* Ubuntu 18.04 or 16.04

* ROS Melodic or Kinetic

* Flask-ask (Python): follow installation from source [here.](https://github.com/johnwheeler/flask-ask/blob/master/README.rst#development)

## Maintainers

* SEUGIL HAN <robotics@kaist.ac.kr>

## Installation

* Navigate to source directory of your ROS catkin workspace (e.g. `catkin_ws`):

  ``` bash
      cd catkin_ws/src
      git clone https://github.com/3SpheresRoboticsProject/flask_ask_ros
  ```

* Build catkin workspace:

  ``` bash
      cd catkin_ws
      catkin_make
  ```

* If necessary, set script file permissions to executable:

  ``` bash
      chmod +x catkin_ws/src/flask_ask_ros/src/*
  ```

* Source workspace:

  ``` bash
      source catkin_ws/devel/setup.bash
  ```

## Usage

### Endpoint configuration

In order for the Alexa requests to reach the local skill server, the local network must be configured to tunnel HTTPS traffic to a specific port on the local machine.

We have tested two ways to accomplish this:

* Using ngrok as a tunnel

* Static IP/Dynamic DNS + self-signed SSL certificate

### ngrok tunnel configuration

1. Set the `ROS_IP` environment variable to be the local machine IP

2. Download [ngrok for Linux](https://ngrok.com/download) and unzip

3. Start an ngrok server:
   
   ``` bash
   ./ngrok http $ROS_IP:5000
   ```
4. Open the [Amazon Developer Console](https://developer.amazon.com/alexa/console/ask) and navigate to your custom skill:
   
   * Under *Configuration*, select *HTTPS* and paste the URL shown on the ngrok terminal (see below).
	 
	 ![alt text][ngrok_url]
   
   * Under *SSL Certificate* select *My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority.*

5. Run the skill server with the ngrok argument set to `true`:
   
   ``` bash
   roslaunch flask_ask_ros start_skill_server.launch ngrok:=true
   ```

## Testing

In order to test the provided skill server, open your [Amazon Developer Console](https://developer.amazon.com/alexa/console/ask), create a custom skill, and follow the [steps above to configure your endpoint](README.md#Usage).

Inside the skill builder, navigate to the *JSON Editor* and paste the contents of `src/test_skill.json`. Save and build the model.

Run the skill server to test your skill.

## TODO

* Sample code for ROS services

This app was not created or endorsed by Amazon.
# flask_ask_ros

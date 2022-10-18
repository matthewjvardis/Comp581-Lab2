#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

def deg_to_rad(y):
    return(y*(3.14159265358979/180))

def run_motors(leftMotor, leftSpeed, rightMotor, rightSpeed):
    leftMotor.run(leftSpeed)
    rightMotor.run(rightSpeed)

def stop_motors(leftMotor, rightMotor):
    leftMotor.run_time(0,0,then=Stop.BRAKE, wait = False)
    rightMotor.run_time(0,0,then=Stop.BRAKE, wait = False)

def wait_for_button():
    pressed = 0
    while (Button.CENTER not in EV3Brick.buttons.pressed()):
        pass

def play_music(ev3):
    ev3.speaker.play_notes(["D3/8", "D3/8", "D4/8"], 225)
    wait(100)
    ev3.speaker.play_notes(["A3/8"], 150)
    wait(200)
    ev3.speaker.play_notes(["G#3/8"], 150)
    wait(50)
    ev3.speaker.play_notes(["G3/8", "F3/8"], 150)
    ev3.speaker.play_notes(["D3/8", "F3/8", "G3/8"], 250)


ev3 = EV3Brick()

# Initialization of Motors and Sensors

leftMotor = Motor(port = Port.B, positive_direction = Direction.CLOCKWISE)
rightMotor = Motor(port = Port.C, positive_direction = Direction.CLOCKWISE)
bump = TouchSensor(port = Port.S2)
us = UltrasonicSensor(port = Port.S4)

# Wait until center button press to move

wait_for_button()

run_motors(leftMotor, 180, rightMotor, 180)
ev3.speaker.beep()

while (not bump.pressed()):
    pass

stop_motors(leftMotor, rightMotor)
stop_motors(leftMotor, rightMotor)
wait(500)

# Turn to face the wall
run_motors(leftMotor, -50, rightMotor, -150)
wait(3200)

stop_motors(leftMotor, rightMotor)
stop_motors(leftMotor, rightMotor)
ev3.speaker.beep()


# Wall following
dist = 225

v = 0
fast_vel = 0
slow_vel = 0
r = 0.03

stop_watch = StopWatch()
stop_watch.resume()
traveled = 0

while(traveled < 1.95):
    us_dist = us.distance()
    print(us_dist)

    if(bump.pressed()):
        stop_watch.pause()
        time = stop_watch.time() / 1000
        traveled += v*time

        stop_watch.reset()
        stop_watch.resume()
        run_motors(leftMotor, 80, rightMotor, -200)
        wait(1500)

        fast_vel = deg_to_rad(-200)
        slow_vel = deg_to_rad(80)

    stop_watch.resume()

    if (us_dist > dist):
        run_motors(leftMotor, 120, rightMotor, 180)
        fast_vel = deg_to_rad(180) * r
        slow_vel = deg_to_rad(120) * r
    elif (us_dist == dist):
        run_motors(leftMotor, 150, rightMotor, 150)
        fast_vel = deg_to_rad(150) * r
        slow_vel = deg_to_rad(150) * r
    else:
        run_motors(leftMotor, 180, rightMotor, 120)
        fast_vel = deg_to_rad(180) * r
        slow_vel = deg_to_rad(120) * r

    v = (fast_vel + slow_vel)/2
    wait(50)
    
    stop_watch.pause()

    time = stop_watch.time() / 1000
    traveled += v*time

    stop_watch.reset()
    stop_watch.resume()

stop_motors(leftMotor, rightMotor)
stop_motors(leftMotor, rightMotor)
wait(10)
stop_motors(leftMotor, rightMotor)

play_music(ev3)
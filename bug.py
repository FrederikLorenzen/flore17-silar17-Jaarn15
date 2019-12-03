import socket
import time # Import the Time library
from gpiozero import CamJamKitRobot, DistanceSensor # Import the GPIO Zero Library CamJam library

# Create a Server Socket and wait for a client to connect
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', 8080))
server_socket.listen(1)

print ("TCPServer Waiting for client on port 8080")

conn, addr = server_socket.accept()

# Define moving functions
robot = CamJamKitRobot()

# Define GPIO pins to use on the Pi
pinTrigger = 17
pinEcho = 18

sensor = DistanceSensor(echo=pinEcho, trigger=pinTrigger)

old_timeout = conn.gettimeout()

while 1:
        try:

                def GETDIST():
                        if not sensor.distance:
                                conn.send('Not able to get distance')
                        else:
                                conn.send('Distance = ' + str(sensor.distance*100))

                def GETMOTORS():
                        conn.send('Leftmotor = ' + str(robot.value[0]) + ' Rightmotor = ' + str(robot.value[1]))

                def START():
                        time.sleep(0.5)
                        if sensor.distance*100 < 15:
                                motorforward = (0.4, 0.3)
                                robot.value = motorforward
                        elif sensor.distance*100 > 17:
                                motorforward = (0.3, 0.4)
                                robot.value = motorforward
                        else:
                                motorforward = (0.4,0.4)
                                robot.value = motorforward

                def STOP():
                        motorforward = (0, 0)
                        robot.value = motorforward

                loopData = 'init'

                while True:

                        if 'start' in loopData:
                                conn.settimeout(0.3)
                                try:
										dataFromClient = conn.recv(1024)
                                except socket.timeout:
										pass
						else:
								try:
										dataFromClient = conn.recv(1024)
								except socket.timeout:
										pass

						if not dataFromClient:
								pass
                        else:

                                if 'getdist' in dataFromClient:
                                        GETDIST()
                                        dataFromClient = loopData
                                elif 'getmotors' in dataFromClient:
                                        GETMOTORS()
                                        dataFromClient = loopData
                                elif 'start' in loopData or 'start' in dataFromClient:
                                        loopData = dataFromClient
                                        START()
								elif 'exit' in dataFromClient:
										print("Exiting")
										conn.close()
										exit()
                                else:
                                        STOP()
										loopData = 'stop'
										conn.settimeout(old_timeout)

        # If you press CTRL+C, cleanup and stop
        except KeyboardInterrupt:
                print("Exiting")
                conn.close()

Portfolio Two by Group 15 - static ip 192.168.99.15
Flore17 - Silar17 - Jaarn15

The solution makes use of the CamJamKitPobot, DistanceSenser, socket and time libraries.
The "python" and the "python gpiozero" packages need to be installed.

Run the program by executing "python bug.py".

This solution opens a TCP-server listening for inputs on port 8080.

Det data received is put in to dataFromClient.

The following commands are allowed:
getdist - returns the distance measured by the distance sensor.
getmotors - returns the set motor value of each motors.
start - starts the wall following program.
stop - stops the wall following program.
exit - closes the TCP-connection and exits the program.

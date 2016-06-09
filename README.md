# IOTPlant

This is a IOT project that utilzes the BeagleBone Black (BBB) microcomputer to collect and upload data to
remotely monitor a plant. The sensors used were the following: soil moisture sensor, Temperature/Pressure sensor,
LDR (light detection), and a logitech USB camera. All data except the picture was uploaded to a public Sparkfun data stream but
the picture was uploaded to a google drive account. The data was collected at the turn of the hour and pushed to the internet.

# To Run

The code was written using the cloud9 IDE on the BBB and the workspace used for the project was "/var/lib/cloud9". If a different path
is used, references to this in the python file and elsewhere need to be replaced with the used path.

Files:

	* data_daemon.py - This is the python program that has to run in the background on the BBB. This is done through the
	                   use of crontab. To invoke crontab run "sudo crontab -e", then append this 
					   "0 * * * * python /var/lib/cloud9/data_daemon.py" to the file to run on top of the hour. Now this 
					   program is executed automatically when the time conditions are met.
	* Photos - This folder is used to log and save uploaded photos locally.
	* client_secrets.json - This was obtained from the Google App Engine and is needed to verify the python application with google servers.
	* mycreds.txt - This file is created after the first login by user to their google account and contains credentials to authorize
	                subsequent acceses to gdrive to upload photos. Note: Initially data_daemon.py has to be tun manually from command line,
					this is because the google login process cannot be completely automated. In this first run a url is provided on the cmdline, 
					entering this url in the browser leads to a google login page for the user to enter into their google account which then creates
					mycreds.txt. Now data_daemon can be run in the background through crontab.
					
Referenced information from http://www.raspberrypi-spy.co.uk/2015/04/bmp180-i2c-digital-barometric-pressure-sensor/ for usage of BMP180.
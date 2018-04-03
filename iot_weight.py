import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711
import smtplib
from email.mime.text import MIMEText

def cleanAndExit():     #clean and exit : gets called when program terminates
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()

hx = HX711(5,6)     #assigning GPIO pin 5 and 6 to the hx711 module

hx.set_reading_format("LSB", "MSB")     #setting the reading format. More info in example.py of hx711 library

hx.set_reference_unit(1274)     #set the reference to calibrate the load cell

hx.reset()
hx.tare()
threshold = 30      #threshold value/minimum weight
flag = 0

while True:
    try:
        val = hx.get_weight(5)      
        print val       #for debugging purpose. can be removed from the final code

        if (val < threshold and flag == 0):
            #use mailgun's SMTP function to send email.
            #code can be replaced to suite your need
            msg = MIMEText('Testing some Mailgun awesomness')
            msg['Subject'] = "Hello"
            msg['From']    = "foo@YOUR_DOMAIN_NAME"
            msg['To']      = "bar@example.com"
            s = smtplib.SMTP('smtp.mailgun.org', 587)
            s.login('postmaster@YOUR_DOMAIN_NAME', '3kh9umujora5')
            s.sendmail(msg['From'], msg['To'], msg.as_string())
            s.quit()

            flag = 1
            print("mail sent")      #just for debugging. Can be removed from the final code
            time.sleep(0.5)

        if (val > threshold):
            flag = 0
        
        else:
            continue

            
        hx.power_down()
        hx.power_up()

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
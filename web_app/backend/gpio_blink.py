import time
import RepkaPi.GPIO as GPIO

# https://repka-pi.ru/blog/post/45
# sudo apt-get install python3-dev python3-setuptools git
# git clone https://gitflic.ru/project/repka_pi/repkapigpiofs.git
# cd repkapigpiofs
# sudo python3 setup.py install

GPIO.setmode(GPIO.BOARD)

print(GPIO.getboardmodel(), GPIO.VERSION, GPIO.RPI_INFO)



# Define GPIO pins
LED_PIN = 18
BUTTON_PIN = 16

# Set up the LED pin as an output
GPIO.setup(LED_PIN, GPIO.OUT)

# Set up the button pin as an input with pull-up resistor
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    i = 0
    while True:
        i += 1
        # Read the button state
        button_state = GPIO.input(BUTTON_PIN)
        
        if button_state == GPIO.LOW:  # Button is pressed
        #if i % 2 == 0:
            print("Button Pressed! Turning LED ON.")
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED ON
        else:
            print("Button Released! Turning LED OFF.")
            GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED OFF
        
        time.sleep(0.5)  # Small delay to debounce

except KeyboardInterrupt:
    print("Exiting program.")

finally:
    GPIO.cleanup()  # Clean up GPIO settings
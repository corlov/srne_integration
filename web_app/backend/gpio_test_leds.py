import time
import RepkaPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
print(GPIO.getboardmodel(), GPIO.VERSION, GPIO.RPI_INFO)

GPIO.setup(22, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)


try:
    i = 0
    while True:
        i += 1
        if i % 2 == 0:
            GPIO.output(22, GPIO.LOW)
            GPIO.output(24, GPIO.LOW)
            GPIO.output(26, GPIO.LOW)
        else:
            GPIO.output(22, GPIO.HIGH)
            GPIO.output(24, GPIO.HIGH)
            GPIO.output(26, GPIO.HIGH)

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program.")

finally:
    GPIO.cleanup()  # Clean up GPIO settings
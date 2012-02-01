/*
  Code to run on an arduino that will monitor the serial feed from a computer.
  If the character C is sent to the arduino, it will turn the motor 1 degree clockwise
  If the character c is sent to the arduino, it will turn the motor 1 degree counterclockwise
  
  Circuit:
  *servo attached to inputs 13, ground, and 5V
  
  by, Matt Maclean
*/
#include <Servo.h> 

Servo myservo;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created
                
int pos = 90; // variable to store the servo position

int val; // Value read from the serial port


void setup()
{
    Serial.begin(9600);
    Serial.flush();
    myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
}

void loop()
{
    // Read from serial port
    if (Serial.available())
    {
        //myservo.attach(9);  //might want to attach and detach at the end of every movement
        val = Serial.read();
        Serial.println(val, BYTE);
        if (val == 99) //99 = c in dec (aka counterclockwise)
        {
            pos -= 1;
        }
        else if (val == 67) //67 = C in dec (aka clockwise)
        {
            pos += 1;
        }
        myservo.write(pos);              // tell servo to go to position in variable 'pos' 
        //myservo.detach(); //detaches the servo on pin 9 to prevent buzzing
    }
}

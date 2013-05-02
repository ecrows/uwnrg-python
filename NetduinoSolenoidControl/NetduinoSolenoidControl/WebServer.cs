/* HTTP Server running on Netduino to service 
 * commmands from python module. */

using System;
using System.Net.Sockets;
using System.Net;
using System.Threading;
using System.Text;
using Microsoft.SPOT.Hardware;
using SecretLabs.NETMF.Hardware.Netduino;
using Microsoft.SPOT;

namespace NetduinoSolenoidControl
{
    public class WebServer : IDisposable
    {
        private double desired_current = 2;
    
        private Socket socket = null;
        private const int MaximumValue = 1023;
        private const double AnalogReference = 3.3f;
        private const double SENSOR_RESISTANCE = 0.5;
        private double CURRENT_THRESHOLD = 0.1;

        private double pwm_val = 0.5;
        private double pwm_right_val = 0.5;
        private double pwm_left_val = 0.5;
        private double pwm_top_val = 0.5;
        private double pwm_bot_val = 0.5;

        private PWM pwm_top;
        private PWM pwm_bot;
        private PWM pwm_right;
        private PWM pwm_left;
        private PWM pwm_led;

        private AnalogInput adcPort;
        private AnalogInput adc_top;
        private AnalogInput adc_bot;
        private AnalogInput adc_right;
        private AnalogInput adc_left;
        
        private OutputPort sol_under = new OutputPort(Pins.GPIO_PIN_D4, false);
        
        public WebServer()
        {
            this.pwm_top = new PWM(PWMChannels.PWM_PIN_D5, 10000, 1.0, false);
            this.pwm_bot = new PWM(PWMChannels.PWM_PIN_D9, 10000, 1.0, false);
            this.pwm_right = new PWM(PWMChannels.PWM_PIN_D6, 10000, 1.0, false);
            this.pwm_left = new PWM(PWMChannels.PWM_PIN_D10, 10000, 1.0, false);
            this.pwm_led = new PWM(PWMChannels.PWM_ONBOARD_LED, 100, 1.0, false);

            this.pwm_top.Start();
            this.pwm_bot.Start();
            this.pwm_right.Start();
            this.pwm_left.Start();
            this.pwm_led.Start();

            this.pwm_top.DutyCycle = 0;
            this.pwm_bot.DutyCycle = 0;
            this.pwm_right.DutyCycle = 0;
            this.pwm_left.DutyCycle = 0;

            this.adcPort = new AnalogInput(AnalogChannels.ANALOG_PIN_A0);
            this.adc_top = new AnalogInput(AnalogChannels.ANALOG_PIN_A1); //PWM5
            this.adc_bot = new AnalogInput(AnalogChannels.ANALOG_PIN_A2); //PWM6
            this.adc_right = new AnalogInput(AnalogChannels.ANALOG_PIN_A3); //PWM9
            this.adc_left = new AnalogInput(AnalogChannels.ANALOG_PIN_A4); //PWM10
            /*adcPort = new AnalogInput(Pins.GPIO_PIN_A0);
            adc_top = new AnalogInput(Pins.GPIO_PIN_A1); //PWM5
            adc_bot = new AnalogInput(Pins.GPIO_PIN_A2); //PWM6
            adc_right = new AnalogInput(Pins.GPIO_PIN_A3); //PWM9
            adc_left = new AnalogInput(Pins.GPIO_PIN_A4); //PWM10*/
            
            //Initialize Socket class
            socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            //Request and bind to an IP from DHCP server
            socket.Bind(new IPEndPoint(IPAddress.Any, 80));
            //Debug print our IP address
            Debug.Print(Microsoft.SPOT.Net.NetworkInformation.NetworkInterface.GetAllNetworkInterfaces()[0].IPAddress);
            //Start listening for web requests
            socket.Listen(10);
            ListenForRequest();
        }

        public void ListenForRequest()
        {
            while (true)
            {
                using (Socket clientSocket = socket.Accept())
                {
                    //Get clients IP
                    IPEndPoint clientIP = clientSocket.RemoteEndPoint as IPEndPoint;
                    EndPoint clientEndPoint = clientSocket.RemoteEndPoint;
                    //int byteCount = cSocket.Available;
                    int bytesReceived = clientSocket.Available;
                    if (bytesReceived > 0)
                    {
                        //Get request
                        byte[] buffer = new byte[bytesReceived];
                        int byteCount = clientSocket.Receive(buffer, bytesReceived, SocketFlags.None);
                        string request = new string(Encoding.UTF8.GetChars(buffer));
                        Debug.Print(request);
                        
                        string response = "";
                        
                        //Blink the onboard
                        string[] words = request.Split(' ');

                        if (words[1] == "1")
                        {
                            if (words[0] == "OFF")
                            {
                                this.pwm_top.DutyCycle = 0;
                            }
                            else if (words[0] == "ON")
                            {
                                //adjust_pwm(ref this.pwm_top, ref this.pwm_top_val);
                                adjust_pwm(ref this.pwm_top, ref this.adc_top, ref this.pwm_top_val);
                            }
                            
                            response = this.pwm_top_val.ToString();
                        }
                        else if (words[1] == "2")
                        {
                            if (words[0] == "OFF")
                            {
                                this.pwm_bot.DutyCycle = 0.0; 
                            }
                            else if (words[0] == "ON")
                            {
                                //adjust_pwm(ref this.pwm_bot, ref this.pwm_bot_val);
                                adjust_pwm(ref this.pwm_bot, ref this.adc_bot, ref this.pwm_bot_val);
                            }
                            
                            response = this.pwm_bot_val.ToString();
                        }
                        else if (words[1] == "3")
                        {
                            if (words[0] == "OFF")
                            { 
                                this.pwm_left.DutyCycle = 0.0;
                            }
                            else if (words[0] == "ON")
                            {
                                //adjust_pwm(ref this.pwm_left, ref this.pwm_left_val);
                                adjust_pwm(ref this.pwm_left, ref this.adc_left, ref this.pwm_left_val);
                            }
                            
                            response = this.pwm_left_val.ToString();
                        }
                        else if (words[1] == "4")
                        {
                            if (words[0] == "OFF")
                            {
                                this.pwm_right.DutyCycle = 0.0;
                            }
                            else if (words[0] == "ON")
                            {
                                //adjust_pwm(ref this.pwm_right, ref this.pwm_right_val);
                                adjust_pwm(ref this.pwm_right, ref this.adc_right, ref this.pwm_right_val);
                            }
                            
                            response = this.pwm_right_val.ToString();
                        }
                        else if (words[1] == "5") //brake   
                        {
                            if (words[0] == "OFF")
                            {
                                sol_under.Write(false);
                            }
                            else if (words[0] == "ON")
                            {
                                sol_under.Write(true);
                            }
                        }/*
                        else if (words[1] == "INCREMENT")
                        {
                            if (pwm_val + 0.10 <= 1.0)
                            {
                                pwm_val += 0.10;
                            }
                            else
                            {
                                pwm_val = 1.0;
                            }
                            pwm_led.DutyCycle = pwm_val;
                        }
                        else if (words[1] == "DECREMENT")
                        {
                            if (pwm_val - 0.10 >= 0.0)
                            {
                                pwm_val -= 0.10;
                            }
                            else
                            {
                                pwm_val = 0.0;
                            }
                            pwm_top_val = pwm_val;
                            pwm_bot_val = pwm_val;
                            pwm_right_val = pwm_val;
                            pwm_left_val = pwm_val;
                            pwm_led.DutyCycle = pwm_val;
                        }*/
                        else if (words[1] == "INCREMENT")
                        {
                            this.desired_current += 0.10;
                            
                            response = this.desired_current.ToString();
                        }
                        else if (words[1] == "DECREMENT")
                        {
                            this.desired_current -= 0.10;
                            
                            response = this.desired_current.ToString();
                        }
                        else if (words[1] == "GETVOLTAGE")
                        {
                            /*double current = get_current(this.adcPort);
                            
                            response = current.ToString();*/
                            response = "a";
                        }
                        
                        //Compose a response
                        string header = "HTTP/1.0 200 OK\r\nContent-Type: text; charset=utf-8\r\nContent-Length: " + response.Length.ToString() + "\r\nConnection: close\r\n\r\n";
                        clientSocket.Send(Encoding.UTF8.GetBytes(header), header.Length, SocketFlags.None);
                        clientSocket.Send(Encoding.UTF8.GetBytes(response), response.Length, SocketFlags.None);
                    }
                }
            }
        }

        #region IDisposable Members
        ~WebServer()
        {
            Dispose();
        }

        //private void adjust_pwm(ref PWM pwm, ref double pwm_val){
        private void adjust_pwm(ref PWM pwm, ref AnalogInput adc, ref double pwm_val){
            pwm.DutyCycle = pwm_val;
            
            int temp = 0;
            double current_voltage = 0;
            
            while (temp++ < 10 && current_voltage <= 0){
                current_voltage = get_voltage(adc);
            }

            Debug.Print(current_voltage.ToString());
            
            if (current_voltage > 0){
                temp = 0;
                while (!(this.get_current(current_voltage) > this.desired_current - this.CURRENT_THRESHOLD && this.get_current(current_voltage) < this.desired_current + this.CURRENT_THRESHOLD) && temp++ < 10){
                    double desired_voltage = this.desired_current * SENSOR_RESISTANCE;
                    
                    double factor = desired_voltage / current_voltage;
                    
                    pwm_val *= factor;
                    
                    if (pwm_val > 1){
                        pwm_val = 1;
                    }
                    
                    
                    pwm.DutyCycle = pwm_val;
                }
            }
        }
            
        private double get_voltage(AnalogInput input){
            // read a digital value from the ADC
            double digitalValue = input.Read();

            // convert digital value to analog voltage value
            return digitalValue * AnalogReference;
        }

        private double get_current(AnalogInput input){
            double analogValue = get_voltage(input);

            return analogValue / SENSOR_RESISTANCE;
        }

        private double get_current(double voltage){
            return voltage / SENSOR_RESISTANCE;
        }
         
        public void Dispose()
        {
            if (socket != null)
                socket.Close();
        }
        #endregion
    }
}


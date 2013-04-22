/* HTTP Server running on Netduino to service 
 * commmands from python module. */

using System;
using Microsoft.SPOT;
using System.Net.Sockets;
using System.Net;
using System.Threading;
using System.Text;
using Microsoft.SPOT.Hardware;
using SecretLabs.NETMF.Hardware.Netduino;

namespace NetduinoSolenoidControl
{
    public class WebServer : IDisposable
    {
        private Socket socket = null;
        double pwm_val = 1.0;

        PWM pwm_top = new PWM(PWMChannels.PWM_PIN_D5, 10000, 1.0, false);
        PWM pwm_bot = new PWM(PWMChannels.PWM_PIN_D6, 10000, 1.0, false);
        PWM pwm_right = new PWM(PWMChannels.PWM_PIN_D9, 10000, 1.0, false);
        PWM pwm_left = new PWM(PWMChannels.PWM_PIN_D10, 10000, 1.0, false);
        PWM pwm_led = new PWM(PWMChannels.PWM_ONBOARD_LED, 100, 1.0, false);

        private OutputPort sol_under = new OutputPort(Pins.GPIO_PIN_D4, false);
        
        public WebServer()
        {
            pwm_top.Start();
            pwm_bot.Start();
            pwm_right.Start();
            pwm_left.Start();
            pwm_led.Start();
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

                        //Compose a response
                        string response = "(\\/)(^,,,^)(\\/)"; //Zoidberg
                        string header = "HTTP/1.0 200 OK\r\nContent-Type: text; charset=utf-8\r\nContent-Length: " + response.Length.ToString() + "\r\nConnection: close\r\n\r\n";
                        clientSocket.Send(Encoding.UTF8.GetBytes(header), header.Length, SocketFlags.None);
                        clientSocket.Send(Encoding.UTF8.GetBytes(response), response.Length, SocketFlags.None);
                        
                        //Blink the onboard
                        string[] words = request.Split(' ');

                        if (words[1] == "1")
                        {
                            if (words[0] == "OFF")
                            {                                
                                pwm_top.DutyCycle = 0;                                
                            }
                            else if (words[0] == "ON")
                            {                             
                                pwm_top.DutyCycle = pwm_val;                              
                            }
                        }
                        else if (words[1] == "2")
                        {
                            if (words[0] == "OFF")
                            {                                                                
                                pwm_bot.DutyCycle = 0.0;                                
                            }
                            else if (words[0] == "ON")
                            {
                                pwm_bot.DutyCycle = pwm_val;                             
                            }
                        }
                        else if (words[1] == "3")
                        {
                            if (words[0] == "OFF")
                            {                                
                                pwm_left.DutyCycle = 0.0;                                
                            }
                            else if (words[0] == "ON")
                            {                                
                                pwm_left.DutyCycle = pwm_val;                              
                            }
                        }
                        else if (words[1] == "4")
                        {
                            if (words[0] == "OFF")
                            {
                                pwm_right.DutyCycle = 0.0;
                            }
                            else if (words[0] == "ON")
                            {
                                pwm_right.DutyCycle = pwm_val;
                            }
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
                        }
                        else if (words[1] == "INCREMENT")
                        {
                            if (pwm_val+0.10 <= 1.0)
                            {
                                pwm_val += 0.10;
                            }
                            else
                                pwm_val = 1.0;

                            pwm_led.DutyCycle = pwm_val;
                        }
                        else if (words[1] == "DECREMENT")
                        {
                            if (pwm_val-0.10 >= 0.0)
                            {
                                pwm_val -= 0.10;
                            }
                            else
                                pwm_val = 0.0;

                            pwm_led.DutyCycle = pwm_val;
                        }
                    }
                }
            }
        }
        #region IDisposable Members
        ~WebServer()
        {
            Dispose();
        }
        public void Dispose()
        {
            if (socket != null)
                socket.Close();
        }
        #endregion
    }
}


using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using Microsoft.SPOT;
using Microsoft.SPOT.Hardware;
using SecretLabs.NETMF.Hardware;
using SecretLabs.NETMF.Hardware.Netduino;
using System.IO;
using System.Text;
using System.IO.Ports;

namespace NetduinoSolenoidControl
{
    public class Program
    {
        public static void Main()
        {
            var interf = Microsoft.SPOT.Net.NetworkInformation.NetworkInterface.GetAllNetworkInterfaces()[0];
            interf.EnableStaticIP("10.0.0.32", "255.255.255.0", "0.0.0.0");
            WebServer webServer = new WebServer();
            webServer.ListenForRequest();
        }
    }
}

using System;
using System.Collections.Generic;

namespace UWNRG_2011
{
    public class VirtualField
    {
        //Number of actuators, this doesn't really do anything right now since I only have the linear stage
        //int actuator_number = 9000;

        //Default resolution is 1000, doesn't really matter though 
        double X_resolution = 20; //Specify the number of equally spaced 'nodes' there are in the X dimension
        double Y_resolution = 20; //Specify the number of equally spaced 'nodes' there are in the Y dimension

        //Specify the length of the width/length (x/y) of how far you want the stage can go (
        //Corresponds with the X dimension - MAX is 131327)
        double wall_width = 131327;
        double wall_length = 131327;

        //Specifies whether the linear actuators are connected or not.
        private bool connected;
        public bool ActuatorsConnected
        {
            get { return connected; }
            set { connected = value; }
        }

        //Zaber Variables
        private ZaberPortFacade portFacade;
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.BindingSource conversationViewBindingSource;
        private String responses;

        public VirtualField()
        {
            Debug.WriteLine("[DEBUG] Virtual Grid Loading");
            int[,] virtual_grid = new int[int.Parse(X_resolution.ToString()), int.Parse(Y_resolution.ToString())];
            clearField(virtual_grid);
            writeMap(virtual_grid);
            //Assigns 1 to the top left corner of the grid (an indicator for where the robot is)
            virtual_grid[0, 0] = 1;
            Point robo_position = new Point(0, 0);

            //Initilize Zaber
            CreatePortFacade();
            ClearMessages();
            this.connected = false;

            ZaberDevice allDevices = portFacade.GetDevice(0);
            this.components = new System.ComponentModel.Container();
            this.conversationViewBindingSource = new System.Windows.Forms.BindingSource(this.components);
            ((System.ComponentModel.ISupportInitialize)(this.conversationViewBindingSource)).BeginInit();
            allDevices.MessageReceived +=
                new EventHandler<DeviceMessageEventArgs>(allDevices_MessageReceived);
            allDevices.MessageSent +=
                new EventHandler<DeviceMessageEventArgs>(allDevices_MessageSent);
        }

        /*-------------------------------------------------------
        * 
        * Methods for the stage written by Elwin
        * 
        --------------------------------------------------------*/

        /*This method moves the stage relative to its current position by X by Y cells
         */
        public void moveRelative(int pass_cell_width, int pass_cell_length)
        {
            var x_convo = portFacade.GetConversation(1);
            var y_convo = portFacade.GetConversation(2);
            var topic = x_convo.StartTopic();
            x_convo.Device.Send(Command.MoveRelative, pass_cell_width, topic.MessageId);
            y_convo.Request(Command.MoveRelative, pass_cell_length);
            topic.Wait();

            //conversation.Request(Command.MoveRelative, 50000);
            //portFacade.GetConversation(1).Request(Command.MoveRelative, -distance);
        }

        /*This method moves the stage recursively using a pass array of points where the X and Y
         * is the passed direction to go to
         */
        public void moveArray(Point[] passed_pointArray)
        {
            var x_convo = portFacade.GetConversation(1);
            var y_convo = portFacade.GetConversation(2);
            var topic = x_convo.StartTopic();

            double temp_double_x = 0;// = (passed_pointArray[0].X / X_resolution) * wall_width;
            double temp_double_y = 0;//= (passed_pointArray[0].Y / Y_resolution) * wall_length;
            int temp_int_x = 0;// = (passed_pointArray[0].X / X_resolution) * wall_width;
            int temp_int_y = 0;//= (passed_pointArray[0].Y / Y_resolution) * wall_length;

            for (var i = 0; i < passed_pointArray.GetLength(0); i++)
            {
                temp_double_x = (double.Parse(passed_pointArray[i].X.ToString()) / X_resolution) * wall_width;
                temp_double_y = (double.Parse(passed_pointArray[i].Y.ToString()) / Y_resolution) * wall_length;

                temp_int_x = int.Parse(Math.Round(temp_double_x).ToString());
                temp_int_y = int.Parse(Math.Round(temp_double_y).ToString());

                topic = x_convo.StartTopic();
                x_convo.Device.Send(Command.MoveRelative, temp_int_x, topic.MessageId);
                y_convo.Request(Command.MoveRelative, temp_int_y);
                topic.Wait();
                //topic.Validate();
            }
        }

        /*This method moves the stage to the specified point.
         *I need Matt's algorithm for this because it'll need to be able to dodge obstacles. If it wants to move to a specific point
         */
        public void moveAbsolute(int x_cell_position, int y_cell_position)
        {

        }

        /*This method injects a node into the specified objects 
         *(ids: 0 = empty, 1 = robot, 2 = obstacle, 3 = special object) or whatever you want it to be.
         *Passes the virtual grid, the x position, the y position, and the id number
         */
        public void insertNode(int[,] pass_virtual_grid, int x_cell, int y_cell, int id_type)
        {
            pass_virtual_grid[x_cell, y_cell] = id_type;
        }

        /*This method clears the field with empty nodes map ids (id for empty node = 0)
         *Passes the virtual grid into the method 
         */
        public void clearField(int[,] pass_virtual_grid)
        {
            for (var i = 0; i < pass_virtual_grid.GetLength(0); i++)
            {
                for (var j = 0; j < pass_virtual_grid.GetLength(1); j++)
                {
                    pass_virtual_grid[i, j] = 0;
                }
            }
        }

        /*This field outputs a really basic shape of the map
         *Mainly for testing purposes. Passes the virtual grid into the method
         */
        public string writeMap(int[,] pass_virtual_grid)
        {
            string map = "";
            for (var j = 0; j < pass_virtual_grid.GetLength(1); j++)
            {
                for (var i = 0; i < pass_virtual_grid.GetLength(0); i++)
                {
                    map += pass_virtual_grid[i, j];
                }

                map += "\n";
            }

            return map;
        }
        // End of Methods that I (Elwin) wrote


        /* Some Zaber functions, modified by Garry Ng to support a Non-Form structure with some useful new methods added. */

        /// <summary>
        /// Create a ZaberPortFacade object, and wire up all its dependencies.
        /// </summary>
        /// <remarks>
        /// This is what replaces the Spring configuration. You lose a couple 
        /// of things that are only in the Spring configuration: a list of
        /// all the device types with their names and ids, as well as a list
        /// of all the commands with help text.
        /// </remarks>
        private void CreatePortFacade()
        {
            var packetConverter = new PacketConverter();
            packetConverter.MillisecondsTimeout = 50;
            var defaultDeviceType = new DeviceType();
            defaultDeviceType.Commands = new List<CommandInfo>();
            portFacade = new ZaberPortFacade();
            portFacade.DefaultDeviceType = defaultDeviceType;
            portFacade.QueryTimeout = 1000;
            portFacade.Port = new TSeriesPort(new SerialPort(), packetConverter);
            portFacade.DeviceTypes = new List<DeviceType>();
        }

        /* This is just a sample array for the linear stage to work with (the passedArray parameter)
            Point[] passedArray = new Point[10];
            passedArray[0] = new Point( 5,  10); */
        private void RunScript(Conversation conversation, Point[] passedArray)
        {
            conversation.Request(Command.Home);
            moveArray(passedArray);
        }

        private void LogMessage(string message)
        {
            responses += message;
        }

        public void ClearMessages()
        {
            responses = "";
        }

        public string GetLog()
        {
            return responses;
        }

        public string[] getPortNames()
        {
            return (portFacade.GetPortNames());
        }

        public void openPort(String portText)
        {
            if (portText.Length > 0)
            {
                try
                {
                    portFacade.Open(portText);
                    Thread.Sleep(1000);

                    foreach (Conversation conversation in portFacade.Conversations)
                    {
                        conversationViewBindingSource.Add(new ConversationView(conversation));
                    }
                    LogMessage("Successfully connected to " + portText + ".\n");
                    this.connected = true;
                }
                catch (LoopbackException)
                {
                    LogMessage("Loopback Connection detected.\n");
                }
                catch (Exception err)
                {
                    LogMessage("Unknown Exception detected. The error was as follows: " + err + "\n");
                }
                this.connected = false;
            }
        }

        public void close_Port()
        {
            portFacade.Close();
            conversationViewBindingSource.Clear();
            LogMessage("Port bindings cleared.\n");
            this.connected = false;
        }


        public void request_Stop()
        {
            CurrentConversation.Request(Command.Stop);
        }


        void allDevices_MessageSent(object sender, DeviceMessageEventArgs e)
        {
            LogMessage(String.Format("Device {0} sent {1}({2})\n",
                e.DeviceMessage.DeviceNumber,
                e.DeviceMessage.Command,
                e.DeviceMessage.Data,
                e.DeviceMessage.MessageId));
        }

        void allDevices_MessageReceived(object sender, DeviceMessageEventArgs e)
        {
            LogMessage(String.Format("Device {0} received {1}({2})\n",
                e.DeviceMessage.DeviceNumber,
                e.DeviceMessage.Command,
                e.DeviceMessage.Data,
                e.DeviceMessage.MessageId));
        }

        private Conversation CurrentConversation
        {
            get
            {
                ConversationView conversationView =
                  (ConversationView)conversationViewBindingSource.Current;
                return conversationView.Conversation;
            }
        }
    }
}

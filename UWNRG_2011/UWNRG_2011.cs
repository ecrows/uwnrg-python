/*Namespace: UWNRG_2011
 *Programmer: Garry Ng
 *Last Updated: 
 *Description: Contains main GUI, image and video recording functions as well as deviec connectioni interface. Based
 *on the IC Control .NET 2008 template provided.*/
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Threading;
using System.Windows.Forms;

namespace UWNRG_2011
{
    public partial class UWNRG_2011 : Form
    {
        //Extra Forms
        SaveFileDialog saveFileDialog1;
        WriteAvi aviForm;
        AboutPage aboutForm;
        ActuatorSettings actuatorForm;

        private delegate void DeviceLostDelegate();
        private delegate void ShowBufferDelegate(TIS.Imaging.ImageBuffer buffer);

        //Virtual Field Controller
        private VirtualField vfield;

        //Mode
        private int currentMode = 0;

        //Key Step Size (when you press)
        const int keyStepSize = 2500;

        public UWNRG_2011()
        {
            InitializeComponent();

            try
            {
                UpdateSystemLog("Virtual Grid loading...\n");
                //Initilize virtual field
                vfield = new VirtualField();
                UpdateSystemLog("Virtual Grid loaded successfully.\n");
            }
            catch (Exception err)
            {
                UpdateSystemLog("Virtual Grid failed to load...\nError as follows:\n" + err);
            }

            //Key Event Handler
            this.KeyPress += new KeyPressEventHandler(this.UWNRG_2011_KeyPress);

            // Update the menu and toolbar controls.
            UpdateControls();
        }

        /// <summary>
        /// Load ICImaging video setting files.
        /// </summary>
        private void UWNRG_Load(object sender, EventArgs e)
        {
            // Try to load the previously used device. 
            try
            {
                //icImagingControl1.LoadDeviceStateFromFile("device.xml", true);
            }
            catch
            {
                // Either the xml file does not exist or the device
                // could not be loaded. In both cases we do nothing and proceed.
                imageControlSettingsToolStripMenuItem.Enabled = false;
            }

            // Update the menu and toolbar controls.
            UpdateControls();
        }

        /// <summary>
        /// Handles the application closing by stopping the live video stream and doing cleanup operations.
        /// </summary>
        private void UWNRG_FormClosing(object sender, FormClosingEventArgs e)
        {
            //if (icImagingControl1.DeviceValid)
            //{
            //    icImagingControl1.LiveStop();
            //}
        }

        /// <summary>
        /// Show the device selection dialog of IC Imaging Control.
        /// </summary>
        private void OpenNewVideoCaptureDevice()
        {

            /**if (icImagingControl1.DeviceValid)
            {
                icImagingControl1.LiveStop();
            }
            else
            {
                icImagingControl1.Device = "";
            }*/
            UpdateControls(); // Disable the controls.

            /**icImagingControl1.ShowDeviceSettingsDialog();
            if (icImagingControl1.DeviceValid)
            {
                // Save the currently used device into a file in order to be able to open it
                // automatically at the next program start.
                icImagingControl1.SaveDeviceStateToFile("device.xml");
                // Enable the menu and toolbar controls.
                UpdateControls();
            }*/
        }

        /// <summary>
        /// Start the live video and update the state of the start/stop button.
        /// </summary>
        private void StartLiveVideo()
        {
            //icImagingControl1.LiveStart();
            UpdateControls();
        }

        /// <summary>
        /// Stop the live video and update the state of the start/stop button.
        /// </summary>
        private void StopLiveVideo()
        {
            //icImagingControl1.LiveStop();
            UpdateControls();
        }

        /// <summary>
        /// Show the device's property dialog for exposure, brightness etc. The 
        /// changes that were made using the dialog are saved to the file 'device.xml'.
        /// </summary>
        private void ShowDeviceProperties()
        {
           // if (icImagingControl1.DeviceValid == true)
            //{
                //icImagingControl1.ShowPropertyDialog();
                //icImagingControl1.SaveDeviceStateToFile("device.xml");
            //}
        }

        /// <summary>
        /// Update the controls in the toolbar and the menu, according to the camera device state.
        /// </summary>
        public void UpdateControls()
        {
            /**imageControlSettingsToolStripMenuItem.Enabled = icImagingControl1.DeviceValid;
            if (icImagingControl1.DeviceValid)
            {
                startLiveFeedToolStripMenuItem.Enabled = !icImagingControl1.LiveVideoRunning;
                stopLiveFeedToolStripMenuItem.Enabled = icImagingControl1.LiveVideoRunning;
                snapPictureToolStripMenuItem.Enabled = icImagingControl1.LiveVideoRunning;
                captureVideoToolStripMenuItem.Enabled = icImagingControl1.LiveVideoRunning;
            }
            else
            {*/
                startLiveFeedToolStripMenuItem.Enabled = false;
                stopLiveFeedToolStripMenuItem.Enabled = false;
                snapPictureToolStripMenuItem.Enabled = false;
                captureVideoToolStripMenuItem.Enabled = false;
            //}

            if (vfield != null)
            {
                //Disables mode buttons we go
                if (vfield.ActuatorsConnected)
                {
                    mode1Button.Enabled = !(currentMode == 1);
                    mode2Button.Enabled = !(currentMode == 2);
                    mode3Button.Enabled = !(currentMode == 3);
                }
                else
                {
                    currentMode = 0;
                    mode1Button.Enabled = false;
                    mode2Button.Enabled = false;
                    mode3Button.Enabled = false;
                }

                switch (currentMode)
                {
                    case 1:
                        startButton.Enabled = true;
                        stopButton.Enabled = true;
                        infiniteButton.Enabled = true;
                        upTextBox.Enabled = false;
                        downTextBox.Enabled = false;
                        leftTextBox.Enabled = false;
                        rightTextBox.Enabled = false;
                        micromobilityRunToolStripMenuItem.Enabled = true;
                        microassemblyRunToolStripMenuItem.Enabled = true;
                        presetToolStripMenuItem1.Enabled = true;
                        UpdateSystemLog("Mode 1 Active...\n");
                        break;
                    case 2:
                        manualGoButton.Enabled = true;
                        upTextBox.Enabled = true;
                        downTextBox.Enabled = true;
                        leftTextBox.Enabled = true;
                        rightTextBox.Enabled = true;
                        startButton.Enabled = false;
                        stopButton.Enabled = false;
                        infiniteButton.Enabled = false;
                        micromobilityRunToolStripMenuItem.Enabled = false;
                        microassemblyRunToolStripMenuItem.Enabled = false;
                        presetToolStripMenuItem1.Enabled = false;
                        UpdateSystemLog("Mode 2 Active...\n");
                        break;
                    case 3:
                        upTextBox.Enabled = false;
                        downTextBox.Enabled = false;
                        leftTextBox.Enabled = false;
                        rightTextBox.Enabled = false;
                        startButton.Enabled = false;
                        stopButton.Enabled = false;
                        infiniteButton.Enabled = false;
                        manualGoButton.Enabled = false;
                        micromobilityRunToolStripMenuItem.Enabled = false;
                        microassemblyRunToolStripMenuItem.Enabled = false;
                        presetToolStripMenuItem1.Enabled = false;
                        UpdateSystemLog("Mode 3 Active...\n");
                        break;
                    default:
                        upTextBox.Enabled = false;
                        downTextBox.Enabled = false;
                        leftTextBox.Enabled = false;
                        rightTextBox.Enabled = false;
                        startButton.Enabled = false;
                        stopButton.Enabled = false;
                        infiniteButton.Enabled = false;
                        manualGoButton.Enabled = false;
                        micromobilityRunToolStripMenuItem.Enabled = false;
                        microassemblyRunToolStripMenuItem.Enabled = false;
                        presetToolStripMenuItem1.Enabled = false;
                        break;
                }
            }
        }

        /// <summary>
        /// Update the main GUI's system log.
        /// </summary>
        public void UpdateSystemLog(string log)
        {
            logTextBox.Text += log;
            logTextBox.Focus();
            logTextBox.SelectionStart = logTextBox.Text.Length;
        }

        /*-----------------------------------------------------------------------------------
         * ----------------------------------EVENT HANDLERS----------------------------------
         * ---------------------------------------------------------------------------------*/

        /// <summary>
        /// Messagehandler for the menu and the toolbar.
        /// </summary>
        private void menuItemDevice_Click(object sender, EventArgs e)
        {
            OpenNewVideoCaptureDevice();
        }

        /// <summary>
        /// Device properties for the camera.
        /// </summary>
        private void imageControlSettingsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            ShowDeviceProperties();
        }

        /// <summary>
        /// Starts video camera and shows the image on the screen.
        /// </summary>
        private void startLiveFeedToolStripMenuItem_Click(object sender, EventArgs e)
        {
            StartLiveVideo();
        }

        /// <summary>
        /// Stops video camera.
        /// </summary>
        private void stopLiveFeedToolStripMenuItem_Click(object sender, EventArgs e)
        {
            StopLiveVideo();
        }

        /// <summary>
        /// Handle the DeviceLost event.
        /// </summary>
        private void DeviceLost()
        {
            MessageBox.Show("Device Lost!");
            UpdateControls();
        }

        /// <summary>
        /// Detects it has lost connecton to the camera device.
        /// </summary>
        private void icImagingControl1_DeviceLost(object sender, TIS.Imaging.ICImagingControl.DeviceLostEventArgs e)
        {
            BeginInvoke(new DeviceLostDelegate(ref DeviceLost));
        }

        /// <summary>
        /// Terminates the application then Exit is pressed.
        /// </summary>
        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Environment.Exit(0);
        }

        /// <summary>
        /// Takes a picture from an active feed and then prompts for a file save via dialogue.
        /// </summary>
        private void snapPictureToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //icImagingControl1.MemorySnapImage();
            saveFileDialog1 = new SaveFileDialog();
            saveFileDialog1.Filter = "bmp files (*.bmp)|*.bmp|All files (*.*)|*.*";
            saveFileDialog1.FilterIndex = 1;
            saveFileDialog1.RestoreDirectory = true;

            if (saveFileDialog1.ShowDialog() == DialogResult.OK)
            {
                //icImagingControl1.MemorySaveImage(saveFileDialog1.FileName);
            }

        }

        /// <summary>
        /// Records a video from an active feed via WriteAvi dialogue.
        /// </summary>
        private void captureVideoToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //aviForm = new WriteAvi(icImagingControl1, this);
           // aviForm.Show();
        }

        /// <summary>
        /// Shows the about page.
        /// </summary>
        private void aboutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            aboutForm = new AboutPage(this);
            aboutForm.Show();
        }

        /// <summary>
        /// Shows the actuator settings page.
        /// </summary>
        private void actuatorSettingsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            actuatorForm = new ActuatorSettings(vfield, this);
            actuatorForm.Show();
        }

        /// <summary>
        /// Sets the application into Mode 1 (preset).
        /// </summary>
        private void mode1Button_Click(object sender, EventArgs e)
        {
            currentMode = 1;
            UpdateControls();
        }

        /// <summary>
        /// Sets the application into Mode 2 (manual).
        /// </summary>
        private void mode2Button_Click(object sender, EventArgs e)
        {
            currentMode = 2;
            UpdateControls();
        }

        /// <summary>
        /// Sets the application into Mode 3 (key).
        /// </summary>
        private void mode3Button_Click(object sender, EventArgs e)
        {
            currentMode = 3;
            UpdateControls();
        }

        /// <summary>
        /// Sends the manual x,y coordinate commands to the VirtualField object for movement. If both up and down inputs are detected,
        /// their difference is taken, and the same happens if both left and right inputs are detected.
        /// </summary>
        private void manualGoButton_Click(object sender, EventArgs e)
        {
            int up, down, left, right, counterclockwise, clockwise;

            if (counterclockwiseTextBox.Text == null)
            {
                counterclockwise = 0;
            }
            else
            {
                counterclockwise = int.Parse(counterclockwiseTextBox.Text);
            }
            if (clockwiseTextBox.Text == null)
            {
                clockwise = 0;
            }
            else
            {
                clockwise = int.Parse(clockwiseTextBox.Text);
            }
            clockwise = clockwise - counterclockwise;

            while (clockwise < -180)
            {
                clockwise += 360;
            }
            while (clockwise > 180)
            {
                clockwise -= 360;
            }
            vfield.rotate(clockwise);

            if (upTextBox.Text == null)
            {
                up = 0;
            }
            else
            {
                up = int.Parse(upTextBox.Text);
            }
            if (downTextBox.Text == null)
            {
                down = 0;
            }
            else
            {
                down = int.Parse(downTextBox.Text);
            }
            if (leftTextBox.Text == null)
            {
                left = 0;
            }
            else
            {
                left = int.Parse(leftTextBox.Text);
            }
            if (rightTextBox.Text == null)
            {
                right = 0;
            }
            else
            {
                right = int.Parse(rightTextBox.Text);
            }
            vfield.moveRelative((right - left), (down - up));
        }

        /// <summary>
        /// Detects the key presses and reacts if in Mode 3.
        /// </summary>
        private void UWNRG_2011_KeyPress(object sender, KeyPressEventArgs keyEvent)
        {
            if (currentMode == 3)
            {
                if (keyEvent.KeyChar == 'w')
                {
                    UpdateSystemLog("'W' was pressed.\n");
                    vfield.moveRelative(0, (-1)*keyStepSize);
                }
                if (keyEvent.KeyChar == 'd')
                {
                    UpdateSystemLog("'D' was pressed.\n");
                    vfield.moveRelative(keyStepSize, 0);
                }
                if (keyEvent.KeyChar == 's')
                {
                    UpdateSystemLog("'S' was pressed.\n");
                    vfield.moveRelative(0, keyStepSize);
                }
                if (keyEvent.KeyChar == 'a')
                {
                    UpdateSystemLog("'A' was pressed.\n");
                    vfield.moveRelative((-1) * keyStepSize, 0);
                }
                if (keyEvent.KeyChar == 'e')
                {
                    UpdateSystemLog("'E' was pressed.\n");
                    vfield.rotate(1);
                }
                if (keyEvent.KeyChar == 'q')
                {
                    UpdateSystemLog("'Q' was pressed.\n");
                    vfield.rotate(-1);
                }

            }
        } 
    }
}

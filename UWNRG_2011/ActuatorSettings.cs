using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace UWNRG_2011
{
    public partial class ActuatorSettings : Form
    {
        private UWNRG_2011 mainForm;
        private VirtualField vfield;

        public ActuatorSettings(VirtualField vfield, UWNRG_2011 mainForm)
        {
            InitializeComponent();
            this.vfield = vfield;
            this.mainForm = mainForm;
            //Get all possible port names from the vfield reference
            serialPortComboBox.Items.AddRange(vfield.getPortNames());
            if(serialPortComboBox.Items.Count > 0) {
                serialPortComboBox.SelectedIndex = 0;
            }
        }

        private void openPortButton_Click(object sender, EventArgs e)
        {
            vfield.openPort(serialPortComboBox.Text);
            logTextBox.Text += vfield.GetLog();
            logTextBox.Focus();
            logTextBox.SelectionStart = logTextBox.Text.Length;
            mainForm.UpdateSystemLog(vfield.GetLog());
            vfield.ClearMessages();
            openPortButton.Focus();
            vfield.ActuatorsConnected = true;
        }

        private void closePortButton_Click(object sender, EventArgs e)
        {
            vfield.close_Port();
            logTextBox.Text += vfield.GetLog();
            logTextBox.Focus();
            logTextBox.SelectionStart = logTextBox.Text.Length;
            mainForm.UpdateSystemLog(vfield.GetLog());
            vfield.ClearMessages();
            closePortButton.Focus();
        }

        private void closeButton_Click(object sender, EventArgs e)
        {
            //Clear the log and close the window.
            vfield.ClearMessages();
            if (vfield.ActuatorsConnected)
            {
                mainForm.UpdateControls();
            }
            this.Close();
        }
    }
}

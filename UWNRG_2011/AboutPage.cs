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
    /* Class: AboutPage
     * Programmer: Garry Ng
     * Last Updated: Feb 27th, 2010
     * Description: An about page showing the credits.*/
    public partial class AboutPage : Form
    {
        private UWNRG_2011 mainForm;

        public AboutPage(UWNRG_2011 mainForm)
        {
            this.mainForm = mainForm;
            InitializeComponent();
        }

        private void label2_Click(object sender, EventArgs e)
        {
            System.Diagnostics.Process.Start("http://uwnrg.org/");
        }

        private void closeButton_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}

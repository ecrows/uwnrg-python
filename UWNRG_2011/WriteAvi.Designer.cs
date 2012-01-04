namespace UWNRG_2011
{
    partial class WriteAvi
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.txtFilename = new System.Windows.Forms.MaskedTextBox();
            this.cboVideoCodec = new System.Windows.Forms.ComboBox();
            this.cmdShowPropertyPage = new System.Windows.Forms.Button();
            this.cmdFilename = new System.Windows.Forms.Button();
            this.cmdStopCapture = new System.Windows.Forms.Button();
            this.cmdStartCapture = new System.Windows.Forms.Button();
            this.chkPause = new System.Windows.Forms.CheckBox();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(14, 14);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(68, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Video Codec";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(14, 46);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(74, 13);
            this.label2.TabIndex = 1;
            this.label2.Text = "AVI File Name";
            // 
            // txtFilename
            // 
            this.txtFilename.Location = new System.Drawing.Point(94, 43);
            this.txtFilename.Name = "txtFilename";
            this.txtFilename.Size = new System.Drawing.Size(323, 20);
            this.txtFilename.TabIndex = 2;
            // 
            // cboVideoCodec
            // 
            this.cboVideoCodec.FormattingEnabled = true;
            this.cboVideoCodec.Location = new System.Drawing.Point(94, 11);
            this.cboVideoCodec.Name = "cboVideoCodec";
            this.cboVideoCodec.Size = new System.Drawing.Size(323, 21);
            this.cboVideoCodec.TabIndex = 3;
            this.cboVideoCodec.SelectedIndexChanged += new System.EventHandler(this.cboVideoCodec_SelectedIndexChanged);
            // 
            // cmdShowPropertyPage
            // 
            this.cmdShowPropertyPage.Location = new System.Drawing.Point(425, 9);
            this.cmdShowPropertyPage.Name = "cmdShowPropertyPage";
            this.cmdShowPropertyPage.Size = new System.Drawing.Size(75, 23);
            this.cmdShowPropertyPage.TabIndex = 4;
            this.cmdShowPropertyPage.Text = "Properties";
            this.cmdShowPropertyPage.UseVisualStyleBackColor = true;
            this.cmdShowPropertyPage.Click += new System.EventHandler(this.cmdShowPropertyPage_Click);
            // 
            // cmdFilename
            // 
            this.cmdFilename.Location = new System.Drawing.Point(425, 40);
            this.cmdFilename.Name = "cmdFilename";
            this.cmdFilename.Size = new System.Drawing.Size(75, 23);
            this.cmdFilename.TabIndex = 5;
            this.cmdFilename.Text = "Browse";
            this.cmdFilename.UseVisualStyleBackColor = true;
            this.cmdFilename.Click += new System.EventHandler(this.cmdFilename_Click);
            // 
            // cmdStopCapture
            // 
            this.cmdStopCapture.Location = new System.Drawing.Point(337, 69);
            this.cmdStopCapture.Name = "cmdStopCapture";
            this.cmdStopCapture.Size = new System.Drawing.Size(80, 23);
            this.cmdStopCapture.TabIndex = 6;
            this.cmdStopCapture.Text = "Stop Capture";
            this.cmdStopCapture.UseVisualStyleBackColor = true;
            this.cmdStopCapture.Click += new System.EventHandler(this.cmdStopCapture_Click);
            // 
            // cmdStartCapture
            // 
            this.cmdStartCapture.Location = new System.Drawing.Point(13, 69);
            this.cmdStartCapture.Name = "cmdStartCapture";
            this.cmdStartCapture.Size = new System.Drawing.Size(86, 23);
            this.cmdStartCapture.TabIndex = 7;
            this.cmdStartCapture.Text = "Start Capture";
            this.cmdStartCapture.UseVisualStyleBackColor = true;
            this.cmdStartCapture.Click += new System.EventHandler(this.cmdStartCapture_Click);
            // 
            // chkPause
            // 
            this.chkPause.AutoSize = true;
            this.chkPause.Location = new System.Drawing.Point(170, 72);
            this.chkPause.Name = "chkPause";
            this.chkPause.Size = new System.Drawing.Size(56, 17);
            this.chkPause.TabIndex = 8;
            this.chkPause.Text = "Pause";
            this.chkPause.UseVisualStyleBackColor = true;
            this.chkPause.CheckedChanged += new System.EventHandler(this.chkPause_CheckedChanged);
            // 
            // WriteAvi
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(512, 101);
            this.Controls.Add(this.chkPause);
            this.Controls.Add(this.cmdStartCapture);
            this.Controls.Add(this.cmdStopCapture);
            this.Controls.Add(this.cmdFilename);
            this.Controls.Add(this.cmdShowPropertyPage);
            this.Controls.Add(this.cboVideoCodec);
            this.Controls.Add(this.txtFilename);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Name = "WriteAvi";
            this.Text = "Record Video";
            this.Load += new System.EventHandler(this.WriteAvi_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.MaskedTextBox txtFilename;
        private System.Windows.Forms.ComboBox cboVideoCodec;
        private System.Windows.Forms.Button cmdShowPropertyPage;
        private System.Windows.Forms.Button cmdFilename;
        private System.Windows.Forms.Button cmdStopCapture;
        private System.Windows.Forms.Button cmdStartCapture;
        private System.Windows.Forms.CheckBox chkPause;
    }
}
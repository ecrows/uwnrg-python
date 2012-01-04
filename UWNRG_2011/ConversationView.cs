using System;
using System.Collections.Generic;
using System.Text;
using Zaber;

namespace UWNRG_2011
{
    class ConversationView
    {
        private Conversation conversation;

        public ConversationView(Conversation conversation)
        {
            this.conversation = conversation;
        }

        public Conversation Conversation
        {
            get { return conversation; }
        }

        public byte DeviceNumber
        {
            get { return conversation.Device.DeviceNumber; }
        }
    }
}

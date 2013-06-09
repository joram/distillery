using System;
using System.Collections;
using System.Threading;
using Microsoft.SPOT;
using Microsoft.SPOT.Presentation;
using Microsoft.SPOT.Presentation.Controls;
using Microsoft.SPOT.Presentation.Media;
using Microsoft.SPOT.Touch;

using Gadgeteer.Networking;
using GT = Gadgeteer;
using GTM = Gadgeteer.Modules;
using Gadgeteer.Modules.GHIElectronics;
using Microsoft.SPOT.Net.NetworkInformation;

/*********
 * ETHERNET CLASS : http://mikedodaro.net/2011/12/13/sending-net-gadgeteer-sensor-data-to-a-rest-web-service/
 * 
 * 
 * *********/
namespace GadgeteerApp1{

    public partial class Program {
        Window mainWindow;
        Canvas canvas = new Canvas();
        Text txtMsg;
        Font baseFont;
        int count = 0;

        void tick(GT.Timer timer){
            log("" + count++);
        }

        void ProgramStarted(){
            SetupDisplay();
            SetupEthernet();
            startLooping(500);
        }

        void startLooping(int ms) {
            GT.Timer timer = new GT.Timer(ms);
            timer.Tick += new GT.Timer.TickEventHandler(tick);
            timer.Start();
        }

        void log(string s){
            txtMsg.TextContent = s;
        }

        void SetupDisplay(){
            baseFont = Resources.GetFont(Resources.FontResources.NinaB);
            mainWindow = display.WPFWindow;
            mainWindow.Child = canvas;
            txtMsg = new Text(baseFont, "Starting…");
            canvas.SetMargin(5);
            canvas.Children.Add(txtMsg);
        }

        void SetupEthernet() {
            ethernet.UseDHCP();
        }

        void OnNetworkDown(GTM.Module.NetworkModule sender, GTM.Module.NetworkModule.NetworkState state){
            Debug.Print("Network down.");
        }

        void OnNetworkUp(GTM.Module.NetworkModule sender, GTM.Module.NetworkModule.NetworkState state){
            Debug.Print("Network up.");
            ListNetworkInterfaces();
        }

        void ListNetworkInterfaces(){
            var settings = ethernet.NetworkSettings;

            Debug.Print("------------------------------------------------");
//          Debug.Print("MAC: " + ByteExtensions.ToHexString(settings.PhysicalAddress, "-"));
            Debug.Print("IP Address:   " + settings.IPAddress);
            Debug.Print("DHCP Enabled: " + settings.IsDhcpEnabled);
            Debug.Print("Subnet Mask:  " + settings.SubnetMask);
            Debug.Print("Gateway:      " + settings.GatewayAddress);
            Debug.Print("------------------------------------------------");
        }
    }
}

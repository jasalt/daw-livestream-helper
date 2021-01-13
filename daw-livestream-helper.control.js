loadAPI(12);

// Remove this if you want to be able to use deprecated methods without causing script to stop.
// This is useful during development.
host.setShouldFailOnDeprecatedUse(true);

host.defineController("com.saltiolabs", "daw-livestream-helper", "0.1", "5a8ba85f-856a-4f36-8546-7d6ef28103aa", "jasalt");

var connection = null;

const map = (value, x1, y1, x2, y2) => (value - x1) * (y2 - x2) / (y1 - x1) + x2;
function bws_tempo_to_bpm(tempo){
   var bpm_mapped = map(tempo, 0, 1, 20, 666);  // Convert decimal value between 0 - 1
   var bpm = bpm_mapped.toFixed(2);  // Two decimal precision
   return bpm;
}

function init() {
   // Setup host server settings accessible from Preferences
   var preferences = host.getPreferences();
   var ipAddressSetting = preferences.getStringSetting("IP Address", "Host", 15, "127.0.0.1");
   var portSetting = preferences.getStringSetting("Port", "Host", 6, "9000");

   var oscModule = host.getOscModule ();
   var ipAddress = ipAddressSetting.get();
   var port = parseInt(portSetting.get());

   ipAddressSetting.addValueObserver(function(value){
      if (value != ipAddress){  // Gets triggered on document change and after restart
         println("Host IP changed to " + value);
         host.restart();
      }});

   portSetting.addValueObserver(function(value){
      if (value != port){  // Gets triggered on document change and after restart
         println("Host port changed to " + value);
         host.restart();
      }});

      
   println("Connecting OSC server " + ipAddress + ":" + port);
   connection = oscModule.connectToUdpServer (ipAddress, port, oscModule.createAddressSpace ());

   var application = host.createApplication();
   var projectName = application.projectName();
   var activeEngine = application.hasActiveEngine();

   var activeProjectName;  // Use for checking if switching back to the same project
   var switchedProjectName;

   var transport = host.createTransport();
   var tempo = transport.tempo();
   var BPM;  // = tempo.value(); => returns RangedValueProxy on init, not value
   
   // Triggers on project tab switch and sets variable for switched project name
   projectName.addValueObserver(	
      function(projectName) {
         // println("switchedProjectName:" + projectName);
         switchedProjectName = projectName;
      });

   const map = (value, x1, y1, x2, y2) => (value - x1) * (y2 - x2) / (y1 - x1) + x2;
   tempo.value().addValueObserver(	
      function(newTempo) {
         var bpm_mapped = map(newTempo, 0, 1, 20, 666);  // Convert decimal value between 0 - 1
         var bpm = bpm_mapped.toFixed(2);  // Two decimal precision
         // println(`New BPM ${bpm} (${newTempo})` );
         BPM = bpm;
      });

   // Triggers on project tab switch
   activeEngine.addValueObserver(	
      function(activeEngine) {
         println('activeEngine: ' + activeEngine);
         println("activeProjectName:" + activeProjectName);

         if (activeEngine){  // if switched project tab has active engine
            if (BPM){  // tempo not uninitialized (during init or restart)
               if (switchedProjectName != activeProjectName){  // and it's not the same/current project
                  activeProjectName = switchedProjectName;
                  var data = `${switchedProjectName} | ${BPM}`
                  println(`Engine on, sending via OSC: ${data} BPM`);
                  connection.sendMessage("/project/info", `${data} BPM`);
               }
            }
         }
      });

   println("daw-livestream-helper initialized!");
}

function flush() {}

function exit() {}
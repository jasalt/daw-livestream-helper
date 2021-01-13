loadAPI(12);

// Remove this if you want to be able to use deprecated methods without causing script to stop.
// This is useful during development.
host.setShouldFailOnDeprecatedUse(true);

host.defineController("com.saltiolabs", "daw-livestream-helper", "0.1", "5a8ba85f-856a-4f36-8546-7d6ef28103aa", "jasalt");

var connection = null;

function init() {
   var preferences = host.getPreferences();
   var ipAddressSetting = preferences.getStringSetting("IP Address", "Host", 15, "127.0.0.1");
   var portSetting = preferences.getStringSetting("Port", "Host", 6, "9000");
   
   var oscModule = host.getOscModule ();
   var ipAddress = ipAddressSetting.get();
   var port = parseInt(portSetting.get());

   println("Connecting OSC server " + ipAddress + ":" + port);
   connection = oscModule.connectToUdpServer (ipAddress, port, oscModule.createAddressSpace ());

   var application = host.createApplication();
   var projectName = application.projectName();
   var activeEngine = application.hasActiveEngine();

   var activeProjectName;  // Use for checking if switching back to the same project
   var switchedProjectName;

   var transport = host.createTransport();
   var tempo = transport.tempo();
   

   // Triggers on project tab switch and sets variable for switched project name
   projectName.addValueObserver(	
      function(projectName) {
         println("switchedProjectName:" + projectName);
         switchedProjectName = projectName;
      });

   tempo.addValueObserver(	
      function(newTempo) {
         println("newTempo" + newTempo);
      });

   // Triggers on project tab switch
   activeEngine.addValueObserver(	
      function(activeEngine) {
         println('activeEngine: ' + activeEngine);
         println("activeProjectName:" + activeProjectName);

         // if switched project tab has active engine
         if (activeEngine){
            if (switchedProjectName != activeProjectName){  // and it's not the current active project
               activeProjectName = switchedProjectName; 
               println(`Engine On, sending project name ${switchedProjectName} via OSC`);
               connection.sendMessage("/project/name", switchedProjectName);  // send the updated active project name
            }
            // println('Switched to previously active project tab, skip sending message.');
         }
      });

   println("daw-livestream-helper initialized!");
}


function flush() {
}

function exit() {
}
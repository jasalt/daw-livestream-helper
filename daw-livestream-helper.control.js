loadAPI(12);

// Remove this if you want to be able to use deprecated methods without causing script to stop.
// This is useful during development.
host.setShouldFailOnDeprecatedUse(true);

host.defineController("com.saltiolabs", "daw-livestream-helper", "0.1", "5a8ba85f-856a-4f36-8546-7d6ef28103aa", "jasalt");

var connection = null;

function init() {
   var oscModule = host.getOscModule ();

   connection = oscModule.connectToUdpServer ("127.0.0.1", 9000, oscModule.createAddressSpace ());

   var application = host.createApplication();
   var projectName = application.projectName();
   var activeEngine = application.hasActiveEngine();

   projectName.addValueObserver(	
      function(projectName) {
         println(`projectName: ${projectName}`);
         println('typeof(projectName): ' + typeof(projectName));
      });

   activeEngine.addValueObserver(	
      function(activeEngine) {
         println('activeEngine: ' + activeEngine);
         println('typeof(activeEngine): ' + typeof(activeEngine));
         // connection.sendMessage("/project/name", projectName);
         // connection.sendMessage("/project/engine", activeEngine);
      });

   println("daw-livestream-helper initialized!");
}


function flush() {
}

function exit() {
}
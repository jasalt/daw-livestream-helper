loadAPI(12);

// Remove this if you want to be able to use deprecated methods without causing script to stop.
// This is useful during development.
host.setShouldFailOnDeprecatedUse(true);

host.defineController("com.saltiolabs", "daw-livestream-helper", "0.1", "5a8ba85f-856a-4f36-8546-7d6ef28103aa", "jasalt");

function init() {
   application = host.createApplication();
   projectName = application.projectName();

   projectName.addValueObserver(	
      function(projectName) {
         println(projectName);
      });

   // TODO: Perform further initialization here.
   println("daw-livestream-helper initialized!");
}


function flush() {
   // TODO: Flush any output to your controller here.
}

function exit() {

}
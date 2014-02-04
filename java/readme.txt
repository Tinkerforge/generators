This ZIP contains a Java library (.jar) for all Tinkerforge Bricks and Bricklets
(Tinkerforge.jar), the source of the library (in source/) and all available Java
examples (in examples/).

The library can be used without any further extensions. As an example let's
compile the configuration example of the Stepper Brick.

For this we create a folder and copy the Tinkerforge.jar and the
examples/Brick/Stepper/ExampleConfiguration.java into this folder.

 example_folder/
 -> Tinkerforge.jar
 -> ExampleConfiguration.java

In this folder we can now call the Java compiler with the following parameters
(1. Windows and 2. Linux/Mac OS)

 1.) javac -cp Tinkerforge.jar;. ExampleConfiguration.java
 2.) javac -cp Tinkerforge.jar:. ExampleConfiguration.java

and run it with the following parameters (1. Windows and 2. Linux/Mac OS X)

 1.) java -cp Tinkerforge.jar;. ExampleConfiguration
 2.) java -cp Tinkerforge.jar:. ExampleConfiguration

(Note: The difference is colon vs semicolon)

Or, alternatively add the JAR and the Example in an Java development environment
of your choice (such as Eclipse or NetBeans).

Documentation for the API can be found at

 http://www.tinkerforge.com/en/doc/Software/API_Bindings_Java.html#api-documentation-and-examples

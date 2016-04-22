1. Tinkerforge Visual Programming Language (TVPL)
=================================================

TVPL is a visual programming language based on Google Blockly
(https://developers.google.com/blockly/) supporting Tinkerforge
Bricks and Bricklets except RED Brick. It is an application with
which the user can graphically create programs using puzzle like
blocks and execute the program directly on a web browser. The
application also includes a GUI (Graphical User Interface) creator
which enables the user to create a GUI to interact with user's
program.

2. Getting Started
==================

To setup TVPL a working web server is required. Once there is
a working web server the application can be deployed by simply
extracting this ZIP file to the desired document root of the
web server and then accessing the application with index.html file.

Optionally, it is also possible to use TVPL locally without a web
server. More information about this is available in section 6 of
this document.

3. Dependencies
===============

TVPL requires a modern web browser with following features,

	* HTML5
	* WebSockets
	* Web Workers
	* BLOB support

The application will report if any dependencies are missing.

4. User Interface
=================

The user interface is divided into three main views,

	* Program Editor
	* GUI Editor
	* Execute Program

The view can be switched by clicking on the three links presented
on the upper right corner of the interface.

Additionally, there is also a main menu which is available by
clicking on the menu icon on the upper left corner of the interface.

	4.1 Program Editor
	------------------

	This is the default view presented to the user when TVPL is loaded.
	On this view the user can create a graphical program. On the left
	side of the screen on this view there is a toolbar which categorizes
	all the different GUI programming blocks available. Right of this toolbar
	is the workspace where the user will construct the graphical program.
	To use a block just drag and drop the block form toolbar to the workspace.
	More about different types of blocks can be found on section 5.

	4.2 GUI Editor
	--------------

	This view provides a GUI editor. GUI elements can be dragged from the 
	left toolbar and dropped on the GUI editor workspace in a stackable
	manner.

	There are three kinds of GUI elements available,

		* Output Field
		* Button
		* Plot

	Each GUI element on the GUI editor has an edit menu which is accessible
	with the little pencil icon once an element is present in the workspace.

		4.2.1 Output Field
		------------------

			This GUI element is used to output text from a program to the GUI.

			Edit menu fields,

			-> Name:

				Value of this read only field uniquely identifies a particular
				GUI element. On the program editor view's toolbar under
				"Miscellaneous" category a block can be found to output text
				from user program to a particular output field element by using
				value of this field.

		4.2.2 Button
		------------

			A button can be used to invoke a function in the program when clicked.

			Edit menu fields,

			-> Function to Call:

				This field specifies the function to call when the button is clicked
				with arguments.
			
			For example, testFunction(1, 'test') or testFunction() etc.

			More about functions can be found in section 5.

		4.2.3 Plot
		----------

			This element works pretty much the same as the "Output Field" element. But
			instead of text this element expects a numeric value from the user program
			to plot.

			Edit menu fields,

			-> Name:

				Identifies a particular Plot element. On the program editor view under
				"Miscellaneous" category a block can be found which can be used
				to provide the Plot element with numeric values.

			-> Width/Height:

				Dimension of the plot element.

			-> Data Points:

				Maximum number of data points to be visible on the plot element.

	4.3 Execute Program
	-------------------

	When a program is constructed it can be executed from this view. On the top part
	of this view there are two buttons to start/stop the execution of the program.
	On the left side there is a console on which the program can output data. Run time
	errors will also be reported on this console. On the right side user created GUI will
	be rendered. This rendered GUI is enabled once a program is running.

	4.4 Main Menu
	-------------

	The main menu provides three actions,

		* Load Project		
		* Save Project
		* About

5 Blocks
========

	A graphical program is constructed with TVPL using different types of blocks.

	5.1 Stackable
	-------------

	With this kind of blocks a stack of blocks can be formed. This is usable when
	order of execution is required. An example of this kind of block is the "print"
	block available under the category "Text" in the program editor.

	5.2 Block input/output
	----------------------

	This kind of blocks provide some data output which can be used in a block which
	require data input. A simple example would be "string" block connected to "print"
	block.

	5.4 Bricks/Bricklets
	--------------------

	These blocks represent functionalities of bricks and bricklets. Three fields are 
	common to all bricks/bricklets blocks, UID, host and port which specify where exactly
	the brick or the bricklet can be found.

	5.5 Variables
	-------------

	Can be used to provide data to other blocks.

	5.6 Functions
	-------------

	A function block contains a stack of stackable blocks which is executed sequentially.
	Each function block has two blocks, a definition block and a function call block.

6. Known Issues
===============

Running TVPL locally without any web server is currently possible only with Mozilla Firefox.
To use TVPL in this way with Google Chrome the browser must be launched with,
"--allow-file-access-from-files" option.

Installation:
    The bindings require an openHAB 2.5.0 Milestone/Snapshot installation.
    To install the bindings, just copy the two JARs into the addons directory
    of your installation. openHAB will then load the bindings. Afterwards
    you can add a Brick Daemon over the inbox.

Configuration:
    Attached devices are automagically put into the inbox after adding the
    Brick Daemon instance.

    Devices and channels can be configured: Channels typically allow changing
    the update rate. Some Bricklet's configuration can show/hide channels, for
    example the IO-4/16's pin configuration will dynamically create input or
    output channels. Sometimes the PaperUI needs to be refreshed by pressing F5
    to show new channels.

    Only configuration that is stored in a Bricklet's RAM is supported.
    Persistant configuration has to be set externally (e.g. by using Brick Viewer),
    because openHAB will often reconfigure devices, for example on startup or when
    reconnected to a Brick Daemon. Writing persistant configuration would then take
    too many write-cycles.

Further documentation:
    Can be found here:
    https://www.tinkerforge.com/en/doc/Software/API_Bindings_openHAB.html#api-bindings-openhab

Actions in rules:
    There are actions to be used in rules available for all devices. To use
    actions of a device in a rule, first the actions have to be loaded with:
    var devActions = getActions("tinkerforge", "tinkerforge:[devicetype]:[Device UID]")
    Then they can be used with devActions.[actionname]([parameters]).
    The following example shows how to show a GUI on an LCD 128x64 Bricklet
    with the UID "HQ6":

    rule "startrule"
    when
        System started
    then
        var lcdActions = getActions("tinkerforge", "tinkerforge:brickletlcd128x64:HQ6")
        lcdActions.brickletLCD128x64ClearDisplay()
        lcdActions.brickletLCD128x64RemoveAllGUI();
        lcdActions.brickletLCD128x64SetGUIButton(0, 0, 0, 60, 20, "button");
        lcdActions.brickletLCD128x64SetGUISlider(0, 0, 30, 60, 0, 50);
        lcdActions.brickletLCD128x64SetGUIGraphConfiguration(0, 1, 62, 0, 60, 52, "X", "Y");
        lcdActions.brickletLCD128x64SetGUIGraphData(0, newArrayList(0, 10, 20, 40, 20, 15));
        lcdActions.brickletLCD128x64SetGUITabConfiguration(3, false);
        lcdActions.brickletLCD128x64SetGUITabText(0, "Tab A");
        lcdActions.brickletLCD128x64SetGUITabText(1, "Tab B");
    end

    Functions that expect arrays as parameters can also
    be called with lists, as shown in the call of setGUIGraphData in the example.
    Results are returned as a Map<String, Object>, that can be used as follows:

    rule "otherrule"
    when
        Item Enx_Button changed to OFF
    then
        val lcdActions = getActions("tinkerforge", "tinkerforge:brickletlcd128x64:HQ6")
        pixels = lcdActions.brickletLCD128x64ReadPixels(0, 0, 127, 63).get("pixels")
        val inverted = pixels.map[p | !p]
        lcdActions.brickletLCD128x64WritePixels(0, 0, 127, 63, inverted)
    end

    This rule is triggered if the Item Enx_Button changes to OFF (i.e. if the
    corresponding RGB LED Button is released). It will then read the pixels
    currently shown on the LCD Bricklet, invert them and draw the inverted
    pixels back on the LCD.

    Nearly the complete API of devices can be used as actions.
    Operations that invalidate the state of channels will refresh them automatically.
    Not supported are operations, that would write EEPROM or Flash Storage, to
    avoid unneccesary write-cycles.

Display Bricklets:
    Text can be set as follows: [line],[position],[text]. Further ',' after
    the first two are handled as part of the text. In the text you can use
    the display's character set directly with \x[two hex digits]. Unicode characters
    are furthermore mapped to the display character set, as is done in the
    code examples, see f.e. here:
    https://www.tinkerforge.com/en/doc/Software/Bricklets/LCD20x4_Bricklet_Java.html#unicode

    As an example 1,2,Hello, opεnH\xE0B! will print Hallo, opεnHαB! stating
    at line 1, column 2 on an LCD 20x4. The small epsilon was mapped from Unicode
    into the LCD character set, 0xE0 (224) is the small alpha.

    PaperUI truncates whitespace at the start and end of commands. So to clear
    (parts of) a line, you can not use f.e. 1,2,[spaces]. Instead you can use
    the empty character like this 1,2,\xFE\xFE\xFE to delete three characters
    at Line 1, Column 2.

Missing features:
    Channels accept one CommandType only. For example the LED of a
    RGB LED Button Bricklet can only be set using an HSBType, not the others
    that openHAB expects support for (e.g. if only the brightness is changed,
    an PercentType is sent).

Known Bugs:
    Display Bricklets show '-' as text (NULL if clicked), if no text was
    already set using the UI.

    PaperUI does not show descriptions of channel(types) and configuration
    parameter groups. These are listed in the doc subfolder per device.

Unknown Bugs:
    If you find another bug, please attach the openHAB Log. This can be found
    in the userdata/logs folder of your openHAB installataion. If the bug is
    reproducable, you can try to increase the log level with
    log:set TRACE org.openhab.binding.tinkerforge in the karaf console.
    Maybe this will show more useful information. log:exception-display can
    help too. If there are errors shown in the PaperUI, they can be
    investigated using the web developer tools of your browser. Run the
    network monitor, reload the page and take a look at the responses of
    requests with status code 500. log:exception-display (in the karaf console)
    could be useful here too.

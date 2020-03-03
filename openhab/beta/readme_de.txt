Installation:
    Die Bindings benötigen eine openHAB 2.5.0 Installation.
    Zum Installieren reicht es, die JAR in das addons-Verzeichnis zu kopieren.
    Nachdem openHAB das Addon geladen hat (das kann einen Moment dauern), kann
    über die Inbox ein Brick Daemon hinzugefügt werden.

Konfiguration:
    Nachdem der Brick Daemon hinzugefügt wurde, werden angeschlossene Geräte
    automagisch in die Inbox gelegt. Nicht unterstützte Geräte haben "This
    device is not supported yet." in der Beschreibung. Zwecks Übersicht können
    diese versteckt werden.

    Sowohl Geräte als auch Channels können Konfiguration haben: Channels
    typischerweise die Aktualisierungsrate (Default: 1s). Die 
    Brickletkonfiguration kann Channels anzeigen/verstecken, z.b. erzeugt die
    Pinkonfiguration der IO-4/16 Input/Output-Channels je nachdem, ob ein Pin
    auf Input oder Output konfiguriert wurde. Die PaperUI braucht manchmal eine
    Aktualisierung per F5, damit neue Channels angezeigt werden.

    Es kann nur Konfiguration gesetzt werden, die im RAM des Geräte
    gespeichert wird. Persistente Konfiguration muss extern (z.b. mit dem Brick
    Viewer) gesetzt werden, da openHAB diese jedes Mal schreiben würde, wenn
    openHAB startet, oder die Verbindung zum Brick Daemon wiederhergestellt
    wurde usw. Das kostet zu viele Flash-Schreibzyklen.

Weitere Dokumentation:
    Findet sich im doc-Unterordner der Bindings. Dort sind pro Gerät die
    unterstützten Konfigurationsparameter und Channel mit Beschreibung
    aufgelistet.

Actions in Rules:
    Es werden für alle unterstützten Geräte Actions zur Verwendung in Rules
    zur Verfügung gestellt. Um in einer Rule auf die Actions eines Gerätes zuzugreifen, müssen
    diese zunächst mit
    var devActions = getActions("tinkerforge", "tinkerforge:[Gerätetyp]:[Device UID]")
    geladen werden. Danach können sie mit devActions.[actionname]([parameter])
    verwendet werden. Zum Beispiel zeigt die folgende Rule auf einem LCD 128x64 Bricklet 
    mit der UID "HQ6" eine graphische Oberfläche an:
    
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
    
    Die Parameter und Rückgabewerte der Actions entsprechen denen der jeweiligen Funktionen der
    Java-Bindings https://www.tinkerforge.com/de/doc/Software/API_Bindings_Java.html
    Java-Bindings-Funktionen, die Arrays erwarten, können in openHAB-Regeln auch mit Listen
    verwendet werden, wie dies im Beispiel von setGUIGraphData gezeigt wurde. Rückgabewerte
    werden als eine Map<String, Object> zurückgeben, diese kann wie folgt verwendet werden:
    
    rule "otherrule"
    when
        Item Enx_Button changed to OFF
    then
        val lcdActions = getActions("tinkerforge", "tinkerforge:brickletlcd128x64:HQ6")
        pixels = lcdActions.brickletLCD128x64ReadPixels(0, 0, 127, 63).get("pixels")
        val inverted = pixels.map[p | !p]
        lcdActions.brickletLCD128x64WritePixels(0, 0, 127, 63, inverted)        
    end
    
    Die Rule wird ausgelöst, wenn das Item Enx_Button auf OFF geändert wird (d.h. wenn der zugehörige
    RGB LED Button losgelassen wird). Sie liest gesamten Pixel des LCD Bricklets aus, invertiert diese
    und zeichnet die invertierten Pixel wieder auf das LCD.
    
    Über Actions kann fast die gesamte API der Geräte genutzt werden. Ausgenommen sind nur Operationen,
    die den Zustand von Channel stören, hierfür müssen dem Channel zugeordnete Items mit .sendCommand
    verwendet werden. Außerdem nicht unterstützt werden Operationen, die EEPROM- oder Flash-Speicher
    der Geräte schreiben würden. Auch hier sollen unnötige Schreibzyklen vermieden werden.
    
    Die verfügbaren Actions pro Gerät werden im doc-Verzeichnis der Bindings aufgelistet,
    die Namen entsprechen denen der Java-Bindings, in denen sich genauere Dokumentation findet.
    
Display-Bricklets:
    Text wird auf folgende Weise gesetzt: [line],[position],[text].
    Weitere ',' nach den ersten beiden werden als Teil des Textes behandelt.
    Der Text kann mit \x[zwei Hex-Ziffern] das Character-Set des Displays
    verwenden. Zusätzlich werden Unicode-Zeichen so gut es geht auf das
    Display-Character-Set abgebildet, wie das auch in den Code-Beispielen
    passiert, siehe z.B. hier: https://www.tinkerforge.com/de/doc/Software/Bricklets/LCD20x4_Bricklet_Java.html#unicode
    
    Beispielsweise gibt 1,2,Hallo, opεnH\xE0B! auf einem LCD 20x4 in
    Zeile 1, Spalte 2 aus: Hallo, opεnHαB!
    Das kleine Epsilon wurde von Unicode in das LCD-Character-Set übersetzt,
    0xE0 (224) entspricht dem kleinen Alpha.
    
    Die PaperUI scheint Leerzeichen am Rand des Commands abzuschneiden.
    Um (Teile) einer Zeile zu löschen kann also nicht ein Befehl wie 
    1,2,[Leerzeichen] verwendet werden. Stattdessen kann 1,2,\xFE\xFE\xFE
    benutzt werden um in Zeile 1, Spalte 2 drei Zeichen zu löschen.
    
Fehlende Features:
    Channels akzeptieren nur einen CommandTypen, d.h. z.B. LED des 
    RGB LED Button Bricklets nimmt nur HSBType an, nicht die anderen, die von
    openHAB erwartet werden (wie PercentType wenn die Brightness geändert wird)

Bekannte Bugs:
    Display Bricklets zeigen auf der Übersichtsseite, solange noch kein Text
    gesendet wurde, '-' als Text an, wenn darauf geklickt wird NULL.
    
    PaperUI zeigt die Description von Channel(Typen) und
    Konfigurationsparameter-Gruppen nicht an. -> Sind im docs-Unterorder pro
    Gerät aufgeführt.

    Löschen von nicht angeschlossenen Geräten funktioniert nur manchmal: Der
    DeviceHandler versucht aufzuräumen, z.b. Callbacks zu deaktivieren. Falls
    das Gerät nicht erreicht wird, fliegen hier Timeouts. Das wird aktuell
    nicht korrekt behandelt.

    Generierter Code muss noch verbessert werden. Kompilieren erzeugt viele
    Warnungen, Listener(de)registrierungen werden teilweise dupliziert.

Unbekannte Bugs:
    Falls ein anderer Bug auftritt, bitte das openHAB-Log mit anhängen. Das Log
    findet sich im userdata/logs-Verzeichnis der openHAB-Installation. Falls der
    Bug reproduzierbar ist, kann mit log:set TRACE org.openhab.binding.tinkerforge
    (in der Karaf-Konsole) das LogLevel erhöht werden, dann erscheinen eventuell
    weitere hilfreiche Informationen im Log. Außerdem hilfreich ist
    log:exception-display. Falls Fehler in der PaperUI angezeigt werden,
    können diese mit der Netzwerkanalyse der Web-Entwickler-Tools untersucht
    werden. Dann mit laufender Analyse die Seite neuladen und die Antworten von
    Anfragen mit Statuscode 500 ansehen. Eventuell hilft hier auch
    log:exception-display.

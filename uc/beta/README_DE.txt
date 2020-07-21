Tinkerforge C/C++ Bindings für Mikrocontroller
===============================================

Mit den C/C++ Bindings für Mikrocontroller können Tinkerforge
Koprozessor-Bricklets mit einem C/C++, das auf einem Mikrocontroller läuft,
kontrolliert werden.

Inhalt der Zip
--------------

 source/bindings/ - Die Implementierung der Bindings
 source/demo/ - Ein Demoprogramm für PTC 2.0 Bricklet und LCD 128x64 Bricklet
 source/hal_arduino/ - HAL für Arduino-Boards (z.B. Arduino Uno oder Teensy)
 source/hal_arduino_esp32/ - HAL für Arduino-Boards mit ESP32 (z.B. NodeMCU)
 source/hal_linux/ - HAL für Linux-Systeme mit spidev Support (z.B. Raspberry Pi)
 
 source/Makefile - Makefile für die Linux-Variante des Demoprogramms
 source/main.c - Linux-Variante des Demoprogramms
 
 source/arduino.ino - Arduino-Variante des Demoprogramms
 source/arduino_esp32.ino - Arduino-ESP32-Variante des Demoprogramms

Die Bindings entsprechen weitestgehend den normalen C/C++-Bindings, die hier
https://www.tinkerforge.com/de/doc/Software/API_Bindings_C.html#api-referenz-und-beispiele
dokumentiert sind.

Es gibt aber folgende, bisher nicht dokumentierte Abweichungen:
    - Es werden nur Koprozessor-Bricklets, also die mit einem 7-Pol-Stecker
      unterstützt
    
    - Alle Funktions-, Konstanten- und Typnamen beginnen mit einem tf_ bzw.
      TF_ Präfix.
      Die (dokumentierte) Funktion ptc_v2_get_temperature heißt hier also
      tf_ptc_v2_get_temperature, der Typ PTCV2 hier TF_PTCV2, die Konstante
      PTC_V2_WIRE_MODE_2 hier TF_PTC_V2_WIRE_MODE_2

    - Es werden keine High-Level-Callbacks unterstüzt.
      "Normale" Callbacks werden nur ausgeliefert, wenn periodisch mit dem Device kommuniziert wird.
      Um Callbacks für alle Devices, die mindestens einen Callback-Handler registriert haben
      zu empfangen, kann die Funktion
      int tf_hal_callback_tick(TF_HalContext *hal, uint32_t timeout_us);
      verwendet werden. Diese Funktion blockiert für die übergebene Zeit (in Mikrosekunden),
      empfängt Callbacks und liefert diese aus. Die Funktion kann mit einem Timeout von 0
      aufgerufen werden, um nur ein Callback zu empfangen, falls eins verfügbar ist.

      Falls das Standard-Round-Robin-Scheduling von tf_hal_callback_tick unerwünscht ist,
      können die Device-spezifischen Funktionen der Form
      int tf_[device]_callback_tick(TF_[device] *[device], uint32_t timeout_us);
      verwendet werden, die identisch, aber nur auf dem übergebenen Device arbeiten.

    - Callbacks bekommen immer als ersten Parameter einen Pointer auf das Bricklet,
      dass das Callback ausgelöst hat: Das dokumentierte input-value-Callback der IO4 2.0
      hat also die Signatur
      void callback(TF_IO4V2 *device, uint8_t channel, bool changed, bool value, void *user_data)
      anstelle der dokumentierten
      void callback(uint8_t channel, bool changed, bool value, void *user_data)

    - Callbacks werden mit einer spezifischen Funktion pro Callback registriert, die allgemeine
      [device]_register_callback-Funktion, die eine Callback-ID übergeben bekommt entfällt.
      Stattdessen müssen spezifische Funktionen wie
      void tf_io4_v2_register_input_value_callback(TF_IO4V2 *io4_v2, TF_IO4V2InputValueHandler handler, void *user_data);
      verwendet werden. Das bedeutet außerdem, dass der Callback-Handler nicht nach
      void (*)(void)
      gecastet werden muss und dass man sich auf die Compiler-Warnungen verlassen kann,
      falls die Signatur des Handlers nicht korrekt ist.

      Um ein Callback zu deregistrieren, kann NULL (C) oder nullptr (C++) als handler übergeben werden.
    
    - Devicefunktionen dürfen nicht aus einem Callback-Handler heraus aufgerufen werden.
    
    - Das Konzept der IP-Connection entfällt, stattdessen wird ein HAL (Hardware Abstraction Layer) benötigt,
      der die plattformspezifische Art und Weise der SPI-Kommunikation abstrahiert.
      HALs für Raspberry Pi sowie Arduinos werden mitgeliefert. Für andere
      Plattformen muss ein eigener HAL implementiert werden. (Siehe unten)

    - Die _create-Funktion eines Bricklets erwartet dementsprechend als letzten
      Parameter nicht einen Pointer auf die IPConnection, sondern auf den (initialisierten) HAL.

    - Die Fehlercodes entsprechen nicht denen der normalen C/C++-Bindings.
      Alle Fehlercodes sind in bindings/errors.h bzw. dem verwendeten HAL definiert.
      Durch Aufrufen von
      const char* tf_strerror(int error_code)
      kann eine Fehlerbeschreibung abgefragt werden.
 
 
Demoprogramm
------------

Es ist ein Demoprogramm für die bisher unterstützten Plattformen beigelegt.
Das Programm ist in die eigentliche Logik (im Ordner source/demo) und die Hardware-
spezifischen Teile (im Ordner source) unterteilt.

Das Demoprogramm kann mit einem Raspberry Pi (bzw. Zero) und einem HAT (bzw. Zero) Brick,
oder mit einer eigenen Schaltung mit einem Arduino verwendet werden.

Damit die Programme funktionieren, müssen die UIDs der Bricklets angepasst
werden. Diese werden z.B im Brick Viewer angezeigt. Außerdem geben die Bindings
beim Start eine Liste der UIDs aller gefundenen Bricklets aus.

Das Programm für den Raspberry Pi kann entweder durch Ausführen von make auf
dem Raspberry Pi selbst kompiliert werden, oder auf einem anderen PC
durch Ausführen von make CROSS_COMPILE=arm-linux-gnueabihf-
Hierfür muss der arm-linux-gnueabihf-gcc (Cross-)Compiler installiert sein.

Die Arduino-Programme können mit der Arduino IDE kompiliert werden.
Für ESP32 basierte Systeme muss hierfür im Board Manager das Paket
esp32 by Espressif Systems installiert werden.

Je nach Verkabelung muss das Port-Mapping in der entsprechenden .ino angepasst
werden.

Damit die Arduino-IDE die Programme kompiliert muss folgende Ordnerstruktur aufgebaut werden
(_esp32 anfügen, falls ein ESP32 basiertes Board verwendet wird):

arduino(_esp32)
├── arduino(_esp32).ino
└── src
    ├── bindings
    │   └── Inhalt des source/bindings-Ordners
    ├── demo
    │   └── Inhalt des source/demo-Ordners
    └── hal_arduino(_esp32)
        └── Inhalt des source/hal_arduino(_esp32)-Ordners

Achtung: Beide Beispielprogramme benutzen nur eine vereinfachte
Fehlerbehandlung!

Hinweise zur Implementierung eigener Programme
----------------------------------------------

Fase alle Funktionen der Bindings geben einen int zurück, der einen Fehlercode
darstellt. Alle Fehlercodes sind in bindings/errors.h bzw. im spezifischen HAL
aufgelistet. const char* tf_strerror(int); liefert eine Fehlerbeschreibung.

Alle HALs stellen automatisch folgende Funktionen zur Verfügung (implementiert
in hal_common.c unter Verwendung der HAL-spezifischen Funktionen)

- void tf_hal_set_timeout(TF_HalContext *hal, uint32_t timeout_us)
  Setzt den Timeout in Mikrosekunden für Funktionsaufrufe der Bricklets.
  Der Standardtimeout beträgt 2500000 = 2,5 Sekunden.

- uint32_t tf_hal_get_timeout(TF_HalContext *hal);
  Gibt den Timeout zurück.
  
- bool tf_hal_get_device_info(TF_HalContext *hal, size_t index, char ret_uid[7], char *ret_port_name, uint16_t *ret_device_id);
  Gibt die UID, den Port und den Device Identifier des n-ten (=index) Bricks/Bricklets zurück.
  Diese Funktion gibt false zurück, wenn der Index zu groß war.
  Es können also alle gefundenen Devices aufgelistet werden, indem die Funktion
  in einer Schleife mit von 0 aus wachsendem Index verwendet wird, bis einmal
  false zurückgegeben wird.

- void tf_hal_log_error(TF_HalContext *hal, const char *format, ...)
  Loggt einen Fehler.
  Unterstützt einen Format-String und weitere Argumente analog zu printf.
- void tf_hal_log_info(TF_HalContext *hal, const char *format, ...)
  Loggt eine Information.
  Unterstützt einen Format-String und weitere Argumente analog zu printf.
- void tf_hal_log_debug(TF_HalContext *hal, const char *format, ...)
  Loggt eine Debug-Meldung.
  Unterstützt einen Format-String und weitere Argumente analog zu printf.

Alle Logging-Funktionen werden über das Log-Level in bindings/config.h gesteuert, Log-Meldungen mit einem
Level kleiner als dem konfigurierten werden zur Compile-Zeit entfernt.

Hinweise zur Implementierung eines eigenen HALs
-----------------------------------------------

Wenn die Bindings auf einer anderen Plattform verwendet werden sollen, muss ein
eigener HAL implementiert werden. Dieser abstrahiert die plattformspezifische
Kommunikation über SPI.

Folgende Schritte sind zur Implementierung eines eigenen HALs notwendig:

Zunächst muss eine eigene TF_HalContext-Struktur definiert werden. Diese hält
alle notwendigen Informationen für die SPI-Kommunikation. Zusätzlich wird
typischerweise eine Instanz von TF_HalCommon, sowie ein Pointer auf ein Array
von Port-Mapping-Informationen gehalten. Das Format der Array-Einträge kann
für den spezifischen HAL angepasst werden. Siehe die struct Port in 
hal_arduino_esp32.h und hal_linux.h für Beispiele.

Bricklets werden anhand ihrer UID, sowie des Ports identifiziert, an dem sie
erreichbar sind. Ein Port entspricht typischerweise einem Chip-Select-Pin,
der geschaltet werden muss, damit Daten per SPI zum Bricklet übertragen werden
können. In einigen HAL-Funktionen wird eine port_id mitgegeben, diese ist
typischerweise ein Index in das Array der Port-Mapping-Informationen.

Nachdem die TF_HalContext-Struktur definiert wurde, muss deren
Initialisierungs-Funktion programmiert werden. Diese hat folgende Aufgaben:
    - Initialisieren der TF_HalCommon-Instanz mit tf_hal_common_init.
    
    - Vorbereiten der SPI-Kommunikation:
      Nachdem die Initialisierungs-Funktion lief, muss SPI-Kommunikation zu allen
      angeschlossenen Devices möglich sein. Alle Chip Select-Pins sollten auf HIGH,
      also disabled gesetzt werden. (Siehe "Details zur SPI-Kommunikation")

    - Aufrufen von tf_hal_finish_init:
      Das ist typischerweise der letzte Schritt der Initialisierung.
      SPI-Kommunikation muss hier bereits möglich sein. Die Funktion erwartet
      die Anzahl der verfügbaren Ports, sowie einen Timeout in micro seconds, wie lange an
      jedem Port auf eine Bricklet-Antwort gewartet werden soll.
      tf_hal_finish_init baut dann eine Liste erreichbarer Bricklets und legt sie
      in der TF_HalCommon-Instanz ab.

Als letztes müssen alle Funktionen, die in bindings/hal_common.h zwischen
// BEGIN - To be implemented by the specific HAL
und
// END - To be implemented by the specific HAL
aufgelistet sind implementiert werden. Diese haben folgende Aufgaben:

    - int tf_hal_destroy(TF_HalContext *hal);
      Beendet die SPI-Kommunikation.
      Achtung: Das Shutdown-Verhalten der Beispiel-HALs ist im Moment ungetestet.

    - int tf_hal_chip_select(TF_HalContext *hal, uint8_t port_id, bool enable);
      Setzt den Chip-Select-Pin für den Port mit der übergebenen port_id.
      Je nach Plattform kann hier mehr Arbeit notwendig sein.
      Beispielsweise müssen auf einem Arduino zusätzlich begin oder endTransaction
      der SPI-Einheit aufgerufen werden. Die Bindings stellen sicher, dass immer
      nur ein Chip-Select-Pin gleichzeitig aktiv ist.
    
    - int tf_hal_transceive(TF_HalContext *hal, uint8_t port_id, const uint8_t *write_buffer, uint8_t *read_buffer, uint32_t length);
      Überträgt length Bytes aus dem write_buffer an das Bricklet am übergebenen
      Port und empfängt ebensoviele Daten (SPI ist bidirektional) in den
      read_buffer. Die übergebenen Buffer sind immer groß genug um length Bytes zu
      lesen oder zu schreiben.
    
    - uint32_t tf_hal_current_time_us(TF_HalContext *hal);
      Gibt die aktuelle Zeit in Mikrosekunden zurück. Die Zeit muss keiner "echten"
      Zeit entsprechen, aber muss (abgesehen von Überläufen) monoton sein.
    
    - void tf_hal_sleep_us(TF_HalContext *hal, uint32_t us);
      Blockiert für die übergebene Zeit in Mikrosekunden.
    
    - TF_HalCommon *tf_hal_get_common(TF_HalContext *hal);
      Gibt die TF_HalCommon-Instanz aus dem spezifischen HalContext zurück.

    - char tf_hal_get_port_name(TF_HalContext *hal, uint8_t port_id);
      Gibt einen Port-Namen (typischerweise ein Buchstabe von 'A' bis 'Z') für die übergebene
      Port-ID zurück. Dieser Name wird z.B. in get_identity()-Aufrufe gepatcht, falls ein
      Brick/Bricklet direkt am System angeschlossen ist.
    
    - void tf_hal_log_message(const char *msg);
      Loggt die übergebene Nachricht. Je nach Plattform kann hier die
      Standardausgabe (Linux) oder eine serielle Konsole (ESP32) o.Ä. verwendet
      werden. Achtung: Diese Funktion darf nicht davon ausgehen, dass die HAL-Initialisierung
      erfolgreich war, da eventuelle Fehler, die während der Initialisierung
      auftreten auch geloggt werden können sollen.
    
    - const char* tf_hal_strerror(int rc);
      Gibt eine Fehlerbeschreibung für den übergebenen Fehlercode zurück. Die
      Bindings stellen eine Funktion tf_strerror zur Verfügung, die die meisten
      Fehlercodes abdeckt. Falls im HAL eigene Fehlercodes definiert werden, müssen
      diese hier behandlet werden, da tf_strerror, bei den Bindungs unbekannten
      Fehlern diese tf_hal_strerror aufruft.


Details zur SPI-Kommunikation
-----------------------------

Die Kommunikation über SPI verwendet den SPI Mode 3, also
- CPOL=1: Clock-Polarität ist invertiert: HIGH wenn inaktiv
- CPHA=1: Clock-Phase ist verschoben: Daten werden bei fallender Taktflanke gelesen
Siehe z.b. hier: https://www.mikrocontroller.net/articles/Serial_Peripheral_Interface#SPI-Modi
Daten werden MSB-First übertragen, die Standard-Taktfrequenz beträgt 1,4 MHz.
Das Logic-Level der Signale beträgt 3,3 Volt.

Aufgrund eines Bugs des auf den Bricklets verwendeten XMC-Mikrocontrollers von
Infineon trennt das Bricklets sich nicht korrekt vom SPI-Bus, wenn das
Chip-Select-Signal deaktiviert wird. Es treibt dann weiterhin auf MISO einen
Wert, was dazu führt, dass sich mehrere Bricklets am selben SPI-Bus gegenseitig
stören. Falls mehrere Bricklets eingesetzt werden sollen, müssen deshalb vom
Chip-Select-Signal kontrollierte Trenner-Chips eingesetzt werden.

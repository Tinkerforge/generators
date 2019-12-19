package com.tinkerforge;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.Arrays;
import java.util.List;
import java.net.URI;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.function.Function;
import java.util.function.BiConsumer;
import org.eclipse.smarthome.config.core.Configuration;
import org.eclipse.smarthome.config.core.ConfigDescription;
import org.eclipse.smarthome.config.core.ConfigDescriptionBuilder;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameter.Type;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameterBuilder;
import org.eclipse.smarthome.config.core.ConfigDescriptionParameterGroup;
import org.eclipse.smarthome.config.core.ParameterOption;
import org.eclipse.smarthome.core.types.State;
import org.eclipse.smarthome.core.types.StateOption;
import org.eclipse.smarthome.core.types.Command;
import org.eclipse.smarthome.core.types.CommandDescriptionBuilder;
import org.eclipse.smarthome.core.types.CommandOption;
import org.eclipse.smarthome.core.thing.ThingTypeUID;
import org.eclipse.smarthome.core.thing.type.ChannelDefinitionBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelType;
import org.eclipse.smarthome.core.thing.type.ChannelTypeBuilder;
import org.eclipse.smarthome.core.thing.type.ChannelTypeUID;
import org.eclipse.smarthome.core.thing.type.ThingType;
import org.eclipse.smarthome.core.thing.type.ThingTypeBuilder;
import org.eclipse.smarthome.core.types.StateDescriptionFragmentBuilder;
import org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeBindingConstants;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 433MHz receiver for outdoor weather station
 */
public class BrickletOutdoorWeather extends Device {
	public final static int DEVICE_IDENTIFIER = 288;
	public final static String DEVICE_DISPLAY_NAME = "Outdoor Weather Bricklet";

    public final static DeviceInfo DEVICE_INFO = new DeviceInfo(DEVICE_DISPLAY_NAME, "outdoorweather", DEVICE_IDENTIFIER, BrickletOutdoorWeather.class, DefaultActions.class, "2.0.4");

	public final static byte FUNCTION_GET_STATION_IDENTIFIERS_LOW_LEVEL = (byte)1;
	public final static byte FUNCTION_GET_SENSOR_IDENTIFIERS_LOW_LEVEL = (byte)2;
	public final static byte FUNCTION_GET_STATION_DATA = (byte)3;
	public final static byte FUNCTION_GET_SENSOR_DATA = (byte)4;
	public final static byte FUNCTION_SET_STATION_CALLBACK_CONFIGURATION = (byte)5;
	public final static byte FUNCTION_GET_STATION_CALLBACK_CONFIGURATION = (byte)6;
	public final static byte FUNCTION_SET_SENSOR_CALLBACK_CONFIGURATION = (byte)7;
	public final static byte FUNCTION_GET_SENSOR_CALLBACK_CONFIGURATION = (byte)8;
	public final static byte FUNCTION_GET_SPITFP_ERROR_COUNT = (byte)234;
	public final static byte FUNCTION_SET_BOOTLOADER_MODE = (byte)235;
	public final static byte FUNCTION_GET_BOOTLOADER_MODE = (byte)236;
	public final static byte FUNCTION_SET_WRITE_FIRMWARE_POINTER = (byte)237;
	public final static byte FUNCTION_WRITE_FIRMWARE = (byte)238;
	public final static byte FUNCTION_SET_STATUS_LED_CONFIG = (byte)239;
	public final static byte FUNCTION_GET_STATUS_LED_CONFIG = (byte)240;
	public final static byte FUNCTION_GET_CHIP_TEMPERATURE = (byte)242;
	public final static byte FUNCTION_RESET = (byte)243;
	public final static byte FUNCTION_WRITE_UID = (byte)248;
	public final static byte FUNCTION_READ_UID = (byte)249;
	public final static byte FUNCTION_GET_IDENTITY = (byte)255;
	private final static int CALLBACK_STATION_DATA = 9;
	private final static int CALLBACK_SENSOR_DATA = 10;

	public final static int WIND_DIRECTION_N = 0;
	public final static int WIND_DIRECTION_NNE = 1;
	public final static int WIND_DIRECTION_NE = 2;
	public final static int WIND_DIRECTION_ENE = 3;
	public final static int WIND_DIRECTION_E = 4;
	public final static int WIND_DIRECTION_ESE = 5;
	public final static int WIND_DIRECTION_SE = 6;
	public final static int WIND_DIRECTION_SSE = 7;
	public final static int WIND_DIRECTION_S = 8;
	public final static int WIND_DIRECTION_SSW = 9;
	public final static int WIND_DIRECTION_SW = 10;
	public final static int WIND_DIRECTION_WSW = 11;
	public final static int WIND_DIRECTION_W = 12;
	public final static int WIND_DIRECTION_WNW = 13;
	public final static int WIND_DIRECTION_NW = 14;
	public final static int WIND_DIRECTION_NNW = 15;
	public final static int WIND_DIRECTION_ERROR = 255;
	public final static int BOOTLOADER_MODE_BOOTLOADER = 0;
	public final static int BOOTLOADER_MODE_FIRMWARE = 1;
	public final static int BOOTLOADER_MODE_BOOTLOADER_WAIT_FOR_REBOOT = 2;
	public final static int BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_REBOOT = 3;
	public final static int BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_ERASE_AND_REBOOT = 4;
	public final static int BOOTLOADER_STATUS_OK = 0;
	public final static int BOOTLOADER_STATUS_INVALID_MODE = 1;
	public final static int BOOTLOADER_STATUS_NO_CHANGE = 2;
	public final static int BOOTLOADER_STATUS_ENTRY_FUNCTION_NOT_PRESENT = 3;
	public final static int BOOTLOADER_STATUS_DEVICE_IDENTIFIER_INCORRECT = 4;
	public final static int BOOTLOADER_STATUS_CRC_MISMATCH = 5;
	public final static int STATUS_LED_CONFIG_OFF = 0;
	public final static int STATUS_LED_CONFIG_ON = 1;
	public final static int STATUS_LED_CONFIG_SHOW_HEARTBEAT = 2;
	public final static int STATUS_LED_CONFIG_SHOW_STATUS = 3;

	private List<StationDataListener> listenerStationData = new CopyOnWriteArrayList<StationDataListener>();
	private List<SensorDataListener> listenerSensorData = new CopyOnWriteArrayList<SensorDataListener>();

	public class StationIdentifiersLowLevel {
		public int identifiersLength;
		public int identifiersChunkOffset;
		public int[] identifiersChunkData = new int[60];

		public String toString() {
			return "[" + "identifiersLength = " + identifiersLength + ", " + "identifiersChunkOffset = " + identifiersChunkOffset + ", " + "identifiersChunkData = " + Arrays.toString(identifiersChunkData) + "]";
		}
	}

	public class SensorIdentifiersLowLevel {
		public int identifiersLength;
		public int identifiersChunkOffset;
		public int[] identifiersChunkData = new int[60];

		public String toString() {
			return "[" + "identifiersLength = " + identifiersLength + ", " + "identifiersChunkOffset = " + identifiersChunkOffset + ", " + "identifiersChunkData = " + Arrays.toString(identifiersChunkData) + "]";
		}
	}

	public class StationData {
		public int temperature;
		public int humidity;
		public long windSpeed;
		public long gustSpeed;
		public long rain;
		public int windDirection;
		public boolean batteryLow;
		public int lastChange;

		public String toString() {
			return "[" + "temperature = " + temperature + ", " + "humidity = " + humidity + ", " + "windSpeed = " + windSpeed + ", " + "gustSpeed = " + gustSpeed + ", " + "rain = " + rain + ", " + "windDirection = " + windDirection + ", " + "batteryLow = " + batteryLow + ", " + "lastChange = " + lastChange + "]";
		}
	}

	public class SensorData {
		public int temperature;
		public int humidity;
		public int lastChange;

		public String toString() {
			return "[" + "temperature = " + temperature + ", " + "humidity = " + humidity + ", " + "lastChange = " + lastChange + "]";
		}
	}

	public class SPITFPErrorCount {
		public long errorCountAckChecksum;
		public long errorCountMessageChecksum;
		public long errorCountFrame;
		public long errorCountOverflow;

		public String toString() {
			return "[" + "errorCountAckChecksum = " + errorCountAckChecksum + ", " + "errorCountMessageChecksum = " + errorCountMessageChecksum + ", " + "errorCountFrame = " + errorCountFrame + ", " + "errorCountOverflow = " + errorCountOverflow + "]";
		}
	}

	/**
	 * Reports the station data every time a new data packet is received.
	 * See {@link BrickletOutdoorWeather#getStationData(int)} for information about the data.
	 *
	 * For each station the listener will be triggered about every 45 seconds.
	 *
	 * Turn the listener on/off with {@link BrickletOutdoorWeather#setStationCallbackConfiguration(boolean)}
	 * (by default it is turned off).
	 */
	public interface StationDataListener extends DeviceListener {
		public void stationData(int identifier, int temperature, int humidity, long windSpeed, long gustSpeed, long rain, int windDirection, boolean batteryLow);
	}

	/**
	 * Reports the sensor data every time a new data packet is received.
	 * See {@link BrickletOutdoorWeather#getSensorData(int)} for information about the data.
	 *
	 * For each station the listener will be called about every 45 seconds.
	 *
	 * Turn the listener on/off with {@link BrickletOutdoorWeather#setSensorCallbackConfiguration(boolean)}
	 * (by default it is turned off).
	 */
	public interface SensorDataListener extends DeviceListener {
		public void sensorData(int identifier, int temperature, int humidity);
	}

	/**
	 * Creates an object with the unique device ID \c uid. and adds it to
	 * the IP Connection \c ipcon.
	 */
	public BrickletOutdoorWeather(String uid, IPConnection ipcon) {
		super(uid, ipcon);

		apiVersion[0] = 2;
		apiVersion[1] = 0;
		apiVersion[2] = 0;
		responseExpected[IPConnection.unsignedByte(FUNCTION_GET_STATION_IDENTIFIERS_LOW_LEVEL)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_GET_SENSOR_IDENTIFIERS_LOW_LEVEL)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_GET_STATION_DATA)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_GET_SENSOR_DATA)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_SET_STATION_CALLBACK_CONFIGURATION)] = RESPONSE_EXPECTED_FLAG_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_GET_STATION_CALLBACK_CONFIGURATION)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_SET_SENSOR_CALLBACK_CONFIGURATION)] = RESPONSE_EXPECTED_FLAG_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_GET_SENSOR_CALLBACK_CONFIGURATION)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_GET_SPITFP_ERROR_COUNT)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_SET_BOOTLOADER_MODE)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_GET_BOOTLOADER_MODE)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_SET_WRITE_FIRMWARE_POINTER)] = RESPONSE_EXPECTED_FLAG_FALSE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_WRITE_FIRMWARE)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_SET_STATUS_LED_CONFIG)] = RESPONSE_EXPECTED_FLAG_FALSE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_GET_STATUS_LED_CONFIG)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_GET_CHIP_TEMPERATURE)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_RESET)] = RESPONSE_EXPECTED_FLAG_FALSE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_WRITE_UID)] = RESPONSE_EXPECTED_FLAG_FALSE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_READ_UID)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;
		responseExpected[IPConnection.unsignedByte(FUNCTION_GET_IDENTITY)] = RESPONSE_EXPECTED_FLAG_ALWAYS_TRUE;

		callbacks[CALLBACK_STATION_DATA] = new IPConnection.DeviceCallbackListener() {
			public void callback(byte[] packet) {
				ByteBuffer bb = ByteBuffer.wrap(packet, 8, packet.length - 8);
				bb.order(ByteOrder.LITTLE_ENDIAN);

				int identifier = IPConnection.unsignedByte(bb.get());
				int temperature = (bb.getShort());
				int humidity = IPConnection.unsignedByte(bb.get());
				long windSpeed = IPConnection.unsignedInt(bb.getInt());
				long gustSpeed = IPConnection.unsignedInt(bb.getInt());
				long rain = IPConnection.unsignedInt(bb.getInt());
				int windDirection = IPConnection.unsignedByte(bb.get());
				boolean batteryLow = (bb.get()) != 0;

				for (StationDataListener listener: listenerStationData) {
					listener.stationData(identifier, temperature, humidity, windSpeed, gustSpeed, rain, windDirection, batteryLow);
				}
			}
		};

		callbacks[CALLBACK_SENSOR_DATA] = new IPConnection.DeviceCallbackListener() {
			public void callback(byte[] packet) {
				ByteBuffer bb = ByteBuffer.wrap(packet, 8, packet.length - 8);
				bb.order(ByteOrder.LITTLE_ENDIAN);

				int identifier = IPConnection.unsignedByte(bb.get());
				int temperature = (bb.getShort());
				int humidity = IPConnection.unsignedByte(bb.get());

				for (SensorDataListener listener: listenerSensorData) {
					listener.sensorData(identifier, temperature, humidity);
				}
			}
		};
	}

	/**
	 * Returns the identifiers (number between 0 and 255) of all `stations
	 * &lt;https://www.tinkerforge.com/en/shop/accessories/sensors/outdoor-weather-station-ws-6147.html&gt;`__
	 * that have been seen since the startup of the Bricklet.
	 *
	 * Each station gives itself a random identifier on first startup.
	 *
	 * Since firmware version 2.0.2 a station is removed from the list if no data was received for
	 * 12 hours.
	 */
	public StationIdentifiersLowLevel getStationIdentifiersLowLevel() throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)8, FUNCTION_GET_STATION_IDENTIFIERS_LOW_LEVEL, this);


		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		StationIdentifiersLowLevel obj = new StationIdentifiersLowLevel();
		obj.identifiersLength = IPConnection.unsignedShort(bb.getShort());
		obj.identifiersChunkOffset = IPConnection.unsignedShort(bb.getShort());
		for (int i = 0; i < 60; i++) {
			obj.identifiersChunkData[i] = IPConnection.unsignedByte(bb.get());
		}

		return obj;
	}

	/**
	 * Returns the identifiers (number between 0 and 255) of all `sensors
	 * &lt;https://www.tinkerforge.com/en/shop/accessories/sensors/temperature-humidity-sensor-th-6148.html&gt;`__
	 * that have been seen since the startup of the Bricklet.
	 *
	 * Each sensor gives itself a random identifier on first startup.
	 *
	 * Since firmware version 2.0.2 a sensor is removed from the list if no data was received for
	 * 12 hours.
	 */
	public SensorIdentifiersLowLevel getSensorIdentifiersLowLevel() throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)8, FUNCTION_GET_SENSOR_IDENTIFIERS_LOW_LEVEL, this);


		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		SensorIdentifiersLowLevel obj = new SensorIdentifiersLowLevel();
		obj.identifiersLength = IPConnection.unsignedShort(bb.getShort());
		obj.identifiersChunkOffset = IPConnection.unsignedShort(bb.getShort());
		for (int i = 0; i < 60; i++) {
			obj.identifiersChunkData[i] = IPConnection.unsignedByte(bb.get());
		}

		return obj;
	}

	/**
	 * Returns the last received data for a station with the given identifier.
	 * Call {@link BrickletOutdoorWeather#getStationIdentifiers()} for a list of all available identifiers.
	 *
	 * The return values are:
	 *
	 * * Temperature in °C/10,
	 * * Humidity in %RH,
	 * * Wind Speed in m/10s,
	 * * Gust Speed in m/10s,
	 * * Rain Fall in mm/10,
	 * * Wind Direction (N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW, WSW, W, WNW, NW, NNW),
	 * * Battery Low (true or false) and
	 * * Last Change (time in seconds since the reception of this data).
	 */
	public StationData getStationData(int identifier) throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)9, FUNCTION_GET_STATION_DATA, this);

		bb.put((byte)identifier);

		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		StationData obj = new StationData();
		obj.temperature = (bb.getShort());
		obj.humidity = IPConnection.unsignedByte(bb.get());
		obj.windSpeed = IPConnection.unsignedInt(bb.getInt());
		obj.gustSpeed = IPConnection.unsignedInt(bb.getInt());
		obj.rain = IPConnection.unsignedInt(bb.getInt());
		obj.windDirection = IPConnection.unsignedByte(bb.get());
		obj.batteryLow = (bb.get()) != 0;
		obj.lastChange = IPConnection.unsignedShort(bb.getShort());

		return obj;
	}

	/**
	 * Returns the last measured data for a sensor with the given identifier.
	 * Call {@link BrickletOutdoorWeather#getSensorIdentifiers()} for a list of all available identifiers.
	 *
	 * The return values are:
	 *
	 * * Temperature in °C/10,
	 * * Humidity in %RH and
	 * * Last Change (time in seconds since the last reception of data).
	 */
	public SensorData getSensorData(int identifier) throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)9, FUNCTION_GET_SENSOR_DATA, this);

		bb.put((byte)identifier);

		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		SensorData obj = new SensorData();
		obj.temperature = (bb.getShort());
		obj.humidity = IPConnection.unsignedByte(bb.get());
		obj.lastChange = IPConnection.unsignedShort(bb.getShort());

		return obj;
	}

	/**
	 * Turns listener for station data on or off. Default is off.
	 */
	public void setStationCallbackConfiguration(boolean enableCallback) throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)9, FUNCTION_SET_STATION_CALLBACK_CONFIGURATION, this);

		bb.put((byte)(enableCallback ? 1 : 0));

		sendRequest(bb.array());
	}

	/**
	 * Returns the configuration as set by {@link BrickletOutdoorWeather#setStationCallbackConfiguration(boolean)}.
	 */
	public boolean getStationCallbackConfiguration() throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)8, FUNCTION_GET_STATION_CALLBACK_CONFIGURATION, this);


		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		boolean enableCallback = (bb.get()) != 0;

		return enableCallback;
	}

	/**
	 * Turns listener for sensor data on or off. Default is off.
	 */
	public void setSensorCallbackConfiguration(boolean enableCallback) throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)9, FUNCTION_SET_SENSOR_CALLBACK_CONFIGURATION, this);

		bb.put((byte)(enableCallback ? 1 : 0));

		sendRequest(bb.array());
	}

	/**
	 * Returns the configuration as set by {@link BrickletOutdoorWeather#setSensorCallbackConfiguration(boolean)}.
	 */
	public boolean getSensorCallbackConfiguration() throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)8, FUNCTION_GET_SENSOR_CALLBACK_CONFIGURATION, this);


		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		boolean enableCallback = (bb.get()) != 0;

		return enableCallback;
	}

	/**
	 * Returns the error count for the communication between Brick and Bricklet.
	 *
	 * The errors are divided into
	 *
	 * * ACK checksum errors,
	 * * message checksum errors,
	 * * framing errors and
	 * * overflow errors.
	 *
	 * The errors counts are for errors that occur on the Bricklet side. All
	 * Bricks have a similar function that returns the errors on the Brick side.
	 */
	public SPITFPErrorCount getSPITFPErrorCount() throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)8, FUNCTION_GET_SPITFP_ERROR_COUNT, this);


		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		SPITFPErrorCount obj = new SPITFPErrorCount();
		obj.errorCountAckChecksum = IPConnection.unsignedInt(bb.getInt());
		obj.errorCountMessageChecksum = IPConnection.unsignedInt(bb.getInt());
		obj.errorCountFrame = IPConnection.unsignedInt(bb.getInt());
		obj.errorCountOverflow = IPConnection.unsignedInt(bb.getInt());

		return obj;
	}

	/**
	 * Sets the bootloader mode and returns the status after the requested
	 * mode change was instigated.
	 *
	 * You can change from bootloader mode to firmware mode and vice versa. A change
	 * from bootloader mode to firmware mode will only take place if the entry function,
	 * device identifier and CRC are present and correct.
	 *
	 * This function is used by Brick Viewer during flashing. It should not be
	 * necessary to call it in a normal user program.
	 */
	public int setBootloaderMode(int mode) throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)9, FUNCTION_SET_BOOTLOADER_MODE, this);

		bb.put((byte)mode);

		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		int status = IPConnection.unsignedByte(bb.get());

		return status;
	}

	/**
	 * Returns the current bootloader mode, see {@link BrickletOutdoorWeather#setBootloaderMode(int)}.
	 */
	public int getBootloaderMode() throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)8, FUNCTION_GET_BOOTLOADER_MODE, this);


		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		int mode = IPConnection.unsignedByte(bb.get());

		return mode;
	}

	/**
	 * Sets the firmware pointer for {@link BrickletOutdoorWeather#writeFirmware(int[])}. The pointer has
	 * to be increased by chunks of size 64. The data is written to flash
	 * every 4 chunks (which equals to one page of size 256).
	 *
	 * This function is used by Brick Viewer during flashing. It should not be
	 * necessary to call it in a normal user program.
	 */
	public void setWriteFirmwarePointer(long pointer) throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)12, FUNCTION_SET_WRITE_FIRMWARE_POINTER, this);

		bb.putInt((int)pointer);

		sendRequest(bb.array());
	}

	/**
	 * Writes 64 Bytes of firmware at the position as written by
	 * {@link BrickletOutdoorWeather#setWriteFirmwarePointer(long)} before. The firmware is written
	 * to flash every 4 chunks.
	 *
	 * You can only write firmware in bootloader mode.
	 *
	 * This function is used by Brick Viewer during flashing. It should not be
	 * necessary to call it in a normal user program.
	 */
	public int writeFirmware(int[] data) throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)72, FUNCTION_WRITE_FIRMWARE, this);

		for (int i = 0; i < 64; i++) {
			bb.put((byte)data[i]);
		}

		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		int status = IPConnection.unsignedByte(bb.get());

		return status;
	}

	/**
	 * Sets the status LED configuration. By default the LED shows
	 * communication traffic between Brick and Bricklet, it flickers once
	 * for every 10 received data packets.
	 *
	 * You can also turn the LED permanently on/off or show a heartbeat.
	 *
	 * If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
	 */
	public void setStatusLEDConfig(int config) throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)9, FUNCTION_SET_STATUS_LED_CONFIG, this);

		bb.put((byte)config);

		sendRequest(bb.array());
	}

	/**
	 * Returns the configuration as set by {@link BrickletOutdoorWeather#setStatusLEDConfig(int)}
	 */
	public int getStatusLEDConfig() throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)8, FUNCTION_GET_STATUS_LED_CONFIG, this);


		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		int config = IPConnection.unsignedByte(bb.get());

		return config;
	}

	/**
	 * Returns the temperature in °C as measured inside the microcontroller. The
	 * value returned is not the ambient temperature!
	 *
	 * The temperature is only proportional to the real temperature and it has bad
	 * accuracy. Practically it is only useful as an indicator for
	 * temperature changes.
	 */
	public int getChipTemperature() throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)8, FUNCTION_GET_CHIP_TEMPERATURE, this);


		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		int temperature = (bb.getShort());

		return temperature;
	}

	/**
	 * Calling this function will reset the Bricklet. All configurations
	 * will be lost.
	 *
	 * After a reset you have to create new device objects,
	 * calling functions on the existing ones will result in
	 * undefined behavior!
	 */
	public void reset() throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)8, FUNCTION_RESET, this);


		sendRequest(bb.array());
	}

	/**
	 * Writes a new UID into flash. If you want to set a new UID
	 * you have to decode the Base58 encoded UID string into an
	 * integer first.
	 *
	 * We recommend that you use Brick Viewer to change the UID.
	 */
	public void writeUID(long uid) throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)12, FUNCTION_WRITE_UID, this);

		bb.putInt((int)uid);

		sendRequest(bb.array());
	}

	/**
	 * Returns the current UID as an integer. Encode as
	 * Base58 to get the usual string version.
	 */
	public long readUID() throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)8, FUNCTION_READ_UID, this);


		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		long uid = IPConnection.unsignedInt(bb.getInt());

		return uid;
	}

	/**
	 * Returns the UID, the UID where the Bricklet is connected to,
	 * the position, the hardware and firmware version as well as the
	 * device identifier.
	 *
	 * The position can be 'a', 'b', 'c' or 'd'.
	 *
	 * The device identifier numbers can be found :ref:`here &lt;device_identifier&gt;`.
	 * |device_identifier_constant|
	 */
	public Identity getIdentity() throws TinkerforgeException {
		ByteBuffer bb = ipcon.createRequestPacket((byte)8, FUNCTION_GET_IDENTITY, this);


		byte[] response = sendRequest(bb.array());

		bb = ByteBuffer.wrap(response, 8, response.length - 8);
		bb.order(ByteOrder.LITTLE_ENDIAN);

		Identity obj = new Identity();
		obj.uid = IPConnection.string(bb, 8);
		obj.connectedUid = IPConnection.string(bb, 8);
		obj.position = (char)(bb.get());
		for (int i = 0; i < 3; i++) {
			obj.hardwareVersion[i] = IPConnection.unsignedByte(bb.get());
		}
		for (int i = 0; i < 3; i++) {
			obj.firmwareVersion[i] = IPConnection.unsignedByte(bb.get());
		}
		obj.deviceIdentifier = IPConnection.unsignedShort(bb.getShort());

		return obj;
	}

	/**
	 * Returns the identifiers (number between 0 and 255) of all `stations
	 * &lt;https://www.tinkerforge.com/en/shop/accessories/sensors/outdoor-weather-station-ws-6147.html&gt;`__
	 * that have been seen since the startup of the Bricklet.
	 *
	 * Each station gives itself a random identifier on first startup.
	 *
	 * Since firmware version 2.0.2 a station is removed from the list if no data was received for
	 * 12 hours.
	 */
	public int[] getStationIdentifiers() throws TinkerforgeException {
		StationIdentifiersLowLevel ret;
		int[] identifiers = null; // stop the compiler from wrongly complaining that this variable is used unassigned
		int identifiersLength;
		int identifiersChunkOffset;
		int identifiersChunkLength;
		boolean identifiersOutOfSync;
		int identifiersCurrentLength;

		synchronized (streamMutex) {
			ret = getStationIdentifiersLowLevel();
			identifiersLength = ret.identifiersLength;
			identifiersChunkOffset = ret.identifiersChunkOffset;
			identifiersOutOfSync = identifiersChunkOffset != 0;

			if (!identifiersOutOfSync) {
				identifiers = new int[identifiersLength];
				identifiersChunkLength = Math.min(identifiersLength - identifiersChunkOffset, 60);

				System.arraycopy(ret.identifiersChunkData, 0, identifiers, 0, identifiersChunkLength);

				identifiersCurrentLength = identifiersChunkLength;

				while (identifiersCurrentLength < identifiersLength) {
					ret = getStationIdentifiersLowLevel();
					identifiersLength = ret.identifiersLength;
					identifiersOutOfSync = ret.identifiersChunkOffset != identifiersCurrentLength;

					if (identifiersOutOfSync) {
						break;
					}

					identifiersChunkLength = Math.min(identifiersLength - ret.identifiersChunkOffset, 60);

					System.arraycopy(ret.identifiersChunkData, 0, identifiers, identifiersCurrentLength, identifiersChunkLength);

					identifiersCurrentLength += identifiersChunkLength;
				}
			}

			if (identifiersOutOfSync) { // discard remaining stream to bring it back in-sync
				while (ret.identifiersChunkOffset + 60 < identifiersLength) {
					ret = getStationIdentifiersLowLevel();
					identifiersLength = ret.identifiersLength;
				}

				throw new StreamOutOfSyncException("Identifiers stream is out-of-sync");
			}
		}

		return identifiers;
	}

	/**
	 * Returns the identifiers (number between 0 and 255) of all `sensors
	 * &lt;https://www.tinkerforge.com/en/shop/accessories/sensors/temperature-humidity-sensor-th-6148.html&gt;`__
	 * that have been seen since the startup of the Bricklet.
	 *
	 * Each sensor gives itself a random identifier on first startup.
	 *
	 * Since firmware version 2.0.2 a sensor is removed from the list if no data was received for
	 * 12 hours.
	 */
	public int[] getSensorIdentifiers() throws TinkerforgeException {
		SensorIdentifiersLowLevel ret;
		int[] identifiers = null; // stop the compiler from wrongly complaining that this variable is used unassigned
		int identifiersLength;
		int identifiersChunkOffset;
		int identifiersChunkLength;
		boolean identifiersOutOfSync;
		int identifiersCurrentLength;

		synchronized (streamMutex) {
			ret = getSensorIdentifiersLowLevel();
			identifiersLength = ret.identifiersLength;
			identifiersChunkOffset = ret.identifiersChunkOffset;
			identifiersOutOfSync = identifiersChunkOffset != 0;

			if (!identifiersOutOfSync) {
				identifiers = new int[identifiersLength];
				identifiersChunkLength = Math.min(identifiersLength - identifiersChunkOffset, 60);

				System.arraycopy(ret.identifiersChunkData, 0, identifiers, 0, identifiersChunkLength);

				identifiersCurrentLength = identifiersChunkLength;

				while (identifiersCurrentLength < identifiersLength) {
					ret = getSensorIdentifiersLowLevel();
					identifiersLength = ret.identifiersLength;
					identifiersOutOfSync = ret.identifiersChunkOffset != identifiersCurrentLength;

					if (identifiersOutOfSync) {
						break;
					}

					identifiersChunkLength = Math.min(identifiersLength - ret.identifiersChunkOffset, 60);

					System.arraycopy(ret.identifiersChunkData, 0, identifiers, identifiersCurrentLength, identifiersChunkLength);

					identifiersCurrentLength += identifiersChunkLength;
				}
			}

			if (identifiersOutOfSync) { // discard remaining stream to bring it back in-sync
				while (ret.identifiersChunkOffset + 60 < identifiersLength) {
					ret = getSensorIdentifiersLowLevel();
					identifiersLength = ret.identifiersLength;
				}

				throw new StreamOutOfSyncException("Identifiers stream is out-of-sync");
			}
		}

		return identifiers;
	}

	/**
	 * Adds a StationData listener.
	 */
	public void addStationDataListener(StationDataListener listener) {
		listenerStationData.add(listener);
	}

	/**
	 * Removes a StationData listener.
	 */
	public void removeStationDataListener(StationDataListener listener) {
		listenerStationData.remove(listener);
	}

	/**
	 * Adds a SensorData listener.
	 */
	public void addSensorDataListener(SensorDataListener listener) {
		listenerSensorData.add(listener);
	}

	/**
	 * Removes a SensorData listener.
	 */
	public void removeSensorDataListener(SensorDataListener listener) {
		listenerSensorData.remove(listener);
	}

    private final Logger logger = LoggerFactory.getLogger(BrickletOutdoorWeather.class);
    private final static Logger static_logger = LoggerFactory.getLogger(BrickletOutdoorWeather.class);

    @Override
    public void initialize(org.eclipse.smarthome.config.core.Configuration config, Function<String, org.eclipse.smarthome.config.core.Configuration> getChannelConfigFn, BiConsumer<String, org.eclipse.smarthome.core.types.State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {
        this.setStationCallbackConfiguration(true);
        this.setSensorCallbackConfiguration(true);
    }

    @Override
    public void dispose(org.eclipse.smarthome.config.core.Configuration config) throws TinkerforgeException {

    }

    @Override
    public List<String> getEnabledChannels(org.eclipse.smarthome.config.core.Configuration config) throws TinkerforgeException{
        List<String> result = new ArrayList<String>();

        return result;
    }

    public static ChannelType getChannelType(ChannelTypeUID channelTypeUID) {
        switch(channelTypeUID.getId()) {

            default:
                static_logger.debug("Unknown channel type ID {}", channelTypeUID.getId());
                break;
        }

        return null;
    }

    public static ThingType getThingType(ThingTypeUID thingTypeUID) {
        return ThingTypeBuilder.instance(thingTypeUID, "Tinkerforge Outdoor Weather Bricklet").isListed(false).withSupportedBridgeTypeUIDs(Arrays.asList(TinkerforgeBindingConstants.THING_TYPE_BRICK_DAEMON.getId())).withConfigDescriptionURI(URI.create("thing-type:tinkerforge:" + thingTypeUID.getId())).withDescription("433MHz receiver for outdoor weather station").withChannelDefinitions(Arrays.asList()).buildBridge();
    }

    public static ConfigDescription getConfigDescription(URI uri) {
        switch(uri.toASCIIString()) {
            case "thing-type:tinkerforge:outdoorweather":
                return ConfigDescriptionBuilder.create(uri).build();
            default:
                static_logger.debug("Unknown config description URI {}", uri.toASCIIString());
                break;
        }
        return null;
    }

        @Override
    public void refreshValue(String value, org.eclipse.smarthome.config.core.Configuration config, org.eclipse.smarthome.config.core.Configuration channelConfig, BiConsumer<String, org.eclipse.smarthome.core.types.State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {
        switch(value) {

            default:
                logger.warn("Refresh for unknown channel {}", value);
                break;
        }
    }


        @Override
    public List<SetterRefresh> handleCommand(org.eclipse.smarthome.config.core.Configuration config, org.eclipse.smarthome.config.core.Configuration channelConfig, String channel, Command command) throws TinkerforgeException {
        List<SetterRefresh> result = Collections.emptyList();
        switch(channel) {

            default:
                logger.warn("Command for unknown channel {}", channel);
        }
        return result;
    }


}

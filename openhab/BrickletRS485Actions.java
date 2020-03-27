package org.eclipse.smarthome.binding.tinkerforge.internal.device;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.LinkedBlockingDeque;
import java.util.concurrent.TimeUnit;

import org.eclipse.jdt.annotation.NonNull;
import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.DeviceHandler;
import org.eclipse.smarthome.core.thing.binding.ThingActions;
import org.eclipse.smarthome.core.thing.binding.ThingActionsScope;
import org.eclipse.smarthome.core.thing.binding.ThingHandler;
import org.openhab.core.automation.annotation.ActionInput;
import org.openhab.core.automation.annotation.ActionOutput;
import org.openhab.core.automation.annotation.RuleAction;

import com.tinkerforge.BrickletRS485;
import com.tinkerforge.BrickletRS485.ModbusMasterReadCoilsResponseListener;
import com.tinkerforge.BrickletRS485.ModbusMasterReadDiscreteInputsResponseListener;
import com.tinkerforge.BrickletRS485.ModbusMasterReadHoldingRegistersResponseListener;
import com.tinkerforge.BrickletRS485.ModbusMasterReadInputRegistersResponseListener;
import com.tinkerforge.BrickletRS485.ModbusMasterWriteMultipleCoilsResponseListener;
import com.tinkerforge.BrickletRS485.ModbusMasterWriteMultipleRegistersResponseListener;
import com.tinkerforge.BrickletRS485.ModbusMasterWriteSingleCoilResponseListener;
import com.tinkerforge.BrickletRS485.ModbusMasterWriteSingleRegisterResponseListener;
import com.tinkerforge.TinkerforgeException;

@NonNullByDefault
@ThingActionsScope(name = "tinkerforge")
public class BrickletRS485Actions implements ThingActions {

    private @Nullable DeviceHandler handler;

    @Override
    public void setThingHandler(@Nullable ThingHandler handler) {
        this.handler = (DeviceHandler) handler;
    }

    @Override
    public @Nullable ThingHandler getThingHandler() {
        return handler;
    }

    @RuleAction(label = "Write")
    public @ActionOutput(name = "messageWritten", type = "int") Map<String, Object> brickletRS485Write(
            @ActionInput(name = "message") char[] message) throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }

        int value = dev.write(message);

        result.put("messageWritten", value);
        return result;
    }

    public static Map<String, Object> brickletRS485Write(@Nullable ThingActions actions, char[] message)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485Write(message);
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Read")
    public @ActionOutput(name = "message", type = "char[]") Map<String, Object> brickletRS485Read(
            @ActionInput(name = "length") int length) throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }

        char[] value = dev.read(length);

        result.put("message", value);
        return result;
    }

    public static Map<String, Object> brickletRS485Read(@Nullable ThingActions actions, int length)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485Read(length);
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Get RS485 Configuration")
    public @ActionOutput(name = "baudrate", type = "long") @ActionOutput(name = "parity", type = "int") @ActionOutput(name = "stopbits", type = "int") @ActionOutput(name = "wordlength", type = "int") @ActionOutput(name = "duplex", type = "int") Map<String, Object> brickletRS485GetRS485Configuration()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }

        BrickletRS485.RS485Configuration value = dev
                .getRS485Configuration();

        result.put("baudrate", value.baudrate);
        result.put("parity", value.parity);
        result.put("stopbits", value.stopbits);
        result.put("wordlength", value.wordlength);
        result.put("duplex", value.duplex);
        return result;
    }

    public static Map<String, Object> brickletRS485GetRS485Configuration(@Nullable ThingActions actions)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485GetRS485Configuration();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Get Mode")
    public @ActionOutput(name = "mode", type = "int") Map<String, Object> brickletRS485GetMode()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }

        int value = dev.getMode();

        result.put("mode", value);
        return result;
    }

    public static Map<String, Object> brickletRS485GetMode(@Nullable ThingActions actions) throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485GetMode();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Get Communication LED Config")
    public @ActionOutput(name = "config", type = "int") Map<String, Object> brickletRS485GetCommunicationLEDConfig()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }

        int value = dev.getCommunicationLEDConfig();

        result.put("config", value);
        return result;
    }

    public static Map<String, Object> brickletRS485GetCommunicationLEDConfig(@Nullable ThingActions actions)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485GetCommunicationLEDConfig();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Get Error LED Config")
    public @ActionOutput(name = "config", type = "int") Map<String, Object> brickletRS485GetErrorLEDConfig()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }

        int value = dev.getErrorLEDConfig();

        result.put("config", value);
        return result;
    }

    public static Map<String, Object> brickletRS485GetErrorLEDConfig(@Nullable ThingActions actions)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485GetErrorLEDConfig();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Get Buffer Config")
    public @ActionOutput(name = "sendBufferSize", type = "int") @ActionOutput(name = "receiveBufferSize", type = "int") Map<String, Object> brickletRS485GetBufferConfig()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }

        BrickletRS485.BufferConfig value = dev.getBufferConfig();

        result.put("sendBufferSize", value.sendBufferSize);
        result.put("receiveBufferSize", value.receiveBufferSize);
        return result;
    }

    public static Map<String, Object> brickletRS485GetBufferConfig(@Nullable ThingActions actions)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485GetBufferConfig();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Get Buffer Status")
    public @ActionOutput(name = "sendBufferUsed", type = "int") @ActionOutput(name = "receiveBufferUsed", type = "int") Map<String, Object> brickletRS485GetBufferStatus()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }

        BrickletRS485.BufferStatus value = dev.getBufferStatus();

        result.put("sendBufferUsed", value.sendBufferUsed);
        result.put("receiveBufferUsed", value.receiveBufferUsed);
        return result;
    }

    public static Map<String, Object> brickletRS485GetBufferStatus(@Nullable ThingActions actions)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485GetBufferStatus();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Get Error Count")
    public @ActionOutput(name = "overrunErrorCount", type = "long") @ActionOutput(name = "parityErrorCount", type = "long") Map<String, Object> brickletRS485GetErrorCount()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }

        BrickletRS485.ErrorCount value = dev.getErrorCount();

        result.put("overrunErrorCount", value.overrunErrorCount);
        result.put("parityErrorCount", value.parityErrorCount);
        return result;
    }

    public static Map<String, Object> brickletRS485GetErrorCount(@Nullable ThingActions actions)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485GetErrorCount();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Get Modbus Configuration")
    public @ActionOutput(name = "slaveAddress", type = "int") @ActionOutput(name = "masterRequestTimeout", type = "long") Map<String, Object> brickletRS485GetModbusConfiguration()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }

        BrickletRS485.ModbusConfiguration value = dev
                .getModbusConfiguration();

        result.put("slaveAddress", value.slaveAddress);
        result.put("masterRequestTimeout", value.masterRequestTimeout);
        return result;
    }

    public static Map<String, Object> brickletRS485GetModbusConfiguration(@Nullable ThingActions actions)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485GetModbusConfiguration();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Get Modbus Common Error Count")
    public @ActionOutput(name = "timeoutErrorCount", type = "long") @ActionOutput(name = "checksumErrorCount", type = "long") @ActionOutput(name = "frameTooBigErrorCount", type = "long") @ActionOutput(name = "illegalFunctionErrorCount", type = "long") @ActionOutput(name = "illegalDataAddressErrorCount", type = "long") @ActionOutput(name = "illegalDataValueErrorCount", type = "long") @ActionOutput(name = "slaveDeviceFailureErrorCount", type = "long") Map<String, Object> brickletRS485GetModbusCommonErrorCount()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }

        BrickletRS485.ModbusCommonErrorCount value = dev
                .getModbusCommonErrorCount();

        result.put("timeoutErrorCount", value.timeoutErrorCount);
        result.put("checksumErrorCount", value.checksumErrorCount);
        result.put("frameTooBigErrorCount", value.frameTooBigErrorCount);
        result.put("illegalFunctionErrorCount", value.illegalFunctionErrorCount);
        result.put("illegalDataAddressErrorCount", value.illegalDataAddressErrorCount);
        result.put("illegalDataValueErrorCount", value.illegalDataValueErrorCount);
        result.put("slaveDeviceFailureErrorCount", value.slaveDeviceFailureErrorCount);
        return result;
    }

    public static Map<String, Object> brickletRS485GetModbusCommonErrorCount(@Nullable ThingActions actions)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485GetModbusCommonErrorCount();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Modbus Master Read Coils")
    public @ActionOutput(name = "exceptionCode", type = "int") @ActionOutput(name = "coils", type = "boolean[]") @Nullable Map<String, Object> brickletRS485ModbusMasterReadCoils(
            @ActionInput(name = "slaveAddress") int slaveAddress,
            @ActionInput(name = "startingAddress") long startingAddress, @ActionInput(name = "count") int count)
            throws TinkerforgeException {

        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }

        int modbusTimeout = ((BigDecimal) h.getConfig().get("masterRequestTimeout")).intValue();

        LinkedBlockingDeque<Integer> reqIDdeque = new LinkedBlockingDeque<>(1);
        LinkedBlockingDeque<@Nullable Map<String, Object>> resultDeque = new LinkedBlockingDeque<>(1);

        ModbusMasterReadCoilsResponseListener listener = (int reqID, int exceptionCode, boolean[] coils) -> {
            @Nullable Integer requestID = null;
            try {
                requestID = reqIDdeque.pollFirst(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
            if (requestID == null) {
                resultDeque.push(null);
                return;
            }
            if (requestID != reqID) {
                reqIDdeque.push(requestID);
                return;
            }
            Map<String, Object> _result = new HashMap<>();
            _result.put("exceptionCode", exceptionCode);
            _result.put("coils", coils);
            resultDeque.push(_result);
        };
        dev.addModbusMasterReadCoilsResponseListener(listener);
        int requestID = dev.modbusMasterReadCoils(slaveAddress, startingAddress, count);
        reqIDdeque.push(requestID); // Push even if requestID == 0 to avoid blocking the callback listener.

        if (requestID != 0) {
            try {
                result = resultDeque.poll(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
        }
        dev.removeModbusMasterReadCoilsResponseListener(listener);

        return result;
    }

    public static @Nullable Map<String, Object> brickletRS485ModbusMasterReadCoils(@Nullable ThingActions actions,
            int slaveAddress, long startingAddress, int count) throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485ModbusMasterReadCoils(slaveAddress, startingAddress,
                    count);
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Modbus Master Read Holding Registers")
    public @ActionOutput(name = "exceptionCode", type = "int") @ActionOutput(name = "coils", type = "boolean[]") @Nullable Map<String, Object> brickletRS485ModbusMasterReadHoldingRegisters(
            @ActionInput(name = "slaveAddress") int slaveAddress,
            @ActionInput(name = "startingAddress") long startingAddress, @ActionInput(name = "count") int count)
            throws TinkerforgeException {

        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }

        int modbusTimeout = ((BigDecimal) h.getConfig().get("masterRequestTimeout")).intValue();

        LinkedBlockingDeque<Integer> reqIDdeque = new LinkedBlockingDeque<>(1);
        LinkedBlockingDeque<@Nullable Map<String, Object>> resultDeque = new LinkedBlockingDeque<>(1);

        ModbusMasterReadHoldingRegistersResponseListener listener = (int reqID, int exceptionCode,
                int[] holdingRegisters) -> {
            @Nullable Integer requestID = null;
            try {
                requestID = reqIDdeque.pollFirst(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
            if (requestID == null) {
                resultDeque.push(null);
                return;
            }
            if (requestID != reqID) {
                reqIDdeque.push(requestID);
                return;
            }
            Map<String, Object> _result = new HashMap<>();
            _result.put("exceptionCode", exceptionCode);
            _result.put("holdingRegisters", holdingRegisters);
            resultDeque.push(_result);
        };
        dev.addModbusMasterReadHoldingRegistersResponseListener(listener);
        int requestID = dev.modbusMasterReadHoldingRegisters(slaveAddress, startingAddress, count);
        reqIDdeque.push(requestID); // Push even if requestID == 0 to avoid blocking the callback listener.

        if (requestID != 0) {
            try {
                result = resultDeque.poll(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
        }
        dev.removeModbusMasterReadHoldingRegistersResponseListener(listener);

        return result;
    }

    public static @Nullable Map<String, Object> brickletRS485ModbusMasterReadHoldingRegisters(@Nullable ThingActions actions,
            int slaveAddress, long startingAddress, int count) throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485ModbusMasterReadHoldingRegisters(slaveAddress,
                    startingAddress, count);
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Modbus Master Write Single Coil")
    public @ActionOutput(name = "exceptionCode", type = "int") @Nullable Map<String, Object> brickletRS485ModbusMasterWriteSingleCoil(
            @ActionInput(name = "slaveAddress") int slaveAddress, @ActionInput(name = "coilAddress") long coilAddress,
            @ActionInput(name = "coilValue") boolean coilValue) throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }
        int modbusTimeout = ((BigDecimal) h.getConfig().get("masterRequestTimeout")).intValue();

        LinkedBlockingDeque<Integer> reqIDdeque = new LinkedBlockingDeque<>(1);
        LinkedBlockingDeque<@Nullable Map<String, Object>> resultDeque = new LinkedBlockingDeque<>(1);

        ModbusMasterWriteSingleCoilResponseListener listener = (int reqID, int exceptionCode) -> {
            @Nullable Integer requestID = null;
            try {
                requestID = reqIDdeque.pollFirst(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
            if (requestID == null) {
                resultDeque.push(null);
                return;
            }
            if (requestID != reqID) {
                reqIDdeque.push(requestID);
                return;
            }
            Map<String, Object> _result = new HashMap<>();
            _result.put("exceptionCode", exceptionCode);
            resultDeque.push(_result);
        };
        dev.addModbusMasterWriteSingleCoilResponseListener(listener);
        int requestID = dev.modbusMasterWriteSingleCoil(slaveAddress, coilAddress, coilValue);
        reqIDdeque.push(requestID); // Push even if requestID == 0 to avoid blocking the callback listener.

        if (requestID != 0) {
            try {
                result = resultDeque.poll(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
        }
        dev.removeModbusMasterWriteSingleCoilResponseListener(listener);

        return result;
    }

    public static @Nullable Map<String, Object> brickletRS485ModbusMasterWriteSingleCoil(@Nullable ThingActions actions,
            int slaveAddress, long coilAddress, boolean coilValue) throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485ModbusMasterWriteSingleCoil(slaveAddress, coilAddress,
                    coilValue);
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Modbus Master Write Single Register")
    public @ActionOutput(name = "exceptionCode", type = "int") @Nullable Map<String, Object> brickletRS485ModbusMasterWriteSingleRegister(
            @ActionInput(name = "slaveAddress") int slaveAddress,
            @ActionInput(name = "registerAddress") long registerAddress,
            @ActionInput(name = "registerValue") int registerValue) throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }
        int modbusTimeout = ((BigDecimal) h.getConfig().get("masterRequestTimeout")).intValue();

        LinkedBlockingDeque<Integer> reqIDdeque = new LinkedBlockingDeque<>(1);
        LinkedBlockingDeque<@Nullable Map<String, Object>> resultDeque = new LinkedBlockingDeque<>(1);

        ModbusMasterWriteSingleRegisterResponseListener listener = (int reqID, int exceptionCode) -> {
            @Nullable Integer requestID = null;
            try {
                requestID = reqIDdeque.pollFirst(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
            if (requestID == null) {
                resultDeque.push(null);
                return;
            }
            if (requestID != reqID) {
                reqIDdeque.push(requestID);
                return;
            }
            Map<String, Object> _result = new HashMap<>();
            _result.put("exceptionCode", exceptionCode);
            resultDeque.push(_result);
        };
        dev.addModbusMasterWriteSingleRegisterResponseListener(listener);
        int requestID = dev.modbusMasterWriteSingleRegister(slaveAddress, registerAddress, registerValue);
        reqIDdeque.push(requestID); // Push even if requestID == 0 to avoid blocking the callback listener.

        if (requestID != 0) {
            try {
                result = resultDeque.poll(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
        }
        dev.removeModbusMasterWriteSingleRegisterResponseListener(listener);

        return result;
    }

    public static @Nullable Map<String, Object> brickletRS485ModbusMasterWriteSingleRegister(@Nullable ThingActions actions,
            int slaveAddress, long registerAddress, int registerValue) throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485ModbusMasterWriteSingleRegister(slaveAddress,
                    registerAddress, registerValue);
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Modbus Master Write Multiple Coils")
    public @ActionOutput(name = "exceptionCode", type = "int") @Nullable Map<String, Object> brickletRS485ModbusMasterWriteMultipleCoils(
            @ActionInput(name = "slaveAddress") int slaveAddress,
            @ActionInput(name = "startingAddress") long startingAddress, @ActionInput(name = "coils") boolean[] coils)
            throws TinkerforgeException {

        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }
        int modbusTimeout = ((BigDecimal) h.getConfig().get("masterRequestTimeout")).intValue();

        LinkedBlockingDeque<Integer> reqIDdeque = new LinkedBlockingDeque<>(1);
        LinkedBlockingDeque<@Nullable Map<String, Object>> resultDeque = new LinkedBlockingDeque<>(1);

        ModbusMasterWriteMultipleCoilsResponseListener listener = (int reqID, int exceptionCode) -> {
            @Nullable Integer requestID = null;
            try {
                requestID = reqIDdeque.pollFirst(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
            if (requestID == null) {
                resultDeque.push(null);
                return;
            }
            if (requestID != reqID) {
                reqIDdeque.push(requestID);
                return;
            }
            Map<String, Object> _result = new HashMap<>();
            _result.put("exceptionCode", exceptionCode);
            resultDeque.push(_result);
        };
        dev.addModbusMasterWriteMultipleCoilsResponseListener(listener);
        int requestID = dev.modbusMasterWriteMultipleCoils(slaveAddress, startingAddress, coils);
        reqIDdeque.push(requestID); // Push even if requestID == 0 to avoid blocking the callback listener.

        if (requestID != 0) {
            try {
                result = resultDeque.poll(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
        }
        dev.removeModbusMasterWriteMultipleCoilsResponseListener(listener);

        return result;
    }

    public static @Nullable Map<String, Object> brickletRS485ModbusMasterWriteMultipleCoils(@Nullable ThingActions actions,
            int slaveAddress, long startingAddress, boolean[] coils) throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485ModbusMasterWriteMultipleCoils(slaveAddress,
                    startingAddress, coils);
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Modbus Master Write Multiple Registers")
    public @ActionOutput(name = "exceptionCode", type = "int") @Nullable Map<String, Object> brickletRS485ModbusMasterWriteMultipleRegisters(
            @ActionInput(name = "slaveAddress") int slaveAddress,
            @ActionInput(name = "startingAddress") long startingAddress,
            @ActionInput(name = "registers") int[] registers) throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }
        int modbusTimeout = ((BigDecimal) h.getConfig().get("masterRequestTimeout")).intValue();

        LinkedBlockingDeque<Integer> reqIDdeque = new LinkedBlockingDeque<>(1);
        LinkedBlockingDeque<@Nullable Map<String, Object>> resultDeque = new LinkedBlockingDeque<>(1);

        ModbusMasterWriteMultipleRegistersResponseListener listener = (int reqID, int exceptionCode) -> {
            @Nullable Integer requestID = null;
            try {
                requestID = reqIDdeque.pollFirst(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
            if (requestID == null) {
                resultDeque.push(null);
                return;
            }
            if (requestID != reqID) {
                reqIDdeque.push(requestID);
                return;
            }
            Map<String, Object> _result = new HashMap<>();
            _result.put("exceptionCode", exceptionCode);
            resultDeque.push(_result);
        };
        dev.addModbusMasterWriteMultipleRegistersResponseListener(listener);
        int requestID = dev.modbusMasterWriteMultipleRegisters(slaveAddress, startingAddress, registers);
        reqIDdeque.push(requestID); // Push even if requestID == 0 to avoid blocking the callback listener.

        if (requestID != 0) {
            try {
                result = resultDeque.poll(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
        }
        dev.removeModbusMasterWriteMultipleRegistersResponseListener(listener);

        return result;
    }

    public static @Nullable Map<String, Object> brickletRS485ModbusMasterWriteMultipleRegisters(@Nullable ThingActions actions,
            int slaveAddress, long startingAddress, int[] registers) throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485ModbusMasterWriteMultipleRegisters(slaveAddress,
                    startingAddress, registers);
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Modbus Master Read Discrete Inputs")
    public @ActionOutput(name = "exceptionCode", type = "int") @ActionOutput(name = "discreteInputs", type = "boolean[]") @Nullable Map<String, Object> brickletRS485ModbusMasterReadDiscreteInputs(
            @ActionInput(name = "slaveAddress") int slaveAddress,
            @ActionInput(name = "startingAddress") long startingAddress, @ActionInput(name = "count") int count)
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }
        int modbusTimeout = ((BigDecimal) h.getConfig().get("masterRequestTimeout")).intValue();

        LinkedBlockingDeque<Integer> reqIDdeque = new LinkedBlockingDeque<>(1);
        LinkedBlockingDeque<@Nullable Map<String, Object>> resultDeque = new LinkedBlockingDeque<>(1);

        ModbusMasterReadDiscreteInputsResponseListener listener = (int reqID, int exceptionCode,
                boolean[] discreteInputs) -> {
            @Nullable Integer requestID = null;
            try {
                requestID = reqIDdeque.pollFirst(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
            if (requestID == null) {
                resultDeque.push(null);
                return;
            }
            if (requestID != reqID) {
                reqIDdeque.push(requestID);
                return;
            }
            Map<String, Object> _result = new HashMap<>();
            _result.put("exceptionCode", exceptionCode);
            _result.put("discreteInputs", discreteInputs);
            resultDeque.push(_result);
        };
        dev.addModbusMasterReadDiscreteInputsResponseListener(listener);
        int requestID = dev.modbusMasterReadDiscreteInputs(slaveAddress, startingAddress, count);
        reqIDdeque.push(requestID); // Push even if requestID == 0 to avoid blocking the callback listener.

        if (requestID != 0) {
            try {
                result = resultDeque.poll(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
        }
        dev.removeModbusMasterReadDiscreteInputsResponseListener(listener);

        return result;
    }

    public static @Nullable Map<String, Object> brickletRS485ModbusMasterReadDiscreteInputs(@Nullable ThingActions actions,
            int slaveAddress, long startingAddress, int count) throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485ModbusMasterReadDiscreteInputs(slaveAddress,
                    startingAddress, count);
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Modbus Master Read Input Registers")
    public @ActionOutput(name = "exceptionCode", type = "int") @ActionOutput(name = "discreteInputs", type = "int[]") @Nullable Map<String, Object> brickletRS485ModbusMasterReadInputRegisters(
            @ActionInput(name = "slaveAddress") int slaveAddress,
            @ActionInput(name = "startingAddress") long startingAddress, @ActionInput(name = "count") int count)
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }
        int modbusTimeout = ((BigDecimal) h.getConfig().get("masterRequestTimeout")).intValue();

        LinkedBlockingDeque<Integer> reqIDdeque = new LinkedBlockingDeque<>(1);
        LinkedBlockingDeque<@Nullable Map<String, Object>> resultDeque = new LinkedBlockingDeque<>(1);

        ModbusMasterReadInputRegistersResponseListener listener = (int reqID, int exceptionCode, int[] inputRegisters) -> {
            @Nullable Integer requestID = null;
            try {
                requestID = reqIDdeque.pollFirst(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
            if (requestID == null) {
                resultDeque.push(null);
                return;
            }
            if (requestID != reqID) {
                reqIDdeque.push(requestID);
                return;
            }
            Map<String, Object> _result = new HashMap<>();
            _result.put("exceptionCode", exceptionCode);
            _result.put("inputRegisters", inputRegisters);
            resultDeque.push(_result);
        };
        dev.addModbusMasterReadInputRegistersResponseListener(listener);
        int requestID = dev.modbusMasterReadInputRegisters(slaveAddress, startingAddress, count);
        reqIDdeque.push(requestID); // Push even if requestID == 0 to avoid blocking the callback listener.

        if (requestID != 0) {
            try {
                result = resultDeque.poll(modbusTimeout, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
            }
        }
        dev.removeModbusMasterReadInputRegistersResponseListener(listener);

        return result;
    }

    public static @Nullable Map<String, Object> brickletRS485ModbusMasterReadInputRegisters(@Nullable ThingActions actions,
            int slaveAddress, long startingAddress, int count) throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485ModbusMasterReadInputRegisters(slaveAddress,
                    startingAddress, count);
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Read UID")
    public @ActionOutput(name = "uid", type = "long") Map<String, Object> brickletRS485ReadUID()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();

        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }
        long value = dev.readUID();

        result.put("uid", value);
        return result;
    }

    public static Map<String, Object> brickletRS485ReadUID(@Nullable ThingActions actions) throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485ReadUID();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Get Chip Temperature")
    public @ActionOutput(name = "temperature", type = "int") Map<String, Object> brickletRS485GetChipTemperature()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();
        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }
        int value = dev.getChipTemperature();

        result.put("temperature", value);
        return result;
    }

    public static Map<String, Object> brickletRS485GetChipTemperature(@Nullable ThingActions actions)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485GetChipTemperature();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Get Status LED Config")
    public @ActionOutput(name = "config", type = "int") Map<String, Object> brickletRS485GetStatusLEDConfig()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();
        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }
        int value = dev.getStatusLEDConfig();

        result.put("config", value);
        return result;
    }

    public static Map<String, Object> brickletRS485GetStatusLEDConfig(@Nullable ThingActions actions)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485GetStatusLEDConfig();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Get Bootloader Mode")
    public @ActionOutput(name = "mode", type = "int") Map<String, Object> brickletRS485GetBootloaderMode()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();
        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }
        int value = dev.getBootloaderMode();

        result.put("mode", value);
        return result;
    }

    public static Map<String, Object> brickletRS485GetBootloaderMode(@Nullable ThingActions actions)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485GetBootloaderMode();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Get SPITFP Error Count")
    public @ActionOutput(name = "errorCountAckChecksum", type = "long") @ActionOutput(name = "errorCountMessageChecksum", type = "long") @ActionOutput(name = "errorCountFrame", type = "long") @ActionOutput(name = "errorCountOverflow", type = "long") Map<String, Object> brickletRS485GetSPITFPErrorCount()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();
        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }
        BrickletRS485.SPITFPErrorCount value = dev.getSPITFPErrorCount();

        result.put("errorCountAckChecksum", value.errorCountAckChecksum);
        result.put("errorCountMessageChecksum", value.errorCountMessageChecksum);
        result.put("errorCountFrame", value.errorCountFrame);
        result.put("errorCountOverflow", value.errorCountOverflow);
        return result;
    }

    public static Map<String, Object> brickletRS485GetSPITFPErrorCount(@Nullable ThingActions actions)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485GetSPITFPErrorCount();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }

    @RuleAction(label = "Get Identity")
    public @ActionOutput(name = "uid", type = "String") @ActionOutput(name = "connectedUid", type = "String") @ActionOutput(name = "position", type = "char") @ActionOutput(name = "hardwareVersion", type = "int[]") @ActionOutput(name = "firmwareVersion", type = "int[]") @ActionOutput(name = "deviceIdentifier", type = "int") Map<String, Object> brickletRS485GetIdentity()
            throws TinkerforgeException {
        Map<String, Object> result = new HashMap<>();
        if(handler == null) {
            return result;
        }
        DeviceHandler h = (@NonNull DeviceHandler)handler;

        @Nullable BrickletRS485Wrapper dev = ((@Nullable BrickletRS485Wrapper)h.getDevice());
        if(dev == null) {
            return result;
        }
        BrickletRS485.Identity value = dev.getIdentity();

        result.put("uid", value.uid);
        result.put("connectedUid", value.connectedUid);
        result.put("position", value.position);
        result.put("hardwareVersion", value.hardwareVersion);
        result.put("firmwareVersion", value.firmwareVersion);
        result.put("deviceIdentifier", value.deviceIdentifier);
        return result;
    }

    public static Map<String, Object> brickletRS485GetIdentity(@Nullable ThingActions actions)
            throws TinkerforgeException {
        if (actions instanceof BrickletRS485Actions) {
            return ((BrickletRS485Actions) actions).brickletRS485GetIdentity();
        } else {
            throw new IllegalArgumentException("Instance is not an BrickletRS485Actions class.");
        }
    }
}

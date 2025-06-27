# Home Assistant Add-on: MPP Solar Monitor

Monitor your MPP Solar inverter and automatically publish sensor data to Home Assistant via MQTT.

## About

This add-on connects to your MPP Solar inverter via USB/HID or USB-Serial connection and publishes real-time data to Home Assistant through MQTT with automatic device discovery.

## Installation

1. Add this repository to your Home Assistant:
   - Navigate to Supervisor → Add-on Store
   - Click the menu (⋮) → Repositories
   - Add: `https://github.com/9991119990/mpp-solar-addon-correct`

2. Install the "MPP Solar Monitor" add-on

3. Configure the add-on (see Configuration section below)

4. Start the add-on

## Configuration

```yaml
device_path: "/dev/hidraw0"
protocol: "PI16"
baud_rate: 2400
mqtt_host: "core-mosquitto"
mqtt_port: 1883
mqtt_username: ""
mqtt_password: ""
device_name: "MPP Solar Inverter"
scan_interval: 30
debug: false
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `device_path` | Path to the device (HID or serial) | `/dev/hidraw0` |
| `protocol` | Communication protocol | `PI16` |
| `baud_rate` | Serial baud rate (for ttyUSB devices) | `2400` |
| `mqtt_host` | MQTT broker hostname | `core-mosquitto` |
| `mqtt_port` | MQTT broker port | `1883` |
| `mqtt_username` | MQTT username (optional) | `""` |
| `mqtt_password` | MQTT password (optional) | `""` |
| `device_name` | Friendly name for the device | `MPP Solar Inverter` |
| `scan_interval` | Data collection interval (seconds) | `30` |
| `debug` | Enable debug logging | `false` |

### Device Path Options

- **HID devices**: `/dev/hidraw0`, `/dev/hidraw1`, etc.
- **USB Serial**: `/dev/ttyUSB0`, `/dev/ttyUSB1`, etc.
- **Built-in Serial**: `/dev/ttyAMA0`

### Protocol Options

- **PI16**: Recommended for most MPP Solar inverters
- **PI30**: For older models or alternative communication
- **PI18**: Additional protocol support

## Supported Sensors

The add-on automatically creates the following sensors in Home Assistant:

### Power & Energy
- **Grid Voltage & Frequency**
- **AC Output Voltage, Frequency & Power**
- **PV Input Voltage, Current & Power**
- **Load Percentage**

### Battery Monitoring
- **Battery Voltage & Capacity**
- **Battery Charging/Discharge Current**

### System Status
- **Inverter Temperature**
- **Device Availability Status**

## Troubleshooting

### Add-on won't start

1. Check the add-on logs for specific error messages
2. Verify your inverter is connected via USB
3. Ensure the device path is correct

### Device not found

Check available devices with add-on logs or SSH:
```bash
ls -la /dev/hidraw* /dev/ttyUSB* /dev/ttyAMA*
```

### Communication issues

Test communication manually:
```bash
mpp-solar -p /dev/hidraw0 -P PI16 -c QPIGS
```

### No sensors appearing in Home Assistant

1. Verify MQTT integration is configured in Home Assistant
2. Check MQTT broker is running (install Mosquitto broker add-on)
3. Enable debug logging to see detailed MQTT messages
4. Restart the add-on after configuration changes

### Permission denied errors

The add-on runs with necessary privileges. If you encounter permission issues:
1. Check if the device exists at the specified path
2. Try different device paths
3. Restart the add-on

## Support

For issues and support:
- Check the [GitHub Issues](https://github.com/9991119990/mpp-solar-addon-correct/issues)
- Enable debug logging for detailed troubleshooting information
- Include add-on logs when reporting issues

## Credits

Based on the excellent [mpp-solar](https://github.com/jblance/mpp-solar) library by jblance.
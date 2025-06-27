# MPP Solar Monitor Add-on Repository

[![GitHub release](https://img.shields.io/github/release/9991119990/mpp-solar-addon-correct.svg)](https://github.com/9991119990/mpp-solar-addon-correct/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Home Assistant add-on for monitoring MPP Solar inverters with full HA OS compatibility.

## Installation

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2F9991119990%2Fmpp-solar-addon-correct)

### Manual Installation

1. **Add this repository to your Home Assistant:**
   - Navigate to **Supervisor** → **Add-on Store**
   - Click **⋮** (menu) → **Repositories**
   - Add: `https://github.com/9991119990/mpp-solar-addon-correct`

2. **Install the add-on:**
   - Find **"MPP Solar Monitor"** in the add-on store
   - Click **Install**

3. **Configure and start:**
   - Configure device path and MQTT settings
   - Click **Start**

## Features

- ✅ **Official HA add-on structure** following Home Assistant standards
- ✅ **Automatic device discovery** via MQTT with HA integration
- ✅ **Multiple protocol support** (PI16, PI30, PI18)
- ✅ **Multi-device support** (HID, USB-Serial, built-in serial)
- ✅ **Real-time monitoring** with configurable scan intervals
- ✅ **Robust error handling** and automatic recovery
- ✅ **Debug logging** for troubleshooting
- ✅ **Graceful shutdown** with proper signal handling

## Quick Setup

1. **Connect your MPP Solar inverter** via USB
2. **Install the add-on** from this repository
3. **Configure device path** (usually `/dev/hidraw0` for USB-HID)
4. **Set MQTT broker** (usually `core-mosquitto`)
5. **Start monitoring** and check logs

## Configuration Example

```yaml
device_path: "/dev/hidraw0"
protocol: "PI16"
mqtt_host: "core-mosquitto"
mqtt_port: 1883
scan_interval: 30
debug: false
```

## Supported Devices

### Tested Hardware
- **PIP5048MG** ✅
- **EASUN Inverters** ✅  
- **Most MPP Solar compatible inverters** ✅

### Connection Types
- **USB-HID**: `/dev/hidraw0`, `/dev/hidraw1`
- **USB-Serial**: `/dev/ttyUSB0`, `/dev/ttyUSB1`
- **Built-in Serial**: `/dev/ttyAMA0`

### Protocols
- **PI16**: Recommended for most modern inverters
- **PI30**: For older/alternative models
- **PI18**: Additional protocol option

## Sensors Created

The add-on automatically creates these sensors in Home Assistant:

### Power System
- Grid Voltage & Frequency
- AC Output Voltage, Frequency & Power
- PV Input Voltage, Current & Power
- Load Percentage

### Battery System
- Battery Voltage & Capacity
- Battery Charging/Discharge Current

### System Monitoring
- Inverter Temperature
- Device Availability Status

## Troubleshooting

### Device Detection
```bash
# Check available devices
ls -la /dev/hidraw* /dev/ttyUSB*

# Test communication
mpp-solar -p /dev/hidraw0 -P PI16 -c QPIGS
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Add-on not visible | Enable Advanced Mode in user profile |
| Device not found | Check USB connection and device path |
| No MQTT data | Verify Mosquitto broker is running |
| Permission denied | Add-on runs with required privileges automatically |
| Communication fails | Try different protocols (PI16, PI30, PI18) |

### Debug Mode

Enable debug logging in configuration:
```yaml
debug: true
```

This provides detailed information about:
- Device communication attempts
- MQTT message publishing
- Data parsing and sensor mapping
- Error conditions and recovery

## Requirements

- **Home Assistant OS** or **Home Assistant Supervised**
- **MPP Solar compatible inverter** with USB connection
- **MQTT broker** (Mosquitto add-on recommended)
- **MQTT integration** configured in Home Assistant

## Support & Contributing

### Getting Help
1. **Check the [troubleshooting guide](mpp-solar-monitor/README.md)**
2. **Enable debug logging** for detailed information
3. **Search existing [GitHub Issues](https://github.com/9991119990/mpp-solar-addon-correct/issues)**
4. **Create a new issue** with logs and configuration

### Contributing
- **Bug reports**: Include logs and configuration details
- **Feature requests**: Describe use case and benefits
- **Pull requests**: Follow existing code style and patterns

## Credits

- Based on the [mpp-solar](https://github.com/jblance/mpp-solar) library by jblance
- Follows [Home Assistant Add-on Development](https://developers.home-assistant.io/docs/add-ons/) guidelines
- Inspired by the Home Assistant community's work on solar monitoring

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**⭐ If this add-on helps you monitor your solar system, please give it a star!**
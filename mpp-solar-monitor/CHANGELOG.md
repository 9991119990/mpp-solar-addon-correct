# Changelog

## [1.0.4] - 2025-01-27

### Added
- Complete rewrite following official Home Assistant add-on structure
- Proper s6-overlay service management
- Enhanced error handling and graceful shutdown
- Signal handling for clean shutdown
- Comprehensive device detection and testing
- Improved MQTT availability status
- Debug logging option for troubleshooting

### Fixed
- Corrected repository structure to match official HA standards
- Fixed Dockerfile with proper base images and labels
- Improved configuration schema validation
- Enhanced device path detection and permissions
- Better error recovery and connection stability

### Technical Changes
- Moved to rootfs/ structure for proper file organization
- Added s6 service supervision with run/finish scripts
- Implemented proper signal handling for graceful shutdown
- Enhanced MQTT discovery with availability topics
- Improved device serial detection for unique identification
- Added comprehensive logging and debug capabilities

### Supported Features
- Multiple device types (HID, USB-Serial, built-in serial)
- Protocol support: PI16, PI30, PI18
- Automatic Home Assistant device discovery
- Real-time sensor monitoring with configurable intervals
- Robust error handling and connection recovery
- Debug mode for detailed troubleshooting

## [1.0.3] - 2025-01-27

### Fixed
- Repository structure corrections
- Basic MQTT functionality

## [1.0.2] - 2025-01-27

### Added
- Initial add-on implementation
- Basic MPP Solar monitoring capabilities
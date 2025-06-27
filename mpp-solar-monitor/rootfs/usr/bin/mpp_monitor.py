#!/usr/bin/env python3
"""
MPP Solar Monitor for Home Assistant Add-on
Monitors inverter and publishes data to MQTT with Home Assistant discovery
"""

import os
import time
import json
import logging
import subprocess
import paho.mqtt.client as mqtt
import sys
import signal

class MPPSolarMonitor:
    def __init__(self):
        # Configuration from environment variables
        self.device_path = os.getenv('DEVICE_PATH', '/dev/hidraw0')
        self.protocol = os.getenv('PROTOCOL', 'PI16')
        self.baud_rate = os.getenv('BAUD_RATE', '2400')
        self.mqtt_host = os.getenv('MQTT_HOST', 'core-mosquitto')
        self.mqtt_port = int(os.getenv('MQTT_PORT', '1883'))
        self.mqtt_username = os.getenv('MQTT_USERNAME', '')
        self.mqtt_password = os.getenv('MQTT_PASSWORD', '')
        self.device_name = os.getenv('DEVICE_NAME', 'MPP Solar Inverter')
        self.scan_interval = int(os.getenv('SCAN_INTERVAL', '30'))
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'
        
        # Setup logging
        log_level = logging.DEBUG if self.debug else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # MQTT setup
        self.mqtt_client = None
        self.connected = False
        self.base_topic = "homeassistant/sensor/mpp_solar"
        self.discovery_prefix = "homeassistant"
        
        # Shutdown flag
        self.shutdown = False
        
        # Sensor definitions
        self.sensors = {
            'grid_voltage': {'unit': 'V', 'device_class': 'voltage', 'name': 'Grid Voltage'},
            'grid_frequency': {'unit': 'Hz', 'device_class': 'frequency', 'name': 'Grid Frequency'},
            'ac_output_voltage': {'unit': 'V', 'device_class': 'voltage', 'name': 'AC Output Voltage'},
            'ac_output_frequency': {'unit': 'Hz', 'device_class': 'frequency', 'name': 'AC Output Frequency'},
            'ac_output_active_power': {'unit': 'W', 'device_class': 'power', 'name': 'AC Output Power'},
            'ac_output_apparent_power': {'unit': 'VA', 'device_class': 'apparent_power', 'name': 'AC Output Apparent Power'},
            'battery_voltage': {'unit': 'V', 'device_class': 'voltage', 'name': 'Battery Voltage'},
            'battery_capacity': {'unit': '%', 'device_class': 'battery', 'name': 'Battery Capacity'},
            'battery_discharge_current': {'unit': 'A', 'device_class': 'current', 'name': 'Battery Discharge Current'},
            'battery_charging_current': {'unit': 'A', 'device_class': 'current', 'name': 'Battery Charging Current'},
            'inverter_heat_sink_temperature': {'unit': '°C', 'device_class': 'temperature', 'name': 'Inverter Temperature'},
            'pv_input_voltage': {'unit': 'V', 'device_class': 'voltage', 'name': 'PV Input Voltage'},
            'pv_input_current': {'unit': 'A', 'device_class': 'current', 'name': 'PV Input Current'},
            'pv_input_power': {'unit': 'W', 'device_class': 'power', 'name': 'PV Input Power'},
            'load_percentage': {'unit': '%', 'device_class': 'power_factor', 'name': 'Load Percentage'},
        }

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.shutdown = True

    def connect_mqtt(self):
        """Connect to MQTT broker"""
        try:
            self.mqtt_client = mqtt.Client()
            
            if self.mqtt_username:
                self.mqtt_client.username_pw_set(self.mqtt_username, self.mqtt_password)
            
            self.mqtt_client.on_connect = self.on_mqtt_connect
            self.mqtt_client.on_disconnect = self.on_mqtt_disconnect
            
            self.logger.info(f"Connecting to MQTT broker {self.mqtt_host}:{self.mqtt_port}")
            self.mqtt_client.connect(self.mqtt_host, self.mqtt_port, 60)
            self.mqtt_client.loop_start()
            
            # Wait for connection
            for i in range(30):  # Wait up to 30 seconds
                if self.connected or self.shutdown:
                    break
                time.sleep(1)
            
            return self.connected
        except Exception as e:
            self.logger.error(f"Failed to connect to MQTT: {e}")
            return False

    def on_mqtt_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info("✅ Connected to MQTT broker")
            self.connected = True
            self.publish_discovery()
        else:
            self.logger.error(f"❌ Failed to connect to MQTT, return code {rc}")
            self.connected = False

    def on_mqtt_disconnect(self, client, userdata, rc):
        self.logger.warning("Disconnected from MQTT broker")
        self.connected = False

    def get_device_serial(self):
        """Get device serial for unique identification"""
        try:
            cmd = ['mpp-solar', '-p', self.device_path, '-P', self.protocol, '-c', 'QID']
            if self.device_path.startswith('/dev/ttyUSB'):
                cmd.extend(['-b', self.baud_rate])
                
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Try to extract serial from output
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'serial' in line.lower() or 'id' in line.lower():
                        parts = line.split(':')
                        if len(parts) > 1:
                            return parts[1].strip()
            
            # Fallback to device path hash
            return f"mpp_solar_{hash(self.device_path) % 10000:04d}"
        except Exception:
            return f"mpp_solar_{hash(self.device_path) % 10000:04d}"

    def publish_discovery(self):
        """Publish Home Assistant discovery messages"""
        self.logger.info("Publishing Home Assistant discovery messages...")
        
        device_serial = self.get_device_serial()
        device_info = {
            "identifiers": [f"mpp_solar_{device_serial}"],
            "name": self.device_name,
            "manufacturer": "MPP Solar",
            "model": "Solar Inverter",
            "sw_version": "1.0.4"
        }
        
        published_count = 0
        for sensor_key, sensor_info in self.sensors.items():
            try:
                discovery_topic = f"{self.discovery_prefix}/sensor/mpp_solar_{sensor_key}/config"
                
                discovery_payload = {
                    "name": f"MPP Solar {sensor_info['name']}",
                    "unique_id": f"mpp_solar_{device_serial}_{sensor_key}",
                    "state_topic": f"{self.base_topic}/{sensor_key}/state",
                    "unit_of_measurement": sensor_info['unit'],
                    "device_class": sensor_info['device_class'],
                    "state_class": "measurement",
                    "device": device_info,
                    "availability_topic": f"{self.base_topic}/availability",
                    "payload_available": "online",
                    "payload_not_available": "offline"
                }
                
                self.mqtt_client.publish(discovery_topic, json.dumps(discovery_payload), retain=True)
                published_count += 1
                
            except Exception as e:
                self.logger.error(f"Error publishing discovery for {sensor_key}: {e}")
        
        # Publish availability
        self.mqtt_client.publish(f"{self.base_topic}/availability", "online", retain=True)
        
        self.logger.info(f"Published discovery for {published_count}/{len(self.sensors)} sensors")

    def get_inverter_data(self):
        """Get data from inverter using mpp-solar"""
        try:
            cmd = ['mpp-solar', '-p', self.device_path, '-P', self.protocol, '-c', 'QPIGS']
            
            # Add baud rate for serial devices
            if self.device_path.startswith('/dev/ttyUSB'):
                cmd.extend(['-b', self.baud_rate])
            
            self.logger.debug(f"Running command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                self.logger.debug(f"Command output: {result.stdout}")
                return self.parse_mpp_output(result.stdout)
            else:
                self.logger.error(f"Command failed (rc={result.returncode}): {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            self.logger.error("Command timed out")
            return None
        except Exception as e:
            self.logger.error(f"Error getting inverter data: {e}")
            return None

    def parse_mpp_output(self, output):
        """Parse mpp-solar output into structured data"""
        if not output:
            return {}
            
        data = {}
        lines = output.strip().split('\n')
        
        # Find data section (after dashes line)
        data_start = False
        for line in lines:
            if '----' in line:
                data_start = True
                continue
                
            if data_start and line.strip() and ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    param_name = parts[0].strip()
                    value_part = parts[1].strip()
                    
                    # Extract value (first word)
                    value_parts = value_part.split()
                    if value_parts:
                        try:
                            value_str = value_parts[0]
                            # Try to convert to number
                            if '.' in value_str:
                                value = float(value_str)
                            else:
                                value = int(value_str)
                            
                            # Create entity-friendly key
                            key = param_name.lower().replace(' ', '_').replace('-', '_')
                            key = ''.join(c for c in key if c.isalnum() or c == '_')
                            
                            data[key] = value
                            self.logger.debug(f"Parsed: {key} = {value}")
                            
                        except ValueError:
                            self.logger.debug(f"Non-numeric value skipped: {param_name} = {value_part}")
        
        return data

    def publish_sensor_data(self, data):
        """Publish sensor data to MQTT"""
        if not data:
            self.logger.warning("No data to publish")
            return
        
        published_count = 0
        
        for sensor_key in self.sensors.keys():
            if sensor_key in data:
                value = data[sensor_key]
                topic = f"{self.base_topic}/{sensor_key}/state"
                
                try:
                    self.mqtt_client.publish(topic, str(value))
                    published_count += 1
                    self.logger.debug(f"Published {sensor_key}: {value}")
                except Exception as e:
                    self.logger.error(f"Failed to publish {sensor_key}: {e}")
        
        if published_count > 0:
            self.logger.info(f"📊 Published {published_count} sensor values")
        else:
            self.logger.warning("No sensor data published - check sensor mappings")
            if self.debug:
                self.logger.debug(f"Available data: {list(data.keys())}")
                self.logger.debug(f"Expected sensors: {list(self.sensors.keys())}")

    def run(self):
        """Main monitoring loop"""
        # Setup signal handlers
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        
        self.logger.info("🚀 Starting MPP Solar Monitor")
        self.logger.info(f"Device: {self.device_path}")
        self.logger.info(f"Protocol: {self.protocol}")
        self.logger.info(f"MQTT: {self.mqtt_host}:{self.mqtt_port}")
        
        # Connect to MQTT
        if not self.connect_mqtt():
            self.logger.error("Failed to connect to MQTT, exiting")
            return 1
        
        self.logger.info(f"⏱️ Monitoring every {self.scan_interval} seconds")
        
        consecutive_failures = 0
        max_failures = 5
        
        try:
            while not self.shutdown:
                try:
                    # Get inverter data
                    data = self.get_inverter_data()
                    
                    if data:
                        # Publish to MQTT
                        self.publish_sensor_data(data)
                        consecutive_failures = 0
                    else:
                        consecutive_failures += 1
                        self.logger.warning(f"No data received from inverter (failure {consecutive_failures}/{max_failures})")
                        
                        if consecutive_failures >= max_failures:
                            self.logger.error("Too many consecutive failures, publishing offline status")
                            self.mqtt_client.publish(f"{self.base_topic}/availability", "offline", retain=True)
                    
                    # Wait for next scan (with shutdown check)
                    for _ in range(self.scan_interval):
                        if self.shutdown:
                            break
                        time.sleep(1)
                        
                except Exception as e:
                    self.logger.error(f"Error in monitoring loop: {e}")
                    consecutive_failures += 1
                    time.sleep(5)
        
        finally:
            # Cleanup
            self.logger.info("Shutting down...")
            if self.mqtt_client and self.connected:
                self.mqtt_client.publish(f"{self.base_topic}/availability", "offline", retain=True)
                self.mqtt_client.loop_stop()
                self.mqtt_client.disconnect()
            
            self.logger.info("Monitor stopped")
        
        return 0

if __name__ == "__main__":
    monitor = MPPSolarMonitor()
    sys.exit(monitor.run())
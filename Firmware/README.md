These are the firmware files for all the board versions. The .bin files are used for the web flasher and OTA updates.

## Building from source

The root `platformio.ini` defines two supported environments:

- `control_board_v4`: ESP32-S3-WROOM-1 used by Control Board V4/V4.1.
- `driver_board_v1`: ESP32-WROOM-32 used by Driver Board V1.

Both are configured for the settings recovered from the published v1.2.1
images: 4 MB flash, DIO at 80 MHz, the Arduino `min_spiffs` dual-OTA partition
layout, and no PSRAM. The S3 environment also enables its native USB CDC serial
port. Dependencies and the PioArduino ESP32 platform are pinned in
`platformio.ini`.

```sh
make control
make driver
make build-all
```

Direct PlatformIO equivalents are:

```sh
pio run -e control_board_v4
pio run -e driver_board_v1
```

The original, extensionless Arduino sketch files remain the canonical firmware
source. The files under `src/` are PlatformIO adapters: they provide the
forward declarations that Arduino's sketch preprocessor used to generate, then
include the corresponding original source. This avoids maintaining a second,
diverging copy of each 1,800-line sketch.

### Flashing and binary types

```sh
make upload                                      # control board, detected port
make upload ENV=driver_board_v1 PORT=/dev/ttyUSB0
make monitor PORT=/dev/ttyUSB0
make ota-bin ENV=control_board_v4
make factory-bin ENV=control_board_v4
```

`firmware.bin`/`*_OTA.bin` starts at flash address `0x10000` and is suitable for
the firmware's OTA updater or a web flasher that supplies the remaining boot
components. Do not write that app-only file at address `0x0000`.

`firmware.factory.bin`/`*_factory.bin` is the complete initial-flash image and
is written at address `0x0000`. On the original ESP32 it contains padding up to
the chip's `0x1000` bootloader location; on ESP32-S3 the bootloader itself is at
`0x0000`. `make upload` handles the individual component offsets automatically.

The checked-in release binaries were produced with Arduino-ESP32 3.3.1 / ESP-IDF
5.5.1. The PlatformIO project uses the pinned, Python-3.14-compatible patch
successor Arduino-ESP32 3.3.8 / ESP-IDF 5.5.4, so newly generated files are not
expected to be byte-for-byte identical to the releases even though the board,
partition, and source configuration is equivalent.

# Changelog:

### 1.2.1
- Changed OTA-Update URL

### 1.2.0
- Added support for upcoming Respooler Pro with precise servo control
- App needs to be uptated to 1.7.0

### 1.1.2
- Added ability to exit Auto-Stop state via long button press
- Fixed issue where speed would decrease after restart

### 1.1.1
- Added support for Control Board V4
- Increased LED brightness

### 1.1.0
- Added option to choose what amount to transfer
- Lowered default fan speed

### 1.0.0
- Added option to pause the Respooler
- Unified current state logic
- Bug fixes

### 0.9.3
- Increased speed and motor strength
- Warning sound in case of Auto-Stop
- Fixed issue where motor strength would decrease after Auto-Stop

### 0.9.2
- Improved stability of Bluetooth connection
  
### 0.9.1
- Fixed bug where High-Speed setting would change after restart
- Bug fixes for Control Board V3
  
### 0.9.0
- First beta version

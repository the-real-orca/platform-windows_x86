# Windows x86: development platform for [PlatformIO](http://platformio.org)
[![Build status](https://ci.appveyor.com/api/projects/status/4tqtddjgafvwawmn/branch/develop?svg=true)](https://ci.appveyor.com/project/ivankravets/platform-windows-x86/branch/develop)

Windows x86 (32-bit) is a metafamily of graphical operating systems developed and marketed by Microsoft. Using host OS (Windows, Linux 32/64 or Mac OS X) you can build native application for Windows x86 platform.

* [Home](http://platformio.org/platforms/windows_x86) (home page in PlatformIO Platform Registry)
* [Documentation](http://docs.platformio.org/page/platforms/windows_x86.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = windows_x86
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/platformio/platform-windows_x86.git
board = ...
...
```

# Configuration

Please navigate to [documentation](http://docs.platformio.org/page/platforms/windows_x86.html).

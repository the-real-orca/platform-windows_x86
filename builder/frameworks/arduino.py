# Copyright (c) 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Arduino

Arduino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.

http://arduino.cc/en/Reference/HomePage
"""


# Extends: https://github.com/platformio/platform-espressif8266/blob/develop/builder/main.py

from os.path import isdir, join

from SCons import Builder, Util
from SCons.Script import DefaultEnvironment


def scons_patched_match_splitext(path, suffixes=None):
    """
    Patch SCons Builder, append $OBJSUFFIX to the end of each target
    """
    tokens = Util.splitext(path)
    if suffixes and tokens[1] and tokens[1] in suffixes:
        return (path, tokens[1])
    return tokens


Builder.match_splitext = scons_patched_match_splitext


env = DefaultEnvironment()
platform = env.PioPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-arduinoespressif8266")
assert isdir(FRAMEWORK_DIR)


env.Append(
    ASFLAGS=["-x", "assembler-with-cpp"],

    CFLAGS=[
        "-std=gnu99",
        "-nostdlib",
        "-fno-common",
        "-g",
        "-m32",
        "-Wall"
    ],

    CCFLAGS=[
        "-std=c++11",
        "-Os",  # optimize for size
        "-U__STRICT_ANSI__",
        "-ffunction-sections",
        "-fdata-sections",
        "-Wall",
        "-nostdlib",
        "-fno-common",
        "-g",
        "-m32",
        "-Wall"
    ],

    CXXFLAGS=[
        "-Wno-error=format-security",
	    "-include", "common/c_types.h",
    	"-include", "common/mock.h"
    ],

    LINKFLAGS=[
        "-Os",
        "-Wl,--no-check-sections",
        "-Wl,-static",
        "-Wl,--gc-sections",
        "-Wl,-wrap,system_restart_local",
        "-Wl,-wrap,spi_flash_read",
        "-u", "app_entry",
        "-u", "_printf_float",
        "-u", "_scanf_float"
    ],

    CPPDEFINES=[
        "__ets__",
        "ICACHE_FLASH",
        ("ARDUINO_BOARD", '\\"PLATFORMIO_%s\\"' % env.BoardConfig().id.upper()),
        "FLASHMODE_${BOARD_FLASH_MODE.upper()}",
        ("LWIP_IPV6",0),
        ("HTTPCLIENT_1_1_COMPATIBLE",0)
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "tests", "host"),
        join(FRAMEWORK_DIR, "tests", "host", "common"),
        join(FRAMEWORK_DIR, "tests", "host", "sys"),
        join(FRAMEWORK_DIR, "cores", "esp8266"),
        join(FRAMEWORK_DIR, "tools", "sdk", "include"),
        join(FRAMEWORK_DIR, "tools", "sdk", "lwip2", "include"),
#TODO        join(FRAMEWORK_DIR, "libraries", "*"),
#TODO        join(FRAMEWORK_DIR, "libraries", "*", "src")
    ],

    LIBPATH=[
#TODO        join(FRAMEWORK_DIR, "tools", "sdk", "lib"),
#TODO        join(FRAMEWORK_DIR, "tools", "sdk", "ld"),
    ],

    LIBS=[
    ],

    LIBSOURCE_DIRS=[
#TODO        join(FRAMEWORK_DIR, "libraries")
    ]
)


# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])

flatten_cppdefines = env.Flatten(env['CPPDEFINES'])


#
# Target: Build Core Library
#

libs = []
print("variant: " + env.BoardConfig().get("build.variant") );
print("core: " + env.BoardConfig().get("build.core") );

if "build.variant" in env.BoardConfig():
    env.Append(
        CPPPATH=[
            join(FRAMEWORK_DIR, "variants",
                 env.BoardConfig().get("build.variant"))
        ]
    )
    libs.append(env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join(FRAMEWORK_DIR, "variants", env.BoardConfig().get("build.variant"))
    ))

"""
libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkArduinoSim"),
    join(FRAMEWORK_DIR, "tests", "host", "common", "MockSerial.cpp")
))
"""

env.Prepend(LIBS=libs)

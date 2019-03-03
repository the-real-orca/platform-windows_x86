# Copyright 2014-present PlatformIO <contact@platformio.org>
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
    Builder for Windows x86 / 32bit
"""

from SCons.Script import AlwaysBuild, Default, DefaultEnvironment

from platformio.util import get_systype

env = DefaultEnvironment()

env.Replace(
    _BINPREFIX="",
    AR="${_BINPREFIX}ar",
    AS="${_BINPREFIX}as",
    CC="${_BINPREFIX}gcc",
    CXX="${_BINPREFIX}g++",
    GDB="${_BINPREFIX}gdb",
    OBJCOPY="${_BINPREFIX}objcopy",
    RANLIB="${_BINPREFIX}ranlib",
    SIZETOOL="${_BINPREFIX}size",

    SIZEPRINTCMD='$SIZETOOL $SOURCES',
    PROGSUFFIX=".exe"
)

env.Append(
    LINKFLAGS=[
        "-static",
        "-static-libgcc",
        "-static-libstdc++"
    ]
)

if get_systype() == "darwin_x86_64":
    env.Replace(
        _BINPREFIX="i586-mingw32-"
    )
elif get_systype() in ("linux_x86_64", "linux_i686"):
    env.Replace(
        _BINPREFIX="i686-w64-mingw32-"
    )

#
# Target: Build executable program
#

target_bin = env.BuildProgram()

#
# Target: Print binary size
#

target_size = env.Alias("size", target_bin, env.VerboseAction(
    "$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)


#
# Target: Execute -> run program
#

target_execute = env.Alias(["upload", "execute"], target_bin, env.VerboseAction(
    ".\$SOURCE", "Execute $SOURCE"))
AlwaysBuild(target_execute)


#
# Default targets
#

Default([target_bin])

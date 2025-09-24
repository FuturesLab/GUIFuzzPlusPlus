# GUIFuzz++: Grey-box Fuzzing for Desktop GUI Apps 

<img align="right" src=".logo.png" alt="GUIFuzz++ logo" width="240" height="240"/>

This repository provides the source code for **GUIFuzz++**: a prototype grey-box fuzzer for GUI-based applications on Linux.

This work is presented in our paper **[GUIFuzz++: Unleashing Grey-box Fuzzing on Desktop Graphical User Interfacing Applications](https://futures.cs.utah.edu/papers/25ASE.pdf)**, appearing in the 2025 IEEE/ACM International Conference on Automated Software Engineering (ASE'25).

* [Installing GUIFuzz++](#installation)
* [Target Setup](#target-setup)
* [Additional Notes](#additional-notes)
* [VM Image](#vm-image)
* [Bug Trophy Case](#bug-trophy-case)

<br><img align="center" src=".guifuzz++.png" alt="GUIFuzz++ workflow" width="100%"/>
<br>
<br><img align="center" src=".fuzzing.gif" alt="GUIFuzz++ in action" width="100%"/>

<table>
  <tr>
    <td><b>Citing this repository:</b></td>
    <td>
      <code class="rich-diff-level-one">@inproceedings{otto:guifuzzplusplus, title = {GUIFuzz++: Unleashing Grey-box Fuzzing on Desktop Graphical User Interfacing Applications}, author = {Dillon Otto and Tanner Rowlett and Stefan Nagy}, booktitle = {{IEEE/ACM} {International} {Conference} on {Automated} {Software} {Engineering} ({ASE})}, year = {2025},}</code>
    </td>
  </tr>
  <tr>
    <td><b>Maintainers:</b></td>
    <td>Tanner Rowlett (<a href="mailto:u1335967@utah.edu">u1335967@utah.edu</a>) and Stefan Nagy (<a href="mailto:snagy@cs.utah.edu">snagy@cs.utah.edu</a>)</td>
  </tr>
  <tr>
    <td><b>License:</b></td>
    <td><a href="LICENSE">MIT License</a></td>
  </tr>
  <tr>
    <td><b>Disclaimer:</b></td>
    <td>This software is provided as-is with no warranty.</td>
  </tr>
</table>

# Installation
This setup was tested on Ubuntu 24.04.3 LTS. You may run into compiling issues if you have less than 16GB of RAM.

Create a new project folder, e.g.:
```
mkdir guifuzzing
cd guifuzzing
```

## 1. Download QT
GUIFuzz++ has typically been used with Qt `6.8.1`, some apps will work with apt installs of Qt as well.

Download dependencies:
```
sudo apt update
sudo apt install libxcb-cursor0 libxcb-cursor-dev
```

Download and install QT via the online installer. This will require you to login to Qt:
```
wget https://download.qt.io/official_releases/online_installers/qt-online-installer-linux-x64-online.run
chmod +x qt-online-installer-linux-x64-online.run
./qt-online-installer-linux-x64-online.run
```
Under `Installation options` pick the directory you want to install e.g. `/home/guifuzz/guifuzzing/Qt`.

Uncheck anything selected by default and only select `Custom Installation`.

Under `Customize` click the `Show` dropdown, and check `Archive`.

**Extensions**
```
Qt WebEngine 6.8.1
```

**Qt**
Select `Desktop`, `Qt Debug Information Files (optional)`, and the following additional libraries:
```
Qt 6.8.1 
```

**Additional Libraries**
```
Qt 5 Compatibility Module
Qt Charts
Qt Multimedia
Qt Quick 3D
Qt Quick Timeline
Qt Shader Tools
Qt Speech
Qt State Machines
Qt WebChannel
Qt WebSockets
Qt WebView
```

Your installation should require ~7.3GB (11.8GB with Debug Info):

## 2. Install Common Dependencies
```
sudo apt install git make cmake extra-cmake-modules build-essential python3-chardet scrot python3-tk python3-dev python3-pip python3-sphinxcontrib*
```

**NOTE:** Use a venv if you have other python projects/installs:
```sudo pip3 install pyautogui --break-system-packages```

Add user to display users: 
```xhost +SI:localuser:$(whoami)```

## 3. Setup GUIFuzz++
Clone this repo:
```git clone https://github.com/FuturesLab/GUIFuzzPlusPlus.git```

**Build GUIFuzz++**
```
cd GUIFuzzPlusPlus
make -j$(nproc)
```

After this, GUIFuzz++ should be ready to go. You'll want to compile some apps to fuzz using the GUIFuzz++ compilers (`afl-clang-fast`, etc.).

## Target Setup
Setup an app following its repo instructions. For KDE apps you can also use kdesrc-build:

### kdesrc-build
kdesrc-build can be used to build some of the applications GUIFuzz++ was benchmarked on, below are steps to get a KDE app setup.

**Initial Setup**
```
git clone https://invent.kde.org/sdk/kdesrc-build
cd kdesrc-build
./kdesrc-build --initial-setup
```

**Modules**
You will need to create a module for each KDE app you want to build using kdesrc-build.

Add modules to the kdesrc config file: 
```nano ~/.config/kdesrc-buildrc```

#### Example: Kolourpaint
```
module kolourpaint
    repository https://invent.kde.org/graphics/kolourpaint.git
    branch master
    set-env CC /home/guifuzz/guifuzzing/GUIFuzzPlusPlus/afl-clang-fast
    set-env CXX /home/guifuzz/guifuzzing/GUIFuzzPlusPlus/afl-clang-fast++
end module
```

**Build**
```./kdesrc-build kolourpaint```

This will install to `~/kde/` by default.

**NOTE:**
kdesrc-build can be difficult with dependencies, it might be easier to install directly from the application git repo.
You can find more info at `https://community.kde.org/Guidelines_and_HOWTOs/Build_from_source`.


## Building Targets
Before building targets you (may) need to add the custom Qt install to your `PATH` and `CMAKE_PREFIX_PATH`:
```
echo 'export PATH="/home/guifuzz/guifuzzing/Qt/6.8.1/gcc_64/bin:$PATH"' >> ~/.bashrc
echo 'export CMAKE_PREFIX_PATH="/home/guifuzz/guifuzzing/Qt/6.8.1/gcc_64:$CMAKE_PREFIX_PATH"' >> ~/.bashrc
source ~/.bashrc
```

Then follow target repo instructions to build, swap `CC` and `CXX` compilers with GUIFuzz++'s compilers:


#### Example: Umbrello
Umbrello is easiest to setup with Qt5, you'll need these dependencies:
```
sudo apt install qtbase5-dev qttools5-dev qttools5-dev-tools libkf5coreaddons-dev libkf5i18n-dev libkf5kio-dev libkf5archive-dev libkf5completion-dev libkf5config-dev libkf5crash-dev libkf5doctools-dev libkf5iconthemes-dev libkf5texteditor-dev libkf5widgetsaddons-dev libkf5windowsystem-dev libkf5xmlgui-dev
```

Clone and build:
```
git clone https://github.com/KDE/umbrello.git
cd umbrello
mkdir build && cd build

# Set CC & CXX
export CC=/home/guifuzz/guifuzzing/GUIFuzzPlusPlus/afl-clang-fast
export CXX=/home/guifuzz/guifuzzing/GUIFuzzPlusPlus/afl-clang-fast++

cmake -DCMAKE_BUILD_TYPE=Debug ../
make -j$(nproc)
```

The binary should be at:
```umbrello/build/bin/umbrello5```


## Starting a Fuzzing Trial
After you've compiled an app with a GUIFuzz++ compiler you can start a trial with a command like this:
```
/path/to/GUIFuzzPlusPlus/afl-fuzz \
-K /path/to/GUIFuzzPlusPlus/gui_utils/atspi_clicks.py \
-t 100000 -i in -o out -m none -- /path/to/app
```

You need to populate the in directory with seed files. The easiest way to do this is use generate_random_bytes.py in ```GUIFuzzPlusPlus/gui_utils```.
Example usage: ```python3 generate_random_bytes.py 300 seed```
This will generate `300` random bytes (i.e., `100` random `3`-byte interactions; see our paper for details).

Adjust `-t` if needed (indivudal executions can be slow, so `100` seconds is reasonable).

For AFL++, you will likely need to run:
```echo core | sudo tee /proc/sys/kernel/core_pattern```


#### Example: Umbrello
We recommend saving the following in a `.sh` for easier spinup:
```
/home/guifuzz/guifuzzing/GUIFuzzPlusPlus/afl-fuzz \
-K /home/guifuzz/guifuzzing/GUIFuzzPlusPlus/gui_utils/atspi_clicks.py \
-t 100000 -i in -o out -m none -- /home/guifuzz/guifuzzing/targets/umbrello/build/bin/umbrello5
```

# Additional Notes
If an app doesn't compile, try different `CC`/`CXX` options (such as `afl-clang-fast`, `afl-gcc`, `afl-clang`, etc.). 

Certain apps may require adding the custom Qt install to `LD_LIBRARY_PATH`.

If the app opens but doesn't interact, check your `XDG` session type, you need to be using `x11`/`Xorg`:
```
echo $XDG_SESSION_TYPE
x11 # GUIFuzz++ won't work with wayland
```

# VM Image
An Ubuntu 24.04.3 `.qcow2` image with GUIFuzz++ ready to run can be found [on Zenodo](https://zenodo.org/records/17155427?token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjBlZmZhMzVjLTY5NWMtNDE3NS1hMjViLWIxYjRiMmMxMTI4ZSIsImRhdGEiOnt9LCJyYW5kb20iOiI0MmFlNzIzMGRkNmQ4NDZmZWZjNTMwMjc4ZjQyYTJlOCJ9.M1JpuYFrLuUsGPiWisIfIq7VIo3JU14Q9J94Vt9d0M9GpIQylRoMWR7qbkstFs91lGf24YXVIF8M_3U88litiw).
This image also comes with Umbrello fuzz ready so you can see GUIFuzz++ in action!


# Bug Trophy Case
| Decompiler | Reported Bugs |
| ---- | ---- |
| Dia | [GNOME/dia#568](https://gitlab.gnome.org/GNOME/dia/-/issues/568) |
| Glaxnimate | [KDE/glaxnimate#703](https://invent.kde.org/graphics/glaxnimate/-/issues/703), [KDE/glaxnimate#707](https://invent.kde.org/graphics/glaxnimate/-/issues/707) |
| Kcalc | [KDE/kcalc#504679](https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1059230.html) |
| KolourPaint | [KDE/kolourpaint#498550](https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1011862.html), [KDE/kolourpaint#502689](https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1044654.html), [KDE/kolourpaint#504786](https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1059927.html), [KDE/kolourpaint#504787](https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1059930.html) |
| LabPlot2 | [KDE/labplot2#502043](https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1039068.html), [KDE/labplot2#504794](https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1059973.html), [KDE/labplot2#504839](https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1060321.html) |
| LibreCAD | [LibreCAD/LibreCAD#2093](https://github.com/LibreCAD/LibreCAD/issues/2093), [LibreCAD/LibreCAD#2161](https://github.com/LibreCAD/LibreCAD/issues/2161) |
| Mate-Calc | [mate-desktop/mate-calc#226](https://github.com/mate-desktop/mate-calc/issues/226) |
| Plotjuggler | [facontidavide/PlotJuggler#1052](https://github.com/facontidavide/PlotJuggler/issues/1052) |
| QCAD | [QCAD/QCAD#11668](https://qcad.org/rsforum/viewtopic.php?f=33&t=11668) |
| Umbrello | [KDE/umbrello#502347](https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1042174.html), [KDE/umbrello#504939](https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1061349.html), [KDE/umbrello#504940](https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1061350.html), [KDE/umbrello#504941](https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1061353.html), [KDE/umbrello#504942](https://www.mail-archive.com/kde-bugs-dist@kde.org/msg1061354.html) |
| Xcalc | [xorg/xcalc#3](https://gitlab.freedesktop.org/xorg/app/xcalc/-/issues/3), [xorg/xcalc#4](https://gitlab.freedesktop.org/xorg/app/xcalc/-/issues/4) |

If you find new bugs using GUIFuzz++, please let us know!

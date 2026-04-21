Gerrit

git push --no-follow-tags  gerrit HEAD:refs/for/master%topic=HT-41531


# Thins needed to be done once
## Install ADB
    start adb service
## Setup ssh to DHU
Switches on box: on   '
                     ' ''
                     1234
Set the settings to
                linkspeed: 100Mb/s as defined on the box as well
                ipv4: 192.168.1.2
                Netmask: 255.255.255.0




# Connect to DHU
$ picocom -b 115200 /dev/ttyUSB1
    Should show IHU-QNX#

# Connect to HKP
$ picocom -b 115200 /dev/ttyUSB0


# Disconnect
$ ctrl-a ctrl-x

# Connect over ssh

## To login over ssh
    ssh root@192.168.1.1


# SPA2

## slog2info (QNX commando)
Display messages from the system log

- For logging of display driver
    `slog2info -w | grep dimd

- For logging DisplaySafetyMonitor
    slog2info -w | grep DisplaySafetyManager

You can add & to run them in background
slog2info -w | grep DisplaySafetyMonitor &
with this you can run other commands and observe the behaviour

## sw-vsync

sw-vsync -display=1 #dim display you will see yellow background and moving blue pipe
## output sw-vsync self layout 0

sw-vsync -display=2
## output sw-vsync self layout 0

# echo command

echo 4 > /dev/display/dim/state #turn display off
cat /dev/display/dim/state #read state of display
echo 2 > /dev/display/dim/state #turn display on
cat /dev/display/dim/state #read state of display

cat /dev/display/dim/actual_state #read actual state of display, this should be the same as state but if something happens while state change it might be different



QNX
export QNXLM_LICENSE_FILE=3400@flexlm.haleytek.net

./tools/haleytek/qnx/qnx_license_activation.sh
+
Register account at QNX
Request QNX at helpdesk




# Source

## SPA2 Android? QNX?
mkdir ~/sources/haleytek-dhu-15
cd \~/sources/haleytek-dhu-15
repo init -u ssh://source-secure.haleytek.net/haleytek/manifest -m ht_vcc/ht-qc8155-android15-vcc-init.xml --reference ~/sources/haleytek-mirror
repo sync -c -d

cd ~/sources/<manifest-safety-8155>

Saftey drivers (8155 => SPA2)
mkdir -p ~/sources/manifest-safety-8155
cd \~/sources/manifest-safety-8155
repo init -u ssh://source-sync.haleytek.net/haleytek/manifest_safety -b master -m ht_safety_qc8155_init.xml --reference ~/sources/haleytek-mirror
# Syncing should take a couple of minutes if you've setup the mirror properly
repo sync


Building



./tools/haleytek/docker-images/run.py --target safety source safety_build/safety-env.sh 8155
make qnx-tools
make qnx-install



--------------------------------------------------------------------------------

# Build the source code
    cd ~/sources/<manifest-safety-8155>

## Start and enter the docker
    $ ./tools/haleytek/docker-images/run.py --target safety

## Build saftey code
    $safety-ht-433366 source safety_build/safety-env.sh 8155
    $safety-ht-433366 make qnx-tools
    $safety-ht-433366 make qnx-install

## Move binary files to QNX repo
    Copy binaries generated in the manifest-safety to comet repo
    $(manifest-safety-8155) ./tools/haleytek/safety_test_tools/update_local_workspace.py -w ~/sources/haleytek-dhu-15/

# Build Comet QNX
    $ cd ~/sources/<comet-15/haleytek-dhu-15>

## Start and enter the qnx docker
    $ ./tools/haleytek/docker-images/run.py --target qnx

### Build Comet QNX
    $qnx-ht-433366 cd qnx/apps/qnx_ap/
    $qnx-ht-433366 source cvendor/haleytek/setenv_QNX.sh 8155
    $qnx-ht-433366 make`
## Move all(?) fils to flashfiles_out
    $ cd ~/sources/haleytek-dhu-15
    $(haleytek-dhu-15) ./nonhlos/vendor/tools/scripts/copy_build_artifacts.py nonhlos/vendor/haleytek/moose/comet.json nonhlos --out flashfiles_out

## Flashing
    $(haleytek-dhu-15) cd flashfiles_out
    $(haleytek-dhu-15) ./flash_qnx.shx
        It will show < waiting for any device >

## Put the device to fastboot mode
    $ picocom -b 115200 /dev/ttyUSB1
    QNX# reset -f

## After it completes flashing
    $ fastboot reboot

# Running dsm test
## Start device testing docker
    $ cd ~/sources/manifest-safety-8155
    $ ./tools/haleytek/docker-images/run.py --target device-testing

## Running test
    $device-testing-ht-433366 devicetek run-pytest components/safety-display/safety/dsm/test/it/pytests




## More specific test

    devicetek run-pytest components/safety-display/safety/dsm/test/it/pytests/test_dsm_broadcast_heartbeats.py::test_dsm_remove_fault[UXC10]

## Generate device_config.json
    devicetek -l DEBUG generate-config


# Unpack HaleyTek build python file:
    When downloading from https://web.haleytek.net/build_search?limit=10
    Download the "one without " a key
    $ ~/.venvs/azstorage/bin/python artifacts-downloader-





Flash HKP with user debug
when running generate-config it identify moose and thats why the ip is whack


HK


DHU2

QNX
NONHLOS
hyperviser linux guest yocto

ref build vs VCC

~1.1 What is HKP?~
1.2 Do HT add anything to it or do we just download from VCC artifactory?

Test failing
2.1 What is ANR file and why is it failing
2.2 Why is the test failing still even after repo sync?

3.1 Why cant I generate device config? No support for comet?

~4.1 What is NONHLOS and Linux guest?~


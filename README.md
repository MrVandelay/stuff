
slog2info -WS | grep -E "Gustaf"
slog2info -WS | awk '/Gustaf/{p=2} p>0{print; p--}'
uds_toolkit -vv --doip 1205 --session EXTENDED -r 1205:192.168.1.1  read_data F186

cat /etc/sdboss/ht_doip_router/ht_doip_router_configuration.json
uds_toolkit_ht_ref --doip 1841 read_data F12E
./nonhlos/vendor/tools/scripts/copy_build_artifacts.py nonhlos/vendor/haleytek/moose/comet.json nonhlos --out flashfiles_out && cd flashfiles_out && ./flash_qnx.shx && cd .. && fastboot reboot

qnx_laod scp /home/fredrik/sources/manifest-safety-8155/build/qnx7_aarch64le/components/safety-display/driver/ALPNS_COMMON_S2_DIMHUD/common_driver/dim_hud_d/dimd root@192.168.1.1:/tmp/

# TODO
A better way to jump between repo


# Move branch to another sha1
git reset --hard SHA1

# Rebase a chain of commits
git rebase --update-refs main

# Undo last commit but keep changes
git reset --soft HEAD~1

# change a specific sha1 to another sha1
sed -i 's/old/new/g' ht_safety_qc8255.xml

SWDL (Software Download Engine)
SWUT Software Update Tool

# unittest

Q: How to buiild and  run unittest from cmake with target instead of running bin
Q:


## run specif test on linux
./tools/haleytek/docker-images/run.py --target safety
build it:
 cmake --build build  --target haleytek_led_utils_ut
Run it:
./build/components/safety-display/qm_common/libled/test/ut/haleytek_led_utils_ut


## build specific target

./tools/haleytek/docker-images/run.py --target safety
source safety_build/safety-env.sh 8155
cmake --build --preset qnx7_aarch64le -j "$(nproc)" --target dimd
push it
scp /home/fredrik/sources/manifest-safety-8155/build/qnx7_aarch64le/components/safety-display/driver/ALPNS_COMMON_S2_DIMHUD/common_driver/dim_hud_d/dimd root@192.168.1.1:/tmp/
TYhen on target
mount -o remount,rw /
mv /tmp/dimd /usr/bin/dim_hud_d
reset


## Code covarage on target:

./tools/haleytek/docker-images/run.py --target safety
source safety_build/safety-env.sh 8155
make qnx
cmake --build --preset qnx7_aarch64le -j "$(nproc)" --target install-all-safety-unittests
tools/haleytek/safety_test_tools/run_tests_on_target.py --dhu-image COMET --copy-result-xml reports_xmls

### Report can be found here:
manifest_safety/build/linux_x86-64/coverage_reports/coverage_details.html


## Not sure about this one:
ctest --preset=linux_x86-64 --output-junit "xml/testreport.xml"
or
make linux-ut


AI
From cli
cop
cluade


# HALETEK software

## HKP
### download from CI
### Build self
### Flash

# DHU
## download from CI
## Build self
### Flash

# UHX
## download from CI
## Build self
### Flash


# VCC software

## HKP
### download from CI
### Build self
### Flash

# DHU
## download from CI
## Build self
### Flash

# UHX
## download from CI
## Build self
### Flash



# Gerrit
## Push (same as git review)
    $ git push --no-follow-tags  gerrit HEAD:refs/for/master%topic=HT-41531
    $ git push --no-follow-tags  origin HEAD:refs/for/master%topic=HT-41531

## Run pre-commit manually
 $ bash .git/hooks/pre-commit



# Thins needed to be done once
## Install ADB
    start adb service
## Setup ssh to DHU
Switches on box: on   '''
                     '
                     1234
Set the settings to
                linkspeed: 1000Mb/s as defined on the box as well
                ipv4: 192.168.1.2
                Netmask: 255.255.255.0




# Connect to DHU
$ picocom -b 115200 /dev/ttyUSB1
    Should show IHU-QNX#

# Connect to HKP
$ picocom -b 115200 /dev/ttyUSB0


# Disconnect
$ ctrl-b ctrl-x

# Connect over ssh

## To login over ssh
    ssh root@192.168.1.1


# SPA2

## slog2info (QNX commando)
Display messages from the system log

- For logging of display driver
    slog2info -w | grep dim_hud_d

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



./tools/haleytek/docker-images/run.py --target safety
source safety_build/safety-env.sh 8155
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
    $ qnx-ht-433366 cd qnx/apps/qnx_ap/
    $ qnx-ht-433366 source cvendor/haleytek/setenv_QNX.sh 8155
    $ qnx-ht-433366 make

# With ht_build.py
## From inside the docker
    $ ./tools/haleytek/docker-images/run.py --target qnx
    $ qnx-ht-433366 ./tools/haleytek/qualcomm/ht_build.py --already-in-docker --product-name comet --target qnx --build-variant userdebug --collect-flash-files --verbose
## From outside the docker
    $ ./tools/haleytek/qualcomm/ht_build.py --product-name comet --target qnx --build-variant userdebug --collect-flash-files --verbose



## Move all(?) files to flashfiles_out
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

# Running dsm test for safety-display
## Start device testing docker
    $ cd ~/sources/manifest-safety-8155
    $ ./tools/haleytek/docker-images/run.py --target device-testing

## Running test
    $device-testing-ht-433366 devicetek run-pytest components/safety-display/safety/dsm/test/it/pytests

## More specific test
    devicetek run-pytest components/safety-display/safety/dsm/test/it/pytests/test_dsm_broadcast_heartbeats.py::test_dsm_remove_fault[UXC10]

# Running dsm test for qnx
## Start device testing docker
    $ cd ~/sources/haleytek-dhu-15
    $ ./tools/haleytek/docker-images/run.py --target device-testing

## Running test
    $device-testing-ht-433366 devicetek run-pytest ./tools/haleytek/platform/test/comet/display/tests/dim_hud_common/test_dim_hud_driver_initialized.py
    $device-testing-ht-433366 devicetek run-pytest ./tools/haleytek/platform/test/comet/display/tests/csd/test_csd_status.py

    devicetek -l DEBUG  run-pytest --pytest-arg="-s -vv" --disable-file-logging --disable-dlt-logging ./tools/haleytek/platform/test/shared/logs_collection_test/test_bugreport_content.py::test_no_unhandled_dumpstate_board_bin_files_exist

    devicetek -l INFO  run-pytest --pytest-arg="--log-cli-level=INFO  -s -vv" --disable-file-logging --disable-dlt-logging ./tools/haleytek/platform/test/comet/display/tests/dim/test_dim_threads_status.py

## Generate device_config.json
    devicetek -l DEBUG generate-config


# Unpack HaleyTek build python file:
    When downloading from https://web.haleytek.net/build_search?limit=10
    Download the "one without " a key
    $ ~/.venvs/azstorage/bin/python artifacts-downloader-


# Restore bricket device
    1. Download FW.zip  from somewhere:
        https://ara-artifactory.volvocars.biz/ui/repos/tree/General/dhum-merged/master/V/26.18.1.21.4042/moose_mp_polestar_gas/userdebug/FW.zip
    2. Move to ~/sources/haleytek-dhu-15/firmware
    3. Unzip the FW.zip
    4. Got to picocom -b 115200 /dev/ttyUSB0 and excute "edl"
    5. Start the device_testing docker wher we have qdl and checkpars.py
       ./tools/haleytek/docker-images/run.py --target device-testing
    6. In the docker run:
        for i in {0..5}; do checksparse.py -i rawprogram${i}.xml; done
        qdl prog_firehose_ddr.elf rawprogram?.xml patch?.xml
    7. Reboot the decice disconnect cable
    8. Now we should be able to get into  picocom -b 115200 /dev/ttyUSB1 and flash qnx



repo checkout someting old repo sync nmu something


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



# VCC
## Download and flash DHU with moose
Latest DHU software are in dhum-merged
For the HKP the software are in DHUK-merged
Find it here: https://ara-artifactory.volvocars.biz/ui/repos/tree/General/

For HKP: Dowload userdebug/artifacts.zip
For DHU: Dowload userdebug/FW.zip

## How to build

It might be that we need to run actiovation first. Think it should be done outside the docker
$ cd tools/volvo/docker_build/toolchain/qnx/
$ source qnx_license_activation.sh


Without docker

./tools/volvo/bin/src_builder/src_builder dhu10 all --android-target=moose_vcc_gas-gap_current-userdebug -j32  Dont work
./tools/volvo/bin/src_builder/src_builder dhu10 qnx



### with docker
tools/volvo/docker_image/run.sh --multiuser
cd qnx/apps/qnx_ap
sudo ln -sf  /usr/bin/python2 /etc/alternatives/python

source cvendor/volvocars/setenv_QNX.sh
make



## How to flash it?
Go to IHU-QNX# and reset -f
moose_update?


Then you can flash the downloaded files using fastboot or qdl depending on the file type and device state




# Spa2 ?
https://ara-artifactory.volvocars.biz/ui/repos/tree/General/dhum-merged/master/V/26.18.4.21.3043

# Spa3?



https://artinfo-gerrit.volvocars.biz/plugins/gitiles/manifest_uxc10/+/refs/heads/master/README.md

https://confluence.volvocars.biz/spaces/ARTINFO/pages/780854392/Artifactory+TokenUpdater+-+setup

How to downdlooad volvovars repo?

But if we have it staart docker like this:
tools/volvo/docker_image/run.sh

Within docker

~/Documents/MooseBuilds/rel2/20/25.40.1.10.3020/moose_mp_polestar_gas/userdebug/FW.zip


The car I have is:

Car: XPK32L
Need to do :
    Dowload and flash the latest FW.zip for this car, which is:?
    Setup if address at laptop
    Install dlt logger at laptop





docker compose -f /home/fredrik/sources/volvocars-dhu/tools/volvo/bin/src_builder/runners/compose.yml build qnx-docker-runner

docker compose -f /home/fredrik/sources/volvocars-dhu/tools/volvo/bin/src_builder/runners/compose.yml run  --rm  --name src_builder_qnx_570_1781023771882115055 --remove-orphans qnx-docker-runner bash -c /home/fredrik/sources/volvocars-dhu/tools/volvo/bin/src_builder/src_builder.sh dhu10 qnx

To  run docker

Set these env variables first:
export DOCKER_CONTAINER_NAME=fredrik \
DOCKER_USER=1000:1000  \
DOCKER_HOST_WORKSPACE=/home/fredrik/sources/volvocars-dhu \
BAZEL_OUTPUT_USER_ROOT=/home/fredrik/.cache/bazel \
CCACHE_DIR=/home/fredrik/.ccache \
DOCKER_PASSWD_FILE=/home/fredrik/sources/volvocars-dhu/passwd \
DOCKER_RUN_QNX_IT_RUNNER_NAME=fredrik \
DOCKER_COMPOSE_YML=tools/volvo/bin/src_builder/runners/compose.yml \
DOCKER_USER_ID=1000 \
DOCKER_GROUP_FILE=/home/fredrik/sources/volvocars-dhu/group \
DOCKER_HOSTNAME=haleytek-433366 \
DOCKER_GROUP_ID=1000 \
AOSP_BUILD_PARAMS=/home/fredrik/sources/volvocars-dhu/build-params-metadata.json \
REPO_DIR=/home/fredrik/sources/volvocars-dhu \
QNX_PATH=qnx/apps/qnx_ap \
USE_BAZEL=1 \
SELECTED_PLATFORM=DHU10


docker compose -f /home/fredrik/sources/volvocars-dhu/tools/volvo/bin/src_builder/runners/compose.yml run --entrypoint bash  qnx-docker-runner
tools/volvo/bin/src_builder/shared_scripts/build_qnx.sh


When running src_builder

IT will first firs run src_bulder
    Will run docker_runner function
        Will call configure_docker_settings
            In here DOCKER_RUNNER_NAME is set

        Will call uni_run.sh

        Will start docker
            From docker we start src_builder.sh with


Set DOCKER_RUNNER_NAME to src_builder_qnx_570_1781023771882115055
Then call uni_run.sh with the docker runner name


Just build test
    cd ~/sources/<manifest-safety-8155>
    $ ./tools/haleytek/docker-images/run.py --target safety

    make qnx-tools
    cmake --build build --target haleytek_led_utils




# Push i2c_tools
$ scp /home/fredrik/sources/haleytek-dhu-15/qnx/apps/qnx_ap/cvendor/haleytek/driver/display/prebuilts/display_dev_tools/bin/i2c_tool root@192.168.1.1:/tmp/
$QNX# chmod +x /tmp/i2c_tool

scp /home/fredrik/sources/manifest-safety-8155/build/qnx7_aarch64le/components/safety-display/display_dev_tools/kill_thread/kill_thread  root@192.168.1.1:/tmp/

To read a register:
/tmp/i2c_tool r /dev/i2c5 0x68 0x02 0 1

This will read from noed /dev/i2c5, device address 0x68, register 0x02, 8 bits (0 = 8 bits, 1 = 16 bits), and read 1 byte (1 = read 1 byte, 2 = read 2 bytes, etc.)





cmake --build --preset qnx7_aarch64le -j "$(nproc)" --target kill_thread




devicetek test-mapping list-tests qnx/apps/qnx_ap/cvendor/haleytek/driver/display/prebuilts/bshalp_common_s3_csd_dim/






devicetek test-mapping --stage presubmit --product asteroid --android-version 15 --with-capabilities filter-test-plan --test-plan-path test_plan.json



devicetek test-mapping list-tests qnx/apps/qnx_ap/cvendor/haleytek/driver/display/prebuilts/bshalp_common_s3_csd_dim/ | devicetek test-mapping --stage presubmit --product asteroid --android-version 15 --with-capabilities filter-test-plan  > test_plan.json



sshfs -o uid=1014,gid=1014 fredrik@172.20.20.105:/home/fredrik/sources/flashfiles/flashfiles_991693  /home/fredrik/sources/flashfolder/





Decide where what test to run in gate? We have HT_TEST_MAPPING

We also have it devided in shared, comet, asteroid

We also have it devided in VCC in there testplan

When we push someting in tool/haleytek/platform/test/comet|asteroid|shared it will run some gate but not all

That is executed when we push binary?? and or push to VCC


# Copyright © 2026 HaleyTek AB. All rights reserved.
#
# NOTICE: This file contains material that is confidential and proprietary to
# HaleyTek AB. No license is granted under any intellectual or industrial
# property rights of HaleyTek AB except as may be provided in an agreement with
# HaleyTek AB.
#
# Any unauthorized copying or distribution of content from this file is
# prohibited.

import pytest
import time
from coppercomm.ssh_connection.ssh_connection import SSHConnection

pid_name = "dim_hud_d"

DIM_EXPECTED_THREADS_WHEN_ON = [
    "1",
    "DimHudUnlogResmgr",
    "McuResmgr",
    "ADC_debug",
    "DoubleTaskBuffer",
    "DimResmgr",
    "DoubleTaskBuffer",
    "HudDiagResmgr",
    "HudAmbillmnResmgr",
    "HudResmgr",
    "pm_handler",
    "DimHudResmgr",
    "HudEventLoop",
    "DimHud-ErrbMonitor",
    "GpioInterruptMonitor",
    "mHud-LinkLockMonitor",
    "GpioInterruptMonitor",
    "ADC Reading Loop",
    "DimDriver::DeRating",
]

DIM_EXPECTED_THREADS_WHEN_OFF = [
    "1",
    "DimHudUnlogResmgr",
    "McuResmgr",
    "ADC_debug",
    "DoubleTaskBuffer",
    "DimResmgr",
    "DoubleTaskBuffer",
    "HudDiagResmgr",
    "HudAmbillmnResmgr",
    "HudResmgr",
    "pm_handler",
    "DimHudResmgr",
    "HudEventLoop",
    "DimHud-ErrbMonitor",
    "GpioInterruptMonitor",
    "mHud-LinkLockMonitor",
    "GpioInterruptMonitor",
]
THREAD_OK_STATE = [
    "BARRIER",
    "CONDVAR",
    "INTR",
    "INTR_ATTACH_EV",
    "JOIN",
    "MQ_RECEIVE",
    "MQ_SEND",
    "MUON_MUTEX",
    "MUTEX",
    "NANOSLEEP",
    "PIPE",
    "READY",
    "RECEIVE",
    "REPLY",
    "RUNNING",
    "RWLOCK_READ",
    "RWLOCK_WRITE",
    "SEM",
    "SEND",
    "SEND_NOTIFY",
    "SIGSUSPEND",
    "SIGWAITINFO",
    "TIMER_DELEGATE",
    "TRACEBUFFER"
]

# A small wrapper so we dont have to repeat the same code in each test
class QnxCommand:
    def __init__(self, qnx_broadrreach_ssh: SSHConnection):
        self.qnx_broadrreach_ssh = qnx_broadrreach_ssh

    def execute(self, command: str) -> None:
        """Send a command to the QNX system."""
        stdout, _, _ = self.qnx_broadrreach_ssh.execute_cmd(command, handle_return_code=False)
        output: str = stdout.read().decode("utf-8").strip()
        return output

# Help function to verify the thread state
def verify_thread_status(qnx: QnxCommand, thread_name: str, exp_state) -> bool:
    """Verify that a thread is running on the QNX system."""
    # Get the status for the thread, since we grep on threadname and if its not
    # running the output should be empty, we alse request the state of the thread.
    # State could be send, receive, running, ready etc, it should NOT be dead or stopped
    # to be considred OK
    # %h name of the thread
    # %J Thread state
    pidin_output = qnx.execute(f"pidin -F '%h %J' -p {pid_name} | grep -F '{thread_name}'")

    # Verify that the thread is  running and state is not  DEAD or STOPPED
    assert pidin_output, f"Thread '{thread_name}' is not running in the dim process"
    assert any(state in pidin_output for state in exp_state), f"Thread: '{thread_name}' does not match expected state, got: {pidin_output}, expected one of: {exp_state}"


# After the thread is set to stopped we cant read log for dim.
# Since log_fixture is autouse, we need to disable it for this test.
@pytest.fixture(scope="function", autouse=True)
def log_fixture():
    return

# We add a fixture to to restore thread status after we have stoped it.
# This will run no mater if the test passes or fails, so we can restore the thread status to running.
# @pytest.fixture(autouse=False)
# def thread_not_running(qnx_broadrreach_ssh: SSHConnection):
#     """Verify that the thread is not running."""
#     thread_name = "ADC Reading Loop"
#     exp_state = ["STOPPED"]
#     SIGSTOP = 23
#     qnx = QnxCommand(qnx_broadrreach_ssh)
#     # Get the tid for ADC Reading Loop thread
#     # %h name of the thread
#     # %b thread id (tid)
#     pidin_output = qnx.execute(f"pidin -F '%h %b' -p {pid_name} | grep -F '{thread_name}'")
#     tid = pidin_output.split()[-1:][0]
#
#     # Send SIGSTOP to the thread to stop it
#     qnx.execute(f"slay -s {SIGSTOP} -T {tid} -m name {pid_name}")
#
#     #We need to have a little sleep here to give the thread time to stop before we check its status.
#     time.sleep(2)
#     verify_thread_status(qnx, thread_name, exp_state)
#
#     yield
#     SIGCONT = 25
#     # Send SIGCONT to the thread to resume it
#     qnx.execute(f"slay -s {SIGCONT} -m name {pid_name}")
#
#     # We need to have a little sleep here to give the thread time to stop before we check its status.
#     time.sleep(2)
#     verify_thread_status(qnx, thread_name, THREAD_OK_STATE)

# Verify that we can detect if a thread has stop running
# def test_dim_thread_is_not_running(
#     thread_not_running
# ):
#     pass

# Verify that the threads are running in the dim process
# @pytest.mark.parametrize("thread_name", DIM_EXPECTED_THREADS)
# def test_dim_thread_is_running(
#     qnx_broadrreach_ssh: SSHConnection, thread_name: str
# ):
#     """Verify that the expected thread is running."""
#     qnx = QnxCommand(qnx_broadrreach_ssh)
#     verify_thread_status(qnx, thread_name, THREAD_OK_STATE)

@pytest.fixture(autouse=True)
def restore_dim_state(
    qnx_broadrreach_ssh: SSHConnection
):
    yield
    qnx = QnxCommand(qnx_broadrreach_ssh)
    qnx.execute(f"echo 2 > /dev/display/dim/state ")


def get_list_of_threads(qnx):
    """
    Since the output from pidin is a string, we need to convert it to a list
    """
    # We need to have something more in the output that thread name, otherwise
    # the command returns just the main thread """
    output = qnx.execute(f"pidin -F '%h %J' -p {pid_name}")
    # Skip the header line
    found_threads = output.splitlines()[1:]

    return [ " ".join(s.split()[:-1]) for s in found_threads]

def verify_thread_status(exp_threads, found_threads):
    """
    Verify that the expected threads are running in the dim process
    """
    missing_from_expected = list(set(exp_threads) - set(found_threads))
    assert not missing_from_expected , f"Thread(s) '{missing_from_expected}' is not running in the dim process"
    # print(f"In the expected list but not in recieved list: {missing_from_expected}")

    missing_from_found = list(set(found_threads) - set(exp_threads))
    assert not missing_from_found , f"Thread(s) '{missing_from_found}' is running in the dim process but should't"
    # print(f"In the found list but not in expected list: {missing_from_found}")

def test_threads_running_when_display_on(
    qnx_broadrreach_ssh: SSHConnection
):
    """Verify that the expected thread is running."""
    qnx = QnxCommand(qnx_broadrreach_ssh)

    found_threads = get_list_of_threads(qnx)
    verify_thread_status(DIM_EXPECTED_THREADS_WHEN_ON, found_threads)

def test_threads_running_when_display_off(
    qnx_broadrreach_ssh: SSHConnection
):
    """Verify that the expected thread is running."""
    qnx = QnxCommand(qnx_broadrreach_ssh)

    qnx.execute(f"echo 4 > /dev/display/dim/state ")
    time.sleep(5)

    found_threads = get_list_of_threads(qnx)
    verify_thread_status(DIM_EXPECTED_THREADS_WHEN_OFF, found_threads)

# "CsdDimDMain",
# "ADC_debug",
# "DimResmgr",
# "ErrorHandlerLoop",
# "TouchManagerDispatch",
# "TouchManagerReply",
# "TouchManagerDispatch",
# "TouchManagerReply",
# "CsdResmgr",
# "DoubleTaskBuffer",
# "dim_power_states",
# "DoubleTaskBuffer",
# "csd_power_states",
# "pm_handler",
# "LinkMonitor",
# "GpioInterruptMonitor",
# "GpioInterruptMonitor",
# #### "TouchInit",
# "AdcMonitor",
# "TconMonitor",
# "rruptHandler(GPIO75)",
# "GpioInterruptMonitor",
# "erruptHandler(GPIO6)",
# "rruptHandler(GPIO53)",
# "ruptHandler(GPIO103)",
# "GpioInterruptMonitor",
# "GpioInterruptMonitor",
# "TouchController",
# "ADC Reading Loop",



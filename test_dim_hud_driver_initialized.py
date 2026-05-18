# Copyright © 2026 HaleyTek AB. All rights reserved.
#
# NOTICE: This file contains material that is confidential and proprietary to
# HaleyTek AB. No license is granted under any intellectual or industrial
# property rights of HaleyTek AB except as may be provided in an agreement with
# HaleyTek AB.
#
# Any unauthorized copying or distribution of content from this file is
# prohibited.

import logging
import os

from coppercomm.ssh_connection.ssh_connection import SSHConnection
from shared.display.utils.assertions import assert_path_exists

if "HOSTNAME" in os.environ and os.environ["HOSTNAME"] != "aic-docker":
    from coppercomm.plugins.pytest_fixtures import filesaver

logger = logging.getLogger(__name__)


def test_dim_hud_driver_initialized(qnx_broadrreach_ssh: SSHConnection):
    """Verify that the DIM_HUD node has been created to ensure its existence for the driver initialization."""
    device_node = "/dev/dimhud_dhu"
    assert_path_exists(qnx_broadrreach_ssh, device_node)


def test_dim_hud_collect_boot_logs(qnx_broadrreach_ssh: SSHConnection, storage_path):
    logger.info(f"PATH: {filesaver.get_raw_dir_for_current_test()}")
    boot_log_path = os.path.join(storage_path, "SPA2Display-boot-dim_hud-logs.log")
    remote_log_path = "/var/log/ht_system_monitor/dim_hud_boot_logs.txt.gz"
    try:
        qnx_broadrreach_ssh.get(remotepath=remote_log_path, localpath=boot_log_path)  # nosec B108
    except Exception:
        logger.exception("Collecting boot log: 'SPA2Display-boot-dim_hud-logs.log' failed!")

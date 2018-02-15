#
# Copyright (c) 2018 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 3 (GPLv3). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv3
# along with this software; if not, see
# https://www.gnu.org/licenses/gpl-3.0.txt.
#
"""ScanTask used for satellite connection task."""
from requests import exceptions
from api.models import (ScanTask, SourceOptions)
from scanner.task import ScanTaskRunner
from scanner.satellite import utils
from scanner.satellite.api import SatelliteException
from scanner.satellite.factory import create


class ConnectTaskRunner(ScanTaskRunner):
    """ConnectTaskRunner satellite connection capabilities.

    Attempts connections to a source using a credential
    and gathers the set of available systems.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, scan_job, scan_task):
        """Set context for task execution.

        :param scan_job: the scan job that contains this task
        :param scan_task: the scan task model for this task
        :param prerequisite_tasks: An array of scan task model objects
        that were execute prior to running this task.
        """
        super().__init__(scan_job, scan_task)
        self.source = scan_task.source

    def run(self):
        """Scan network range ang attempt connections."""
        satellite_version = None
        options = self.source.options
        if options:
            satellite_version = options.satellite_version

        if (satellite_version is None or
                satellite_version == SourceOptions.SATELLITE_VERSION_5):
            error_message = 'Satellite version %s is not yet supported.\n' %\
                SourceOptions.SATELLITE_VERSION_5
            error_message += 'Connect scan failed for %s.' % self.scan_task
            return error_message, ScanTask.FAILED

        try:
            status_code, api_version = utils.status(self.scan_task)
            if status_code == 200:
                api = create(satellite_version, api_version,
                             self.scan_task)
                if not api:
                    error_message = 'Satellite version %s with '\
                        'api version %s is not supported.\n' %\
                        (satellite_version, api_version)
                    error_message += 'Connect scan failed for %s.' % \
                        self.scan_task
                    return error_message, ScanTask.FAILED
                api.host_count()
                api.hosts()
            else:
                error_message = 'Connect scan failed for %s.' % self.scan_task
                return error_message, ScanTask.FAILED
        except SatelliteException as sat_error:
            error_message = 'Satellite error encountered: %s\n' % sat_error
            error_message += 'Connect scan failed for %s.' % self.scan_task
            return error_message, ScanTask.FAILED
        except exceptions.ConnectionError as conn_error:
            error_message = 'Satellite error encountered: %s\n' % conn_error
            error_message += 'Connect scan failed for %s.' % self.scan_task
            return error_message, ScanTask.FAILED

        return None, ScanTask.COMPLETED

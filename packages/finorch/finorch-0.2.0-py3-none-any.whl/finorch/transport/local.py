import subprocess
import xmlrpc.client

from finorch.config.config import client_config_manager
from finorch.transport.exceptions import TransportConnectionException, TransportTerminateException, \
    TransportGetJobStatusException, TransportGetJobFileException, TransportGetJobFileListException
from finorch.transport.abstract_transport import AbstractTransport
from finorch.utils.port import test_port_open


class LocalTransport(AbstractTransport):
    """
    Transport for running jobs on the local machine (Where the API is running)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._client_rpc = None

    def _check_client_connectivity(self, port=None):
        """
        Checks if the client is already running by reading the details from the config file and trying to connect to
        the clients last used port
        :param port: An option port to check for connectivity. If this is None the port from the client configuration
        is used.
        :return: True if the client is running and accepting connections, otherwise False
        """
        if port := port or client_config_manager.get_port():
            self._port = int(port)

            self._connected = test_port_open(self._port)

        return self._connected

    def _spawn_client(self):
        """
        Uses subprocess to spawn the client and returns the port that the client is listening on

        :return: The port that the client is listening on
        """

        # Start the client process
        args = [
            "python",
            "-m",
            "finorch.client.client",
            self._session.callsign
        ]
        p = subprocess.Popen(args, stdout=subprocess.PIPE)

        # Because we need to read the output of the client asynchronously, we need to wait for the "=EOF=" line to
        # indicate that the client process has finished with it's output.
        stdout = []
        while _line := p.stdout.readline().decode('utf-8').strip():
            if _line == "=EOF=":
                break

            stdout.append(_line)

        # Check if the client started successfully
        if stdout[0] == "error":
            # Report the error from the client
            raise TransportConnectionException('\n'.join(stdout[1:]))

        # Try to parse the first line of the output from the client as the port it is running on and check the
        # connectivity.
        self._port = str(stdout[0])
        if not self._check_client_connectivity(self._port):
            raise TransportConnectionException("Unable to connect to the port reported by the client")

    def connect(self):
        # Check if the client is already running and start it with subprocess, which will manage it's own finesse
        # processes, if it's not
        if not self._check_client_connectivity():
            self._spawn_client()

        self._client_rpc = xmlrpc.client.ServerProxy(
            f'http://localhost:{self._port}/rpc',
            allow_none=True,
            use_builtin_types=True
        )

        self._client_rpc.set_exec_path(self.exec_path)

    def start_job(self, katscript):
        return self._client_rpc.start_job(katscript)

    def terminate(self):
        if not self._connected:
            raise TransportTerminateException("Client is not connected")

        self._client_rpc.terminate()

    def disconnect(self):
        raise NotImplementedError()

    def get_job_file(self, job_identifier, file_path):
        status = self._client_rpc.get_job_file(job_identifier, file_path)
        if type(status) is bytes:
            return status
        else:
            raise TransportGetJobFileException(status[1])

    def get_job_file_list(self, job_identifier):
        status = self._client_rpc.get_job_file_list(job_identifier)
        if type(status) is list and status[0] is not None:
            return status
        else:
            raise TransportGetJobFileListException(status[1])

    def get_job_status(self, job_identifier):
        status = self._client_rpc.get_job_status(job_identifier)
        if type(status) is int:
            return status
        else:
            raise TransportGetJobStatusException(status[1])

    def get_jobs(self):
        return self._client_rpc.get_jobs()

    def stop_job(self, job_identifier):
        raise NotImplementedError()

import logging
import logging.handlers
import os
import sys
import traceback
from tempfile import NamedTemporaryFile

from finorch.config.config import client_config_manager
from finorch.sessions import session_map, LocalSession
from finorch.utils.xmlrpc import XMLRPCServer


def daemonize():  # pragma: no cover
    """
    do the UNIX double-fork magic, see Stevens' "Advanced
    Programming in the UNIX Environment" for details (ISBN 0201563177)
    http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
    """
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)

    # decouple from parent environment
    # os.chdir("/")
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)

    # redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    si = open('/dev/null', 'r')
    so = open('/dev/null', 'ab+', 0)
    se = open('/dev/null', 'ab+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def start_client():
    """
    Starts the client.

    :return: None
    """
    # Get the client from the provided session parameter
    if len(sys.argv) != 2:
        raise Exception("Incorrect number of parameters")

    if sys.argv[1] not in session_map:
        raise Exception(f"Session type {sys.argv[1]} does not exist.")

    session_klass = session_map[sys.argv[1]]
    client = session_klass.client_klass(session_klass)

    # Create the XMLRPC server on a random port
    with XMLRPCServer(('localhost', 0)) as server:
        server.register_introspection_functions()

        client.set_server(server)
        server.register_instance(client)

        # Save the port in the client configuration
        port = server.server_address[1]
        client_config_manager.set_port(port)

        # Return the port via stdout to the caller
        print(server.server_address[1], flush=True)
        print("=EOF=", flush=True)

        n = NamedTemporaryFile()
        sys.stdout = open(n.name, "w")
        sys.stderr = sys.stdout

        if session_klass is not LocalSession:
            daemonize()  # pragma: no cover because testing linux daemonize is almost impossible

        # Run the server's main loop
        server.serve_forever()


def prepare_log_file():
    """
    Creates the log file and sets up logging parameters
    :return: None
    """
    # Reset any logging configuration
    from importlib import reload
    logging.shutdown()
    reload(logging)

    # Get the log file name
    log_file_name = client_config_manager.get_log_directory() / 'client.log'

    # Create the logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create the log handler
    handler = logging.handlers.RotatingFileHandler(log_file_name, maxBytes=10485760, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

    # Add the handler to the logger
    logger.addHandler(handler)


def run():
    # Attempt to start the client and if there is an error print error to stdout, and the stack trace to stderr.
    try:
        prepare_log_file()
        start_client()
    except Exception as exc:
        # An exception occurred, log the exception to the log file
        logging.error("Error starting client")
        logging.error(type(exc))
        logging.error(exc.args)
        logging.error(exc)

        # And log the stack trace
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        exc_log = ''.join('!! ' + line for line in lines)
        logging.error(exc_log)

        # Log to stdout and stderr
        print("error", flush=True)
        print(exc_log, flush=True)
        print("=EOF=")


if __name__ == '__main__':
    run()

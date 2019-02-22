import sys
import os
from getpass import getpass
from argparse import ArgumentParser
from subprocess import Popen, PIPE, TimeoutExpired
from sarnieploy.config import Config


def parse_options():
    parser = ArgumentParser(
        description="Deploy a war artifact to a jetty server."
    )

    parser.add_argument(
        "server",
        help="The server to deploy to",
        type=str
    )

    parser.add_argument(
        "--branch",
        nargs=1,
        dest="branch",
        type=str,
        help="The branch you want to build from (defaults to current branch)"
    )

    parser.add_argument(
        "--war-file",
        nargs=1,
        dest="war",
        type=str,
        help="Skip war artifact creation and use specified war file"
    )

    parser.add_argument(
        "-P",
        "--pull",
        dest="pull",
        default=False,
        action="store_true",
        help="Perform a 'git pull' before building the war artifact"
    )

    parser.add_argument(
        "-C",
        "--no-copy",
        dest="no_copy",
        default=False,
        action="store_true",
        help="Do not copy and symlink war artifact to wars folder"
    )

    parser.add_argument(
        "-N",
        "--no-restart",
        dest="no_restart",
        default=False,
        action="store_true",
        help="Do everything except restarting the server"
    )

    parser.add_argument(
        "-c",
        "--clean",
        dest="clean",
        default=False,
        action="store_true",
        help="Clean target directory right before exiting"
    )

    return parser.parse_args()


def run_command(cmd):
    returncode = Popen(cmd).wait()

    if returncode is not 0:
        print(
            "Command '{}' terminated with code {}".format(
                " ".join(cmd),
                returncode
            )
        )

        sys.exit(1)


def run_sudo_command(desc, password, cmd):
    print("Running {}".format(" ".join(cmd)))
    proc = Popen(
            cmd,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True
        )

    try:
        out, err = proc.communicate(input=password, timeout=15)
    except TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        print("{} timed out, see below:".format(desc))
        print(" ".join(cmd))
        print("stdout: {}".format(out))
        print("stderr: {}".format(err))
        sys.exit(1)


def load_config(server):
    return Config(server)


def get_password():
    user = os.getlogin()
    password = getpass("Password for {}: ".format(user))
    password += "\n"
    return password


def validate_war(war):
    path = os.path.join("target", war)
    is_valid = os.path.isfile(path)

    if not is_valid:
        print("Could not find war artifact: {}".format(path))
        print("Please check the file name and try again.")
        sys.exit(1)

    return war

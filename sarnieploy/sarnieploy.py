import os
import sys
from subprocess import Popen, PIPE, TimeoutExpired
from sarnieploy.utils import (
    load_config,
    get_password,
    validate_war,
    parse_options,
    run_command,
    run_sudo_command
)
from wargery.wargery import create_war_artifact
from wargery.utils import check_git


def deploy_to_server():
    print("Sarnieploy is ready.")

    # Check if the current folder is a git repository
    is_git_repository = check_git()

    if not is_git_repository:
        print("The current folder is not a git repository, aborting.")
        sys.exit(1)

    # Parse arguments and instantiate Config object
    args = parse_options()
    config = load_config(args.server)

    # Superuser privileges are required for copy, symlinking and restart
    if args.no_copy and args.no_restart:
        print("No operations require superuser, skipping password input.")
    else:
        print("Some operations require root access.")
        password = get_password()

    # Checkout branch
    if args.branch:
        cmd = ['git', 'checkout', args.branch]
        run_command(cmd)

    # Pull
    if args.pull:
        cmd = ['git', 'pull']
        run_command(cmd)

    # Use Wargery to create a war artifact or use the supplied argument
    # If using the supplied war file, make sure it exists
    if args.war:
        print("Using supplied war file: {}".format(args.war))
        target = validate_war(args.war)
    else:
        target = create_war_artifact()

    # Copy generated war file to wars direcory and symlink it to current war
    if args.no_copy:
        print("Skipping copy and symlinking.")
    else:
        print("Ready to copy {} to {}".format(target, config.wars_folder))
        path_to_target = os.path.join("target", target)

        cmd = [
            'sudo',
            '-S',
            'cp',
            path_to_target,
            config.wars_folder
        ]

        run_sudo_command("Copying", cmd, password)

        print("Copied {} to {}".format(target, config.wars_folder))
        print("Ready to symlink {} to {}".format(target, config.current))
        path_to_current = os.path.join(config.wars_folder, config.current)

        cmd = [
            'sudo',
            '-S',
            'ln',
            '-fs',
            target,
            path_to_current
        ]

        run_sudo_command("Symlinking", cmd, password)

    # Restart the server
    if args.no_restart:
        print("Skipping server restart.")
    else:
        print("Ready to stop server.")

        cmd = ['sudo', '-S'] + config.jetty_stop

        run_sudo_command("Stopping the server", cmd, password)

        print("Successfully stopped server.")
        print("Ready to start server.")

        cmd = ['sudo', '-S', 'nohup'] + config.jetty_start

        print("Running {}".format(" ".join(cmd)))
        proc = Popen(
            cmd,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True
        )

        try:
            out, err = proc.communicate(input=password, timeout=10)
        except TimeoutExpired:
            # This process just hangs forever, so it's ok even if it times out
            pass

        print("Successfully started server.")

    # Remove all war files from target directory
    if args.clean:
        print("Ready to clean target directory.")

        # Not using os.path.splitext here as the case is simple enough
        # and a one-liner fits nicely with list comprehension
        warfiles = [f for f in os.listdir("target") if f.endswith(".war")]
        for f in warfiles:
            os.remove(os.path.join("target", f))
        print("Finished cleaning target directory.")

    print("All done.")

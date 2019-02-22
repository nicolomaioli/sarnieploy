# Sarnieploy

Deploy a Wargery generated war artifact to a Jetty server running on Linux.


## Install

Sarnieploy is compatible with Python 3.3+.

Sarnieploy depends on [Wargery](https://github.com/nicolomaioli/wargery), which
is not available on PyPI. You have the option to install Sarnieploy using the
depracated `--process-dependency-links`, or you can install wargery separately
by installing `requirements.txt` first.

```
$ git clone https://github.com/nicolomaioli/sarnieploy.git
$ cd sarnieploy
$ pip -e install . --process-dependency-links --user`
```

This will create a `sarnieploy` command to `~/.local/bin/`, just make sure it's
in your path and you're good to go.

## Usage

Run `sarnieploy` in the root of your repository. This assumes that you have
already cloned it to the deployment server. Sarnieploy looks for a
`.deploy_config.json` file with the following structure:

```json
{
    "jetty-server-name": {
        // Path to the folder where you store the
        // war files for this server
        // Sarnieploy assumes superuser privilegies are required
        // to write to this folder
        "wars_folder": "/path/to/wars/directory",
        // Command to stop the Jetty server
        // This will be fed to a Popen object
        // Sarnieploy assumes superuser privilegies are required
        // to run this command
        "jetty_stop": [
            "command",
            "optional arguments"
        ],
        // Command to start the Jetty server
        // This will be fed to a Popen object
        // Sarnieploy assumes superuser privilegies are required
        // to run this command
        "jetty_start": [
            "command",
            "optional arguments"
        ],
        // War file to symlink
        // Sarnieploy assumes that this file lives in "wars_folder"
        // and superuser privilegies are required to write it
        // It will symlink with the '-fs' argument
        "current": "current.war"
    },
    // You can specify as many servers as you want
    "another-jetty-server-name": {
        // [ ... ]
    }
}
```

Check out `sarnieploy -h` for a list of CLI options.

## Is this on PyPI?

Nope.

Frankly the use case for Sarnieploy is so specific, it most likely won't meet
your needs. However, you can use it a starting point for a similar tool, and
then install it as a package.

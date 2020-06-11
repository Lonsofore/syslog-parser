# syslog-parser

Technical home task for a job.

Script to parse and summarize syslog file.


## Usage

You can just run the script with python:

```python3 parser.py```

It will parse and summarize /var/log/syslog per application name by default.

You could use arguments to change default settings:
* --path --- path of the syslog file (default /var/log/syslog);
* --type --- type of summarize, per "minute" or "app" (default: app);
* --skip --- a flag to skip incorrect lines of syslog file.

To test the script install PyTest and run it in script directory via ```pytest``` command.


## Docker

You also could run the script with Docker.

Build Docker image:

```./docker_build.sh```

And run it (it will use /var/log/syslog by defualt):

```./docker_run.sh```

If you want to provide arguments (e.g. type):

```./docker_run.sh --type minute```

## Output example

```app                                  events
-------------------------------------------
kernel                               25032
dbus-daemon                          222
dhclient                             232
NetworkManager                       556
systemd                              545
CRON                                 19
cron                                 6
systemd-sleep                        2
PackageKit                           2
containerd                           16
dockerd                              10
systemd-timesyncd                    1
```

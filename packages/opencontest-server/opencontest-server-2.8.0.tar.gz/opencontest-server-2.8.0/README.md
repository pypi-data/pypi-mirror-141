# OpenContest Server

An [OpenContest](https://github.com/LadueCS/OpenContest) server written using Python's HTTPServer and SQLite, with no external dependencies other than the Python standard library, [requests](https://docs.python-requests.org/en/latest/), and [Firejail](https://github.com/netblue30/firejail).

## Installation

### Docker

Run the [Docker Hub image](https://hub.docker.com/r/laduecs/opencontest-server):
```
docker run -d -p 9534:9534 --name opencontest-server -v $PWD/contests:/usr/src/app/contests laduecs/opencontest-server:latest
```
> Note: `$PWD/contests` is where the contests folder in the container is mapped to on the host and by default creates a new folder called `contests` in the current directory. It can be replaced with the full path to a different if desired.

### AUR

Install the [opencontest-server-git](https://aur.archlinux.org/packages/opencontest-server-git) from the AUR:
```
paru -S opencontest-server-git
```

Start the server with `systemctl start opencontest-server`.

### Pip

Install [opencontest-server](https://pypi.org/project/opencontest-server/) with `pip`:
```
pip install opencontest-server
```

Run the server with `ocs`.

## Usage

You can place contests like the [sample contest](https://github.com/LadueCS/Test) in a `contests` directory.

For debugging, you can run the server with the `--verbose` flag.

For production usage, you should put this server behind a reverse proxy like NGINX or Caddy because Python's HTTPServer does not implement any security features. You will also need to a domain name and a TLS certificate which you can easily obtain using [Let's Encrypt](https://letsencrypt.org/).

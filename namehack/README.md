# Iptables Name Hack Protection

Module to protect against so called *name hack* using iptables. Please note that this module is now obsolete in favor of NodeJS proxy solution [prproxy](https://github.com/pavelhoral/pr-gameproxy).

## Introduction

Evil player can bring down full server by connecting with the same name as already connected player. Ideally player’s name is determined by GameSpy login and should not be modifiable. However a hacker can modify his name in the PR process memory.
Current PR server is not verifying player’s name against GameSpy server (Master Server). This was probably initially responsibility of PunkBuster, which is no longer used.

## What Is Happening

The sequence of events is as follows:

1. Hacker connects to the server, exchanging some game packets (e.g. map, connected players).
2. Hacker's game sends `ClientInfo` packet with a forged duplicate name.
3. Packet is received and send to Python’s `PlayerConnect` handler (no action here can prevent the next step).
4. Information about the new player is sent to other connected clients.
5. As soon as other players receive information about the new player with duplicate name, they crash.

If we want really to prevent the crashes, we need to stop the packet with offending name before it reaches the PR server. This means we need to implement either a firewall or proxy solution with deep packet inspection.

## Module's Approach

This module is managing NAMEHACK iptables chain which contains rules to prevent packets with same name as any connected player to reach the actual server. The overall solution consist of the following components:

* `NAMEHACK` chain in iptables which processes all UDP packets starting detected as `ClientInfo` packets.
* Chain management BASH script `namehack.sh` capable of adding and removing rules in the `NAMEHACK` chain.
* Python script `namehack.py`, which calls management script on `PlayerConnect` and `PlayerDisconnect` events.

## Installation

Files in this module needs to be owned by *root* user and have to be immutable (i.e. only root should be allowed to modify them). This is necessary as the `namehack.sh` script will be called with NOPASSWD `sudo`.

Installation steps are:

* Store module files under some immutable location, e.g. `/opt/pr/shared/utils/namehack`.
* Link namehack module under `$SERVER_BASE/python` or add utils folder to `sys.path`.
* Import and initialize Name Hack hook inside `$SERVER_BASE/python/bf2/__init__.py`.
   * Place the initialization on the global script scope, not inside the `init_module` method.
* Copy `sudoers.conf` as `/etc/sudoers.d/namehack`.

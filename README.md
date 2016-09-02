# Project Reality Server Folder

This document serves as a description of the *Project Reality Server Folder* and also as a cheat sheet for the most common administration tasks.

Main idea behind the PR Server Folder is that there is exactly one PR server master copy called *BASE* and then there are multiple server instances (e.g. *MAIN*, *EVENT*, *TRAINING*). Every directory is under Git version control. BASE directory has a *master* branch which are vanilla PR files and a *merk* branch which contains common server modifications. Server instance directories are direct clone of *base/merk* and have their own modifications (consisting namely of server configuration).

The root general folder structure is:

* `base/` - BASE PR server files
* `{instance}/` - server instances (clone of the BASE PR)
* `shared/` - shared server components
** `nodejs/` - NodeJS installation
** `utils/` - shared utility scripts (clone of merk-utils)
* `work/` - work directory for any other stuff


## Preparing BASE Server Files

You will need server package downloaded from the license page of realitymod.com. After unpacking the server files they should be immediatelly put under version control:

    git init
    git add .
    git commit -m 'Base server files.'

Next a special branch which will hold BASE server modifications:

    git checkout -b merk

To link everything up the following modifications should be done indifr BASE directory:

    ln -s ../shared shared
    ln -s shared/utils/prserver/start_server.sh .


## Creating New Server Instance

Let's say you want to create new instance called `foobar`. First you need to clone the BASE server files:

    git clone -b merk foobar



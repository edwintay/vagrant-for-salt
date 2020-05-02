# vagrant-for-salt
Vagrant environment for developing Salt state files

## Contents
  1. [Dependencies](#deps)
  1. [Expected file layout](#file-layout)
  1. [Linking working directories](#linking-work)
  1. [Setup sudoer on host](#host-sudoer)



## <a name="deps" />Dependencies

* Vagrant
* VirtualBox
* NFS server

* macOS

```
> brew cask install vagrant
> brew cask install virtualbox
```

* Ubuntu

```
> sudo apt install virtualbox
> sudo apt install nfs-kernel-server
> sudo ufw allow in from 192.168.50.0/24 to any port nfs
```



## <a name="file-layout" />Expected file layouts
Configuration files
* etc/
  * master

Encryption keys
* keys/
  * master.minion.pem
  * master.minion.pub

Roots
* srv
  * salt
  * formulas
    * salt-formula
    * ... other formula repos ...
  * ... other salt repos ...



## <a name="linking-work" />Linking working directories
Link your working directory into the Vagrant guests using bin/link-dirs.py.

The Vagrantfile will mount directories found in ./srv/ to /srv/ on the guests.

See python bin/link-dirs.py --help for usage information.



## <a name="host-sudoer" />Setup sudoer on host
Syncing folders from host with NFS requires elevated privileges. To avoid
having to repeatedly enter the password, the host can be configured not to
require password for a limited subset of Vagrant commands.

See https://www.vagrantup.com/docs/synced-folders/nfs.html

# vagrant-for-salt
Vagrant environment for developing Salt state files

## Contents
  1. [Dependencies](#deps)
  1. [Expected file layout](#file-layout)
  1. [Linking working directories](#linking-work)
  1. [Setup sudoer on host](#host-sudoer)



## <a name="deps" />Dependencies
* Git
* Vagrant
* VirtualBox

On macOS
```
brew install git
brew cask install virtualbox
brew cask install vagrant
```

* VirtualBox Guest Additions
Ensure version of guest additions on Virtualbox guest matches host
```
vagrant plugin install vagrant-vbguest
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
  * secret
  * formulas



## <a name="linking-work" />Linking working directories
Link your working directory into the Vagrant guests using bin/link-dirs.py

See python bin/link-dirs.py --help for usage information.



## <a name="host-sudoer" />Setup sudoer on host
Syncing folders from host with NFS requires elevated privileges. To avoid
having to repeatedly enter the password, the host can be configured not to
require password for a limited subset of Vagrant commands.

See https://www.vagrantup.com/docs/synced-folders/nfs.html

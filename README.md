# vagrant-for-salt
Vagrant environment for developing Salt state files

## Contents
  1. [Dependencies](#deps)
  1. [Expected file layout](#file-layout)
  1. [Linking working directories](#linking-work)



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
  * master\_minion.pem
  * master\_minion.pub

Roots
* srv
  * salt
  * secret
  * formulas



## <a name="linking-work" />Linking working directories
Link your working directory into the Vagrant guests using bin/link-dirs.py

See python bin/link-dirs.py --help for usage information.

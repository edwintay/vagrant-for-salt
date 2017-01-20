# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
  end

  config.vm.define :master do |master_config|
    master_config.vm.box = "ubuntu/trusty64"
    master_config.vm.host_name = 'saltmaster.local'
    master_config.vm.network "private_network", ip: "192.168.50.10"

    # ./srv/ should contain symlinks to actual working directories for
    # salt-shared, salt-secret, and salt-formulas.
    # Run ./bin/link-dirs.py to set up these symlinks.
    master_config.vm.synced_folder "srv/salt", "/srv/salt", type: "nfs"
    master_config.vm.synced_folder "srv/secret", "/srv/secret", type: "nfs"
    master_config.vm.synced_folder "srv/formulas", "/srv/formulas", type: "nfs"

    master_config.vm.provision :salt do |salt|
      salt.master_config = "etc/master"
      salt.master_key = "keys/master_minion.pem"
      salt.master_pub = "keys/master_minion.pub"
      salt.minion_key = "keys/master_minion.pem"
      salt.minion_pub = "keys/master_minion.pub"
      salt.install_type = "stable"
      salt.install_master = true
      salt.no_minion = false
      salt.verbose = true
      salt.colorize = true
      salt.bootstrap_options = "-P -c /tmp"
    end
  end

end

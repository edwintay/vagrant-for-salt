require 'json'

def find_links(root)
  Enumerator.new do |yy|
    Dir.glob("#{root}/**/*") do |path|
      if File.symlink?(path)
        yy << path
      end
    end
  end
end

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  saltvers = "2016.11.7"
  machines = {
    :master => {
      :ip => "192.168.50.10",
      :hostname => "master.local",
      :cpus => 2,
      :memory => 2048,
      :box => "ubuntu/xenial64"
    },
    :'centos-7-1' => {
      :ip => "192.168.50.20",
      :hostname => "centos-7-1.local",
      :cpus => 1,
      :memory => 1024,
      :box => "centos/7"
    },
    :'centos-6-1' => {
      :ip => "192.168.50.21",
      :hostname => "centos-6-1.local",
      :cpus => 1,
      :memory => 1024,
      :box => "centos/6"
    },
    :'ubuntu-1604-1' => {
      :ip => "192.168.50.22",
      :hostname => "ubuntu-1604-1.local",
      :cpus => 1,
      :memory => 1024,
      :box => "ubuntu/xenial64"
    }
  }

  masters = machines.slice(:master)
  minions = machines.except(:master)

  masters.each do |master_n, spec|
    config.vm.define master_n, primary: true do |master_c|
      master_c.vm.provider "virtualbox" do |vb|
        vb.name = "#{master_n}"
        vb.cpus = spec[:cpus]
        vb.memory = spec[:memory]
      end
      master_c.vm.box = spec[:box]
      master_c.vm.hostname = spec[:hostname]
      master_c.vm.network "private_network", ip: spec[:ip]

      # Default sync is not needed, and takes up time during provisioning
      master_c.vm.synced_folder ".", "/vagrant", disabled: true

      # ./srv/ should contain symlinks to actual working directories
      # Run ./bin/link-dirs.py to set up these symlinks.
      find_links("srv").each { |path|
        local = File.join(path)
        guest = File.join("/", path)
        master_c.vm.synced_folder local, guest, type: "nfs",
          mount_options: ["ro"]
      }

      master_c.vm.provision :salt do |salt|
        salt.master_config = "etc/#{master_n}"
        salt.master_key = "keys/#{master_n}.pem"
        salt.master_pub = "keys/#{master_n}.pub"

        # Preseed master with self and all other minions
        seeds = { spec[:hostname] => "keys/#{master_n}.minion.pub" }
        minions.each { |mn, mspec|
          seeds[ mspec[:hostname] ] = "keys/#{mn}.pub"
        }
        salt.seed_master = seeds

        salt.minion_config = "etc/master.minion"
        salt.minion_key = "keys/#{master_n}.minion.pem"
        salt.minion_pub = "keys/#{master_n}.minion.pub"

        salt.install_type = "stable"
        salt.install_args = "#{saltvers}"
        salt.install_master = true

        salt.verbose = true
        salt.colorize = true
        salt.bootstrap_options = "-P -c /tmp"
      end
    end
  end

  minions.each do |minion_n, spec|
    config.vm.define minion_n do |minion_c|
      minion_c.vm.provider "virtualbox" do |vb|
        vb.name = "#{minion_n}"
        vb.cpus = spec[:cpus]
        vb.memory = spec[:memory]
      end
      minion_c.vm.box = spec[:box]
      minion_c.vm.hostname = spec[:hostname]
      minion_c.vm.network "private_network", ip: spec[:ip]

      # Default sync is not needed, and takes up time during provisioning
      minion_c.vm.synced_folder ".", "/vagrant", disabled: true

      minion_c.vm.provision :salt do |salt|
        salt.minion_config = "etc/minion"
        salt.minion_key = "keys/#{minion_n}.pem"
        salt.minion_pub = "keys/#{minion_n}.pub"

        salt.install_type = "stable"
        salt.install_args = "#{saltvers}"

        salt.verbose = true
        salt.colorize = true
        salt.bootstrap_options = "-P -c /tmp"
      end
    end
  end

  # Use vagrant-hostmanager plugin to manage only guest /etc/hosts
  # Include all VMs and use their private_ip
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = false
  config.hostmanager.manage_guest = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true

end

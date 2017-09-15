# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  saltvers = "2016.3.4"
  machines = {
    :master => {
      :ip => "192.168.50.10",
      :cpus => 2,
      :memory => 2048,
      :box => "ubuntu/xenial64"
    }
  }

  masters = machines.slice(:master)

  masters.each do |master_n, spec|
    config.vm.define master_n, primary: true do |master_c|
      master_c.vm.provider "virtualbox" do |vb|
        vb.name = "#{master_n}"
        vb.cpus = spec[:cpus]
        vb.memory = spec[:memory]
      end
      master_c.vm.box = spec[:box]
      master_c.vm.hostname = "#{master_n}.local"
      master_c.vm.network "private_network", ip: spec[:ip]

      # ./srv/ should contain symlinks to actual working directories for
      # salt-shared, salt-secret, and salt-formulas.
      # Run ./bin/link-dirs.py to set up these symlinks.
      master_c.vm.synced_folder "srv/salt", "/srv/salt", type: "nfs"
      master_c.vm.synced_folder "srv/secret", "/srv/secret", type: "nfs"
      # Each symlink in srv/formulas needs to be synced separately
      Dir["srv/formulas/*"].select { |ff| File.symlink? ff }.each { |ff|
        fname = File.basename(ff)
        tdir = "/srv/formulas"
        master_c.vm.synced_folder ff, "#{tdir}/#{fname}", type: "nfs"
      }

      master_c.vm.provision :salt do |salt|
        salt.master_config = "etc/#{master_n}"
        salt.master_key = "keys/#{master_n}.pem"
        salt.master_pub = "keys/#{master_n}.pub"

        # Preseed master with self and all other minions
        salt.seed_master = { master_n => "keys/#{master_n}.minion.pub" }

        salt.minion_config = "etc/#{master_n}.minion"
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
end

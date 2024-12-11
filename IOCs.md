# IOCs for MOUSE operation

The steps to run are written with the code directory as working
directory.

## detector movement, beam stop and slits (ims)

- code at `~/synApps/spec2epics`
- steps to run:

  ```sh
  ./convert.py echomode -a cfg/addressesAliases.md 4001 2
  ./convert.py echomode -a cfg/addressesAliases.md 4002 2
  ./convert.py echomode -a cfg/addressesAliases.md 4003 2
  ./convert.py echomode -a cfg/addressesAliases.md 4005 2
  ./generated/moxa01020305.cmd
  ```

## sample stage(s) (Trinamic)

- code at `~/IOCs/Trinamic_TMCL_IOC`
- configuration file will be different for transmission scattering and GISAXS/XRR
- steps to run (for standard operation)

  ```sh
  . ../.ioc-env/bin/activate
  python3.11 . --configfile ../../motor_config_yzstage.yaml --list-pvs
  ```

## metadata exchange (parrot)

- code at `~/IOCs/parrot/`
- steps to run

  ```sh
  . .parrot_env/bin/activate
  python -m parrot --list-pvs
  ```

## multi-function device, Arduino/Portenta Machine Control (NetworkedPortentaIOC)

- code at `~/IOCs/NetworkedPortentaIOC/`
- steps to run

  ```sh
  . .ioc_env/bin/activate
  python3.11 NetworkedPortentaIOC.py --host 172.17.1.124 --port 1111 --list-pvs
  ```

## x-ray source copper&moly: (Genix_IOC)

- code at `~/IOCs/MOUEModbusDevices/`
- steps to run

  ```sh
  . .ioc_env/bin/activate
  python3.11 MOUSEModbusDevices/src/Genix_IOC.py --host 172.17.1.3 --port 502 --unit-id 1 --prefix source_cu: --list-pvs -v
  python3.11 MOUSEModbusDevices/src/Genix_IOC.py --host 172.17.1.5 --port 502 --unit-id 1 --prefix source_mo: --list-pvs -v
  ```

## Inficon pressure gauge: (pressure_gauge_ioc)

- code at `~/IOCs/pressure_gauge_ioc/`
- steps to run

  ```sh
  . .ioc_env/bin/activate
  python3.11 pressure_IOC.py --host 172.17.1.14 --port 4012 --prefix pressure_gauge: --list-pvs
  ```

## systemd
### EPICS IMS motor IOC

1. Regarding systemd for running IOCs this will be the way: https://github.com/NSLS-II/systemd-softioc/README.md

2. Make sure the directory for the IOCs exists and is configured:

       sudo mkdir -p /opt/epics
       cd /opt/epics
       sudo sed -i -e "/^IOCPATH/{ s/^\(IOCPATH=\)/#\1/;aIOCPATH=$(pwd)" -e "}" /usr/local/systemd-softioc/epics-softioc.conf

3. Create a start up script, so that the final command does not contain spaces:

       mkdir -p /opt/epics/ims
       cd /opt/epics/ims
       cat << EOF > startup.sh
           #!/bin/sh
           scriptdir="\$(dirname "\$(readlink -f "\$0")")"
           cd "\$scriptdir/../spec2epics"
           ./convert.py echomode -a cfg/addressesAliases.md 4001 2
           ./convert.py echomode -a cfg/addressesAliases.md 4002 2
           ./convert.py echomode -a cfg/addressesAliases.md 4003 2
           ./convert.py echomode -a cfg/addressesAliases.md 4005 2
           ./generated/moxa01020305.cmd
       EOF
       chmod 755 startup.sh

4. Set up the IOC config like this:

       cat << EOF > config
           NAME=$(basename "$(pwd)")
           PORT=$(manage-iocs nextport)
           HOST=$(hostname -s)
           USER=$(id -un)
           EXEC="\$CHDIR/startup.sh"
       EOF

5. Check the currently set up IOCs ('$' indicates the command, other lines are output):

       $ manage-iocs report
       BASE            | IOC             | USER            |  PORT | EXEC
       /opt/epics      | ioc_ims         | poduser         |  4050 | /opt/epics/ioc_ims/../spec2epics/generated/moxa05.cmd

6. Install the IOC ('$' indicates the command, other lines are output):

       $ sudo manage-iocs install ioc_ims
       Installing IOC /opt/epics/ioc_ims ...
       the unit file /etc/systemd/system/softioc-ioc_ims.service has been created
       To start the IOC:
       manage-iocs start ioc_ims

7. Start the IOC ('$' indicates the command, other lines are output):

       $ sudo manage-iocs start ioc_ims
       Starting the IOC 'ioc_ims' ...
       The IOC 'ioc_ims' has been started successfully
       Do you want to enable auto-start 'ioc_ims' at boot? Type 'yes' if you do. yes
       Created symlink /etc/systemd/system/multi-user.target.wants/softioc-ioc_ims.service → /etc/systemd/system/softioc-ioc_ims.service.
       auto-start the IOC 'ioc_ims' at boot has been enabled successfully

8. Check the service status (or `start`, `stop`, `restart`) with standard `systemctl` tools:

       systemctl status softioc-ioc_ims

### Trinamic (python based IOCs)

1. Create a start up script, so that the final command does not contain spaces:

       cd /opt/epics/Trinamic_TMCL_IOC
       cat << EOF > startup.sh
           #!/bin/sh
           scriptdir="\$(dirname "\$(readlink -f "\$0")")"
           \$scriptdir/.pyenv/bin/python3 . --configfile motor_config_yzstage.yaml --list-pvs
       EOF
       chmod 755 startup.sh

2. Set up the IOC config like this:

       cat << EOF > config
           NAME=$(basename "$(pwd)")
           PORT=$(manage-iocs nextport)
           HOST=$(hostname -s)
           USER=$(id -un)
           EXEC="\$CHDIR/startup.sh"
       EOF

3. Check the currently set up IOCs ('$' indicates the command, other lines are output):

       $ manage-iocs report
       BASE            | IOC             | USER            |  PORT | EXEC
       /opt/epics      | Trinamic_TMCL_IOC | poduser         |  4054 | /opt/epics/Trinamic_TMCL_IOC/startup.sh

4. Install the IOC ('$' indicates the command, other lines are output):

       $ sudo manage-iocs install Trinamic_TMCL_IOC
       Installing IOC /opt/epics/Trinamic_TMCL_IOC ...
       the unit file /etc/systemd/system/softioc-Trinamic_TMCL_IOC.service has been created
       To start the IOC:
       manage-iocs start Trinamic_TMCL_IOC

5. Start the IOC ('$' indicates the command, other lines are output):

       $ sudo manage-iocs start Trinamic_TMCL_IOC
       Starting the IOC 'Trinamic_TMCL_IOC' ...
       The IOC 'Trinamic_TMCL_IOC' has been started successfully
       Do you want to enable auto-start 'Trinamic_TMCL_IOC' at boot? Type 'yes' if you do. yes
       Created symlink /etc/systemd/system/multi-user.target.wants/softioc-Trinamic_TMCL_IOC.service → /etc/systemd/system/softioc-Trinamic_TMCL_IOC.service.
       auto-start the IOC 'Trinamic_TMCL_IOC' at boot has been enabled successfully

6. Check the status with `systemctl`:

       $ systemctl status softioc-Trinamic_TMCL_IOC
       ● softioc-Trinamic_TMCL_IOC.service - IOC Trinamic_TMCL_IOC via procServ
       Loaded: loaded (/etc/systemd/system/softioc-Trinamic_TMCL_IOC.service; enabled; preset: enabled)
       Active: active (running) since Wed 2024-12-11 14:11:07 UTC; 28s ago
       Main PID: 1693 (procServ)
       Tasks: 34 (limit: 307)
       Memory: 43.1M (peak: 47.2M)
       CPU: 2.506s
       CGroup: /system.slice/softioc-Trinamic_TMCL_IOC.service
       ├─1693 /usr/bin/procServ -f -q -c /opt/epics/Trinamic_TMCL_IOC -i ^D^C^] -p /var/run/softioc-Trinamic_TMCL_IOC.pid -n Trinamic_TMCL_IOC --restrict -L /v>
       ├─1695 /bin/sh /opt/epics/Trinamic_TMCL_IOC/startup.sh
       └─1698 /opt/epics/Trinamic_TMCL_IOC/.pyenv/bin/python3 . --configfile motor_config_yzstage.yaml --list-pvs

### Use `systemctl` to query IOCs

    $ systemctl list-units 'softioc-*'
    UNIT                              LOAD   ACTIVE SUB     DESCRIPTION
    softioc-ims.service               loaded active running IOC ims via procServ
    softioc-ioc_ims.service           loaded active running IOC ioc_ims via procServ
    softioc-Trinamic_TMCL_IOC.service loaded active running IOC Trinamic_TMCL_IOC via procServ
    
    Legend: LOAD   → Reflects whether the unit definition was properly loaded.
    ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
    SUB    → The low-level unit activation state, values depend on unit type.
    
    3 loaded units listed. Pass --all to see loaded but inactive units, too.
    To show all installed unit files use 'systemctl list-unit-files'.

More details status:
    
    $ systemctl status 'softioc-*'
    ● softioc-Trinamic_TMCL_IOC.service - IOC Trinamic_TMCL_IOC via procServ
    Loaded: loaded (/etc/systemd/system/softioc-Trinamic_TMCL_IOC.service; enabled; preset: enabled)
    Active: active (running) since Wed 2024-12-11 14:11:07 UTC; 13min ago
    Main PID: 1693 (procServ)
    Tasks: 34 (limit: 307)
    Memory: 47.1M (peak: 50.7M)
    CPU: 15.257s
    CGroup: /system.slice/softioc-Trinamic_TMCL_IOC.service
    ├─1693 /usr/bin/procServ -f -q -c /opt/epics/Trinamic_TMCL_IOC -i ^D^C^] -p /var/run/softioc-Trinamic_TMCL_IOC.pid -n Trinamic_TMCL_IOC --restrict -L /v>
    ├─2221 /bin/sh /opt/epics/Trinamic_TMCL_IOC/startup.sh
    └─2224 /opt/epics/Trinamic_TMCL_IOC/.pyenv/bin/python3 . --configfile motor_config_yzstage.yaml --list-pvs
    
    ● softioc-ims.service - IOC ims via procServ
    Loaded: loaded (/etc/systemd/system/softioc-ims.service; enabled; preset: enabled)
    Active: active (running) since Wed 2024-12-11 14:19:52 UTC; 4min 42s ago
    Main PID: 2121 (procServ)
    Tasks: 13 (limit: 307)
    Memory: 2.4M (peak: 3.6M)
    CPU: 462ms
    CGroup: /system.slice/softioc-ims.service
    ├─2121 /usr/bin/procServ -f -q -c /opt/epics/ims -i ^D^C^] -p /var/run/softioc-ims.pid -n ims --restrict -L /var/log/softioc/ims/ims.log 4055 /opt/epics>
    ├─2123 /bin/sh /opt/epics/ims/startup.sh
    └─2126 /opt/epics/synapps/support/motor-R7-3-1/modules/motorIms/iocs/imsIOC/bin/linux-x86_64/ims ./generated/moxa05.cmd
    
    ● softioc-ioc_ims.service - IOC ioc_ims via procServ
    Loaded: loaded (/etc/systemd/system/softioc-ioc_ims.service; enabled; preset: enabled)
    Active: active (running) since Wed 2024-12-11 13:18:16 UTC; 1h 6min ago
    Main PID: 1223 (procServ)
    Tasks: 12 (limit: 307)
    Memory: 2.4M (peak: 3.0M)
    CPU: 11.079s
    CGroup: /system.slice/softioc-ioc_ims.service
    ├─1223 /usr/bin/procServ -f -q -c /opt/epics/ioc_ims/../spec2epics -i ^D^C^] -p /var/run/softioc-ioc_ims.pid -n ioc_ims --restrict -L /var/log/softioc/i>
    └─1225 /opt/epics/synapps/support/motor-R7-3-1/modules/motorIms/iocs/imsIOC/bin/linux-x86_64/ims /opt/epics/ioc_ims/../spec2epics/generated/moxa05.cmd

### Beyond systemd

Another insightfull discussion on tech-talk about configuring process limits and various settings independent of systemd: https://epics.anl.gov/tech-talk/2020/msg00537.php

### Place to put them
(From https://unix.stackexchange.com/a/367237)

**The best place to put system unit files:** `/etc/systemd/system` Just be sure to add a target under the [Install] section, read "How does it know?" for details. UPDATE: `/usr/local/lib/systemd/system` is another option, read "Gray Area" for details."

**The best place to put user unit files:** `/etc/systemd/user` or `$HOME/.config/systemd/user` but it depends on permissions and the situation. Note also that user services will only run while a user is logged in unless you explicitly enable them to run at boot with `loginctl enable-linger <username>`. "linger" means remain after logout, but also start at boot. In linger mode, a user manager is created at boot, which persists outside of the user session lifecycle.

### Creating the service units

As a regular user, after creating the service unit, for example in `~/synApps/spec2epics/ioc_ims.service` I ran:

    mkdir -p ~/.config/systemd/user
    ln -s ~/synApps/spec2epics/ioc_ims.service .config/systemd/user/
    systemctl --user enable ioc_ims

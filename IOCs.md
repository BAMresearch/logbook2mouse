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

## Notes systemd

**Update:** Regarding systemd for running IOCs this will be the way: https://github.com/NSLS-II/systemd-softioc
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

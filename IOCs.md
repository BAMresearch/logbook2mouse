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

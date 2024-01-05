# Installing the modules required for specfem3D_globe


1. Edit `main.cfg` to define which packages to install, and what system you
   are on, e.g. `frontier`.
2. Edit `configs/system.cfg` mainly to define where you want the module and
   package files to be installed.
3. Edit `configs/system.cfg` compilers etc. only if you know what you are doing.
4. Make sure you update the `MODULEPATH`, this one you will have to define
   yourself in, e.g., your `.bashrc` file. Make sure it is the same
   as the `MODULE_PATH` in you want to load.

After setting the `MODULE_PATH` in the startup file, you can run `install.sh`,
and it will setup the module files first load necessary, download the packages,
and install the packages

# TODO

When using installed hdf5 and/or adios have the option to give root dir. For the
root dir following patter should do:

ADIOS_ROOT=/path/to/adios
HDF5_ROOT=/path/to/hdf5

Then the setup.py will set the necessary variables.

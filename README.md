# SFMODULES

The goal of this set of scripts is to streamline the installation of
dependencies of specfem. Once installation is done, all that needs to be done
is
```bash
module load core-<suffix> hdf5-<suffix> adios2-<suffix>
```
to load environment variables relevant for the compilation of specfem.




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

# Note on installing h5py afterwards.

If you want to install hdf5, you have to install openssl on Frontier manually.
```bash
conda install conda-forge::libssh
```
for some reason the local `/usr/lib64/libssh.so` is missing a symbol

# TODO

When using installed hdf5 and/or adios have the option to give root dir. For the
root dir following patter should do:

ADIOS_ROOT=/path/to/adios
HDF5_ROOT=/path/to/hdf5

Then the setup.py will set the necessary variables.

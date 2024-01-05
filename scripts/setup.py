import toml
import os

filedirectory = os.path.dirname(os.path.realpath(__file__))
configdir = os.path.join(filedirectory, '..', 'configs')

def base():

    # Load configs
    maincfg = toml.load(os.path.join(configdir,'main.toml'))
    system = maincfg['SYSTEM']
    systemcfg = toml.load(os.path.join(configdir,'system.toml'))[system]
    compiler = systemcfg['COMPILER']
    modules = systemcfg['MODULES']

    # Module path
    modulepath = systemcfg['MODULE_PATH']
    module_dir = os.path.join(modulepath, 'base')
    modulefilename = os.path.join(module_dir, maincfg['VERSION'])

    # Get compiler variables from the config
    if compiler == 'IBM':

        # Frontier is a special case
        if system == 'frontier':
            cdict = dict(
                CC="cc",
                CXX="cc",
                MPICC="cc",
                MPICXX="cc",
                FC="ftn",
                MPIFC="ftn"
            )
        else:
            cdict = dict(
                CC="xlc",
                CXX="xlc++",
                MPICC="mpicc",
                MPICXX="mpic++",
                FC="xlf90",
                MPIFC="mpif90"
            )

    elif compiler == 'GNU':

        # Frontier is a special case
        if system == 'frontier':

            cdict = dict(
                CC="cc",
                CXX="cc",
                MPICC="cc",
                MPICXX="cc",
                FC="ftn",
                MPIFC="ftn"
            )

        else:

            cdict = dict(
                CC="gcc",
                CXX="g++",
                MPICC="mpicc",
                MPICXX="mpic++",
                FC="gfortran",
                MPIFC="mpif90"
            )

    elif compiler == 'CRAY':

        # So far I only know about frontier having the CRAY and
        # the compilers are all the same
        if system != 'frontier':
            raise ValueError(
                "CRAY compiler only supported on frontier. Exiting...")

        cdict = dict(
            CC="cc",
            CXX="cc",
            MPICC="cc",
            MPICXX="cc",
            FC="ftn",
            MPIFC="ftn"
        )

    else:

        raise ValueError(
            f"{compiler} compiler not supported yet. Exiting...")



    filestring = ""
    filestring += "#%Module\n\n"

    filestring += "proc ModulesHelp { } {\n"
    filestring += "    puts stderr 'Module is used to set compiler env vars.'\n"
    filestring += "}\n"
    filestring += "\n"
    filestring += 'module-whatis "This module is used to set all compilers etc."\n'
    filestring += "\n\n"

    filestring += "# Setting prereq\n"
    filestring += f'prereq {modules}\n'
    filestring += "\n\n"


    filestring += "# Setting environment variables\n"
    filestring += f'setenv COMPILER "{compiler}"\n'

    # Set values from compiler dictionary
    for key, value in cdict.items():
        filestring += f'setenv {key} "{value}"\n'

    # Make sure module_dir exists
    if not os.path.exists(module_dir):
        os.makedirs(module_dir)

    # Write module file
    with open(modulefilename, 'w') as f:
        f.write(filestring)



def adios():

    # Load configs
   # Load configs
    maincfg = toml.load(os.path.join(configdir,'main.toml'))
    system = maincfg['SYSTEM']
    systemcfg = toml.load(os.path.join(configdir,'system.toml'))[system]
    packcfg = toml.load(os.path.join(configdir,'package.toml'))

    if maincfg['ADIOS'] == False:
        print("ADIOS not enabled in main.toml. Exiting...")
        return

    # Some main variables
    packagedir = systemcfg['PACKAGE_DIR']
    base_module = packcfg['ADIOS']['BASE_MODULE']
    adios_link = packcfg['ADIOS']['LINK']
    adios_version = packcfg['ADIOS']['VERSION']
    adios_base_dir = os.path.join(packagedir, base_module, adios_version)
    adios_dir = os.path.join(adios_base_dir, 'main')
    adios_build = os.path.join(adios_base_dir, 'build')
    adios_install = os.path.join(adios_base_dir, 'install')

    # Define where to
    modulepath = systemcfg['MODULE_PATH']
    module_dir = os.path.join(modulepath, base_module)
    modulefilename = os.path.join(module_dir, adios_version)


    # Creating module file dynamically

    filestring = ""
    filestring += "#%Module\n\n"

    filestring += "proc ModulesHelp { } {\n"
    filestring += "    puts stderr 'Module is used to load ADIOS compiled for use with Specfem'\n"
    filestring += "}\n"
    filestring += "\n"
    filestring += 'module-whatis "This module load all necessary variables to build and use ADIOS"\n'
    filestring += "\n\n"

    filestring += "# Setting environment variables\n"
    filestring += f'setenv ADIOS_LINK "{adios_link}"\n'
    filestring += f'setenv ADIOS_BUILD "{adios_build}"\n'
    filestring += f'setenv ADIOS_INSTALL "{adios_install}"\n'
    filestring += f'setenv ADIOS_VERSION "{adios_version}"\n'
    filestring += f'setenv ADIOS_DIR "{adios_dir}"\n'

    # Very specfem specific flags
    if int(adios_version[0]) >= 2:
        filestring += 'setenv ADIOS_WITH "--with-adios2"\n'
        filestring += f'setenv ADIOS_CONFIG "{adios_install}/bin/adios2_config"'
    else:
        filestring += 'setenv ADIOS_WITH "--with-adios"'
        filestring += f'setenv ADIOS_CONFIG "{adios_install}/bin/adios2_config"'

    filestring += "\n\n\n"
    filestring += "# Setting path\n"

    # Set path variable
    filestring += 'set PATH $::env(PATH)\n'
    filestring += f'pushenv PATH "{adios_install}/bin:$PATH"'

    # Make sure module_dir exists
    if not os.path.exists(module_dir):
        os.makedirs(module_dir)

    # Write module file
    with open(modulefilename, 'w') as f:
        f.write(filestring)



def hdf5():

    # Load configs
    maincfg = toml.load(os.path.join(configdir,'main.toml'))
    system = maincfg['SYSTEM']
    systemcfg = toml.load(os.path.join(configdir,'system.toml'))[system]
    packcfg = toml.load(os.path.join(configdir,'package.toml'))

    if maincfg['HDF5'] == False:
        print("HDF5 not enabled in main.toml. Exiting...")
        return

    # Some main variables
    packagedir = systemcfg['PACKAGE_DIR']
    base_module = packcfg['HDF5']['BASE_MODULE']
    hdf5_link = packcfg['HDF5']['LINK']
    hdf5_version = packcfg['HDF5']['VERSION']
    hdf5_base_dir = os.path.join(packagedir, base_module, hdf5_version)
    hdf5_dir = os.path.join(hdf5_base_dir, 'main')
    hdf5_build = os.path.join(hdf5_base_dir, 'build')
    hdf5_install = os.path.join(hdf5_base_dir, 'install')

    # Define where to put the module file
    modulepath = systemcfg['MODULE_PATH']
    module_dir = os.path.join(modulepath, base_module)
    modulefilename = os.path.join(module_dir, hdf5_version)

    # Creating module file dynamically

    filestring = ""
    filestring += "#%Module\n\n"

    filestring += "proc ModulesHelp { } {\n"
    filestring += "    puts stderr 'Module is used to load HDF5 compiled for use with Specfem'\n"
    filestring += "}\n"
    filestring += "\n"
    filestring += 'module-whatis "This module load all necessary variables to build and use HDF5"\n'
    filestring += "\n\n"

    filestring += "# Setting environment variables\n"
    filestring += f'setenv HDF5_LINK "{hdf5_link}"\n'
    filestring += f'setenv HDF5_DIR "{hdf5_dir}"\n'
    filestring += f'setenv HDF5_BUILD "{hdf5_build}"\n'
    filestring += f'setenv HDF5_INSTALL "{hdf5_install}"\n'
    filestring += f'setenv HDF5_ROOT "{hdf5_install}"\n'
    filestring += f'setenv HDF5_CC "{hdf5_install}/bin/h5pcc"\n'
    filestring += f'setenv HDF5_FC "{hdf5_install}/bin/h5fc"\n'
    filestring += f'setenv MPIFC_HDF5 "{hdf5_install}/bin/h5fc"\n'
    filestring += f'setenv HDF5_MPI "ON"\n'
    filestring += f'setenv HDF5_VERSION "{hdf5_version}"\n'

    filestring += "\n\n\n"
    filestring += "# Setting path\n"

    # Set path variable
    filestring += 'set PATH $::env(PATH)\n'
    filestring += f'pushenv PATH "{hdf5_install}/bin:$PATH"\n'
    filestring += f'prepend-path PATH "{hdf5_install}/bin"\n'
    filestring += f'prepend-path LD_LIBRARY_PATH "{hdf5_install}/lib"\n'
    filestring += f'prepend-path C_INCLUDE_PATH "{hdf5_install}/include"\n'
    filestring += f'prepend-path F_INCLUDE_PATH "{hdf5_install}/include"\n'
    filestring += f'prepend-path PKG_CONFIG_PATH "{hdf5_install}/lib/pkgconfig"\n'

    # Make sure module_dir exists
    if not os.path.exists(module_dir):
        os.makedirs(module_dir)

    # Write module file
    with open(modulefilename, 'w') as f:
        f.write(filestring)


if __name__ == '__main__':
    base()
    adios()
    hdf5()

import os
import toml
import subprocess

filedirectory = os.path.dirname(os.path.realpath(__file__))
configdir = os.path.join(filedirectory, '..', 'configs')


def adios():

    # Load configs
    maincfg = toml.load(os.path.join(configdir,'main.toml'))
    system = maincfg['SYSTEM']
    systemcfg = toml.load(os.path.join(configdir,'system.toml'))[system]

    # Skip if installed version is being used.
    if len(systemcfg['USE_INSTALLED_ADIOS']) != 0:
        print("No need to install ADIOS, when it is already installed.")
        print(f"Using: systemcfg['USE_INSTALLED_ADIOS']")
        return

    # Get environment variables
    adios_dir = os.environ['ADIOS_DIR']
    adios_build = os.environ['ADIOS_BUILD']
    adios_install = os.environ['ADIOS_INSTALL']
    adios_version = os.environ['ADIOS_VERSION']
    adios_link = os.environ['ADIOS_LINK']

    # Download ADIOS if it doesnt exist
    if os.path.exists(adios_install):
        print(72*"=")
        print('This adios version is already installed.')
        print('If you want to reinstall, please delete the install directory.')
        print(f'--> {adios_install}')
        print(72*"=")
        return

    # Make sure path exists
    if not os.path.exists(adios_build):
        os.makedirs(adios_build)

    if int(adios_version[0]) == 1:

        # FIXME: ADIOS 1 - Only if someone is asking for it

        # Make sure path exists
        if os.path.exists(adios_dir) == False:
            os.makedirs(adios_dir)

        # Get ADIOS
        subprocess.run(f'wget --no-check-certificate -O adios.tar.gz "{adios_link}"', check=True, shell=True)
        subprocess.run(f'tar -xzvf adios.tar.gz --strip-components=1 -C {adios_dir}', check=True, shell=True)

    else:

        # Make sure path exists
        if not os.path.exists(adios_build):
            os.makedirs(adios_build)

        cmakecmd = (
            f'cd {adios_build} && '
            'CC=$(which mpicc) CXX=$(which mpicxx) MPICC=$(which mpicc) '
            f'cmake -DCMAKE_INSTALL_PREFIX={adios_install} '
            '-DADIOS2_USE_MPI=ON '
            '-DADIOS2_USE_FORTRAN=ON '
            '-DADIOS2_USE_HDF5=OFF '
            f'{adios_dir}'
            )

        # Configure
        subprocess.run(f'{cmakecmd}', check=True, shell=True)

        # Make
        makecmd = f'cd {adios_build} && make -j 16'
        subprocess.run(f'{makecmd}', check=True, shell=True)

        # Install
        installcmd = f'cd {adios_build} && make install'
        subprocess.run(f'{installcmd}', check=True, shell=True)


def hdf5():

     # Load configs
    maincfg = toml.load(os.path.join(configdir,'main.toml'))
    system = maincfg['SYSTEM']
    systemcfg = toml.load(os.path.join(configdir,'system.toml'))[system]

    if len(systemcfg['USE_INSTALLED_HDF5']) != 0:
        print("No need to install HDF5, when it is already installed.")
        print(f"Using: systemcfg['USE_INSTALLED_HDF5']")
        return

    # Get environment variables
    hdf5_dir = os.environ['HDF5_DIR']
    hdf5_build = os.environ['HDF5_BUILD']
    hdf5_version = os.environ['HDF5_VERSION']
    hdf5_install = os.environ['HDF5_INSTALL']
    hdf5_dirs = [
        os.path.join(hdf5_dir, 'hdf5-'+hdf5_version),
        os.path.join(hdf5_dir, 'CMake-hdf5-'+hdf5_version, 'hdf5-'+hdf5_version),
        os.path.join(hdf5_dir, 'hdf5-'+hdf5_version,
                     'CMake-hdf5-'+hdf5_version, 'hdf5-'+hdf5_version),
    ]

    # Looping over all possible directories, checking for cmakelists.txt
    for _hdf5_dir in hdf5_dirs:
        if os.path.exists(os.path.join(_hdf5_dir, 'CMakeLists.txt')):
            hdf5_dir = _hdf5_dir
            break

    # Raise error if none of the directories exist
    else:
        dirstring = '\n- '.join(hdf5_dirs)
        raise FileNotFoundError(f"Could not find HDF5 directory in \n\n- {dirstring}\n")

    hdf5_root = os.environ['HDF5_ROOT']

    # Download HDF5 if it doesn't exist
    if os.path.exists(hdf5_install):
        print(72*"=")
        print('This HDF5 version is already installed.')
        print('If you want to reinstall, please delete the install directory.')
        print(f'--> {hdf5_install}')
        print(72*"=")
        return

    # Make sure build directory is empty
    if os.path.exists(hdf5_build):
        subprocess.run(f'rm -rf {hdf5_build}/*', check=True, shell=True)
    else:
        # Make sure path exists
        os.makedirs(hdf5_build)

    # Configuration
    cmakecmd = (
        f'cd {hdf5_build} && '
        'CC=$MPICC '
        'FC=$MPIFC '
        'CXX=$MPICXX '
        f'cmake -S {hdf5_dir} -B {hdf5_build} '
        '-G "Unix Makefiles" '
        '-DCMAKE_BUILD_TYPE=Release '
        f'-DCMAKE_INSTALL_PREFIX={hdf5_install} '
        '-DHDF5_ENABLE_PARALLEL=ON  '
        '-DBUILD_SHARED_LIBS=ON '
        '-DHDF5_BUILD_CPP_LIB=OFF '
        '-DHDF5_BUILD_FORTRAN=ON '
        '-DHDF5_BUILD_JAVA=OFF '
        '-DHDF5_ENABLE_THREADSAFE=OFF '
    )

    # Configure
    subprocess.run(f'{cmakecmd}', check=True, shell=True)

    # Make
    makecmd = f'cmake --build {hdf5_build} --parallel 10'
    subprocess.run(f'{makecmd}', check=True, shell=True)

    # Install
    installcmd = f'cmake --install {hdf5_build} --prefix {hdf5_install}'
    subprocess.run(f'{installcmd}', check=True, shell=True)

if __name__ == "__main__":

    adios()
    hdf5()


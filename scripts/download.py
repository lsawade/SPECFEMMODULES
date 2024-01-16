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
    adios_version = os.environ['ADIOS_VERSION']
    adios_link = os.environ['ADIOS_LINK']

    # Download ADIOS if it doesnt exist
    if os.path.exists(adios_dir) == False:

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
            if os.path.exists(os.path.dirname(adios_dir)) == False:
                os.makedirs(os.path.dirname(adios_dir))

            # Getting the git directory
            subprocess.run(f'git clone "{adios_link}" {adios_dir}', check=True, shell=True)


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
    hdf5_link = os.environ['HDF5_LINK']

    # Download HDF5 if it doesn't exist
    if os.path.exists(hdf5_dir) == False:

        # Make sure path exists
        if os.path.exists(hdf5_dir) == False:
            os.makedirs(hdf5_dir)

        # Get HDF5
        subprocess.run(f'wget -O hdf5.tar.gz "{hdf5_link}"',
                       check=True, shell=True)
        subprocess.run(f'tar -xzvf hdf5.tar.gz --strip-components=1 -C {hdf5_dir}',
                       check=True, shell=True)


if __name__ == "__main__":

    adios()
    hdf5()

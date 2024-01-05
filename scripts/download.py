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

            # Make sure path exists
            os.makedirs(adios_dir)

            # Get ADIOS
            subprocess.run(f'wget --no-check-certificate -O adios.tar.gz "{adios_link}"')
            subprocess.run(f'tar -xzvf adios.tar.gz --strip-components=1 -C {adios_dir}')

        else:

            # Make sure path exists
            os.makedirs(os.path.dirname(adios_dir))

            # Getting the git directory
            subprocess.run(f'git clone {adios_link} {adios_dir}')


def hdf5():

     # Load configs
    maincfg = toml.load(os.path.join(configdir,'main.toml'))
    system = maincfg['SYSTEM']
    systemcfg = toml.load(os.path.join(configdir,'system.toml'))[system]

    if len(systemcfg['USE_INSTALLED_HDF5']) != 0:
        print("No need to install ADIOS, when it is already installed.")
        print(f"Using: systemcfg['USE_INSTALLED_ADIOS']")
        return




if __name__ == "__main__":

    adios()

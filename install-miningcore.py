import subprocess
#define global vars which will be used in instalation procdure

ubuntuversion = "0"
miningcore_git_repo = "https://github.com/oliverw/miningcore"
# START Helper functions

def run_command(command):
    p = subprocess.run(command,
                         shell=True, check=True)
    return p

def run_command_returnoutput(command):
    return subprocess.getoutput(command)

def getubuntuversion():
    versionconf = run_command_returnoutput('cat /etc/os-release | grep VERSION_ID')
    actualversion = versionconf.replace('"','')
    actualversion = actualversion.replace('VERSION_ID=','')
    print(actualversion)

#END Helper code

#actual installation code here

def setupinitaldb():
    run_command('createuser miningcore')
    run_command('createdb miningcore')
    run_command('psql -d miningcore -U miningcore -f ~/miningcore/src/Miningcore/Persistence/Postgres/Scripts/createdb.sql')

def update_system_packages():
    run_command('sudo apt update')
    run_command('sudo apt upgrade -y')

def installbuildtools():
    run_command('sudo apt-get install build-essential make cmake wget curl git tmux -y')

def install_postgresql():
    run_command('echo \'deb http://apt.postgresql.org/pub/repos/apt/'+ ubuntuversion +'-pgdg main\'/etc/apt/sources.list.d/pgdg.list')
    run_command('wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -')
    run_command('sudo apt-get update')
    run_command('sudo apt install postgresql-12')

def install_dotnet():
    run_command('wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb')
    run_command('sudo dpkg -i packages-microsoft-prod.deb')
    run_command('sudo apt-get update')
    run_command('sudo apt-get install apt-transport-https')
    run_command('sudo apt-get update')
    run_command('sudo apt-get install dotnet-sdk-3.1')

def install_miningcore():
    run_command('cd ~ && git clone ' + miningcore_git_repo)
    print('Building miningcore from source')
    run_command('cd miningcore/src/Miningcore && dotnet publish -c Release --framework netcoreapp3.1  -o ..\..\build')
    print('Done building miningcore')

def doinstall():
    update_system_packages()
    installbuildtools()
    #Now begin actual install of dependencies 1 by one
    install_dotnet()
    install_postgresql()
    install_miningcore()
    setupinitaldb()
    


# Ubuntu 18.04 disk image with RSH and MPI installed

## Download the ubuntu-18.04-arm64-docker.img.bz2 disk image from gem5 official repository: 
https://www.gem5.org/documentation/general_docs/fullsystem/guest_binaries \

## Mount the disk image through following commands
sudo mount -o loop,offset=65536 $HOME/COSSIM/kernels/disks/ubuntu-18.04-arm64-docker.img /mnt \
cd /mnt \
sudo mount --bind /proc /mnt/proc \
sudo mount --bind /dev /mnt/dev \
sudo chroot .

echo "nameserver 8.8.8.8" > /etc/resolv.conf


## Install the following packets
apt update \
apt install build-essential \
apt install net-tools \
apt install rsh-server \
apt install rsh-client \
apt install xinetd \
apt install vim \
apt install iputils-ping

## Start rsh server in Ubuntu 18.04 simulated image
Add the [rsh](rsh) file content in /etc/xinetd.d/rsh file

## Create the hosts file in Ubuntu 18.04 simulated image
The following configuration is for 2 nodes (i.e. node0 and node1). To be noticed that you must add all simulated nodes (e.g. if you would like to simulate 3 nodes, node2 must be added in the last /etc/hosts line).

echo "127.0.0.1 localhost" >> /etc/hosts \
echo "192.168.0.2 node0" >> /etc/hosts \
echo "192.168.0.3 node1" >> /etc/hosts

## Create a .rhosts file in the root home directory and write the hostnames of the hosts in order to access password-free
The following configuration is for 2 nodes (i.e. node0 and node1). To be noticed that you must add all simulated nodes (e.g. if you would like to simulate 3 nodes, node2 must be added).

echo "node0 root" >> /root/.rhosts \
echo "node1 root" >> /root/.rhosts

# OpenMPI Instalation
## Download the openmpi (v2.1.6)
https://www.open-mpi.org/software/ompi/v2.1/ 

## Install from source the openmpi (v2.1.6)
https://edu.itp.phys.ethz.ch/hs12/programming_techniques/openmpi.pdf 

## Create an mpi script file in Ubuntu 18.04 simulated image
The following configuration is for 2 nodes (i.e. node0 and node1). To be noticed that you must add all simulated nodes (e.g. if you would like to simulate 3 nodes, node2 must be added).

echo "hostname node0" >> mpi_execution_script \
echo "rsh 192.168.0.3 hostname node1" >> mpi_execution_script \
echo "m5 resetstats" >> mpi_execution_script \
echo "mpirun --allow-run-as-root --prefix /opt/openmpi -np 2 --host node0,node1 ./mpi_hello_world" >> mpi_execution_script \
echo "m5 dumpstats" >> mpi_execution_script \
echo "rsh 192.168.0.3 m5 exit &" >> mpi_execution_script \
chmod +x mpi_execution_script

# MPICH Instalation
apt install mpich

## Create a host_file
echo "node0:1" >> host_file \
echo "node1:1" >> host_file

Use this command: mpirun -launcher rsh -n 2 -f host_file ./mpi_hello_world

## Add the following line in gem5 script
/etc/init.d/xinetd start 


## Umount the disk image
exit \
cd \
sudo umount /mnt/proc \
sudo umount /mnt/dev \
sudo umount /mnt


# VEF traces (optional)
apt install cmake \
Download and install VEF prospector from here: https://gitraap.i3a.info/fandujar/VEF-Prospector

## Create a VEF mpi script file in Ubuntu 18.04 simulated image (obtain traces)
The following configuration is for 2 nodes (i.e. node0 and node1). To be noticed that you must add all simulated nodes (e.g. if you would like to simulate 3 nodes, node2 must be added). \

echo "hostname node0" >> vef_mpi_execution_script \
echo "rsh 192.168.0.3 hostname node1" >> vef_mpi_execution_script \
echo "export PATH=$PATH:/opt/vef_prospector/bin/" >> vef_mpi_execution_script \
echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/vef_prospector/lib/" >> vef_mpi_execution_script \
echo "m5 resetstats" >> vef_mpi_execution_script \
echo "vmpirun -launcher rsh -n 2 -f host_file ./mpi_hello_world" >> vef_mpi_execution_script \
echo "m5 dumpstats" >> vef_mpi_execution_script \
echo "rsh 192.168.0.3 m5 exit &" >> vef_mpi_execution_script \
chmod +x vef_mpi_execution_script

# Get the comm and veft files from other gem5 nodes
```
cd /mpi_hello_world-*
rsh 192.168.0.3 cat /mpi_hello_world-*/1.comm >> 1.comm
rsh 192.168.0.3 cat /mpi_hello_world-*/1.veft >> 1.veft
```


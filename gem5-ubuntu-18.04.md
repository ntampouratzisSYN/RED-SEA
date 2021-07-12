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
Add the rsh file content in /etc/xinetd.d/rsh file

## Create the hosts file in Ubuntu 18.04 simulated image
The following configuration is for 2 nodes (i.e. node0 and node1). To be noticed that you must add all simulated nodes (e.g. if you would like to simulate 3 nodes, node2 must be added in the last /etc/hosts line). \

echo "127.0.0.1 localhost" >> /etc/hosts \
echo "192.168.0.2 node0" >> /etc/hosts \
echo "192.168.0.3 node1" >> /etc/hosts

## Create an mpi script file in Ubuntu 18.04 simulated image
The following configuration is for 2 nodes (i.e. node0 and node1). To be noticed that you must add all simulated nodes (e.g. if you would like to simulate 3 nodes, node2 must be added). \

echo "hostname node0" >> execution_script \
echo "rsh 192.168.0.3 hostname node1" >> execution_script \
echo "m5 resetstats" >> execution_script \
echo "mpirun --allow-run-as-root --prefix /opt/openmpi -np 2 --host node0,node1 ./mpi_hello_world" >> execution_script \
echo "m5 dumpstats" >> execution_script \
echo "rsh 192.168.0.3 m5 exit &" >> execution_script \
chmod +x execution_script

## Add the following line in gem5 script
/etc/init.d/xinetd restart 


## Umount the disk image
exit \
cd \
sudo umount /mnt/proc \
sudo umount /mnt/dev \
sudo umount /mnt

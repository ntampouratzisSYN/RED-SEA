# How to execute MPI on COSSIM?

## Declare how many gem5 nodes you want to simulate
```
gedit /home/red-sea/COSSIM/cgem5/run.sh
```

This is an example with 3 nodes:
```
$GEM5/build/ARM/gem5.opt --listener-mode=on -r -d $GEM5/node0 $GEM5/configs/example/arm/starter_fs.py --kernel=vmlinux.arm64 --num-cores=2 --disk-image=ubuntu-18.04-arm64-docker.img --SynchTime=100us --RxPacketTime=10us --TotalNodes=3 --nodeNum=0 --script=$GEM5/configs/boot/COSSIM/script0.rcS --etherdump=$GEM5/node0/ether_node0 --cossim &
$GEM5/build/ARM/gem5.opt --listener-mode=on -r -d $GEM5/node1 $GEM5/configs/example/arm/starter_fs.py --kernel=vmlinux.arm64 --num-cores=2 --disk-image=ubuntu-18.04-arm64-docker.img --SynchTime=100us --RxPacketTime=10us --TotalNodes=3 --nodeNum=1 --script=$GEM5/configs/boot/COSSIM/script1.rcS --etherdump=$GEM5/node1/ether_node1 --cossim &
$GEM5/build/ARM/gem5.opt --listener-mode=on -r -d $GEM5/node2 $GEM5/configs/example/arm/starter_fs.py --kernel=vmlinux.arm64 --num-cores=2 --disk-image=ubuntu-18.04-arm64-docker.img --SynchTime=100us --RxPacketTime=10us --TotalNodes=3 --nodeNum=2 --script=$GEM5/configs/boot/COSSIM/script2.rcS --etherdump=$GEM5/node2/ether_node2 --cossim &
```

If you may need to add more nodes please the add the following line (where XXX the number of node - i.e. if you would like to add a 4th node, XXX=3 and XXX+1=4. To be notoced that you need to change the TotalNodes to TotalNodes=4 in all commands):
```
$GEM5/build/ARM/gem5.opt --listener-mode=on -r -d $GEM5/nodeXXX $GEM5/configs/example/arm/starter_fs.py --kernel=vmlinux.arm64 --num-cores=2 --disk-image=ubuntu-18.04-arm64-docker.img --SynchTime=100us --RxPacketTime=10us --TotalNodes=XXX+1 --nodeNum=XXX --script=$GEM5/configs/boot/COSSIM/scriptXXX.rcS --etherdump=$GEM5/nodeXXX/ether_nodeXXX --cossim &
```





## Mount the disk image
sudo mount -o loop,offset=65536 $HOME/COSSIM/kernels/disks/ubuntu-18.04-arm64-docker.img /mnt \
cd /mnt \

## Copy the MPI application to Ubuntu 18.04 simulated image
cp /home/red-sea/Desktop/mpi_hello_world.c .

# Emulate the image through QEMU
sudo mount --bind /proc /mnt/proc \
sudo mount --bind /dev /mnt/dev \
sudo chroot .

echo "nameserver 8.8.8.8" > /etc/resolv.conf

## Create the hosts file in Ubuntu 18.04 simulated image
You need to add the IP with the hostname for each gem5 node
```
vi /etc/hosts
```

This is an example for 3 nodes: \
127.0.0.1 localhost \
192.168.0.2 node0 \
192.168.0.3 node1 \
192.168.0.4 node2

## Create a .rhosts file in Ubuntu 18.04 simulated image
You need to create a .rhosts in the root home directory and write the hostnames of the hosts in order to access password-free
```
vi /root/.rhosts
```

This is an example for 3 nodes: \
node0 root \
node1 root \
node2 root

## Create a host_file in Ubuntu 18.04 simulated image
You need to create a host_file in order to tell the MPI where the application must be executed

```
vi host_file
```

This is an example for 3 nodes: \
node0:1 \
node1:1 \
node2:1

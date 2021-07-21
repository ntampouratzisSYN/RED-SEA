#How to execute MPI on COSSIM?

## Mount the disk image through following commands
sudo mount -o loop,offset=65536 $HOME/COSSIM/kernels/disks/ubuntu-18.04-arm64-docker.img /mnt \
cd /mnt \
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

#!/bin/bash

export VAGRANT_EXPERIMENTAL="disks"
export EXP="auto"

qemu-img create -f raw /tmp/disk1.img 100M

vagrant up 2> /dev/null
vagrant ssh -- "sudo umount /mnt && sudo mkfs -t ext4 /dev/sdb && sudo mount /dev/sdb /mnt" 2> /dev/null
vagrant ssh -- "cd /browserbench && gcc -O3 smallfile.c -o smallfile && gcc -O3 largefile.c -o largefile" 2> /dev/null

mkdir -p results

for i in {0..499}
do
  vagrant ssh -- "mkdir -p /tmp/testdir && rm -r /tmp/testdir/*; /browserbench/smallfile /tmp/testdir" > results/smallfile.${EXP}.${i} 2> /dev/null
done

for i in {0..499}
do
   vagrant ssh -- "mkdir -p /tmp/testdir && rm -r /tmp/testdir/*; /browserbench/largefile /tmp/testdir" > results/largefile.${EXP}.${i} 2> /dev/null
done

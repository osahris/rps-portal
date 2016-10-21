[[!meta title="Setting up and rolling out new systems"]]

When setting up a new machine or virtual machine
and installing the operating system of your choice,
make sure to follow these steps:

Partitioning
------------
If the disk is not already partitioned, initialize it using the
"GUID Partition Table" (GPT).

As first partition, create an "EFI System Partition" (ESP) of 
about 500 MiB size.

If installing Windows™, partitioning the system drive using GPT means
you _have_ to boot using UEFI - so make sure your mainboard is new
enough to handle this.

Installing the Operating System
-------------------------------


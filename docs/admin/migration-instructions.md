Instructions on migrating instance data into a new deployment
=============================================================

Nextcloud
---------

### Exporting the SQL database
Add the old host temporarily to an inventory file, e.g. `inventory-mine`, in the group `[rps_old_servers]`.
Make sure to set the variables `ansible_ssh_user`, `rps_admin_email` and `rps_dns_suffix` here.

<!-- TODO: set nextcloud_import=local_folder or call the specialized playbook when it works. -->

On the old system, create an export of Nextcloud's PostgreSQL database using `pg_dump`.
On an RPS legacy instance (RPS 1.0 and below), this would look as follows:

```
root@legacyhost:~# lxc exec cloud -- su postgres -c 'pg_dump nextcloud' - > /tmp/nextclouddb.sql
```

Now for the simplified workflow (assuming your data privacy guidelines allow
this), copy the file to your local machine:

```
$ rsync -avrzP --inplace root@legacyhost:/tmp/nextclouddb.sql
```

### Importing the SQL database

TODO

### Moving the `files` storage from one system to the other

TODO


# Ansible role for a MVP of a service under Traefik

This is a minimum viable product (MVP) of a service running in a docker container.
Runs under the reverse proxy from a Traefik container.
Deployable as an Ansible role.

## How to run this role in an Ansible playbook:

As an example, you may organize the following simple Ansible playbook structure for your stack to be deployed:
```text
.
├── inventory
├── <playbook-name>.yaml
└── roles
    ├── my_project
    │   ├── defaults
    │   ├── files
    │   ├── tasks
    │   ├── templates
    │   └── vars
    └── traefik
        └── ...
```
  The content of each file and folder is discussed below.

1. In the **inventory** file you specify the hosts on which Ansible should perform the tasks. Example of that file content:
  ```yaml
  # ./inventory/hosts
  [<server_group>]
  <domain.name.net> ansible_ssh_host=12.34.56.78 ansible_ssh_user=root admin_email=adminusername@domain.name.net
  ```

2. In the  **<playbook-name>.yaml** file you specify the tasks and roles that this Ansible playbook consists of. Example of that file content:
  ```yaml
  # <playbook-name>.yaml
  ---
  - name: <playbook-name>
    hosts: <server_group>
    become: yes
  
    roles:
      - role: traefik
        tags: traefik
      - role: my_project
        tags: my_project
  ```

3. In the **/tasks/** folder content you specify the tasks that this Ansible role consists of. For each role named in the  **<playbook-name>.yaml** file Ansible executes tasks at least from **/tasks/main.yaml**. In this MVP demo the tasks are the following:
    - a. display target host(s)
    - b. create the project directory
    - c. copy all static files from **./files** to {{remote_path}} on the host(s)
    - d. copy some templated .j2 files from **./templates** to {{remote_path}} on the host(s). Files to template-copy are listed under *with_items*
    - e. copy the dynamic configuration for Traefik
    - f. deploy the project stack with docker-compose files listed under *with_items*
Here, the {{remote_path}} will be automatically replaced by the value from the **./defaults/main.yaml**, **./vars/main.yaml** or **./inventory** (increasing priority order).

4. The variables from **/defaults/main.yaml** will be used for templating on the step **d** in the list above.

5. The variables from **/vars/main.yaml** will be used for templating on the step **d** in the list above. These ones will override the values from **/defaults/main.yaml**.

6. The folder **./roles/traefik** contains the Ansible role for a Docker container with Treafik (https://gitlab.com/idcohorts/rps/research-project-suite/-/tree/dev/roles/traefik).

4. To execute this Ansible playbook run in the shell:
    ```shell
    $ ansible-playbook -i ./inventory ./<playbook-name>.yaml
    ```
    If you don't have a needed SSH Key, use password authentication:
    ```shell
    $ ansible-playbook -i ./inventory ./<playbook-name>.yaml --ask-pass --ask-become-pass
    ```

5. Observe your web-service by default under **https://mvp.<domain.name.net>** with **<domain.name.net>** taken from the **./inventory** file. This is defined via the **{{service_domain_name}}** value in the **./defaults/main.yaml** and the configuration of Traefik (see more info below).



## How to use this MVP to create a role for your own service:

By default this MVP will set up a NginX webserver listening to a custom port value 801. The SSL certificate provider is by default **letsencrypt** as defined by variable **traefik_certresolver** in **./vars/main.yaml**.

As defined in **templates/docker-compose.yaml.j2**, additional environment variables are take from **./templates/env.j2**. The docker network **proxy** is used to connect with Traefik, the network **{{project_name}}** is used for internal communications of different docker containers (if there are more) out of scope of Traefik.

1. Copy this role folder and rename it to some **./roles/\<project_name\>**.

2. Change **service_name** in **./defaults/main.yaml** and add the required content in:
    - **./files/...**
    - **./templates/docker-compose.yaml.j2**
    - **./templates/env.j2**
    - **./vars/main.yaml**

3. By default, your service will run under the domain **https://{{service_domain_name}}** defined in **./vars/main.yaml** by the following code:
    ```yaml
    # ./vars/main.yaml
    traefik_dynamic_config:
      http:
        routers:
          mvp: # <-- Change this to your service name
            rule: "Host(`{{service_domain_name}}`)"
    ```

4. If you need your service running under **https://{{service_domain_name}}/app_name/**, use this in **./vars/main.yaml**:
    ```yaml
    # ./vars/main.yaml
    traefik_dynamic_config:
      http:
        routers:
          mvp: # <-- Change this to your service name
            rule: "Host(`{{service_domain_name}}`) && ( PathPrefix(`/app_name/`) || Path(`/app_name`) ) )"
    ```

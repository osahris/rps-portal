# how traefik works:
1. for every service there needs to be a config on the host machine: "/etc/traefik/conf.d/servicename.yaml"
# example: 
```
{
    "http": 
    {
        "routers": 
        {
            "servicename": 
            {
                "rule": "Host(`servicename.{{rps_dns_suffix}}`)", 
                "entrypoints": "websecure", 
                "service": "servicename"
                
            }
        },     
        "services":
        {
            "servicename": 
            {
                "loadBalancer": 
                {
                    "servers": 
                        [
                            {
                                "url": "http://service_container_name:8080"
                            }
                        ]
                }
            }
        }
    }
}
```

2. deploy traefik


# things to do to create new ansible role and use reverse-proxy
1. create role folder -> mkdir ansible-role-example
2. create subfolder -> 
        mkdir ansible-role-example/defaults 
        && mkdir ansible-role-example/tasks 
        && mkdir ansible-role-example/vars 
        && mkdir ansible-role-example/...
3. set var service_traefik_dynamic_config in vars
    ```
    service_traefik_dynamic_config:
        http:
            routers:
                servicename:
                    rule: "Host(`servicename{{inventory_host}}`)"
                    entrypoints: websecure
                    service: servicename
            services:
                servicename:
                    loadBalancer:
                        servers:
                            - url: http://service_container_name:8080
    ```
4. copy var to traefik conf directory
    ```
        - name: traefik dynamic config
    	    copy:
                content: "{{ keycloak_traefik_dynamic_config | to_nice_yaml(indent=2, width=777) }}"
                dest: "{{traefik_config_directory}}/conf.d/keycloak.yaml" 
    ```

5. deploy and enjoy :)
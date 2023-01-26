Role Name
=========

Ansible role to deploy keycloak

Requirements
------------

This ansible role uses the community.general module



## Registration mask

Files can be found in /templates folder

Configuration on which items should the NUM regisration mask should have can be found [here] (https://cloud.netzwerk-universitaetsmedizin.de/f/33227)

Example for NAPKON Keycloak Theme can be found [here] (https://gitlab.com/idcohorts/napkon/keycloak-theme/)

### Testing the registration mask
Deploy it by executing following playbook with no inventory give

```sh
ansible-playbook dev-registration-page.yaml
```

Then check on the registration [page] (https://accounts.dev.numhub.de/realms/numhub/account/)

### Warning
Please #rules and structure keep them identical!!!

### TODOs:
- [ ] Configure Keycloak User Attributes
- [ ] NUM Projekte ergänzen
- [ ] Add Unorm for user name (https://github.com/walling/unorm)
- [ ] Add validation for the form
- [ ] Add filtering to all other questions (as of now it is just implemented for dropdownmenus)

Theming
- [ ] Einheitliches Design/Theme verwenden
- [ ] Split into multiple step form

Fragen:
- [ ] Verlinkung zu anderen Projekten ermöglichen?
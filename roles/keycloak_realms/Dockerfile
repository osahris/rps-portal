FROM python:3

RUN pip install ansible
RUN ansible-galaxy collection install community.general

WORKDIR /ansible

RUN mkdir -p roles/keycloak-realms
COPY . roles/keycloak-realms
COPY docker/playbook.yml .

VOLUME /config

CMD ["ansible-playbook", "playbook.yml", "--extra-vars", "@/config/realms.yml"]


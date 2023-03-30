FROM debian:bookworm

RUN apt-get install -y ansible && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /usr/share/ansible/collections/ansible_collections/rps/apps

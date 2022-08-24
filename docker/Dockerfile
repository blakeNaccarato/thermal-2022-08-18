FROM gunns_loaded
RUN yum remove -y git \
    && rpm -U https://repo.ius.io/ius-release-el7.rpm \
    && yum install -y git236 \
    && rm /root/.bashrc
COPY setup.sh /root/setup.sh

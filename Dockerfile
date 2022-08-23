FROM gunns_loaded
RUN yum remove -y git \
        && rpm -U https://repo.ius.io/ius-release-el7.rpm \
        && yum install -y git236 \
        && \cp /home/gunns/bin/bashrc /root/.bashrc \
        && \cp /home/gunns/bin/cshrc /root/cshrc \
        && sed -i "s/cshrc/.cshrc/g" "/root/.bashrc"

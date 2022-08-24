FROM gunns_loaded
RUN yum remove -y git \
    && rpm -U https://repo.ius.io/ius-release-el7.rpm \
    && yum install -y git236
RUN git clone https://github.com/blakeNaccarato/gunns-sims.git /root/gunns-sims
RUN /bin/cp gunns-sims/root/.bashrc /root/.bashrc \
    && /bin/cp gunns-sims/root/.cshrc /root/.cshrc

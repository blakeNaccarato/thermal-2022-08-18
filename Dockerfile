FROM gunns_loaded
RUN yum remove -y git \
    && rpm -U https://repo.ius.io/ius-release-el7.rpm \
    && yum install -y git236
RUN rm -r /root
COPY root /root
COPY . /root/gunns-sims

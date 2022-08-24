FROM gunns_loaded
RUN yum remove -y git \
    && rpm -U https://repo.ius.io/ius-release-el7.rpm \
    && yum install -y git236 \
RUN adduser user && passwd -d user
WORKDIR /home
COPY ./user ./user
COPY . /user/gunns-sims
COPY ./volume-setup-in-container.sh /home/
ENTRYPOINT ["su", "user"]

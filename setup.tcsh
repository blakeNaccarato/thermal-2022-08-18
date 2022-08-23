#!/bin/tcsh
# Source the `.tcshrc` from this repo to the root user.

cat <<EOF > .tcshrc
#!/bin/tcsh
source /root/gunns_sims/.tcshrc
EOF

#!/bin/tcsh
# Source the `.cshrc` from this repo to the root user.

cat <<EOF > .cshrc
#!/bin/tcsh
source thermal-2022-08-18/.cshrc
EOF

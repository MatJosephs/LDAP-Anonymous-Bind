#!/bin/sh
for target in $(cat targets.txt); do echo "Naming Context for $target"; timeout 5 ldapsearch -H ldap://$target -x -s base namingcontexts;echo "#########################################################";done

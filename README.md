# LDAP Anonymous Bind

This project helps extract information from LDAP when anonymous binding is allowed. 

## Worflow
1. Search for "LDAP Anonymous" on Shodan
2. Generate a JSON report
3. Extract the IPs from the Shodan report
4. Save the list of IPs as **target.txt**
5. Run ```findnamingcontexts.sh | tee ldap_search.output```
6. Run ```python3 ldapparse.py```
7. Check the **OUTPUT** folder

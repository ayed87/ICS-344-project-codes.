#!/bin/bash



# Path to the Apache access log file

APACHE_LOG="/var/log/apache2/access.log"


# Threshold for failed login attempts

THRESHOLD=5



# Path to a blacklist file for logging blocked IPs

BLACKLIST_FILE="/var/www/html/wordpress/defense/blacklist.txt"



# Search for repeated POST requests to wp-login.php

SUSPICIOUS_IPS=$(grep "POST /wordpress/wp-login.php" $APACHE_LOG | awk '{print $1}' | sort | uniq -c | awk '$1 > '"$THRESHOLD"' {print $2}')

echo $SUSPICIOUS_IPS

for IP in $SUSPICIOUS_IPS; do

    echo "Blocking IP: $IP"



    # Add IP to UFW block list (or iptables)
    ufw insert 1 deny from $IP




    # Optionally, log the blocked IP

    echo "$(date) - Blocked IP: $IP" >> $BLACKLIST_FILE

done

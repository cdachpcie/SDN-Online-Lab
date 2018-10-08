#! /bin/bash
while sleep 5
do    
    shutter -f -o 'date+%H%M%S.jpg' -e
done

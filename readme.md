# lokinet exit provider 

docker jizz for running lokinet exits.

**ABSOLUTELY *ZERO* TECH SUPPORT PROVIDED**

## running

### requirements

to use this you need the following:

* docker
* docker-compose

### usage

to start a new unauthenticated exit:

    $ docker-compose up -d

get the `.loki` address:

    $ docker-compose exec lokinet print-lokinet-address.sh

to update the exit image:

    $ docker-compose down
    $ docker-compose pull lokinet
    $ docker-compose up -d



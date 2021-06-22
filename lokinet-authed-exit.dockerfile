# set up auth
FROM registry.oxen.rocks/lokinet-exit:latest
COPY contrib/lokinet-auth.ini /var/lib/lokinet/conf.d/auth.ini

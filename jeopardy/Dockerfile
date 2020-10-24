############################################################
# Dockerfile to host a binary challenge
# Based on python image
############################################################

# Set the base image to python
FROM python

# File Author / Maintainer
MAINTAINER fabiano

# Update the repository
RUN apt-get update

# Install necessary tools
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -qq gdbserver socat

# Expose ports
EXPOSE 2222:2222 2223:2223 2224:2224

# Set the default command to execute
# when creating a new container
WORKDIR /root
CMD python3 ./run.py

FROM ubuntu:latest
LABEL authors="user1"

ENTRYPOINT ["top", "-b"]
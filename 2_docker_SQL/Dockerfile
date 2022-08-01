FROM python:3.9

RUN pip install pandas

# Where it goes when it is run
WORKDIR /app

COPY pipeline.py pipeline.py

#ENTRYPOINT [ "bash" ] # (1)
ENTRYPOINT [ "python" , "pipeline.py" ] # (2)

# To build:
# docker build -t test:pandas 2_docker_SQL/ <--- since you are standing at root

# To run:
# docker run -it test:pandas (1)
# docker run -it test:pandas 1 345 (2) <---- since pipeline has inparameters ... or ask for sys.argv[1]


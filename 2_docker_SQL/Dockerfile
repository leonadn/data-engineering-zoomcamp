FROM python:3.9

RUN pip install pandas

# Where it goes when it is run
WORKDIR /app

COPY pipeline.py pipeline.py

#ENTRYPOINT [ "bash" ]
ENTRYPOINT [ "python" , "pipeline.py" ]


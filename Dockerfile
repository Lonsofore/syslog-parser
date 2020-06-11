# test stage
FROM python:3-slim

# copy script files
COPY ./parser.py ./test_parser.py ./requirements_test.txt ./requirements.txt /app/

# test the script
RUN pip install --no-cache-dir -r /app/requirements_test.txt \
    && pip install --no-cache-dir -r /app/requirements.txt
RUN pytest /app


# final stage
FROM python:3-slim

# copy script file
COPY ./parser.py ./requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# run script
CMD python /app/parser.py

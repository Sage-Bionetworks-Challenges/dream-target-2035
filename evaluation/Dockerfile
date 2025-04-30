FROM --platform=linux/amd64 python:3.12.9-slim-bullseye

# Set default working directory.
WORKDIR /usr/local/bin

# Copy over Python dependencies file and install.
COPY requirements.txt .
RUN pip install \
    --no-cache-dir \
    --break-system-packages \
    -r requirements.txt

# Copy over validation and scoring scripts.
COPY evaluation_function.py .
COPY validate.py .
COPY score.py .

ENTRYPOINT [ "python" ]
CMD [ "score.py" ]

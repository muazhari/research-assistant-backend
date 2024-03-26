# Initialize the base image.
FROM muazhari/cuda-torch-tensorflow:latest

# Set the working directory environment.
ENV WORKDIR /app

# Set the working directory.
WORKDIR $WORKDIR
COPY . .

# Install python dependencies from requirements.txt.
RUN pip3 install -r requirements.txt



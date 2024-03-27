# Initialize the base image.
FROM muazhari/cuda-torch-tensorflow:latest

# Set the working directory environment.
ENV WORKDIR /app

# Set the working directory.
WORKDIR $WORKDIR

# Copy requirements.txt to the working directory.
COPY ./requirements.txt ./requirements.txt

# Install python dependencies from requirements.txt.
RUN pip3 install -r requirements.txt

# Copy rest of the files to the working directory.
COPY . .



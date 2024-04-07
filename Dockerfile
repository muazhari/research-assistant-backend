# Initialize the base image.
FROM muazhari/cuda-torch-tensorflow:latest

# Set the working directory environment.
ENV WORKDIR /app

# Set the working directory.
WORKDIR $WORKDIR

# Install apt dependencies.
RUN yes | DEBIAN_FRONTEND=noninteractive apt install -y \
    libmagic-dev \
    poppler-utils \
    tesseract-ocr \
    libreoffice \
    pandoc \
    libxml2-dev \
    libxslt1-dev \
    libgraphviz-dev \
    graphviz

# Install paddleocr
RUN pip3 install paddlepaddle-gpu -i https://pypi.tuna.tsinghua.edu.cn/simple

# Install unstructured[all-docs]
RUN pip3 install unstructured[all-docs]

# Install pymilvus[model]
RUN pip3 install pymilvus[model]

# Copy requirements.txt to the working directory.
COPY ./requirements.txt ./requirements.txt

# Install python dependencies from requirements.txt.
RUN pip3 install -r requirements.txt

# Copy rest of the files to the working directory.
COPY . .



# Initialize the base image.
FROM muazhari/cuda-torch-tensorflow:latest

# Set the working directory environment.
ENV WORKDIR=/workdir

# Set the working directory.
WORKDIR $WORKDIR

# Update the apt package index.
RUN apt update

# Install apt dependencies.
RUN yes | DEBIAN_FRONTEND=noninteractive apt install -y \
    libopencv-dev \
    libmagic-dev \
    poppler-utils \
    tesseract-ocr \
    libreoffice \
    pandoc \
    libxml2-dev \
    libxslt1-dev \
    libgraphviz-dev \
    graphviz \
    wkhtmltopdf

# Install paddlepaddle-gpu.
RUN pip3 install paddlepaddle-gpu --use-feature=fast-deps --break-system-packages

# Install unstructured[all-docs].
RUN pip3 install unstructured[all-docs] --use-feature=fast-deps --break-system-packages

# Install pymilvus[model].
RUN pip3 install pymilvus[model] --use-feature=fast-deps --break-system-packages

# Install onnxruntime-gpu.
RUN pip3 install onnxruntime-gpu --extra-index-url=https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/ --break-system-packages

# Install ray.
RUN pip3 install ray[default] --use-feature=fast-deps --break-system-packages

# Copy requirements.txt to the working directory.
COPY ./requirements.txt ./requirements.txt

# Install python dependencies from requirements.txt.
RUN pip3 install -r requirements.txt --use-feature=fast-deps --break-system-packages

# Copy rest of the files to the working directory.
COPY . .



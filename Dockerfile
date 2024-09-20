# Initialize the base image.
FROM muazhari/cuda-torch-tensorflow:latest

# Set the working directory environment.
ENV WORKDIR=/workdir

# Set the working directory.
WORKDIR $WORKDIR

# Copy files to the working directory.
COPY . .

# Install apt dependencies.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-fast update -y \
    && \
    yes | apt-fast install -y \
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

# Install pip dependencies.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system \
    unstructured[all-docs]  \
    pymilvus[model] \
    ray[default]  \
    --break-system-packages \
    && \
    uv pip install --system \
    onnxruntime-gpu \
    --extra-index-url=https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/ \
    --break-system-packages \
    && \
    uv pip install --system \
    -r requirements.txt \
    --break-system-packages


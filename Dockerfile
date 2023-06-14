# Initialize the base image.
FROM nvidia/cuda:11.8.0-base-ubuntu22.04

# Set the working directory.
WORKDIR /app
COPY . .

# Update apt repositories.
RUN apt update -y

# Install apt dependencies.
RUN yes | DEBIAN_FRONTEND=noninteractive apt install -y \
    wkhtmltopdf \
    xvfb \
    libopenblas-dev \
    libomp-dev \
    poppler-utils  \
    openjdk-8-jdk \
    libpq-dev  \
    gdb \
    wget \
    git \
    python3 \
    python3-pip

# Install pytorch.
RUN pip3 install \
    torch \
    torchvision \
    torchaudio \
    --index-url https://download.pytorch.org/whl/cu118

# Install python dependencies.
RUN pip3 install \
    -r requirements.txt \
    git+https://github.com/deepset-ai/haystack.git@main#egg=farm-haystack[all] \
    txtai[all] \
    pydantic[dotenv] \
    aiopg[sa] \
    sqlalchemy[asyncio] \
    pydevd-pycharm

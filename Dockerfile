# Menginstall base image
FROM python:3.9-alpine

# Mengganti workdir
WORKDIR /app

# Melakukan copy file di folder ini menuju folder /app di container
COPY . /app

# Install dependencies yang diperlukan untuk kubectl dan gcloud CLI
RUN apk add --no-cache curl gnupg bash git google-cloud-sdk-gke-gcloud-auth-plugin

RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm kubectl

# Install gcloud SDK
RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-372.0.0-linux-x86_64.tar.gz && \
    tar -xzf google-cloud-sdk-372.0.0-linux-x86_64.tar.gz && \
    ./google-cloud-sdk/install.sh --quiet && \
    rm google-cloud-sdk-372.0.0-linux-x86_64.tar.gz

# Set environment variables for gcloud
ENV PATH="/app/google-cloud-sdk/bin:$PATH"

# Melakukan upgrade pip untuk memastikan semua requirements dapat terinstall
RUN python -m pip install --upgrade pip

# Menginstall semua requirement yang dibutuhkan
RUN pip install -r requirements.txt


# Membuka port 8000 agar dapat diakses dari luar container
EXPOSE 8000

# Menjalankan setup_gke.sh dan kemudian main.py
CMD [ "python", "main.py" ]
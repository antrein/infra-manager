# Menginstall base image
FROM python:3.9-alpine

# Mengganti workdir
WORKDIR /app

# Melakukan copy file di folder ini menuju folder /app di container
COPY . /app

# Menginstall dependencies yang diperlukan untuk kubectl dan cron
RUN apk add --no-cache curl gnupg bash git busybox jq

RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev

# Menginstall kubectl
RUN curl -sLO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm kubectl

# Install gcloud SDK
RUN curl -sSL https://sdk.cloud.google.com | bash > /dev/null

# Add gcloud to PATH
ENV PATH $PATH:/root/google-cloud-sdk/bin

# Install kubectl and gke-gcloud-auth-plugin
RUN gcloud components install kubectl gke-gcloud-auth-plugin --quiet

# Melakukan upgrade pip untuk memastikan semua requirements dapat terinstall
RUN python -m pip install --upgrade pip

# Menginstall semua requirement yang dibutuhkan
RUN pip install -r requirements.txt

# Set the KUBECONFIG environment variable
ENV KUBECONFIG=/root/.kube/config

# Setup the cron job
RUN echo "0 * * * * /bin/bash /app/script/service/gcp-refresh-token.sh >> /var/log/cron.log 2>&1" > /etc/crontabs/root

# Run the gcp-refresh-token.sh script during the build process
RUN /bin/bash /app/script/service/gcp-refresh-token.sh

# Ensure crond is running
CMD ["sh", "-c", "crond && python main.py"]

# Membuka port 8000 agar dapat diakses dari luar container
EXPOSE 8000

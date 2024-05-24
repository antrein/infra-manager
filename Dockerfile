# Menginstall base image
FROM python:3.9-alpine

# Mengganti workdir
WORKDIR /app

# Melakukan copy file di folder ini menuju folder /app di container
COPY . /app

# Menginstall dependencies yang diperlukan untuk kubectl
RUN apk add --no-cache curl gnupg bash git

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

# Copy the kubeconfig file into the container (assuming it's provided at build time)
# COPY ./k8s/authorization/kubeconfig.yml /root/.kube/config

# Set the KUBECONFIG environment variable
ENV KUBECONFIG=/root/.kube/config

# Test KUBECTL connection
# RUN kubectl config current-context
# RUN kubectl get ns

# Membuka port 8000 agar dapat diakses dari luar container
EXPOSE 8000

# Menjalankan main.py
CMD ["python", "main.py"]
FROM quay.io/astronomer/astro-runtime:6.0.0
COPY --from=lachlanevenson/k8s-kubectl:v1.10.3 /usr/local/bin/kubectl /usr/local/bin/kubectl

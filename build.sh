set -e

cat GCP_SERVICE_JSON.json | docker login -u _json_key --password-stdin https://us-east4-docker.pkg.dev

docker buildx build \
  --push \
  --platform linux/amd64 \
  -t us-east4-docker.pkg.dev/tennis-rally-app/tennis/tennis-rally-streamlit-csv \
  -f Dockerfile .
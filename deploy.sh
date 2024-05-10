# Deploy image
gcloud run deploy tennis-rally-streamlit-csv \
  --image=us-east4-docker.pkg.dev/tennis-rally-app/tennis/tennis-rally-streamlit-csv:latest \
  --allow-unauthenticated \
  --min-instances=1 \
  --max-instances=1 \
  --region=us-east4 \
  --cpu-boost \
  --memory=512Mi \
  --project=tennis-rally-app
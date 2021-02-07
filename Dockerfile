FROM public.ecr.aws/lambda/python:latest
RUN pip install --no-cache-dir pandas numpy gspread oauth2client boto3 statsmodels
COPY src/ .
COPY .env/ ../.env/
CMD [ "service.handler" ]
# statsTool
## Functions
1. Prediction (autoregression model by buildings)
2. Autocorrelations (autocorrelation by building)
3. Stats(Cases by building sorted by number of cases)

## Architecture

## Usage

## Setup
1. cd src/lambda
2. docker build -t [tag name] .
3. ecr get-login-password --region [aws region] | docker login --username AWS --password-stdin [erc account number].dkr.ecr.us-east-1.amazonaws.com
4. docker push [erc account number].dkr.ecr.us-east-1.amazonaws.com/[tag name]

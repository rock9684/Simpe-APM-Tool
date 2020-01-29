# Application Performance Management (APM) Tool

This project is based on University of Toronto's ECE1779 class.

## Introduction
An APM tool is a kind of tools to track applications' performance, which is widely used across all industries. Our tool could monitor a PC's performance in terms of CPU, disk and memory utilization in a resolution of one minute. Future work could include build a ML model to predict the performance of a specific machine at a specific time. If it is over the threshold, the tool could send an email alert to the user. A report of this projcet is also provided and it covers more details.

## To Run
### Server Side
This tool is supposed to run on AWS. It uses DynamoDB and RDS. We deployed it on a AWS Lambda function using Zappa to make the webapp serverless. However, you could also deploy it to a EC2 instance.
### Agent
The agent.py script is used collect all metrics from your PC or laptop.

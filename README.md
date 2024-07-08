
# AWS CDK Sample Project

## List

- Aurora instance with tag
- SQS QueuePolicy from json
- EventBridge Schedule Invoke Lambda
- EventBridge Rule Invoke Lambda Use Schedule
- StepFunctions From ASL
- AutoScaling with StepScalingPolicy for SQS own metric
- AutoScaling with Elastic Graphics
- IAM Role with customer managed policies
- Security Group
- DynamoDB from S3
- EC2 from LaunchTemplate
- SSM Change Calndar

## Deploy

```bash
# single stacks
cdk deploy MyStack
# multiple stacks
cdk deploy Stack1 Stack2
# all stacks
cdk deploy "*"    
```

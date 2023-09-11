# air-tek

This repo consists of files and images related to the assessment

Iac used: Pulumi
Infrastructures deployed using pulumi
1. Elastic Beanstalk
2. Elastic Container Registry

Important files used:
1. main.yaml: Github actions file that helped move application code in a zipped format to Elastic Beanstalk
2. push_to_ecr.sh : shell script that helped push docker images to ECR
3. elasticbanestalk/__main__.py: contains pulumi code or beanstalk deployment
4. ecr/__main__.py: contains pulumi code or ECR deployment. 
5. Snapshot of final output on browser, security groups, Load balancer listeners and architectural diagram is located in images/ folder
terragrunt_source = "git::https://git.rockfin.com/terraform/aws-ecs-app-tf.git?ref=4.8.9" # Substitute X with the latest release

# ---------------------------------------------------------------------------------------------------------------------
# Required variables for AWS
# ---------------------------------------------------------------------------------------------------------------------

development_team_email        = "RocketTechServicingSRE@QuickenLoans.com"
infrastructure_team_email     = "RocketTechServicingSRE@QuickenLoans.com"
infrastructure_engineer_email = "RocketTechServicingSRE@QuickenLoans.com"

# ---------------------------------------------------------------------------------------------------------------------
# Standard Module Required Variables
# ---------------------------------------------------------------------------------------------------------------------

app_id           = "208604"
application_name = "terratattle" #Alphanumeric characters, lowercase ONLY, 16 characters MAX. DO NOT EXCEED

# ---------------------------------------------------------------------------------------------------------------------
# Infrastructure Tags
# ---------------------------------------------------------------------------------------------------------------------

app_tags = {
  hal-app-id = "8423"
}

# ---------------------------------------------------------------------------------------------------------------------
# Infrastructure Variables
# ---------------------------------------------------------------------------------------------------------------------

vpc_id                  = "vpc-081b68dc3b6833671" 
subnet_ids              = ["subnet-0ab0cb0ab571277f2","subnet-03127f6de0f3cc8ea","subnet-054d83a5aff26de0d"] # private
desired_number_of_tasks = 3 # Recommended values: 1 for dev/test, 3(or however many subnets you have) for beta/prod
min_number_of_tasks     = 3 # Recommended values: 1 for dev/test, 3(or however many subnets you have) for beta/prod
max_number_of_tasks     = 9 # Recommended values: 1 for dev/test, 9(or however many subnets you have) for beta/prod
use_fargate             = true

# ---------------------------------------------------------------------------------------------------------------------
# Load Balancer Variables
# ---------------------------------------------------------------------------------------------------------------------

load_balancer_type       = "public" # Should be set to "private" for most internally hosted API's, then fronted with an API GW; public for user-facing websites
load_balancer_subnet_ids = ["subnet-0e0d7ab7d3774803d","subnet-00becf0415e0b1ce3","subnet-040f2b48d95709d3d"] # public
use_tls                  = true
acm_certificate          = "arn:aws:acm:us-east-2:340355219019:certificate/d6f18999-6691-47f8-8e93-325d4d34f66e"
idle_timeout             = 360

# ---------------------------------------------------------------------------------------------------------------------
# Health Check Variables
# ---------------------------------------------------------------------------------------------------------------------

health_check_path = "/" # Health check path for your application

# ---------------------------------------------------------------------------------------------------------------------
# AutoScaling Variables
# ---------------------------------------------------------------------------------------------------------------------

use_auto_scaling = true # Recommended values: false for dev/test, true for beta/prod
use_blue_green   = false # Recommended values: false for dev/test/beta, true for prod
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

vpc_id                  = "vpc-0bb2ac24578b1e696" 
subnet_ids              = ["subnet-051a46bf1066f3990","subnet-06380a4382d223fe3","subnet-09dd864547923b320"] # private
desired_number_of_tasks = 3 # Recommended values: 1 for dev/test, 3(or however many subnets you have) for beta/prod
min_number_of_tasks     = 3 # Recommended values: 1 for dev/test, 3(or however many subnets you have) for beta/prod
max_number_of_tasks     = 9 # Recommended values: 1 for dev/test, 9(or however many subnets you have) for beta/prod
use_fargate             = true

# ---------------------------------------------------------------------------------------------------------------------
# Load Balancer Variables
# ---------------------------------------------------------------------------------------------------------------------

load_balancer_type       = "public" # Should be set to "private" for most internally hosted API's, then fronted with an API GW; public for user-facing websites
load_balancer_subnet_ids = ["subnet-0aed2416e189a671e","subnet-0c8ec220ead1a9fd6","subnet-00fa442a7a96747b0"] # public
use_tls                  = true
acm_certificate          = "arn:aws:acm:us-east-2:153607920631:certificate/fa4d2611-3acc-40fd-91a8-8aa94e5381f6"
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
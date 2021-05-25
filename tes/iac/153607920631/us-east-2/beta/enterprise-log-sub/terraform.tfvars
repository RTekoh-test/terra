terragrunt_source = "git::https://git.rockfin.com/terraform/aws-enterprise-log-exporter-system.git//modules/subscription?ref=2.2.1" # Substitute X with the latest release

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

cloudwatch_log_group_name = "beta-208604-terratattle" # the name of the log group that will be subscribed to the log exporter
exporter_app_id = "202306" # the Core App ID of the log exporter

#splunk_hec_token = "" # set in environment variable TF_VAR_splunk_hec_token 
splunk_index  = "cloud_apps_nonprod" # Either (cloud_apps_nonprod|cloud_apps_prod) based on environment, it the splunk index to which the logs will be sent
splunk_source = "ECS" # an optional string that should help identify these logs belong to your app.


terragrunt_source = "git::https://git.rockfin.com/terraform/aws-route53-tf.git//modules/aws-route53-record-tf?ref=1.4.0" # Replace X.X.X with your desire release

#-----------------------------------------------------
#---------------Infrastructure Variables--------------
#-----------------------------------------------------

zone_id     = "Z00271812FOP0YG6DZI53"
record_name = "terratattle.rms.beta.servicing.foc.zone"
record_type = "CNAME"
records     = ["ecs-beta-208604-terratattle-1740059403.us-east-2.elb.amazonaws.com"] #- (Required for non-alias records) A string list of records. 
# To specify a single record value longer than 255 characters such as a TXT record for DKIM, 
# add \"\" inside the Terraform configuration string (e.g. "first255characters\"\"morecharacters").
ttl = 300

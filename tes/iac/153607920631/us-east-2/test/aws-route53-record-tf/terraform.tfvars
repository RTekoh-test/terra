terragrunt_source = "git::https://git.rockfin.com/terraform/aws-route53-tf.git//modules/aws-route53-record-tf?ref=1.4.0" # Replace X.X.X with your desire release

#-----------------------------------------------------
#---------------Infrastructure Variables--------------
#-----------------------------------------------------

zone_id     = "Z0004740SDVO2JU3GEWG"
record_name = "terratattle.rms.test.servicing.foc.zone"
record_type = "CNAME"
records     = ["ecs-test-208604-terratattle-213416097.us-east-2.elb.amazonaws.com"] #- (Required for non-alias records) A string list of records. 
# To specify a single record value longer than 255 characters such as a TXT record for DKIM, 
# add \"\" inside the Terraform configuration string (e.g. "first255characters\"\"morecharacters").
ttl = 300
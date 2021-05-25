#!/usr/bin/env python3

# Import modules
from github import Github # https://pygithub.readthedocs.io/en/latest/introduction.html
import os
from os import path
import re
import colored
import argparse
import json
import sys
import semver
import pickle
from datetime import datetime, timedelta

### Color VARs
red    = '\u001b[31m'
green  = '\u001b[32m'
yellow = '\u001b[33m'
blue   = '\u001b[36m'
res    = colored.attr('reset')

### Argument parse ###
parser = argparse.ArgumentParser()
parser.add_argument("--circleci", action = "store_true", help = "Runs CircleCI version of this application")
parser.add_argument("--repo", action = "store_true", help = "Runs Terratattle at the repo level")
parser.add_argument("--search", action = "store_true", help = "Searches Git Enterprise for all instances of a module")
parser.add_argument("--audit", action = "store_true", help = "Searches Git Enterprise for all instances of a module not running minimum version")
parser.add_argument("--output", choices = ["json", "console"], default = "console", help = "Output for results. Default: console")
args = parser.parse_args()
output_console = args.output == "console"

# Github Enterprise with custom hostname
g = Github(base_url = "https://git.rockfin.com/api/v3", login_or_token = os.environ.get('TOKEN'))

# Check if cache files exist, if older than 1 day, delete them
def cache_check(cache, is_dict=False):
  try:
    cache_file= "cache/"+cache+".tt"
    path.exists(cache_file)
    cache = pickle.load( open(cache_file, "rb" ) )
    day_ago = datetime.now() - timedelta(days=1)
    filetime = datetime.fromtimestamp(path.getctime(cache_file))
#    print("cached!")
    if filetime < day_ago:
      os.remove(cache_file) 
      print("Cache file is more than 1 day old: DELETED!")
      if is_dict == 1:
        return {}
      else:
        return []
    else:
      return cache
  except:
    if is_dict == 1:
      return {}
    else:
      return []

# set cacheable lists + dict
gitorgs = cache_check(cache="gitorgs")
current = cache_check(cache="current", is_dict=True)
archive = cache_check(cache="archive")

# Counters
updated_count         = 0
outdated_count        = 0
warn_count            = 0
major_outdated_count  = 0
pass_count            = 0 
fail_count            = 0

# For JSON output
items = []

if not gitorgs:
  # Create list of all Git organizations
  for gitorg in g.get_organizations():
    try:
      gitorgs.append(gitorg.login.lower())
    except:
      continue
  cache_file= "cache/gitorgs.tt"
  pickle.dump( gitorgs, open( cache_file, "wb" ) )
  gitorgs= pickle.load( open( cache_file, "rb" ) )
#  print("not cached!")

# Find all terraform modules per Git org
def modules_per_org():
  tf_count = 0 
  tf_org = 0
  print("\nTotal Terraform modules per Git organization:\n")
  for git_org in gitorgs:
    try:
      git_query = "org:" + git_org + " filename:terraform.tfvars"
      git_search=(g.search_code(query = git_query))
      if git_search.totalCount > 0:
        print(blue + git_org + res + " " + str(git_search.totalCount))
        tf_org = tf_org + 1
        tf_count = tf_count + git_search.totalCount
    except:
      continue
  print("\nTotal orgs with Terraform modules: " + yellow + str(tf_org) + res + "\n")
  print("\nTotal Terraform modules in all orgs: " + yellow + str(tf_count) + res + "\n")

# modules_per_org()
# sys.exit()

if not current:
  # Create dictionary of Terraform org modules, with terraform module name as keys, latest release as values
  for repo in g.get_organization("terraform").get_repos("all"):
    try:
        latest_release = repo.get_latest_release()
        current[repo.name] = str(latest_release.tag_name)
    except:
      continue
  cache_file= "cache/current.tt"
  pickle.dump( current, open( cache_file, "wb" ) )
  current= pickle.load( open( cache_file, "rb" ) )
#  print("not cached!")

if not archive:
  # Create list of all modules in terraform-archive org
  for repo in g.get_organization("terraform-archive").get_repos("all"):
    try:
      archive.append(repo.name)
    except:
      continue
  cache_file= "cache/archive.tt"
  pickle.dump( archive, open( cache_file, "wb" ) )
  archive= pickle.load( open( cache_file, "rb" ) )
#  print("not cached!")

# Change org based on arg flags
if args.circleci:
  org = os.environ.get('CIRCLE_PROJECT_USERNAME')
elif args.repo:
  org = os.environ.get('ORG')
elif args.search or args.audit:
  org = ''
else:
  try:
    org = os.environ.get('ORG')
    # Check if org input is a valid org
    if org not in gitorgs:
      print("\n" + yellow + org + red +  " is not a valid Git Organization!\n" + res) 
      sys.exit(1)
  except Exception:
    print(Exception)

# Search org for all files named "terraform.tfvars"
## Switch logic for arg flags
if args.circleci:
    git_query = "repo:" + org + "/" + os.environ.get('CIRCLE_PROJECT_REPONAME') + " filename:terraform.tfvars"
    if output_console:
      print("\nTerraform files in the " + blue + org + "/" + os.environ.get('CIRCLE_PROJECT_REPONAME') + res + " repo:")
elif args.repo:
    git_query = "repo:" + org + "/" + os.environ.get('REPONAME') + " filename:terraform.tfvars"
    if output_console:
      print("\nTerraform files in the " + blue + org + "/" + os.environ.get('REPONAME') + res + " repo:")      
elif args.search or args.audit:
    git_query = os.environ.get('MODULE') + " filename:terraform.tfvars"
    if output_console:
      print("\nFinding all instances of module: " + blue + os.environ.get('MODULE') + res + " in Git Enterprise:")    
else:
    git_query = "org:" + org + " filename:terraform.tfvars"
    if output_console:
      print("\nTerraform files in the " + blue + org + res + " organization:")

# Check for API limit (1000) in search 
# https://docs.github.com/en/rest/reference/search
git_search=(g.search_code(query = git_query))
if git_search.totalCount == 1000:
  print( red + "\nResults are truncated!\n" + res)

# Main loop
for repo in git_search:
  try:
    live_warn = 0  
    sections = list(reversed(repo.html_url.split("/"))) # flip the url parts to get more details
    item = {
      'name': repo.repository.full_name,
      'url': repo.html_url,
      'env': sections[2],
      'region': sections[3],
      'account': sections[4]
    }

    if output_console:
      print(blue + "\nREPO NAME: " + res + repo.repository.full_name)
      # Get the ENV out of the url here - test, beta, prod
      print(blue + "REPO URL: " + res + repo.html_url)
    # VAR for RAW "terraform.tfvars" content
    tfvars = repo.decoded_content
    # VAR for regex that cuts URL from RAW content
    regex = re.search("(?P<url>https?://[^\s]+)", str(tfvars))
    # Catch inline modules (../../../../modules)
    if regex == None:
      warn_count = warn_count + 1
      live_warn = 1
      if output_console:
        print(blue + "LIVE VERSION: " + yellow + "This looks to be a custom/in-line module!")
    # Cleaning URL using " as a delimiter
    clean = regex.group(1).split('"')
    tf_source = clean[0]

    item["source"] = tf_source

    if output_console:
      print(blue + "TERRAGRUNT SOURCE: " + res + tf_source)
    module = tf_source.split("/")[4]
    # Fixes issues if module doesn't have .git in Terragrunt URL
    if "git" not in module:
      dirty_module = module.split("?")[0]
      if output_console:
        print(blue + "TERRAFORM MODULE: " + res + dirty_module)
    else:
      dirty_module = module.split(".")[0]
      if output_console:
        print(blue + "TERRAFORM MODULE: " + res + dirty_module)

    item["module"] = dirty_module

    # Catch having no 'ref'
    if "ref" not in tf_source:
      warn_count = warn_count + 1
      live_warn = 1
      if output_console:
        print(blue + "LIVE VERSION: " + yellow + "Please use a version/release!")
    # Bug fix where aws-acm-certificate gets redirected to aws-acm-certificate-tf
    if dirty_module == "aws-acm-certificate":
      dirty_module = "aws-acm-certificate-tf"
    # Split version from =
    v_version = tf_source.split("=")[1]
    # Remove 'v' in version
    live_version = v_version.replace('v', '')
  except:
    continue

# live_version catch loop
  # Catch modules using master
  if live_version == "master":
    warn_count = warn_count + 1
    live_warn = 1
    if output_console:
      print(blue + "LIVE VERSION: " + yellow + "Please use a version/release!")
  # Catch modules using placeholder
  elif live_version == "x.x.x" or live_version == "X.X.X":
    warn_count = warn_count + 1
    live_warn = 1
    if output_console:
      print(blue + "LIVE VERSION: " + yellow + "Change the placeholder version!")
  # Catch 'ref' not being in terragrunt_source
  elif live_version == None:
    warn_count = warn_count + 1
    live_warn = 1
    if output_console:
      print(blue + "LIVE VERSION: " + yellow + "Please use a version/release!")
  else:
    if output_console:
      print(blue + "LIVE VERSION: " + res + live_version)

  item['version'] = live_version

  # Remove ?ref from module name
  if "?" in dirty_module:
    tf_module = dirty_module.split("?")[0]
  else:
    tf_module = dirty_module

# latest_version catch loop
  # Catch modules in terraform-emerging
  if "terraform-emerging" in tf_source:
    if live_warn == 0:
      warn_count = warn_count + 1
    item["latest"] = "DEPRECATED"
    if output_console:
      print(blue + "LATEST VERSION: " + yellow + "This is a deprecated module from terraform-emerging!")
  # Catch modules in tf-modules
  elif "tf-modules" in tf_source:
    if live_warn == 0:
      warn_count = warn_count + 1
    item["latest"] = "DEPRECATED"
    if output_console:
      print(blue + "LATEST VERSION: " + yellow + "This is a deprecated module from tf-modules!")
  # Catch modules moved to terraform-archive
  elif tf_module in archive:
    if live_warn == 0:
      warn_count = warn_count + 1
    item["latest"] = "DEPRECATED"
    if output_console:
      print(blue + "LATEST VERSION: " + yellow + "This is an archived module from terraform-archive!")
  # Final catch for all modules not in terraform org
  elif "terraform" not in tf_source:
    if live_warn == 0:
      warn_count = warn_count + 1
    item["latest"] = "UNOFFICIAL"
    if output_console:
      print(blue + "LATEST VERSION: " + yellow + "Not an official Terraform module!")

  else:
  # Search 'current' dictionary for matching key (module name), if found display value (latest release)
    for key, latest_vers in current.items():
      try:
        if tf_module == key:
          item["latest"] = latest_vers
          latest_parse = semver.parse(latest_vers)
          current_vers = clean[0].split("=")[1]
          current_parse = semver.parse(current_vers)
          semver_compare = semver.compare(current_vers, latest_vers)
          if output_console:
            print(blue + "LATEST VERSION: " + res + latest_vers)
          # compare live and latest versions
          if semver_compare == 0:
            updated_count = updated_count + 1
            item["outdated"] = False
            if output_console:
              print(green + "Module up to date!" + res)
          elif current_parse["major"] != latest_parse["major"]:
            major_outdated_count = major_outdated_count + 1
#            outdated_count = outdated_count + 1
            item["outdated"] = True
            if output_console:
              print(red + "Module MAJORLY out of date!!" + res)
          else:
            outdated_count = outdated_count + 1
            item["outdated"] = True
            if output_console:
              print(red + "Module out of date!" + res)
          if args.audit:
            if semver.match(current_vers, ">=" + os.environ.get('MODULE_VERS')):
              pass_count = pass_count + 1
              print(green + "Audit Pass!" + res)
            else:
              fail_count = fail_count + 1
              print(red + "Audit Fail!" + res)
      except:
        continue

  items.append(item)

if output_console and not args.audit:
  # Report section
  # Switch logic for arg flags
  if args.circleci:
      print(res + "\n===== Terratattle Report for " + blue + org + "/" + os.environ.get('CIRCLE_PROJECT_REPONAME') + res + " =====\n")
  elif args.repo:
      print(res + "\n===== Terratattle Report for " + blue + org + "/" + os.environ.get('REPONAME') + res + " =====\n")
  elif args.search or args.audit:
      print(res + "\n===== Terratattle Report for module: " + blue + os.environ.get('MODULE') + res + " =====\n")
  else:
      print(res + "\n===== Terratattle Report for " + blue + org + res + " =====\n")

  print("There were: " + green + str(updated_count) + res + " up-to-date Terraform modules!")
  print("There were: " + red + str(outdated_count) + res + " outdated Terraform modules!")
  print("There were: " + red + str(major_outdated_count) + res + " MAJORLY outdated Terraform modules!")
  print("There were: " + yellow + str(warn_count) + res + " Terraform module warnings!")
  print("There were: " + blue + str(git_search.totalCount) + res + " total Terraform modules!\n")

else:
  if not args.audit:
    # JSON output
    payload = {
      'org': org,
      'modules': items,
      'updated': updated_count,
      'outdated': outdated_count,
      'major_outdated': major_outdated_count,
      'warnings': warn_count,
      'total': git_search.totalCount
    }

    print(json.dumps(payload))

if args.audit: 
  percentage = round(pass_count / fail_count * 100)
  print(res + "\n===== Audit Results for module: " + blue + os.environ.get('MODULE') + res +  " version: " + blue + os.environ.get('MODULE_VERS') + res +  " =====\n")
  print("There were: " + green + str(pass_count) + res + " modules that PASSED the audit!")
  print("There were: " + red + str(fail_count) + res + " modules that FAILED the audit!")
  print("Compliance: " + yellow + str(percentage) + res + "%\n")
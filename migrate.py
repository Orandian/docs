import os
import shutil
import re
import json

DEV_SOLUTIONS_DIR = "/Users/yannainghtwe/Documents/creation/dev-solutions/docs"
DOCS_DIR = "/Users/yannainghtwe/Documents/creation/docs"
TARGET_DIR = os.path.join(DOCS_DIR, "dev-solutions")

os.makedirs(TARGET_DIR, exist_ok=True)

# Define the navigation structure from mkdocs.yaml
nav_structure = {
  "Home": {"src": "index.md", "title": "Dev Solutions Overview"},
  "Nest": [
      {"src": "nest/server_setup.md", "title": "Server Setup"}
  ],
  "Git": [
      {"src": "git/merge-conflict.md", "title": "Merge Conflict"},
      {"src": "git/detached-head.md", "title": "Detached Head"},
      {"src": "git/branching-merging.md", "title": "Branching & Merging"},
      {"src": "git/industry_git_commands.md", "title": "Industry Git Commands"}
  ],
  "Hosting": [
      {"src": "hosting/vercel-deploy.md", "title": "Vercel Deploy"}
  ],
  "Caddy": [
      {"src": "caddy/ssl-renewal.md", "title": "SSL Renewal"}
  ],
  "CI/CD": [
      {"src": "CI_CD/spring_boot_ci_cd_setup_guide.md", "title": "Spring Boot CI/CD Setup Guide"}
  ],
  "Docker": [
      {"src": "docker/docker_process_guide.md", "title": "Spring boot process"},
      {"src": "docker/essential_docker_commands.md", "title": "Essential Docker Commands"}
  ],
  "AWS": [
      {"src": "aws/aws-sqs-guide.md", "title": "SQS Guide"},
      {"src": "aws/aws-sns-guide.md", "title": "SNS Guide"},
      {"src": "aws/aws-kinesis-data-streams.md", "title": "Kinesis Data Streams"},
      {"src": "aws/sqs-vs-sns-vs-kinesis.md", "title": "SQS vs SNS vs Kinesis"},
      {"src": "aws/aws-apache-flink.md", "title": "Amazon Managed Service for Apache Flink"},
      {"src": "aws/aws-data-firehose.md", "title": "Amazon Data Firehose"},
      {"src": "aws/aws-ai-practitioner.md", "title": "AWS AI Practitioner"}
  ],
  "Kubernetes": [
      {"src": "kubernetes/kubernetes_comprehensive_guide.md", "title": "Kubernetes Comprehensive Guide"}
  ],
  "Expo": [
      {"src": "expo/expo_solutions_guide.md", "title": "Expo Solutions Guide"}
  ],
  "React": [
      {"src": "react/state_management.md", "title": "State Management"}
  ]
}

def to_kebab_case(s):
    # Replace underscores with hyphens
    s = s.replace('_', '-')
    # To lowercase
    return s.lower()

mintlify_groups = []

for section, items in nav_structure.items():
    if section == "Home":
        src = items["src"]
        title = items["title"]
        # Handle index
        target_path = "dev-solutions/index.mdx"
        full_src = os.path.join(DEV_SOLUTIONS_DIR, src)
        full_target = os.path.join(DOCS_DIR, target_path)
        
        # Write frontmatter
        if os.path.exists(full_src):
            with open(full_src, "r") as f:
                content = f.read()
            with open(full_target, "w") as f:
                f.write(f"---\ntitle: \"{title}\"\ndescription: \"{title}\"\n---\n\n" + content)
        
        mintlify_groups.append({
            "group": "Overview",
            "pages": ["dev-solutions/index"]
        })
        continue

    group_pages = []
    
    for item in items:
        src = item["src"]
        title = item["title"]
        
        # Make kebab case target
        src_dir = os.path.dirname(src)
        src_name = os.path.basename(src)
        # Convert folder to kebab case
        kebab_dir = to_kebab_case(src_dir)
        kebab_name = to_kebab_case(src_name).replace(".md", ".mdx")
        
        if kebab_dir:
            target_rel_dir = os.path.join("dev-solutions", kebab_dir)
            os.makedirs(os.path.join(DOCS_DIR, target_rel_dir), exist_ok=True)
            target_path = os.path.join(target_rel_dir, kebab_name)
        else:
            target_path = os.path.join("dev-solutions", kebab_name)
            
        full_src = os.path.join(DEV_SOLUTIONS_DIR, src)
        full_target = os.path.join(DOCS_DIR, target_path)
        
        if os.path.exists(full_src):
            with open(full_src, "r") as f:
                content = f.read()
            with open(full_target, "w") as f:
                f.write(f"---\ntitle: \"{title}\"\ndescription: \"{title}\"\n---\n\n" + content)
        
        # Add to pages array, without extension
        page_ref = target_path.replace(".mdx", "")
        group_pages.append(page_ref)
        
    if group_pages:
        mintlify_groups.append({
            "group": section,
            "pages": group_pages
        })

# Read docs.json
docs_json_path = os.path.join(DOCS_DIR, "docs.json")
with open(docs_json_path, "r") as f:
    docs_config = json.load(f)

# check if dev-solutions tab exists
has_dev_solutions = False
for tab in docs_config.get("navigation", {}).get("tabs", []):
    if tab.get("tab") == "Dev Solutions":
        has_dev_solutions = True
        tab["groups"] = mintlify_groups
        break

if not has_dev_solutions:
    docs_config["navigation"]["tabs"].append({
        "tab": "Dev Solutions",
        "groups": mintlify_groups
    })

with open(docs_json_path, "w") as f:
    json.dump(docs_config, f, indent=2)

print("Migration completed successfully.")

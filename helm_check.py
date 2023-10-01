import subprocess
import json

# Run the Helm list command across all namespaces and capture the output as a JSON string
helm_list_command = "helm list -A -o json"
try:
    helm_list_output = subprocess.check_output(helm_list_command, shell=True, text=True)
except subprocess.CalledProcessError as e:
    print(f"Error executing Helm command: {e}")
    exit(1)

# Parse the JSON output
try:
    helm_releases = json.loads(helm_list_output)
except json.JSONDecodeError as e:
    print(f"Error parsing Helm output as JSON: {e}")
    exit(1)

# # Function to install repos locally
# def get_helm_repo(release):
#     repo_name = release['chart'].split('-', 1)[0]
#     repo_urls = [
#         "https://charts.jetstack.io",
#         "https://charts.k8sgpt.ai/"
#     ]
#     for repos in repo_urls:
#         repo_install_command = f"helm repo add {repo_name} {repos}"
#         print("Added: {repos}")
#         try:
#             chart_app_version_output = subprocess.check_output(repo_install_command, shell=True, text=True)
#             return chart_app_version_output.strip()
#         except subprocess.CalledProcessError as e:
#             return "N/A"

# Function to get the latest chart version for a release
def get_latest_chart_version(release):
    repo_name = release['chart'].split('-', 1)[0]
    chart_version_command = f"helm search repo {repo_name} | awk 'NR==2{{print $2}}'"
    try:
        chart_version_output = subprocess.check_output(chart_version_command, shell=True, text=True)
        return chart_version_output.strip()
    except subprocess.CalledProcessError as e:
        return "N/A"

# Function to get the latest chart APP version for a release
def get_latest_chart_app_version(release):
    repo_name = release['chart'].split('-', 1)[0]
    chart_app_version_command = f"helm search repo {repo_name} | awk 'NR==2{{print $3}}'"
    try:
        chart_app_version_output = subprocess.check_output(chart_app_version_command, shell=True, text=True)
        return chart_app_version_output.strip()
    except subprocess.CalledProcessError as e:
        return "N/A"

# Function to compare current version with latest version, if chart name follows x-x-0.0.0 naming convention
def compare_chart_version(release):
    current_chart = release['chart']
    # print(current_chart)
    current_version = current_chart.split('-')[2]
    # print(current_version)
    latest_chart_version = get_latest_chart_version(release)
    # print(latest_chart_version)
    if current_version != latest_chart_version:
        return f"Upgrade needed for release {release['name']} ({current_chart})"
    else:
        return f"Release {release['name']} ({current_chart}) is up to date"

# Print the Helm releases with the latest chart version
for release in helm_releases:
    # get_helm_repo_list = get_helm_repo(release)
    latest_chart_version = get_latest_chart_version(release)
    latest_app_version = get_latest_chart_app_version(release)
    compare_versions = compare_chart_version(release)

    print(f"Release Name: {release['name']}")
    print(f"Namespace: {release['namespace']}")
    print(f"Status: {release['status']}")
    print(f"Chart: {release['chart']}")
    print(f"Latest Chart Version: {latest_chart_version}")
    print(f"Latest App Version: {latest_app_version}")
    print(f"Upgrade Needed: {compare_versions}")
    print("\n")

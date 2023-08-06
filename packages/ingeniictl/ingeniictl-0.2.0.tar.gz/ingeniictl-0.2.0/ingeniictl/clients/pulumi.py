import copy
from inspect import stack
import json
import os
import subprocess
from typing import Any

from ingeniictl.clients.logger import log_client


def _run(
    args: list,
    cwd: str = None,
) -> Any:
    if cwd:
        args.append("--cwd")
        args.append(cwd)
    return subprocess.run(["pulumi"] + args, capture_output=True).stdout


def _get_stack(name: str, cwd: str = None) -> Any:
    cmd = ["stack", "export", "--stack", name]
    return _run(cmd, cwd)

def _export_stack(name: str, output_file: str, cwd: str = None) -> Any:
    cmd = ["stack", "export", "--stack", name, "--file", output_file]
    return _run(cmd, cwd)

def _import_stack(name: str, input_file: str, cwd: str = None) -> Any:
    cmd = ["stack", "import", "--stack", name, "--file", input_file]
    return _run(cmd, cwd)

def _destroy_stack(name: str, cwd: str = None) -> Any:
    cmd = ["destroy", "--stack", name,"--yes", "--skip-preview"]
    _run(cmd, cwd)

def _delete_stack(name: str, cwd: str = None) -> Any:
    cmd = ["stack", "rm", "--stack", name, "--yes", "--force"]
    _run(cmd, cwd)

def remove_protect_flags(stack_name: str, cwd: str = None) -> Any:
    log_client.info("Removing Pulumi resource protection flags...")

    cmd = ["state", "unprotect", "--all", "--yes", "--stack", stack_name]

    return _run(cmd, cwd)


def remove_azure_management_locks(stack_name: str, cwd: str = None) -> Any:
    log_client.info("Looking for Azure Management Locks...")

    stack = _get_stack(stack_name, cwd)
    stack_obj = json.loads(stack)

    if not stack_obj["deployment"].get("resources"):
        log_client.info(f"No resources found on stack: {stack_name}")
        exit(1)

    stack_resources = stack_obj["deployment"]["resources"]

    found_locks = []

    for resource in stack_resources:
        urn = resource["urn"]

        if "azure-native:authorization:ManagementLock" in urn:
            found_locks.append("--target")
            found_locks.append(urn)

    # Do not _run the 'remove_command' unless we have management locks to remove.
    if len(found_locks) >= 2:
        log_client.info(f"Removing {int(len(found_locks)/2)} Azure Management Locks...")
        cmd = [
            "destroy",
            "--yes",
            "--skip-preview",
            "--stack",
            stack_name,
        ] + found_locks
        _run(cmd, cwd)
    else:
        log_client.info("No Azure Management Locks found.")


def destroy_stack(stack_name: str, cwd: str = None) -> Any:
    log_client.info(f"Destroying Pulumi stack {stack_name}...")

    stack_file = os.path.join(os.getcwd(),"pulumistack.json")
    
    _export_stack(stack_name, stack_file, cwd)

    with open(stack_file, "r") as file:
        stack_obj = json.load(file)

    if not stack_obj["deployment"].get("resources"):
        log_client.info(f"No resources found on stack: {stack_name}")
        exit(1)

    filtered_stack_obj = dict(copy.deepcopy(stack_obj))
    # Remove all resources from the stack copy.
    # We'll be adding only the resources Pulumin has to destroy.
    filtered_stack_obj["deployment"]["resources"] = []

    
    for resource in stack_obj["deployment"]["resources"]:

        # ID based filtering
        if resource.get("id"):
            resource_id = resource["id"].lower()

            # Filter out child resources that are deployed in a resource group
            if "/resourcegroups/" in resource_id and "/providers/" in resource_id:
                continue
        
        # Type based filtering
        if resource.get("type"):
            resource_type = resource["type"].lower()

            # Filter out child resources of Azure Databricks workspaces.
            if "databricks:" in resource_type:
                continue
            if "pulumi:providers:databricks" in resource_type:
                continue

            # Filter out child resources of Azure storage accounts.
            if "azure:storage" in resource_type:
                continue
            
            # Filter out child resources of Azure DevOps Project resource.
            if "azuredevops:" in resource_type and "index/project:" not in resource_type:
                continue
        
        # If the resource was not filtered out, it means we should include it in our final stack state
        filtered_stack_obj["deployment"]["resources"].append(resource)
    
    # Save the new (filtered) stack into a new file
    filtered_stack_file = os.path.join(os.getcwd(),"pulumi-filtered-stack.json")
    with open(filtered_stack_file, "w") as filtered_file:
        filtered_file.write(json.dumps(filtered_stack_obj))
    
    # Import stack to Pulumi
    _import_stack(stack_name, filtered_stack_file, cwd)

    # Run Pulumi destroy
    _destroy_stack(stack_name, cwd)

    # Delete Pulumi stack
    _delete_stack(stack_name, cwd)
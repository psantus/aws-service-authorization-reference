from typing import Any
import httpx
import json
import sys
import asyncio
from typing import Any, Optional, Tuple
from thefuzz import fuzz
from mcp.server.fastmcp import FastMCP, Context

# Initialize FastMCP server
mcp = FastMCP("aws-service-authorization-reference")

# Constants
AWS_API_BASE = "https://servicereference.us-east-1.amazonaws.com"
USER_AGENT = "aws-service-authorization-reference-mcp-server/1.0"

class ServiceCache:
    """Class to manage service cache state"""
    def __init__(self):
        self.cache: Optional[dict[str, Any]] = None
        self.lock = asyncio.Lock()

# Global cache manager
_cache_manager = ServiceCache()

import asyncio
import httpx
import sys
from typing import Any, Optional, Tuple
from thefuzz import fuzz


class ServiceCache:
    """Class to manage service cache state"""
    def __init__(self):
        self.cache: Optional[dict[str, str]] = None
        self.lock = asyncio.Lock()


# Global cache manager
_cache_manager = ServiceCache()

@mcp.tool()
async def retrieve_service_codes() -> str | None:
    """
    Retrieve all services codes that you can use when calling retrieve_service_information, as a comma-separated list
    """
    service_urls = await get_services_list()
    if not service_urls:
        print("Failed to retrieve services list", file=sys.stderr)
        return None

    return ", ".join(service_urls.keys())

# @mcp.resource("serviceAuthorizationReference://{service}") # disabled because I get MCP error 0: Unknown resource: every time this is invoked
async def retrieve_service_information(service: str) -> Any | None:
    """
    Retrieve the full Authorization reference data (IAM actions, resources and condition keys) for a single AWS service

    Args:
        service: String. The code of the AWS service need to retrieve information for. If you don't know what the code is, call retrieve_service_codes

    Outputs:
        a json object (can be huge, call only if it fits your context window
    """
    url = await find_service_url(service)
    if not url:
        print(f"No matching service found for '{service}'", file=sys.stderr)
        return None

    print(f"Found service match: {url} for service code: {service})", file=sys.stderr)

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            response_json = response.json()
            # Convert to string to get actual character count
            return response_json
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
            return None

@mcp.tool()
async def retrieve_service_stats(service: str) -> Any | None:
    """
    Retrieve statistics (number of Actions, Resources, ConditonKeys) for a single AWS service

    Args:
        service: String. The code of the AWS service need to retrieve information for. If you don't know what the code is, call retrieve_service_codes

    Outputs:
        a json object with stats for this service
    """
    service_data = await retrieve_service_information(service)
    if not service_data:
        print(f"No matching service found for '{service}'", file=sys.stderr)
        return None

    return {
        "Actions": len(service_data['Actions']),
        "Resources": len(service_data['Resources']),
        "ConditionKeys": len(service_data['ConditionKeys'])
    }

@mcp.tool()
async def retrieve_service_actions(service: str) -> Any | None:
    """
    Retrieve the list of actions for a single AWS service

    Args:
        service: String. The code of the AWS service need to retrieve information for. If you don't know what the code is, call retrieve_service_codes

    Outputs:
        comma separated list of actions for this service
    """
    url = await find_service_url(service)
    if not url:
        print(f"No matching service found for '{service}'", file=sys.stderr)
        return None

    print(f"Found service match: {url} for service code: {service})", file=sys.stderr)

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return ", ".join([action['Name'] for action in data['Actions']])
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
            return None

@mcp.tool()
async def retrieve_service_resources(service: str) -> Any | None:
    """
    Retrieve the list of resources for a single AWS service

    Args:
        service: String. The code of the AWS service need to retrieve information for. If you don't know what the code is, call retrieve_service_codes

    Outputs:
        comma separated list of resources for this service
    """
    url = await find_service_url(service)
    if not url:
        print(f"No matching service found for '{service}'", file=sys.stderr)
        return None

    print(f"Found service match: {url} for service code: {service})", file=sys.stderr)

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return ", ".join([resource['Name'] for resource in data['Resources']])
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
            return None


@mcp.tool()
async def retrieve_service_condition_keys(service: str) -> Any | None:
    """
    Retrieve the list of condition keys for a single AWS service

    Args:
        service: String. The code of the AWS service need to retrieve information for. If you don't know what the code is, call retrieve_service_codes

    Outputs:
        comma separated list of condition keys for this service
    """
    url = await find_service_url(service)
    if not url:
        print(f"No matching service found for '{service}'", file=sys.stderr)
        return None

    print(f"Found service match: {url} for service code: {service})", file=sys.stderr)

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return ", ".join([condition_key['Name'] for condition_key in data['ConditionKeys']])
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
            return None


@mcp.tool()
async def retrieve_service_action_information(service: str, action: str) -> Any | None:
    """
    Retrieve the Authorization reference data (resources and condition keys) for a single AWS service action

    Args:
        service: String. The code of the AWS service need to retrieve information for. If you don't know what the code is, call retrieve_service_codes
        action: String. The action you want to retrieve information for

    Outputs:
        a json object
    """
    url = await find_service_url(service)
    if not url:
        print(f"No matching service found for '{service}'", file=sys.stderr)
        return None

    print(f"Found service match: {url} for service code: {service})", file=sys.stderr)

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            for action_data in data['Actions']:
                if action_data['Name'] == action:
                    # If action has a Resources array, enrich that array with the corresponding resource ARNFormats and ConditionKeys
                    if 'Resources' in action_data:
                        for resource in action_data['Resources']:
                            resource_name = resource['Name']
                            # Find the corresponding resource in the Resources array of the service data
                            for service_resource in data['Resources']:
                                if service_resource['Name'] == resource_name:
                                    resource['ARNFormats'] = service_resource['ARNFormats']
                                    if 'ConditionKeys' in service_resource:
                                        resource['ConditionKeys'] = service_resource['ConditionKeys']
                    return action_data
            return None
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
            return None


@mcp.tool()
async def retrieve_service_resource_information(service: str, resource: str) -> Any | None:
    """
    Retrieve the Authorization reference data (actions that target this resource or have condition keys that rely on this resource) for a single AWS service resource

    Args:
        service: String. The code of the AWS service need to retrieve information for. If you don't know what the code is, call retrieve_service_codes
        resource: String. The resource you want to retrieve information for

    Outputs:
        a json object
    """
    url = await find_service_url(service)
    if not url:
        print(f"No matching service found for '{service}'", file=sys.stderr)
        return None

    print(f"Found service match: {url} for service code: {service})", file=sys.stderr)

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            for resource_data in data['Resources']:
                if resource_data['Name'] == resource:
                    print('Found resource match!', file=sys.stderr)
                    if 'ARNFormats' in resource_data and len(resource_data['ARNFormats']) > 0:
                        resource_identifier = resource_data['ARNFormats'][0].split('/')[-1]
                        if resource_identifier.startswith('${') and resource_identifier.endswith('}'):
                            resource_identifier = resource_identifier[2:-1]
                            # Build full resource identifier as "service:resources_identifier"
                            full_resource_identifier = f"{service}:{resource_identifier}"
                            print(f'Resource Identifier is {full_resource_identifier}', file=sys.stderr)

                            # Initialize array if it doesn't exist
                            resource_data['ActionsWhereResourceAppearInConditionKey'] = []
                            resource_data['ActionsTargetingResource'] = []
                            resource_data['ConditionKeysThatRelyOnResource'] = []

                            # Find ConditionKeys, if any, that rely on this resource
                            for condition_key in data['ConditionKeys']:
                                if full_resource_identifier in condition_key['Name']:
                                    resource_data['ConditionKeysThatRelyOnResource'].append(condition_key['Name'])
                                    # Find Actions that rely on this ConditionKey
                                    for action in data['Actions']:
                                        if 'ActionConditionKeys' in action:
                                            if condition_key['Name'] in action['ActionConditionKeys']:
                                                resource_data['ActionsWhereResourceAppearInConditionKey'].append(action['Name'])

                            # Find actions that target this resource as their target
                            for action in data['Actions']:
                                if 'Resources' in action:
                                   for action_resource in action['Resources']:
                                        if resource == action_resource['Name']:
                                            resource_data['ActionsTargetingResource'].append(action['Name'])

                    return resource_data
            return None
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
            return None

@mcp.tool()
async def retrieve_service_condition_key_information(service: str, condition_key: str) -> Any | None:
    """
    Retrieve the Authorization reference data (actions that rely on this condition key) for a single AWS service condition key

    Args:
        service: String. The code of the AWS service need to retrieve information for. If you don't know what the code is, call retrieve_service_codes
        condition_key: String. The condition key you want to retrieve information for

    Outputs:
        a json object
    """
    url = await find_service_url(service)
    if not url:
        print(f"No matching service found for '{service}'", file=sys.stderr)
        return None

    print(f"Found service match: {url} for service code: {service})", file=sys.stderr)

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            for condition_key_data in data['ConditionKeys']:
                if condition_key_data['Name'] == condition_key:
                    print('Found condition key match!', file=sys.stderr)
                    # Initialize array if it doesn't exist
                    condition_key_data['ActionsUsingConditionKey'] = []
                    # Find Actions that rely on this ConditionKey
                    for action in data['Actions']:
                        if 'ActionConditionKeys' in action:
                            if condition_key in action['ActionConditionKeys']:
                                condition_key_data['ActionsUsingConditionKey'].append(action['Name'])

                    # Find resources that rely on this ConditionKey
                    if 'Resources' in data:
                        condition_key_data['ResourcesUsingConditionKey'] = []
                        for resource in data['Resources']:
                            if 'ConditionKeys' in resource:
                                if condition_key in resource['ConditionKeys']:
                                    # Name and ARNFormats
                                    del resource['ConditionKeys']
                                    condition_key_data['ResourcesUsingConditionKey'].append(resource)
                    return condition_key_data
            return None
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
            return None

async def retrieve_services_list() -> dict[str, str] | None:
    """
    Retrieve the list of AWS Services for which AWS provides Authorization reference
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(AWS_API_BASE, headers=headers, timeout=30.0)
            response.raise_for_status()
            service_data = response.json()

            if not isinstance(service_data, list):
                print("Unexpected response format: not a list", file=sys.stderr)
                return None

            return {service['service']: service['url'] for service in service_data}

        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            return None


async def get_services_list() -> dict[str, str] | None:
    """
    Get the AWS services list, fetching it only once and caching the result.
    Subsequent calls will return the cached result.
    """
    async with _cache_manager.lock:
        # Return cached result if available
        if _cache_manager.cache is not None:
            return _cache_manager.cache

        # Fetch and cache if not available
        _cache_manager.cache = await retrieve_services_list()
        return _cache_manager.cache


async def find_service_url(service_code: str) -> Optional[str]:
    """
    Find the service URL based on service code.
    """
    service_urls = await get_services_list()
    if not service_urls:
        print("Failed to retrieve services list", file=sys.stderr)
        return None

    return service_urls.get(service_code)

@mcp.prompt()
def get_iam_reference_data_for_service():
    """Retrieve Authorization reference data (IAM Actions, Objects and Condition Keys) for AWS services"""
    return ('To retrieve information about AWS service, you can use a step by step approach: '
            'first use the retrieve_service_codes '
            'and find code for the service, '
            'then use the retrieve_service_actions or retrieve_service_resources '
            'depending on whether you need to find information on a specific action '
            'then use retrieve_service_action_information or retrieve_service_resource_information '
            'to get specific information.'
            )

if __name__ == "__main__":
    # Initialize and run the server
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Runtime Error: {str(e)}")



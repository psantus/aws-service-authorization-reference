# AWS Service Reference Information MCP Server

A Model Context Protocol server providing access to AWS Service Reference Information. 
This server enables LLMs to retrieve IAM actions, resources and conditions keys.

### What is AWS Service Authorization Reference?
AWS Service Authorization Reference is a piece of documentation [available here](https://docs.aws.amazon.com/service-authorization/latest/reference/reference.html) 
where AWS gives exhaustive reference data on all IAM Actions, Resources and Condition Keys, 
grouping information that was otherwise scattered across multiple service documentations.

In 2024, AWS added programmatic support to access this data. 

Since March 13, 2025, [Service Reference Information includes](https://aws.amazon.com/about-aws/whats-new/2025/03/aws-service-reference-information-resources-condition-keys/) Resources and Condition Keys.

### Available Tools

- `retrieve_service_codes` - Lists all service codes for which we have documentation available
- `retrieve_service_stats` - Tells how many Actions, Resources and Condition Keys are documented.
    - `service` (string, required): the code of the service
- `retrieve_service_actions` - A comma-separeted list of all actions for a service
    - `service` (string, required): the code of the service
- `retrieve_service_resources` - A comma-separeted list of all resources for a service
    - `service` (string, required): the code of the service
- `retrieve_service_condition_keys` - A comma-separeted list of all conditions keys for a service
    - `service` (string, required): the code of the service
- `retrieve_service_action_information` - Retrieve the authorization reference data (resources and condition keys) for a single AWS service action
    - `service` (string, required): the code of the service
    - `action` (string, required): the code of the action
- `retrieve_service_resource_information` - Retrieve the authorization reference data (resources and condition keys) for a single AWS service action
    - `service` (string, required): the code of the service
    - `resource` (string, required): the code of the action
- `retrieve_service_condition_key_information` - Retrieve the authorization reference data (resources and condition keys) for a single AWS service action
    - `service` (string, required): the code of the service
    - `condition_key` (string, required): the code of the action

## Installation

### Using uv

With [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. Run `uv build` then `uv run main.py`.

## Configuration

### Configure for Claude.app

Add to your Claude settings:

<details>
<summary>Using uv</summary>

```json
"aws-service-authorization-reference": {
  "command": "uv",
  "args": [
    "--directory",
    "/root/to/folder/aws-service-authorization-reference", 
    "run",
    "main.py"
    ]
  }
```

## Debugging

You can use the MCP inspector to debug the server. For uv installations:

```
npx @modelcontextprotocol/inspector \                            
  uv \
  --directory /Root/to/folder/aws-service-authorization-reference \
  run \
  main.py

```
## License

aws-service-authorization-reference MCP Server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.

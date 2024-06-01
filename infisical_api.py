"""Infisical REST API Client"""  # pylint: disable=invalid-name

import json
import requests


class infisical_api:  # pylint: disable=invalid-name
    """Infisical API Functions"""

    def __init__(
        self,
        service_token: str,
        infisical_url: str = "https://app.infisical.com",
        workspace_id: str = "dynamic",
    ):
        self.service_token = service_token
        self.infisical_url = infisical_url
        self.workspace_id = workspace_id

    def get_secret(
        self, secret_name: str, environment: str = "prod", path: str = "/"
    ) -> dict:  # pylint: disable=no-self-argument
        """Retrieve Secret"""
        if self.service_token == "":
            raise PermissionError("Please provide a valid service_token")

        try:
            if self.workspace_id == "dynamic":
                workspace_id = self.get_workspace_id()
            else:
                workspace_id = self.workspace_id
            response = requests.get(
                url=f"{self.infisical_url}/api/v3/secrets/raw/{secret_name}",
                params={
                    "workspaceId": workspace_id,
                    "environment": environment,
                    "secretPath": path,
                },
                headers={
                    "Authorization": f"Bearer {self.service_token}",
                },
                timeout=15,
            )
            data = json.loads(response.text)
            secret = data["secret"]
            return convert_to_dot_notation(secret)
        except requests.exceptions.RequestException:
            return {}

    def get_workspace_id(self) -> str:
        """Get Workspace ID"""

        try:
            response = requests.get(
                url=f"{self.infisical_url}/api/v2/service-token",
                headers={
                    "Authorization": f"Bearer {self.service_token}",
                },
                timeout=15,
            )
            print(response)
            data = json.loads(response.text)
            return data["workspace"]
        except requests.exceptions.RequestException:
            print("Failed to get Workspace ID")


class convert_to_dot_notation(dict):
    """
    Access dictionary attributes via dot notation
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

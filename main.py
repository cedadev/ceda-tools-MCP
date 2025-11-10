import asyncio
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ceda-tools")
observation_api_url = "http://api.catalogue.ceda.ac.uk/api/v3/observations/"

async def call_observation_api(observation_uuid):
    response = requests.get(observation_api_url+"?uuid="+observation_uuid)
    return response.json()

# search observations (datasets)
@mcp.tool()
async def search_whole_observation_by_uuid(observation_uuid: str) -> str:
    """
    Search for a MOLES observation record using its uuid.
    This function will return the whole JSON response.
    """

    return await call_observation_api(observation_uuid)



# get filepath given an observation (dataset) id
@mcp.tool()
async def get_observation_filepath_by_uuid(observation_uuid: str) -> str:
    """
    Search for a MOLES observation record using its uuid.
    This function will return the filepath of the dataset.
    """

    json_response = await call_observation_api(observation_uuid)
    
    if json_response["count"] != 1:
        return "MOLES record not found (or has multiple uuids (unlikely))"

    return (json_response["results"][0]["result_field"]["dataPath"])



# Is MOLES record complete
@mcp.tool()
async def get_observation_completion_status_by_uuid(observation_uuid: str) -> str:
    """
    Search for a MOLES observation record using its uuid.
    This function will return only the completion status.
    """

    json_response = await call_observation_api(observation_uuid)
    
    if json_response["count"] != 1:
        return "MOLES record not found (or has multiple uuids (unlikely))"

    return (json_response["results"][0]["status"])


if __name__ == "__main__":
    mcp.run(transport="stdio")


""" ###
api_url = "http://api.catalogue.ceda.ac.uk/api/v0/obs/get_info/"
moles_path = "badc/ukmo-midas/data/GL"
response = requests.get(api_url+moles_path)
print(response.json())
### """

""" ###
api_url = "http://api.catalogue.ceda.ac.uk/api/v3/observations/?uuid="
observation_uuid = "7e23b82ec3bdc8e5297c0b623697c559"
response = requests.get(api_url+observation_uuid)
json_response = response.json()
if json_response["count"] != 1:
    print("MOLES record not found (or has multiple uuids (unlikely))")
print(json_response["results"][0]["status"])
### """

""" ###
observation_uuid = "7e23b82ec3bdc8e5297c0b623697c559"
json_response = asyncio.run(call_observation_api(observation_uuid))
print(json_response["results"][0]["status"])
### """
import aiohttp
from urllib.parse import urlencode
import argparse
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ceda-tools")
OBSERVATION_API_URL = "http://api.catalogue.ceda.ac.uk/api/v3/observations/"
DEFAULT_PAGE_SIZE = 3
STRIP_FIELDS = {
    "phenomena",
    "identifier_set",
    "responsiblepartyinfo_set",
    "discoveryKeywords",
}

async def call_observation_api(params: dict, page: int = 1) -> dict:
    """
    Call the CEDA observations API with the given parameters.
    Applies pagination and removes heavy fields from each dataset.
    Returns the JSON response as a Python dict.
    """
    # Add pagination params to query
    paginated_params = {
        **params,
        "limit": DEFAULT_PAGE_SIZE,
        "offset": (page - 1) * DEFAULT_PAGE_SIZE,
    }
    
    query_string = urlencode(paginated_params)
    url = f"{OBSERVATION_API_URL}?{query_string}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return {
                    "error": f"Request failed with status {response.status}",
                    "url": url,
                }
            try:
                data = await response.json()
            except Exception as e:
                return {
                    "error": f"Failed to parse JSON: {str(e)}",
                    "url": url,
                }

    # Strip heavy fields
    if "results" in data and isinstance(data["results"], list):
        for entry in data["results"]:
            for field in STRIP_FIELDS:
                entry.pop(field, None)

    return data

# --------------------------------------------------------------------------- #
#  TOOLS
# --------------------------------------------------------------------------- #

@mcp.tool()
async def search_whole_observations_with_keywords( # WAY TOO BIG FOR MODELS (maybe make it return the first 5? Paginate it so you can chose different sections of the 5?)
    abstract_contains: str, title_contains: str
) -> dict:
    """
    Search for a MOLES observation record using keywords for title and abstract.
    Returns the full JSON response.
    """
    params = {
        "abstract__icontains": abstract_contains,
        "title__icontains": title_contains,
    }
    return await call_observation_api(params)


@mcp.tool()
async def search_whole_observation_by_uuid(observation_uuid: str) -> dict:
    """
    Search for a MOLES observation record using its UUID.
    Returns the full JSON response.
    """
    return await call_observation_api({"uuid": observation_uuid})



@mcp.tool()
async def get_observation_filepath_by_uuid(observation_uuid: str) -> dict:
    """
    Retrieve the dataset filepath from a MOLES observation record by UUID.
    Returns a dict with either the filepath or an error message.
    """
    response = await call_observation_api({"uuid": observation_uuid})

    if response.get("count") != 1:
        return {"error": "MOLES record not found or multiple UUIDs found", "response": response}

    try:
        filepath = response["results"][0]["result_field"]["dataPath"]
        return {"filepath": filepath}
    except KeyError:
        return {"error": "Filepath not found in record", "response": response}



@mcp.tool()
async def get_observation_completion_status_by_uuid(observation_uuid: str) -> dict:
    """
    Retrieve the completion status of a MOLES observation record by UUID.
    Returns a dict with either the status or an error message.
    """
    response = await call_observation_api({"uuid": observation_uuid})

    if response.get("count") != 1:
        return {"error": "MOLES record not found or multiple UUIDs found", "response": response}

    try:
        status = response["results"][0]["status"]
        return {"status": status}
    except KeyError:
        return {"error": "Status field not found in record", "response": response}

# --------------------------------------------------------------------------- #
#  ENTRY POINT
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Start the server
    print("🚀Starting server... ")

    # Debug Mode
    #  uv run mcp dev server.py

    # Production Mode
    # uv run server.py --server_type=sse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server_type", type=str, default="sse", choices=["sse", "stdio"]
    )

    args = parser.parse_args()
    mcp.run(args.server_type)
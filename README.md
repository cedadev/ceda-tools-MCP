```
python -m venv server_venv
source server_venv/bin/activate
pip install --upgrade pip
```

requirements.txt
```txt
mcp[cli]
requests
pytest-asyncio
```
After creating that file, run:
```
pip install -r requirements.txt


python main.py
pytest -s
```


---


To run the server on VS Code so that you can use github copilot to run the MCP tools:


what I did was add a file into my working directory with the server. This runs the MCP server allowing the AI to use it.

```
mkdir .vscode
cd .vscode
touch mcp.json
vim mcp.json
```

```json
{
  "servers": {
    "ceda-tools": {
      "type": "stdio",
      "command": "${workspaceFolder}/server_venv/bin/python",
      "args": [
        "main.py"
      ]
    }
  }
}

```
`.vscode/mcp.json`

Once that file is created, restart VS code opening the workspace with the server in. For example, this is what my workspace looked like:

```
main.py
.
├── .vscode
│   └── mcp.json
├── main.py
├── requirements.txt
├── README.md
└── tests
    └── test_server.py
```

once that is done, open copilot in vs code and click the bottom on the bottom left of the input box.
Here select Agent. Once agent is selected, click the tools icon on the bottom right (to the left of send). here scroll to the bottom of the Configure Tools menu and look for `ceda-tools`. Tick that box if it isn't already.
Within ceda-tools, there should be a list of all of the tools created in the tutorial.

Once this has been selected, you can ask the chatbot for information, and it should run a tool and ask you permission to do so.


For more information on MCP in VS Code, see here:
https://code.visualstudio.com/docs/copilot/customization/mcp-servers
(this guide was the add an MCP server to a dev container section)
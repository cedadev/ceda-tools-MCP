Give me the completion status and filepath as well as the uuid. Do this for the first Sentinel observation. Use the tools that you have access to, do not use your pre-trained data.

Give me some highlights for the dataset with this uuid: ba5618b8ad6540c4b16df4877350464c


https://skywork.ai/skypage/en/ollama-mcp-servers-ai-agents/1977924408481091584
https://github.com/jonigl/mcp-client-for-ollama?tab=readme-ov-file#how-tool-calls-work

ollama pull {model}

ollmcp -j ~/.config/ollmcp/mcp-servers/config.json -m llama3.1:8b-instruct-q8_0



clone the repo
rm -rf .git (to remove tracking for git)
make a venv
update pip
pip install .

add the json server mcp file (adjust command depending on where it is)
ollmcp -j config.json -m llama3.1:8b-instruct-q8_0

run command



ollmcp -j config.json -m qwen3:14b

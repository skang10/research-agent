
# Simple Research Agent

## 1. Installation & Run

Requirements:

* Python 3.12
* uv
* OpenRouter API key
* Tavily API key

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173/`

### Backend

1. Create an `.env` file

```bash
cd backend
cp .env.example .env
```

2. Setup API keys

```env
OPENROUTER_API_KEY=your_key
TAVILY_API_KEY=your_key
```

3. Run the backend in Docker

Make sure you are at the `backend` folder:

```bash
docker build -t research-agent-backend .
docker run \
  --env-file .env \
  -p 8787:8787 \
  research-agent-backend
```

- Backend runs at `http://localhost:8787/`
- Check API docs at `http://localhost:8787/docs`

## Development

1. Start backend with `uv`, the server reloads automatically when files change

```bash
cd backend
uv sync
uv run python -m app.main
```

2. Change the configuration file for different setups: [config.yaml](backend/config.yaml)

3. Run unit & integration tests

```bash
cd backend
uv run pytest # all tests
uv run pytest integration/* # integration tests
```

## 2. Architecture and Design

### Frameworks

- Backend service: FastAPI
- Agent framework: Pydantic AI
- Model provider: OpenRouter

### Implementation

The backend is implemented in the following order:

1. Identify the two APIs to implement, `/api/sources` and `/api/research`
2. Set up the model schemas for the two APIs
3. Implement dummy input and output for the two APIs
4. Implement a minimal `/api/sources` for `.txt` files, with an ingestion flow of: parse → chunk → embed → add to FAISS
5. Implement a minimal `/api/research` by setting up a research agent with 3 tools: `local_search`, `tavily_search_tool`, and `web_fetch_tool`
6. Test the backend APIs with example files and prompts
7. Integrate with the frontend

### Design principles

1. Build a minimal working project
2. Try to follow the dependency injection principle
2. Try to make the project extensible using abstraction, e.g. [backend/app/db/vector_store/base.py](backend/app/db/vector_store/base.py)

### Plans for future

1. Improve backend logging using a proper logger and HTTP response status codes
2. Enable upload of more document types, e.g. pdf/docx
3. Replace FAISS with a proper vector database
4. Add persistence for uploaded data and indexed embeddings
5. Add chat history, better context management, and session management for the agent
6. Add more comprehensive unit/integration tests
7. Enable cloud deployment

## 3. Example queries and expected outputs

### Upload txt document: [text_source.txt](backend/tests/fixtures/test_source.txt)

```bash
curl -X POST   http://127.0.0.1:8787/api/sources   -F "files=@tests/fixtures/test_source.txt"
```

### Example query 1:

```bash
curl -N -X POST   http://127.0.0.1:8787/api/research   -H "Content-Type: application/json"   -d '{"request":"Who is the attendee of the meeting?"}'
```

If `test_source.txt` is not uploaded, example output:
```plain text
[Thinking] **Seeking clarification on meeting attendees**

The user is asking, "Who is the attendee of the meeting?" but it feels pretty vague without context. I see that we have the tools to search but no specific meeting details to refer to. I think it's best to ask them for clarification: "Which meeting are you referring to?" I could also suggest ways to identify attendees, like checking calendar invites or attendance lists. If it's fictional, I could propose steps to help retrieve attendees.**Clarifying meeting details**

I want to ask the user if they have a link or a calendar invite for the meeting. Is it a virtual one, like on Zoom or Teams, where there’s an attendee list? I could also suggest searching Tavily for any news on the meeting and attendees if it's a public event. Since we lack local documents, I’ll respond with clarifying questions. If they provide more context—like the meeting title or date—I can help them further.**Crafting a helpful response**

I recognize that I don’t have enough information to identify the meeting attendees, so I’ll ask the user for more details or permission to search. If they want, I can look up specific meeting attendees if
 it’s public. I’ll keep my response concise but helpful, suggesting they provide the meeting name, date, or organizer, or upload any invites. I also need to mention privacy; I can't access private calendars unless they share that information.**Offering options for meeting attendees**

I want to ensure I’m as helpful as possible. If the user shares a document, I can parse it for attendee information, but I can't accept file uploads right now. I can encourage them to paste any text with meeting minutes or an attendee list here. My approach will be to provide clear options: "Could you specify which meeting you're referring to? If you have the meeting title, date, or a link, I can help find the attendee list. Also, I can look up attendees using Tavily for public events."**Clarifying the meeting inquiry**

I think running a search in parallel might not be the best approach since the meeting isn’t known yet. Instead, it seems clearer to focus on asking the user for clarification. I want to maintain brevity while ensuring I gather enough information to help effectively. So, I’ll respond with clear and concise questions to understand what meeting they’re referring to. Keeping it simple will make it easier to get the information I need!

[Answer] I don’t have enough information to identify the attendees. Could you clarify which meeting you mean? Here are a few options:

- Share the meeting title, date, and organizing body (and the organization if applicable).
- Provide a link or invite (if you have one).
- If you have a minutes or agenda document, paste it here and I can extract the attendee names.
- If this is a public meeting, I can try to search for attendee lists online—let me know the event name and date.

Once I have the details, I’ll try to locate the attendee list or guide you on how to retrieve it.
```

If `test_source.txt` is uploaded, example output:
```plain text
[Thinking] **Searching for meeting details**

The user wants to know who attended the meeting and has provided a document named test_source.txt. I should use local_search to find relevant info, with queries like "attendee" or "meeting attendee." First, I'll check the content of test_source.txt. The local_search tool will help me extract info from uploaded files, so my plan is to execute it with the query "attendee" and see what results come up. Then I can summarize the findings for the user.

[Tool] Calling local_search...
[Tool] local_search completed.
[Thinking]

[Answer] According to the uploaded document, the Platform Team Meeting on 12 Sept 2026 had attendees: Mara, Jonas, Priyanka, and Felix. If you meant a different meeting, tell me which one.
```

### Example query 2:

```bash
curl -N -X POST   http://127.0.0.1:8787/api/research   -H "Content-Type: application/json"   -d '{"request":"Search the web and tell me the latest stable Python release."}'
```

Example output:

```plain text
[Thinking] **Searching for Python release info**

The user wants me to search the web for the latest stable Python release. I've got some tools I can use like tavily_search for web searching. Considering the time frame, I need to look for the latest stable release as of now in September 2026. Python 3.11 was out, and possibly 3.12 or even 3.13, but I can't rely on what I remember. So, I'll perform a search using the tavily_search tool for queries like "latest stable Python release" or "Python 3.x latest stable version."**Deciding on search parameters**

I need to find the latest stable Python release. To be safe, I should choose "month" for the time range, but picking "day" will fetch the most recent results. The time range options include "day," "week," "month," "year," and null, so I’ll go with "day."

For the topic, since this is news about a release, using "news" would be better to catch any official announcements. I’ll also check the uploaded document, "test_source.txt," to search for relevant Python version information.**Searching for Python version info**

To see if the document "test_source.txt" contains relevant information, I should use local_search to check for "Python" or "version." Since I haven't loaded the document yet, I'll search it with the query "latest Python release." However, I suspect the documents might not be related. Still, it's worth checking for the user's benefit.

So, I’ll run a parallel search using both tavily_search for the latest stable release and local_search for any mentions in the document. I'll make sure the tools work together seamlessly!**Choosing search parameters**

I’ll use "basic" for the search depth since that’ll cover general information well. I want to use the time range of "day" to fetch the latest updates, and I’ll set the topic to "news." For the local search, I’ll query for "latest Python release."

Once I receive results from both searches, I'll present the user with the newest stable Python version, its release date, and possibly link to official notes. Given we're in 2026, it might be Python 3.14, but I'll confirm that once I see the results!**Running parallel searches**

I’m ready to proceed by using multi_tool_use.parallel to run two tools simultaneously. This way, I can gather information efficiently. I’ll make sure both the tavily_search and local_search tools are called at the same time to get comprehensive results on the latest Python release. It's nice to streamline the process and grab all the relevant info for the user quickly! Let's get those searches rolling!

[Tool] Calling tavily_search...


[Tool] Calling local_search...
[Tool] local_search completed.[Tool] tavily_search completed.
...

[Answer] Latest stable Python release: Python 3.14.7 (final)

- Release date: 2026-08-05
- What it is: the latest patch release in the 3.14.x series (stable, with security and bugfix updates)
- Read more:
  - Python.org downloads page: https://www.python.org/downloads/release/python-3147/
  - Changelog / what's new: https://docs.python.org/release/3.14.7/whatsnew/changelog.html

If you’d like, I can pull out the key highlights from the 3.14.7 changelog or help you upgrade your environment.
```

### Example query 3:

```bash
curl -N -X POST   http://127.0.0.1:8787/api/research   -H "Content-Type: application/json"   -d '{"request":"Read https://www.python.org/about/ and summarize what Python is and what it is commonly used for."}'
```

Example output:

```plain text
[Thinking] **Fetching and summarizing Python info**

I need to respond as an AI assistant to summarize what Python is and its common uses based on the user's request to read a URL. I'll use the web_fetch tool to fetch content from the Python.org about page. Once I have the page, I can summarize that Python is an interpreted, high-level programming language that emphasizes readability. I'll also note its uses, including web development, data science, automation, and more. Let's do this!**Summarizing Python's characteristics**

I need to summarize what Python is and its uses based on the information from a URL. I'll fetch the page using the web_fetch tool, then extract key points about Python being a versatile programming language that allows for quick work and effective integration. It’s interpreted, high-level, general-purpose, and emphasizes readability and simplicity. Its applications range from web development and data science to automation and education. Let’s proceed with the tool call to get the details!**Fetching and parsing Python information**

Next, I'll parse the content fetched from the Python page. The tool will likely return HTML or markdown format, which I need to extract the main points from. I expect to find information like, "Python is a programming language that lets you work quickly and integrate systems effectively." Once I have that, I'll compose a concise summary. So, let’s go ahead and perform the web_fetch call!

[Tool] Calling web_fetch...
[Tool] web_fetch completed.

...

[Answer] Here’s a concise summary based on Python.org’s About Python page.

What Python is
- Python is a general-purpose programming language described as powerful, fast, and open.
- It is designed to be friendly and easy to learn, with code that is readable and approachable.
- It runs on many platforms (cross-platform) and has a strong, open-source ecosystem (OSI-approved license).

Common uses
- Web and Internet development
- Database access
- Desktop GUI applications
- Scientific and numeric computing
- Education and teaching programming
- Network programming
- Software and game development

Additional context
- The Python Package Index (PyPI) hosts thousands of third-party modules, enabling a wide range of capabilities beyond the standard library.
- Python’s community and documentation are highlighted as supportive resources for getting started and ongoing learning.
```

## 4. Agent evaluation

Currently, I am using two AI generated [text files](backend/tests/fixtures/) to test whether the `local_search` tool works properly,
with a few queries to test the `web_search` and `web_fetch` tools.

In the future, more test files and queries will be needed to evaluate:
1. Retrieval quality
2. Tool selection
3. Answer quality
4. Other RAG/agent behaviors and edge cases

Therefore, a golden dataset would be useful for more systematic evaluation. Human evaluation and LLM-as-a-judge could also
be used to assess the agent's performance.


## Note: AI-Assitance

I did not use Claude Code/Codex for this project. The steps are implemented on my own.
The task file `AI Engineer Technical Test.pdf` was not provided to any AI tool.

I used ChatGPT chat for:

1. Discussing the overall project design, e.g. the directory structure and breakdown of steps
2. Helping with points where I got stuck, such as agent streaming for pydantic ai agent
3. Helping with the Dockerfile implementation
4. README

I also used GitHub Copilot Autocomplete for:

1. The ingestion pipeline, as I was already familiar with embedding search and knew what I wanted to implement
2. Tests
3. Other code where I already had a clear idea of what I wanted to implement

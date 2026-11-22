# Spring AI ChatClient API

A learning-focused Spring Boot REST API that sends questions to an OpenAI chat model using Spring AI's fluent `ChatClient` API. It demonstrates a direct chat request, a resource-based prompt template, configuration through an environment variable, and controller tests that do not call an external AI service.

> **Attribution:** This project is based on the [`chatclient-api` example](https://github.com/LearnCodeWithDurgesh/spring-ai-yt-series/tree/main/chatclient-api) from [LearnCodeWithDurgesh/spring-ai-yt-series](https://github.com/LearnCodeWithDurgesh/spring-ai-yt-series). This copy includes cleanup, documentation, and tests. Review the original repository's license and attribution terms before redistributing it.

## Features

- Synchronous AI responses through Spring AI `ChatClient`.
- Direct chat endpoint and prompt-template endpoint.
- System and user prompt templates stored under `src/main/resources/prompts/`.
- OpenAI API key read from `OPENAI_API_KEY` rather than committed in source.
- Input validation for blank query parameters.
- Controller tests using a mocked service (no API key or network call needed).
- Maven Wrapper included.

## Technology

| Technology | Version / configuration |
| --- | --- |
| Java | 21 (Maven compiler target) |
| Spring Boot | 3.5.5 |
| Spring AI | 1.0.1 |
| Build | Maven Wrapper |
| AI provider | OpenAI; model configured as `gpt-4.1` |
| Server port | `8081` |

## Project structure

This follows the conventional Spring Initializr Maven structure, with **one `src` directory**:

```text
chatclient-api/
├── .mvn/wrapper/                 # Maven Wrapper configuration
├── src/
│   ├── main/
│   │   ├── java/com/spring/ai/firstproject/
│   │   │   ├── FirstProjectApplication.java  # Spring Boot entry point
│   │   │   ├── config/AiConfig.java          # ChatClient bean and defaults
│   │   │   ├── controllers/ChatController.java # HTTP routes and validation
│   │   │   ├── service/
│   │   │   │   ├── ChatService.java          # Service contract
│   │   │   │   └── ChatServiceImpl.java      # Prompt creation and AI calls
│   │   │   └── entity/Tut.java               # Example data class
│   │   └── resources/
│   │       ├── application.properties        # Port, model, key setting
│   │       └── prompts/
│   │           ├── system-message.st         # Assistant behavior
│   │           └── user-message.st           # User prompt template
│   └── test/java/com/spring/ai/firstproject/
│       └── FirstProjectApplicationTests.java # Controller tests
├── mvnw
├── mvnw.cmd
├── pom.xml
└── README.md
```

Maven generates `target/` when you build or test. It is build output, not another source directory.

## Requirements

- JDK 21 or newer.
- An OpenAI API key with access to the configured model.
- Internet access to download Maven dependencies and make AI requests.

A separate Maven installation is not needed; use the included wrapper.

## Configure and run

Set the API key in your terminal environment. **Do not put a real key in `application.properties`, commit it to Git, or include it in screenshots.**

### Windows PowerShell

```powershell
$env:OPENAI_API_KEY = "your-openai-api-key"
.\mvnw.cmd spring-boot:run
```

### macOS / Linux / Git Bash

```bash
export OPENAI_API_KEY="your-openai-api-key"
./mvnw spring-boot:run
```

The application starts at `http://localhost:8081`. The API key and model are configured in `src/main/resources/application.properties`:

```properties
spring.application.name=chatclient-api
server.port=8081
spring.ai.openai.api-key=${OPENAI_API_KEY}
spring.ai.openai.chat.options.model=gpt-4.1
```

## API endpoints

All successful endpoints return the AI response as plain text. URL-encode query values when they contain spaces or special characters.

### Direct chat

```http
GET /api/chat?q=Explain%20dependency%20injection%20in%20Spring
```

Example with `curl`:

```bash
curl --get "http://localhost:8081/api/chat" \
  --data-urlencode "q=Explain dependency injection in Spring"
```

The original tutorial route is also supported:

```http
GET /chat?q=Explain%20dependency%20injection%20in%20Spring
```

### Prompt-template chat

```http
GET /api/chat/template?concept=Java%20streams
```

Example with `curl`:

```bash
curl --get "http://localhost:8081/api/chat/template" \
  --data-urlencode "concept=Java streams"
```

This endpoint loads the system prompt from `system-message.st` and the user prompt from `user-message.st`, then substitutes the requested concept.

### Input errors

- Missing required query parameters return `400 Bad Request`.
- Blank `q` or `concept` values return `400 Bad Request` with a short explanation.

## How a request works

```text
HTTP request
    -> ChatController validates the input
    -> ChatService describes the operation
    -> ChatServiceImpl builds a ChatClient prompt
    -> Spring AI sends the prompt to the configured OpenAI model
    -> The model response is returned as plain text
```

`AiConfig` creates the shared `ChatClient` bean from Spring AI's auto-configured builder. The direct endpoint uses the default system instruction; the template endpoint uses the prompt resources.

## Run tests

Tests do not require `OPENAI_API_KEY` because the controller's service dependency is mocked.

### Windows PowerShell

```powershell
.\mvnw.cmd clean test
```

### macOS / Linux / Git Bash

```bash
./mvnw clean test
```

The current test suite covers a successful chat request, a missing question parameter, and a blank question. It does not make a live request to OpenAI.

## Limitations

This is a small learning project, not a production-ready chatbot. It does not currently provide conversation history, streaming responses, authentication, rate limiting, a frontend, or dedicated handling for all provider/network failures. Live model requests require a valid key, network access, model availability, and may incur provider charges.

## License and source

The tutorial source is available at [LearnCodeWithDurgesh/spring-ai-yt-series/chatclient-api](https://github.com/LearnCodeWithDurgesh/spring-ai-yt-series/tree/main/chatclient-api). Check its license and attribution requirements before publishing or redistributing this modified copy.

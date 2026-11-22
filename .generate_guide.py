from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, PageBreak

OUT = Path(__file__).with_name("chatclient-api-project-guide.pdf")
styles = getSampleStyleSheet()
navy = colors.HexColor("#17324D")
blue = colors.HexColor("#176B87")
light = colors.HexColor("#EEF4F7")
muted = colors.HexColor("#52616B")
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=31, textColor=navy, alignment=0, spaceAfter=7))
styles.add(ParagraphStyle(name="SubCustom", parent=styles["Normal"], fontSize=11, leading=16, textColor=muted, spaceAfter=13))
styles.add(ParagraphStyle(name="H1Custom", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=navy, spaceBefore=7, spaceAfter=8))
styles.add(ParagraphStyle(name="H2Custom", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=blue, spaceBefore=7, spaceAfter=4))
styles.add(ParagraphStyle(name="BodyCustom", parent=styles["BodyText"], fontSize=9.4, leading=14, spaceAfter=6))
styles.add(ParagraphStyle(name="SmallCustom", parent=styles["BodyText"], fontSize=8, leading=11, textColor=muted, spaceAfter=4))
styles.add(ParagraphStyle(name="BulletCustom", parent=styles["BodyText"], fontSize=9.2, leading=13, leftIndent=12, firstLineIndent=-8, spaceAfter=4))
styles.add(ParagraphStyle(name="CodeCustom", fontName="Courier", fontSize=7.5, leading=10, backColor=light, borderColor=colors.HexColor("#D6E1E8"), borderWidth=0.5, borderPadding=7, leftIndent=4, rightIndent=4, spaceBefore=4, spaceAfter=8))
styles.add(ParagraphStyle(name="THCustom", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8.2, leading=10, textColor=colors.white))
styles.add(ParagraphStyle(name="TCCustom", parent=styles["BodyText"], fontSize=8.2, leading=11))

def P(s, style="BodyCustom"):
    return Paragraph(s, styles[style])

def bullet(s):
    return Paragraph("&bull; " + s, styles["BulletCustom"])

def code(s):
    return Preformatted(s.strip("\n"), styles["CodeCustom"])

def make_table(rows, widths):
    data = []
    for ri, row in enumerate(rows):
        st = "THCustom" if ri == 0 else "TCCustom"
        data.append([Paragraph(str(x), styles[st]) for x in row])
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), navy),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CFD9DF")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, light]),
    ]))
    return t

def footer(canvas, doc):
    canvas.saveState()
    w, _ = A4
    canvas.setStrokeColor(colors.HexColor("#D5DEE4"))
    canvas.line(18*mm, 15*mm, w-18*mm, 15*mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(muted)
    canvas.drawString(18*mm, 10*mm, "Spring AI ChatClient API - Project Guide")
    canvas.drawRightString(w-18*mm, 10*mm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=19*mm, leftMargin=19*mm, topMargin=17*mm, bottomMargin=21*mm, title="Spring AI ChatClient API - Project Guide", author="Project documentation")
story = []
story += [P("Spring AI ChatClient API", "CoverTitle"), P("Project guide | Spring Boot, Java, Spring AI, OpenAI", "SubCustom")]
story += [P("1. Project at a glance", "H1Custom"),
          P("This is a Java REST API that demonstrates how a Spring Boot application can send a question to an OpenAI chat model through Spring AI's fluent <b>ChatClient</b> API. It has a direct-question endpoint and a second endpoint that builds a request from reusable prompt-template files."),
          make_table([["Item", "Details"], ["Purpose", "Learn and demonstrate Spring AI ChatClient integration"], ["Backend", "Spring Boot 3.5.5, Java 21 target, Maven"], ["AI integration", "Spring AI 1.0.1 OpenAI model starter"], ["Default model", "gpt-4.1 (configurable in application.properties)"], ["Local server", "http://localhost:8081"], ["Attribution", "Based on LearnCodeWithDurgesh spring-ai-yt-series chatclient-api"]], [38*mm, 133*mm]),
          P("Request flow", "H2Custom"),
          code("HTTP request -> ChatController validates input -> ChatService defines the operation\n            -> ChatServiceImpl builds a ChatClient prompt -> Spring AI calls OpenAI\n            -> The model answer is returned as plain text"),
          P("The application separates HTTP handling (controller) from AI request logic (service). Prompt wording for the template-based route is stored in resource files instead of Java code.")]
story += [PageBreak(), P("2. Traditional Spring Initializr structure", "H1Custom"),
          P("There is one source root named <b>src</b>. Standard Spring/Maven layout places application source, resources, and tests beneath it:"),
          code("chatclient-api/\n|-- pom.xml\n|-- mvnw, mvnw.cmd\n|-- .mvn/wrapper/maven-wrapper.properties\n|-- README.md\n|-- src/\n    |-- main/\n    |   |-- java/com/spring/ai/firstproject/\n    |   |   |-- FirstProjectApplication.java\n    |   |   |-- config/AiConfig.java\n    |   |   |-- controllers/ChatController.java\n    |   |   |-- service/ChatService.java\n    |   |   |-- service/ChatServiceImpl.java\n    |   |   |-- entity/Tut.java\n    |   |-- resources/\n    |       |-- application.properties\n    |       |-- prompts/system-message.st\n    |       |-- prompts/user-message.st\n    |-- test/java/com/spring/ai/firstproject/\n        |-- FirstProjectApplicationTests.java"),
          make_table([["File / folder", "Responsibility"], ["FirstProjectApplication.java", "Spring Boot entry point; starts the application context and embedded server."], ["config/AiConfig.java", "Creates the ChatClient bean from Spring AI's auto-configured builder."], ["controllers/ChatController.java", "Maps HTTP routes, validates input, delegates to ChatService, returns responses."], ["service/ChatService.java", "Declares the application's chat operations."], ["service/ChatServiceImpl.java", "Builds direct or template-based prompts and calls ChatClient."], ["resources/prompts/*.st", "Reusable system instructions and user prompt template with a {concept} placeholder."], ["application.properties", "Port, environment-based API key binding, and model configuration."], ["src/test/java/...", "Controller tests using a mocked service; no key or live model call."], ["pom.xml", "Java/Maven settings and Spring Boot, Spring AI, and test dependencies."]], [55*mm, 116*mm]),
          P("Maven creates target/ during builds; it is generated output, not another source folder. IDE views may list individual source roots separately even though the project has one src directory.", "SmallCustom")]
story += [PageBreak(), P("3. Configure, run, and call the API", "H1Custom"),
          P("Prerequisites", "H2Custom"),
          bullet("Java 21 or newer (the Maven compiler targets Java 21)."),
          bullet("An OpenAI API key and network access for model calls."),
          bullet("Maven Wrapper is included; a separate Maven installation is not required."),
          P("Set the key in a terminal environment variable. Do not commit a real key or put it in source files."),
          P("Windows PowerShell", "H2Custom"), code('$env:OPENAI_API_KEY = "your-key"\n.\\mvnw.cmd spring-boot:run'),
          P("macOS / Linux / Git Bash", "H2Custom"), code('export OPENAI_API_KEY="your-key"\n./mvnw spring-boot:run'),
          P("Direct chat endpoint", "H2Custom"), code("GET http://localhost:8081/api/chat?q=Explain%20dependency%20injection"),
          P("The original tutorial path is also supported: <font name='Courier'>/chat?q=...</font>. A blank question returns HTTP 400. Successful responses contain the generated answer as plain text."),
          P("Prompt-template endpoint", "H2Custom"), code("GET http://localhost:8081/api/chat/template?concept=Java%20streams"),
          P("This endpoint combines the system instructions from <font name='Courier'>system-message.st</font> with the user message in <font name='Courier'>user-message.st</font>, substituting the requested concept."),
          P("Key configuration", "H2Custom"), code("spring.application.name=chatclient-api\nserver.port=8081\nspring.ai.openai.api-key=${OPENAI_API_KEY}\nspring.ai.openai.chat.options.model=gpt-4.1"),
          P("Model availability and billing depend on the provider account. Change the model or port through the properties file or Spring configuration overrides.", "SmallCustom")]
story += [PageBreak(), P("4. Tests, limitations, and interview notes", "H1Custom"),
          P("Tests", "H2Custom"), P("Run from the project directory:"),
          code(".\\mvnw.cmd test    # Windows PowerShell\n./mvnw test        # macOS / Linux / Git Bash"),
          P("The controller tests use a mocked ChatService. They verify response behavior, missing input, and blank input without an API key or an external model request. The latest clean test run completed with <b>3 tests, 0 failures</b>."),
          P("What the project demonstrates", "H2Custom"),
          bullet("Spring dependency injection with constructor-injected dependencies."),
          bullet("REST controller/service separation and HTTP input validation."),
          bullet("Spring AI ChatClient prompt construction and synchronous model calls."),
          bullet("Externalized API credentials and reusable classpath prompt templates."),
          bullet("Controller testing without an external API dependency."),
          P("Limitations", "H2Custom"),
          bullet("A real OpenAI response requires a valid key, model access, and internet; provider charges may apply."),
          bullet("Tests cover controller behavior, not a live model call or full application startup with provider credentials."),
          bullet("This is a compact learning example, not a production chat platform: it has no conversation history, authentication, rate limiting, streaming, or UI."),
          P("Interview explanation", "H2Custom"),
          P("“I worked on a Spring Boot REST API that demonstrates using Spring AI's ChatClient to call an OpenAI model. Requests enter through a controller, are delegated to a service, and the service builds a prompt and returns the model's response. There is a direct chat endpoint and a template-based endpoint, with the API key supplied through an environment variable. I also added input validation and controller tests that do not make external API calls.”"),
          P("Be transparent that this project is based on the linked LearnCodeWithDurgesh tutorial. Explain only changes you understand and can demonstrate. Review the original repository's license and attribution terms before redistributing.", "SmallCustom"),
          Spacer(1, 5), P("Source reference", "H2Custom"),
          P("Original: https://github.com/LearnCodeWithDurgesh/spring-ai-yt-series/tree/main/chatclient-api", "SmallCustom")]
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT.resolve())
print(f"{OUT.stat().st_size} bytes")

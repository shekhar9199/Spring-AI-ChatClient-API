package com.spring.ai.firstproject.service;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;

/**
 * Implements the chat use cases using Spring AI's fluent ChatClient API.
 */
@Service
public class ChatServiceImpl implements ChatService {

    private final ChatClient chatClient;

    // Prompt templates live in src/main/resources/prompts and are loaded from the classpath.
    @Value("classpath:/prompts/user-message.st")
    private Resource userMessage;

    @Value("classpath:/prompts/system-message.st")
    private Resource systemMessage;

    public ChatServiceImpl(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    @Override
    public String chat(String query) {
        // The parameter named query is the actual user input; do not substitute template text here.
        return chatClient.prompt()
                .user(query)
                .call()
                .content();
    }

    @Override
    public String chatTemplate(String concept) {
        // The system prompt sets the assistant's behavior; the user prompt supplies the concept.
        return chatClient.prompt()
                .system(system -> system.text(systemMessage))
                .user(user -> user.text(userMessage).param("concept", concept))
                .call()
                .content();
    }
}

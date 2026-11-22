package com.spring.ai.firstproject.config;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Creates the application-wide ChatClient using Spring AI's auto-configured model.
 * Model settings and credentials are supplied through application.properties.
 */
@Configuration
public class AiConfig {

    @Bean
    public ChatClient chatClient(ChatClient.Builder builder) {
        // Configure a useful default for the direct-chat endpoint. Spring AI supplies the
        // model and API credentials through the spring.ai.openai.* properties.
        return builder
                .defaultSystem("You are a helpful programming assistant. Explain clearly and use Java examples when useful.")
                .build();
    }
}

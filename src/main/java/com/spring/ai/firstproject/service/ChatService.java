package com.spring.ai.firstproject.service;

/** Application operations for sending questions to the AI model. */
public interface ChatService {

    /** Sends a coding question to the AI model and returns its answer. */
    String chat(String query);

    /** Sends a question rendered from the prompt templates in resources/prompts. */
    String chatTemplate(String concept);
}

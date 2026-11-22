package com.spring.ai.firstproject.controllers;

import com.spring.ai.firstproject.service.ChatService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/** HTTP API for asking the configured AI model a question. */
@RestController
@RequestMapping
public class ChatController {

    private final ChatService chatService;

    // Constructor injection makes the service dependency explicit and testable.
    public ChatController(ChatService chatService) {
        this.chatService = chatService;
    }

    /**
     * Example: GET /api/chat?q=What%20is%20dependency%20injection
     */
    @GetMapping({"/chat", "/api/chat"})
    public ResponseEntity<String> chat(@RequestParam("q") String question) {
        if (question.isBlank()) {
            return ResponseEntity.badRequest().body("Query parameter 'q' must not be blank.");
        }
        return ResponseEntity.ok(chatService.chat(question));
    }

    /** Example: GET /api/chat/template?concept=Java%20streams */
    @GetMapping({"/chat/template", "/api/chat/template"})
    public ResponseEntity<String> chatTemplate(@RequestParam("concept") String concept) {
        if (concept.isBlank()) {
            return ResponseEntity.badRequest().body("Query parameter 'concept' must not be blank.");
        }
        return ResponseEntity.ok(chatService.chatTemplate(concept));
    }
}

package com.spring.ai.firstproject;

import com.spring.ai.firstproject.controllers.ChatController;
import com.spring.ai.firstproject.service.ChatService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.setup.MockMvcBuilders.standaloneSetup;

/** Controller tests use a mocked service, so they need no OpenAI key or network access. */
class FirstProjectApplicationTests {

    private ChatService chatService;
    private MockMvc mockMvc;

    @BeforeEach
    void setUp() {
        chatService = mock(ChatService.class);
        mockMvc = standaloneSetup(new ChatController(chatService)).build();
    }

    @Test
    void chatEndpointReturnsTheServiceAnswer() throws Exception {
        when(chatService.chat("What is dependency injection?"))
                .thenReturn("It is a design technique for providing dependencies.");

        mockMvc.perform(get("/api/chat").param("q", "What is dependency injection?"))
                .andExpect(status().isOk())
                .andExpect(content().string("It is a design technique for providing dependencies."));

        verify(chatService).chat("What is dependency injection?");
    }

    @Test
    void chatEndpointRequiresAQuestion() throws Exception {
        mockMvc.perform(get("/api/chat"))
                .andExpect(status().isBadRequest());
    }

    @Test
    void chatEndpointRejectsBlankQuestions() throws Exception {
        mockMvc.perform(get("/api/chat").param("q", "   "))
                .andExpect(status().isBadRequest())
                .andExpect(content().string("Query parameter 'q' must not be blank."));
    }
}

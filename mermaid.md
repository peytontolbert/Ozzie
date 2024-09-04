sequenceDiagram
    participant User
    participant VE as VirtualEnvironment
    participant MM as MainMenu
    participant IS as IntroductionScreen
    participant AM as AgentManager
    participant A as Agent
    participant EE as ExperienceEngine
    participant LLM as LLMInterface

    User->>VE: Start application
    VE->>MM: Display main menu
    alt No previous memory
        MM->>IS: Show introduction
        IS->>AM: Create new agent
    else Has previous memory
        MM->>AM: Load existing agent
    end
    AM->>A: Initialize agent
    loop Main interaction loop
        VE->>MM: Display options
        User->>MM: Select option
        MM->>EE: Generate scenario
        EE->>LLM: Process scenario
        LLM-->>EE: Generate response
        EE->>A: Present scenario
        A->>A: Perform action
        A->>EE: Submit action
        EE->>LLM: Evaluate outcome
        LLM-->>EE: Provide feedback
        EE->>A: Update agent (memory, skills, goals)
    end
    VE->>AM: Save agent state
    VE->>User: End session
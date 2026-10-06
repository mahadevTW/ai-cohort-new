# system one vs system to
"THinking fast and slow" book by Danial Kanman

System 1 thinks lot before puthing the answer and explicitly need to mention and expect output in structured format
Jev -> by default has structural model

Faster in latency, 10 times faster than Opus
Lower in cost --> 100 times opus
## it is designed as a different primitive: a model that makes decisions for software rather than generating text for humans. TypeSafe calls this class “System One Models.”

Jev is specifically trained using **Reinforcement Learning for Calibrated Decisions (RLCD)**,


# LLMs generate tokens; Jev evaluates questions

2. Jev has three primitive decision types

Noul --> True false
Choice --> multiple choice
Score --> numeric score 

             ┌── Q1 → probability
State ───────┼── Q2 → probability
             ├── Q3 → probability
             └── Q4 → probability
                      ↓
                 YOUR CODE
                      ↓
              business decision


6. "Structured output" from an LLM is NOT the same thing

    "Why don't I just use GPT/Claude with JSON schema?"
    though output looks structural 
    But the model is still fundamentally a generative model producing tokens.

                    AI APPLICATION
                         │
          ┌──────────────┴──────────────┐
          │                             │
     GENERATIVE AI                 DECISION AI
          │                             │
          ↓                             ↓
   GPT / Claude / etc.                 Jev
          │                             │
   Generate things               Evaluate things
          │                             │
   ┌──────┼──────┐               ┌─────┼─────┐
   │      │      │               │     │     │
 text   code   reasoning       choice score noul
   │      │      │               │     │     │
   └──────┴──────┘               └─────┴─────┘
          │                             │
          ↓                             ↓
     Humans / agents               Software


Use case -> choose best LLM:

                    Incoming request
                           │
                           ↓
                         Jev
                    "What is this?"
                           │
                ┌──────────┴──────────┐
                ↓                     ↓
             simple                 complex
                │                     │
                ↓                     ↓
             code path              LLM
                                      │
                                      ↓
                                  explanation

- Use confidance from the response to decide wether to rely on decision or not



Billing:
1. LLM works based on tokens and its billed around it 
per million for both input and output tokens, output tokens are costly
2. Jev is charged based 42$ per billian tokens
    Output tokens are not charged because it does not work in tranformer based model



1. We are sending all files
    Based on inout question decide If I reallyt need to pass file or not, if not needed dont pass
2. I dont need to pass entire document rather I can pass subset of document to llm
     - How do I decide the subset
     - Ask llm to break document into multiple sub sestions and store them
      - We can also write code to break it down

==================================================
SQL *** --> symantic search

you need database --> which can understand and store the meaning
Way to convert the text into some representation as meaning --> store into Databas

Q1 --> 1,2,3
S1 --> 3456
s2--> 45678

Representation text data in form of meaning is called as embedding


s1
s2
s3
---> store into database in the form of embedding 

Q1 comes
-> convert the q1 into embedding using same embedding model
--> fire quesry to databse saying--> give me all sections which matches the the q1 embedding

--> pass this sections to LLM


for given document
    convert this document into smaller chunks
    for each chunk convert into embeddings
    store this embeddings into database --> Vector databases

Question comes: 

    for q -> convert into embedding
    fire query on db --> return relevent embeddings back, or text back
    pass this sections retrived from datyabse to llm




select * from document_sections where meaning of section is similar to meaning of question top 10





===================================================================================
1. Build way to find relevent information from document and only send the relevent information to LLM
     - . Pass only index of my document to llm and question and ask llm which sections fro this index is importent for this question
     - . s1,s2,s3
     - read only those sections and send it to llm
     - We can further optimize and and do I evenn need to read the document itself


3. current LLM which we are using is trained on public information
    -> Add my enterprise information to this training data
    -> thids is called as fine tuning
4. 
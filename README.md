# **Smart Reader**

## Project Description

    A platform for automatically generating short, descriptive versions of articles with reader engagement analytics.

    Users upload long texts (articles, reports, and essays), the system generates short summaries, and then tracks which sections attract readers' attention through reading heatmaps.

### Read more

    1. Authors upload texts → receive an AI-shortened version (TL;DR)

    2. Readers read the shortened version and can expand the original.

    3. The system tracks reader behavior (scrolling, time spent on sections, clicks).

    4. Authors receive analytics: which topics generate interest, where readers drop off.

### Architecture

    1. Gateway (FastAPI)

        - Single entry point for all requests

        - Authentication via Supabase Auth

        - Load balancing between services

        - Key metrics for Prometheus

    2. Content Service (FastAPI)

        - Receiving and storing original texts in Supabase

        - Generating a unique ID for each document

        - Version management (text editing)

        - Linked files (PDF, DOCX) → Supabase Storage

    3. AI Processor Service (FastAPI)

        - Receiving text from RabbitMQ

        - Using free AI models (e.g., via Hugging Face or Ollama locally)

        Generates:

        - Summary

        - Key tags

        - Key points with timecodes (for audio/video)

        - Sends the result back via RabbitMQ

    4. Analytics Service (FastAPI)

        Collects read events from RabbitMQ:

        - Page scrolling

        - Time spent on each paragraph

        - Expand/collapse clicks

        - Read rate (% of text read)

        - Stores aggregated data in Supabase

        - Generates engagement heatmaps

    5. Notification Service (FastAPI)

        - Sending notifications

        - Uses RabbitMQ templates and queues for delayed sending

### Start

    1. Create a .env file in the root of the project:
        #DB
        DB_SYSTEM=supabase
        DB_TABLE_DOCUMENTS=documents
        DB_TABLE_SUMMARIES=summaries

        #SUPABASE 
        SUPABASE_URL=https://bczgwezulkolmvxxwmjr.supabase.co
        SUPABASE_KEY=sb_publishable_Z4ViRTV8O5HnUaTgSmoMeA_9Y5s6ovz

        #AI
        AI_SYSTEM=groq
        GROQ_KEY= Get you Groq key
        AI_MODEL=llama-3.3-70b-versatile
        AI_TEMPERATURE=0.3
        AI_MAX_TOKENS=256

        # RABBITMQ
        RABBITMQ_HOST=rabbitmq
        RABBITMQ_PORT=5672
        RABBITMQ_USER=guest
        RABBITMQ_PASS=guest

        #SERVICES
        CONTENT_SERVICE_PORT=8000
        AI_SERVICE_PORT=8001

    2. Run Docker
        docker-compose up -d
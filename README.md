# KindoTest Project
## Demo video 
[screen-capture (1).webm](https://github.com/user-attachments/assets/f18205b7-24c5-46b2-96b6-bf8f8ea77d35)


   

## WIKI
   WIKI Page[https://github.com/peterhashair/kindoTest/wiki]

## Getting Started

1. **Copy the example environment file:**

   ```sh
   cp .env.example .env

   ## More Information

   For detailed documentation and advanced usage, see the [project wiki](../../wiki).

   ```

2. **Build and start all services with Docker Compose:**

   ```sh
   docker compose up -d --build
   ```

3. **Access the app:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Notes
- Edit `.env` to change database credentials, backend URL, or CORS settings.
- For local browser access, set `VITE_BACKEND_URL` to `http://localhost:8000` in `.env`.
- For container-to-container access, use `http://backend:8000`.
- To stop all services:

   ```sh
   docker compose down
   ```

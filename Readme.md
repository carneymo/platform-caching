# Platform Caching API

## Overview
The **Platform Caching API** is a unified caching interface that abstracts underlying caching mechanisms like Redis, Garnet, or Dragonfly. It provides a consistent API to interact with different caching backends, allowing developers to swap implementations without modifying their application logic.

## Features
- **Unified API** for multiple caching backends
- **Create, Retrieve, Update, Delete** key-value pairs
- **Supports TTL (Time-To-Live)** for cache expiration
- **Dockerized setup** for easy deployment
- **Swagger UI** for interactive API documentation
- **Postman Collection** included for testing

## Getting Started

### Prerequisites
Ensure you have the following installed:
- Docker
- Docker Compose

### Clone the Repository
```sh
git clone https://github.com/your-repo/platform-caching.git
cd platform-caching
```

### Run the Application
```sh
docker compose up --build
```
This will start the following services:
- **Web (Flask API)** on `http://localhost:5000`
- **Redis (Caching Backend)** on `localhost:6379`
- **Swagger UI** on `http://localhost:8080`

### API Endpoints
| Method  | Endpoint            | Description                |
|---------|---------------------|----------------------------|
| POST    | `/api/cache`        | Create a key-value pair    |
| GET     | `/api/cache/{key}`  | Retrieve a value by key    |
| PUT     | `/api/cache/{key}`  | Update an existing key     |
| DELETE  | `/api/cache/{key}`  | Delete a key from cache    |

### Testing with Postman
1. Open **Postman**.
2. Import the Postman Collection file: `platform-caching.postman_collection.json`.
3. Set the base URL to `http://localhost:5000`.
4. Run the requests to test API functionality.

### Running Unit Tests
Run the following command inside the container to execute unit tests:
```sh
docker exec -it platform-caching-web pytest
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a pull request

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

---

For any issues or suggestions, please open an issue in the repository. 🚀

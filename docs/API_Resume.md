## Endpoints Summary

| Method | Endpoint                   | Description                         | 
| ------ | -------------------------- | ----------------------------------- |
| GET    | `/health`                  | Health check                        | 
| GET    | `/`                        | API information                     | 
| POST   | `/api/pokemon/fetch/:name` | Fetch single Pokemon from PokeAPI   | 
| POST   | `/api/pokemon/fetch/batch` | Fetch multiple Pokemon from PokeAPI | 
| GET    | `/api/pokemon/`            | List all Pokemon                    | 
| GET    | `/api/pokemon/:id`         | Get Pokemon by ID                   |
| GET    | `/api/pokemon/name/:name`  | Get Pokemon by name                 | 

### Health and Information Endpoints

| Endpoint  | Method | Parameters | Request Body | Response                                  | Status Codes |
| --------- | ------ | ---------- | ------------ | ----------------------------------------- | ------------ |
| `/health` | GET    | None       | None         | `{"status": "healthy", "message": "..."}` | 200          |
| `/`       | GET    | None       | None         | API info with available endpoints         | 200          |

### Pokemon Operations

| Endpoint                   | Method | Parameters                | Request Body                  | Response Format                | Status Codes |
| -------------------------- | ------ | ------------------------- | ----------------------------- | ------------------------------ | ------------ |
| `/api/pokemon/fetch/:name` | POST   | `name` (path)             | None                          | Pokemon data with full details | 201, 404     |
| `/api/pokemon/fetch/batch` | POST   | None                      | `{"pokemon": ["name1", ...]}` | Batch results summary          | 200, 400     |
| `/api/pokemon/`            | GET    | `limit` (query, optional) | None                          | Array of Pokemon objects       | 200, 500     |
| `/api/pokemon/:id`         | GET    | `id` (path)               | None                          | Single Pokemon object          | 200, 404     |
| `/api/pokemon/name/:name`  | GET    | `name` (path)             | None                          | Single Pokemon object          | 200, 404     |

## Request Parameters

### Path Parameters

| Parameter | Type    | Description         | Validation                                           |
| --------- | ------- | ------------------- | ---------------------------------------------------- |
| `:name`   | string  | Pokemon name        | 1-50 chars, alphanumeric + hyphens, case-insensitive |
| `:id`     | integer | Pokemon database ID | Positive integer                                     |

### Query Parameters

| Parameter | Type    | Default | Max | Description                         |
| --------- | ------- | ------- | --- | ----------------------------------- |
| `limit`   | integer | 100     | 500 | Maximum number of results to return |

### Request Body Schemas

**Batch Fetch Request:**

```json
{
  "pokemon": ["string", "string", ...]
}
```

**Validation Rules:**

- `pokemon` array required
- Minimum 1 Pokemon
- Maximum 50 Pokemon per request
- Each name must be valid Pokemon name format

## Response Formats

### Success Response

```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response

```json
{
  "success": false,
  "error": "Error message description"
}
```

### Examples

**Health Check:**

```bash
curl http://localhost:5050/health
```

**Fetch Single Pokemon:**

```bash
curl -X POST http://localhost:5050/api/pokemon/fetch/pikachu
```

**Fetch Multiple Pokemon:**

```bash
curl -X POST http://localhost:5050/api/pokemon/fetch/batch \
  -H "Content-Type: application/json" \
  -d '{"pokemon": ["pikachu", "charizard", "bulbasaur"]}'
```

**Get All Pokemon:**

```bash
curl http://localhost:5050/api/pokemon/?limit=10
```

**Get Pokemon by ID:**

```bash
curl http://localhost:5050/api/pokemon/1
```

**Get Pokemon by Name:**

```bash
curl http://localhost:5050/api/pokemon/name/pikachu
```

## Notes

- All endpoints return JSON
- Pokemon names are case-insensitive
- Timestamps are in ISO 8601 format (UTC)
- Duplicate fetch requests return existing Pokemon (idempotent)
- Database operations are atomic (rollback on failure)

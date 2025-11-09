# Contributing to Telegram Bot Dashboard

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/bot-dashboard.git`
3. Install dependencies: `./dashboard.sh install`
4. Create a branch: `git checkout -b feature/your-feature-name`

## Development Workflow

### Backend Development

1. Activate virtual environment:
```bash
cd backend
source venv/bin/activate
```

2. Make your changes in `backend/app/`

3. If you modify models, create a migration:
```bash
./dashboard.sh migrate "description of changes"
```

4. Run tests:
```bash
./dashboard.sh test
```

5. Format code (optional):
```bash
cd backend
source venv/bin/activate
black app/
isort app/
```

### Frontend Development

1. Start dev server:
```bash
./dashboard.sh dev-frontend
```

2. Make your changes in `frontend/src/`

3. Run linter:
```bash
cd frontend
npm run lint
```

4. Build to verify:
```bash
npm run build
```

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use async/await for I/O operations
- Write docstrings for public functions

Example:
```python
async def get_product(db: AsyncSession, product_id: UUID) -> Optional[Product]:
    """
    Retrieve a product by ID.
    
    Args:
        db: Database session
        product_id: UUID of the product
        
    Returns:
        Product if found, None otherwise
    """
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()
```

### TypeScript/React
- Use TypeScript for all new files
- Follow React best practices
- Use functional components with hooks
- Prefer composition over inheritance
- Use meaningful variable names

Example:
```typescript
interface ProductCardProps {
  product: Product
  onDelete: (id: string) => void
}

export function ProductCard({ product, onDelete }: ProductCardProps) {
  // Component logic
}
```

## Testing

### Backend Tests

Location: `backend/tests/`

Run tests:
```bash
./dashboard.sh test
```

Example test:
```python
@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/products", json={
            "name": "Test Bot",
            "contract_months": 6
        })
    assert response.status_code == 201
```

### Frontend Tests

(Add when implemented)

## Commit Messages

Use conventional commits format:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(products): add bulk delete functionality
fix(api): correct pagination offset calculation
docs(readme): update installation instructions
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md (if exists)
5. Create a Pull Request with clear description
6. Link related issues

## Database Migrations

When modifying models:

1. Create migration:
```bash
./dashboard.sh migrate "add field to products table"
```

2. Review generated migration in `backend/alembic/versions/`

3. Test migration:
```bash
./dashboard.sh upgrade
./dashboard.sh downgrade
./dashboard.sh upgrade
```

4. Commit migration file with your changes

## Adding New Dependencies

### Python
1. Add to `backend/requirements.txt`
2. Document reason in PR description
3. Update installation docs if needed

### JavaScript
1. Use `npm install --save package-name`
2. Update `package.json` is automatically updated
3. Document usage in PR description

## Security

- Never commit `.env` files
- Don't hardcode secrets or credentials
- Use environment variables for configuration
- Validate all user inputs
- Use parameterized queries (ORM handles this)
- Keep dependencies updated

## Documentation

Update documentation when:
- Adding new features
- Changing API endpoints
- Modifying configuration options
- Changing deployment process

Files to update:
- `README.md` - Main documentation
- `docs/API.md` - API changes
- `docs/SETUP.md` - Setup/installation changes
- `docs/ARCHITECTURE.md` - Architecture changes

## Questions?

- Open an issue for bugs or feature requests
- Use discussions for questions
- Check existing issues before creating new ones

Thank you for contributing!

# Contributing to ResearchHub AI

Thank you for your interest in contributing to ResearchHub AI! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

1. **Check existing issues** - Search the [issue tracker](https://github.com/yourusername/researchhub/issues) first
2. **Create a detailed report** - Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Screenshots (if applicable)
   - Environment details (OS, Python version, browser)

### Suggesting Features

1. **Check existing feature requests** first
2. **Open a new issue** with:
   - Clear description of the feature
   - Use cases and benefits
   - Potential implementation approach (optional)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow the code style (PEP 8 for Python)
   - Add tests if applicable
   - Update documentation
4. **Commit with clear messages**
   ```bash
   git commit -m "Add: Feature description"
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request**
   - Reference any related issues
   - Describe your changes clearly
   - Include screenshots for UI changes

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/researchhub.git
   cd researchhub
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Set up environment**
   - Copy `.env.example` to `.env`
   - Configure your AI provider (Ollama or OpenAI)

5. **Run tests**
   ```bash
   pytest tests/
   ```

## Code Style

- **Python**: Follow PEP 8 guidelines
- **Line Length**: Max 100 characters
- **Imports**: Group stdlib, third-party, and local imports
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Add type hints where applicable

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update relevant guides in `docs/` folder

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help create a welcoming community

## Questions?

Open an issue or reach out to the maintainers. We're here to help!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

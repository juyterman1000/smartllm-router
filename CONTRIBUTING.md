# 🤝 Contributing to SmartLLM Router

Thank you for your interest in contributing to SmartLLM Router! We're building the future of cost-effective AI, and we'd love your help.

## 🌟 Ways to Contribute

### 🐛 **Bug Reports**
Found a bug? Help us fix it!
- Check [existing issues](https://github.com/yourusername/smartllm-router/issues) first
- Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
- Include reproduction steps and environment details

### 💡 **Feature Requests**
Have an idea for improvement?
- Check [existing discussions](https://github.com/yourusername/smartllm-router/discussions)
- Use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
- Explain the use case and expected behavior

### 📝 **Documentation**
Help others understand SmartLLM Router:
- Fix typos and improve clarity
- Add examples and tutorials
- Translate documentation
- Create video tutorials

### 🔧 **Code Contributions**
Ready to code? Here's how:
- Fix bugs and implement features
- Improve performance and reliability
- Add new model providers
- Enhance testing coverage

## 🚀 Getting Started

### 1. **Fork & Clone**
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/yourusername/smartllm-router.git
cd smartllm-router
```

### 2. **Set Up Development Environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -e ".[dev]"
```

### 3. **Run Tests**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=smartllm_router

# Run specific test file
pytest tests/test_router.py
```

### 4. **Code Quality Checks**
```bash
# Format code
black smartllm_router tests

# Sort imports
isort smartllm_router tests

# Lint code
flake8 smartllm_router

# Type checking
mypy smartllm_router
```

## 📋 Development Guidelines

### **Code Style**
- Follow [PEP 8](https://pep8.org/) Python style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [isort](https://isort.readthedocs.io/) for import sorting
- Maximum line length: 127 characters

### **Testing**
- Write tests for all new features
- Maintain >90% test coverage
- Use descriptive test names
- Include both unit and integration tests

### **Documentation**
- Add docstrings to all public functions/classes
- Update README.md for new features
- Include examples in docstrings
- Keep documentation up-to-date

### **Commit Messages**
Use conventional commit format:
```
type(scope): description

feat(router): add support for new model provider
fix(analyzer): handle edge case in complexity calculation
docs(readme): update installation instructions
test(router): add tests for custom routing rules
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `style`, `chore`

## 🔄 Pull Request Process

### 1. **Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number
```

### 2. **Make Changes**
- Write clean, well-documented code
- Add tests for new functionality
- Update documentation as needed
- Follow code style guidelines

### 3. **Test Your Changes**
```bash
# Run full test suite
pytest

# Check code quality
black --check smartllm_router tests
isort --check-only smartllm_router tests
flake8 smartllm_router
mypy smartllm_router
```

### 4. **Submit Pull Request**
- Use our [PR template](.github/PULL_REQUEST_TEMPLATE.md)
- Link related issues
- Describe changes and motivation
- Include screenshots for UI changes

### 5. **Code Review**
- Address reviewer feedback
- Keep discussions constructive
- Update PR based on suggestions
- Ensure CI passes

## 🏗️ Project Structure

```
smartllm-router/
├── smartllm_router/          # Main package
│   ├── __init__.py
│   ├── router.py            # Core routing logic
│   ├── analyzer.py          # Query analysis
│   ├── selector.py          # Model selection
│   ├── tracker.py           # Cost tracking
│   ├── rules.py             # Routing rules
│   ├── dashboard.py         # Analytics dashboard
│   └── benchmark.py         # Benchmarking tools
├── tests/                   # Test suite
├── examples/                # Usage examples
├── docs/                    # Documentation
├── .github/                 # GitHub templates
└── setup.py                # Package configuration
```

## 🎯 Priority Areas

We're especially looking for help with:

### **High Priority**
- 🔥 **Async Support**: Implement async/await for better performance
- 🌍 **New Providers**: Add support for more LLM providers
- 📊 **Advanced Analytics**: Enhanced monitoring and metrics
- 🔒 **Security**: Improve security and compliance features

### **Medium Priority**
- 🧪 **Testing**: Expand test coverage and add integration tests
- 📚 **Documentation**: More examples and tutorials
- 🎨 **Dashboard**: Improve UI/UX of analytics dashboard
- ⚡ **Performance**: Optimize routing speed and memory usage

### **Good First Issues**
- 📝 Fix typos in documentation
- 🐛 Handle edge cases in query analysis
- 🧹 Code cleanup and refactoring
- 📊 Add new chart types to dashboard

## 🏆 Recognition

Contributors are recognized in several ways:

### **Hall of Fame**
Top contributors are featured in our README and documentation.

### **Contributor Badges**
- 🥇 **Gold**: 10+ merged PRs
- 🥈 **Silver**: 5+ merged PRs
- 🥉 **Bronze**: 1+ merged PR

### **Special Recognition**
- 🌟 **Feature Champion**: Major feature implementation
- 🐛 **Bug Hunter**: Finding and fixing critical bugs
- 📚 **Documentation Hero**: Significant documentation improvements
- 🧪 **Test Master**: Major testing improvements

## 💬 Community

### **Communication Channels**
- 💬 [GitHub Discussions](https://github.com/yourusername/smartllm-router/discussions) - General discussion
- 🐛 [GitHub Issues](https://github.com/yourusername/smartllm-router/issues) - Bug reports and feature requests
- 📧 [Email](mailto:contributors@smartllm-router.com) - Private communication

### **Community Guidelines**
- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow our [Code of Conduct](CODE_OF_CONDUCT.md)

## 📅 Release Process

### **Version Numbering**
We follow [Semantic Versioning](https://semver.org/):
- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backward compatible
- **Patch** (0.0.1): Bug fixes, backward compatible

### **Release Schedule**
- **Major releases**: Quarterly
- **Minor releases**: Monthly
- **Patch releases**: As needed

## 🎉 Getting Help

### **Stuck? We're here to help!**
- 💬 Ask in [Discussions](https://github.com/juyterman1000/smartllm-router/discussions)
- 📧 Email us at [fastunner10090@gmail.com](mailto:fastunner10090@gmail.com)
- 📖 Check our [documentation](docs/)

### **Mentorship Program**
New to open source? We offer mentorship for first-time contributors:
- Pair programming sessions
- Code review guidance
- Career advice and networking

## 🙏 Thank You

Every contribution, no matter how small, makes SmartLLM Router better for everyone. Thank you for being part of our community!

---

**Ready to contribute? [Check out our good first issues](https://github.com/juyterman1000/smartllm-router/labels/good%20first%20issue) to get started!**

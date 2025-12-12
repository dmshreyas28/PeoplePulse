# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in PeoplePulse, please report it responsibly.

### How to Report

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead:

1. Email security concerns to: [your-email@example.com]
2. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- We will acknowledge receipt within 48 hours
- We will provide an initial assessment within 5 business days
- We will work with you to understand and resolve the issue
- We will credit you in the fix (if desired) unless you prefer to remain anonymous

## Security Best Practices

When deploying PeoplePulse:

### Data Privacy

- Never commit real employee PII data to version control
- Use anonymized or synthetic data for development
- Implement proper data access controls
- Follow GDPR, CCPA, and other relevant regulations

### Configuration

- Change default passwords and secrets
- Use strong, unique passwords
- Store secrets in environment variables, not code
- Use HTTPS in production
- Enable database encryption at rest

### Authentication & Authorization

- Implement proper authentication (not included in demo)
- Use role-based access control (RBAC)
- Enforce principle of least privilege
- Implement session management and timeouts

### Network Security

- Use firewalls to restrict access
- Enable CORS only for trusted origins
- Use VPNs for sensitive environments
- Regularly update dependencies

### Model Security

- Validate all input data
- Implement rate limiting on API endpoints
- Monitor for adversarial attacks
- Version control models with MLflow

### Logging & Monitoring

- Log security events
- Monitor for unusual activity
- Set up alerts for security issues
- Regularly review logs

## Dependencies

We regularly update dependencies to patch known vulnerabilities.

To check for vulnerabilities:

```bash
# Python
pip install safety
safety check

# Node.js
npm audit
```

## Supported Versions

Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Disclosure Policy

We follow responsible disclosure:

1. Report received
2. Issue confirmed and assessed
3. Fix developed and tested
4. Fix deployed to supported versions
5. Public disclosure (with credit to reporter)

Thank you for helping keep PeoplePulse secure! 🔒

# Docker Hub Organization Permission Matrix

This document provides an example permission matrix for a Docker Hub organization, showing how different teams should access different types of repositories.

## Team Types

| Team | Description | Typical Members |
|------|-------------|----------------|
| Admins | Organization administrators with full access | DevOps leads, Engineering managers |
| Developers | Development team working on applications | Software engineers, QA engineers |
| Operations | Team responsible for production environments | SRE, Operations engineers |
| Security | Team responsible for security reviews | Security engineers, Compliance |
| CI/CD | Automated build systems | Service accounts for CI/CD systems |
| Contractors | External contractors | Temporary staff, Consultants |

## Repository Types

| Repository Type | Description | Example |
|-----------------|-------------|---------|
| Base Images | Foundation images used by all applications | `base-python`, `base-nodejs` |
| Dev Images | Development versions of applications | `myapp-dev`, `api-service-dev` |
| Staging Images | Pre-production images | `myapp-staging`, `api-service-staging` |
| Production Images | Production-ready images | `myapp-prod`, `api-service-prod` |
| Tool Images | Utility and tooling images | `db-backup`, `log-collector` |
| Third-party Images | Customized versions of external images | `custom-nginx`, `custom-postgres` |

## Permission Matrix

The table below shows the recommended permissions for each team on each repository type:

| Team/Repository | Base Images | Dev Images | Staging Images | Production Images | Tool Images | Third-party Images |
|----------------|-------------|------------|----------------|-------------------|-------------|-------------------|
| Admins | Admin | Admin | Admin | Admin | Admin | Admin |
| Developers | Read | Write | Read | Read | Read | Read |
| Operations | Read | Read | Write | Write | Write | Write |
| Security | Read | Read | Read | Read | Read | Read |
| CI/CD | Write | Write | Write | Write | Read | Write |
| Contractors | No access | Read | No access | No access | No access | No access |

## Permission Levels Explained

- **Admin**: Can push, pull, modify settings, and delete repositories
- **Write**: Can push and pull images
- **Read**: Can only pull images
- **No access**: Cannot access the repository at all

## Special Considerations

### Sensitive Repositories

For repositories containing sensitive configurations or secrets:

| Team/Repository | Sensitive Config Repos |
|----------------|------------------------|
| Admins | Admin |
| Developers | No access |
| Operations | Read |
| Security | Read |
| CI/CD | Read |
| Contractors | No access |

### Implementation Notes

1. **Principle of least privilege**: Always grant the minimum permissions necessary
2. **Regular audits**: Review permissions quarterly
3. **Temporary access**: For contractors, grant and revoke access as needed
4. **Separation of concerns**: Keep dev and prod repositories strictly separated
5. **Break glass procedures**: Document emergency access procedures

## Example API Commands

To implement this permission matrix using the Docker Hub API:

```bash
# Grant admin permissions to admins team for a base image repository
curl -X PUT "https://hub.docker.com/v2/repositories/orgname/base-python/groups/admins" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"permission": "admin"}'

# Grant read permissions to developers team for a production repository
curl -X PUT "https://hub.docker.com/v2/repositories/orgname/myapp-prod/groups/developers" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"permission": "read"}'
```

## Sample Implementation Script

Use the provided `org-structure.sh` script in this directory to implement a basic version of this permission matrix. 
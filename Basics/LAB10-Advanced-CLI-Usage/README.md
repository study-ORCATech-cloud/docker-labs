# LAB10: Advanced Docker CLI Usage

This lab teaches advanced Docker CLI techniques to improve your efficiency and productivity when working with Docker containers and images.

## Lab Overview

In this lab, you will:
- Learn advanced Docker CLI commands and flags
- Master filtering and formatting output
- Understand resource monitoring and management
- Explore Docker CLI plugins and extensions
- Learn Docker CLI automation techniques
- Understand Docker context management

## Important Note

**This lab is designed for hands-on learning:**
- Implement all TODOs in the example directories yourself before checking solutions
- Consult the `solutions.md` file *only after* attempting to solve the problems yourself
- Focus on understanding the principles behind each command
- All code examples in this lab use Python for consistency

## Learning Objectives

- Master advanced Docker CLI filtering and formatting
- Efficiently manage resources using CLI tools
- Create custom Docker CLI plugins
- Implement CLI-based automation
- Configure and use multiple Docker contexts
- Use advanced logging and debugging techniques
- Optimize CLI-based workflows

## Prerequisites

- Docker Engine installed
- Completion of LAB01-LAB09
- Basic understanding of Docker CLI commands
- Basic familiarity with shell scripting
- Basic knowledge of Python (for some examples)

## Lab Projects

This lab includes a series of directories in the `examples` folder, each focusing on a specific aspect of advanced Docker CLI usage.

## Lab Tasks

### Task 1: Advanced Filtering and Formatting

Navigate to the `examples/filtering-formatting` directory:

```bash
cd examples/filtering-formatting
```

TODO:
1. Learn to use advanced filter patterns with `docker ps`, `docker images`, and other commands
2. Master output formatting using `--format` with Go templates
3. Create custom view templates for different commands
4. Implement script to generate formatted reports of your Docker resources
5. Document your preferred formatting templates

### Task 2: Context Management

Navigate to the `examples/context-management` directory:

```bash
cd ../context-management
```

TODO:
1. Create and configure multiple Docker contexts
2. Learn to switch between contexts for different environments
3. Use context-specific commands efficiently
4. Implement a Python script to automate context switching based on conditions
5. Document your context management strategy

### Task 3: Resource Monitoring and Inspection

Navigate to the `examples/resource-monitoring` directory:

```bash
cd ../resource-monitoring
```

TODO:
1. Use advanced `docker stats` commands with custom formatting
2. Implement monitoring scripts for container resource usage
3. Learn to use `docker inspect` effectively with filters and formatting
4. Create a real-time dashboard script for monitoring multiple containers
5. Document insights gained from monitoring resource usage

### Task 4: CLI Plugins and Extensions

Navigate to the `examples/cli-plugins` directory:

```bash
cd ../cli-plugins
```

TODO:
1. Install and use official Docker CLI plugins
2. Understand how Docker CLI plugins work
3. Develop a simple custom Docker CLI plugin
4. Document the functionality of your plugin and installation process
5. Create a plugin that addresses a specific container management need

### Task 5: Event Monitoring and Automation

Navigate to the `examples/events-automation` directory:

```bash
cd ../events-automation
```

TODO:
1. Learn to use `docker events` command with filters
2. Create a script that reacts to specific Docker events
3. Implement event-based automation for common tasks
4. Test your automation with different event triggers
5. Document your event automation patterns

### Task 6: Advanced Image Management

Navigate to the `examples/image-management` directory:

```bash
cd ../image-management
```

TODO:
1. Implement scripts for advanced image cleanup and maintenance
2. Create image inventory management tools
3. Develop automated image update workflows
4. Use CLI commands to analyze image layers and contents
5. Document your image management strategy

### Task 7: Container Orchestration from CLI

Navigate to the `examples/cli-orchestration` directory:

```bash
cd ../cli-orchestration
```

TODO:
1. Implement container dependency management using CLI tools
2. Create scripts for coordinated container deployments
3. Learn advanced restart and recovery options
4. Develop health check monitoring and automated recovery
5. Document your CLI-based orchestration patterns

### Task 8: Security Scanning and Checks

Navigate to the `examples/security-cli` directory:

```bash
cd ../security-cli
```

TODO:
1. Use Docker Scout and other CLI security tools
2. Create automated security scanning workflows
3. Implement baseline security checks before container deployment
4. Generate container security reports using CLI tools
5. Document security scanning process and remediation steps

### Task 9: CLI-Based Backup and Restore

Navigate to the `examples/backup-restore` directory:

```bash
cd ../backup-restore
```

TODO:
1. Implement container state backup scripts
2. Create volume data backup and restore tools
3. Develop container configuration backup strategies
4. Test restore procedures from backups
5. Document your backup and restore workflow

### Task 10: Creating a Complete CLI Workflow

Navigate to the `examples/complete-workflow` directory:

```bash
cd ../complete-workflow
```

TODO:
1. Integrate techniques from previous examples into a comprehensive workflow
2. Create a CLI-based deployment and management system
3. Implement monitoring, alerting, and auto-recovery
4. Develop documentation and usage instructions for your workflow
5. Test and optimize your workflow for efficiency

## Testing Your Understanding

After completing the lab exercises, you should be able to:
- Use advanced filtering and formatting techniques
- Manage multiple Docker contexts efficiently
- Monitor and inspect Docker resources in detail
- Create and use custom Docker CLI plugins
- Implement CLI-based automation for common tasks
- Manage Docker images efficiently
- Orchestrate containers from the CLI
- Perform security scanning using CLI tools
- Backup and restore container environments
- Create comprehensive CLI-based workflows

## Lab Cleanup

Clean up resources created during this lab:

```bash
# Remove containers created during the lab
docker rm -f $(docker ps -aq --filter "name=lab10*")

# Remove images created during the lab
docker rmi $(docker images -q "lab10*")

# Remove volumes created during the lab
docker volume rm $(docker volume ls -q --filter "name=lab10*")

# Remove networks created during the lab
docker network rm $(docker network ls -q --filter "name=lab10*")

# Remove custom Docker contexts
docker context rm dev staging prod
```

## Additional Resources

- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
- [Docker CLI Experimental Features](https://docs.docker.com/engine/reference/commandline/cli/#experimental-features)
- [Docker CLI Plugins](https://docs.docker.com/engine/extend/plugins_authorization/)
- [Go Templates Reference](https://pkg.go.dev/text/template)
- [Docker Events Documentation](https://docs.docker.com/engine/reference/commandline/events/) 
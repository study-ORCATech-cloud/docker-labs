# Docker Labs Repository

A comprehensive collection of hands-on Docker labs for learning containerization, orchestration, and deployment techniques.

## Repository Overview

This repository contains structured labs designed to help you learn Docker and container orchestration through practical, hands-on exercises. The labs progress from basic Docker concepts to more advanced orchestration techniques.

## Repository Structure

```
docker-labs/
│
├── Basics/                  # Fundamental Docker concepts
│   ├── LAB01-GettingStarted/     # Docker installation and basic commands
│   ├── LAB02-BuildingImages/     # Creating custom Docker images
│   └── ...
│
├── Compose/                 # Docker Compose labs
│   ├── LAB01-ServiceCommunication/  # Multi-container applications with communication
│   └── ...
│
├── Swarm/                   # Docker Swarm orchestration
│   ├── LAB01-ClusterDeployment/     # Swarm initialization and services
│   └── ...
│
├── Networking/              # Docker networking concepts
│   ├── LAB01-ContainerNetworking/   # Network types and communication
│   └── ...
│
└── Registry/                # Private registry setup and usage
    └── LAB01-PrivateRegistry/      # Setting up and using a local registry
```

## Getting Started

### Prerequisites

To use these labs, you'll need:

- [Docker](https://docs.docker.com/get-docker/) installed (latest stable version recommended)
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- Basic command-line knowledge
- Text editor of your choice

### How to Use These Labs

1. Clone this repository to your local machine
2. Navigate to the specific lab directory you're interested in
3. Follow the instructions in each lab's README.md file
4. Execute the commands as directed in the lab instructions
5. Complete the TODO exercises to reinforce learning
6. Check solutions in the solutions.md file (if available) only after attempting the exercises

Each lab contains:
- Step-by-step instructions in README.md
- Required Docker configuration files (Dockerfile, docker-compose.yml, etc.)
- Source code for sample applications where needed
- TODO exercises with specific learning objectives
- Solutions to the exercises (check only after attempting yourself)

## Learning Path

The labs follow a natural progression:

1. **Basics**: Docker fundamentals, images, containers, and basic commands
2. **Compose**: Multi-container applications, environment variables, networks
3. **Swarm**: Container orchestration, scaling, service discovery
4. **Networking**: Custom networks, communication between containers, network drivers
5. **Registry**: Setting up and using private Docker registries

## Lab Features

- **Hands-on Exercises**: Each lab provides practical exercises that reinforce theoretical concepts
- **TODO Sections**: Specific tasks for you to implement independently
- **Solutions**: Reference implementations available for verification
- **Real-world Scenarios**: Labs designed to emulate real DevOps workflows

## Contributing

Contributions to this repository are welcome! If you'd like to add new labs or improve existing ones, please follow the standard GitHub workflow:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Acknowledgments

- Docker documentation and community
- Open-source projects used in these examples

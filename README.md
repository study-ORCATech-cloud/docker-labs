# Docker Labs Repository

Welcome to the **Docker Labs** repository — a hands-on, progressive journey into containerization, multi-container orchestration, networking, and registry management using Docker.

This repository is built for learners who want to:
- Understand **containerization fundamentals**
- Develop **real-world multi-container applications**
- Master **Docker Swarm orchestration** and **advanced networking**
- Deploy and manage **private Docker registries**

Each lab is practical, structured, and designed to mirror real DevOps and cloud-native workflows.

---

## 📦 Repository Structure

```bash
docker-labs/
├── Basics/         # Core Docker concepts and skills
├── Compose/        # Multi-container orchestration with Docker Compose
├── Swarm/          # Container orchestration with Docker Swarm
├── Networking/     # Docker networking and service discovery
└── Registry/       # Managing and securing private Docker registries
```

Each track contains 10 progressively challenging labs, each housed in its own folder:

```bash
Basics/LAB01-Getting-Started-With-Docker/
Compose/LAB01-Service-Communication/
Swarm/LAB01-Cluster-Deployment/
Networking/LAB01-Container-Networking-Basics/
Registry/LAB01-Private-Registry-Setup/
...
```

Each lab includes:
- `README.md` with objectives, instructions, validation checklist, and key concepts
- Dockerfiles, Compose files, configuration files, and example applications as needed
- Hands-on **TODO exercises** to reinforce learning

---

## 🛠️ Prerequisites

Before starting these labs, ensure you have:
- [Docker Engine](https://docs.docker.com/get-docker/) installed (latest stable version)
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- Basic command-line knowledge (Linux/Windows/macOS)
- A text editor (VSCode recommended)

Optional:
- Access to multiple VMs for Swarm and Networking labs

---

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/<your-org>/docker-labs.git
cd docker-labs
```

2. Choose a track based on your experience level:

```bash
# Beginners
cd Basics/LAB01-Getting-Started-With-Docker/

# Intermediate
cd Compose/LAB01-Service-Communication/

# Advanced
cd Swarm/LAB01-Cluster-Deployment/
```

3. Follow the instructions in each lab's `README.md`
4. Complete the TODO exercises before checking the provided solutions

---

## 📚 Learning Tracks

| Track | Focus |
|------|-------|
| Basics | Docker fundamentals: images, containers, volumes, best practices |
| Compose | Orchestrating multi-container apps, scaling, resilience |
| Swarm | Cluster deployment, service orchestration, HA design |
| Networking | Networking types, security, service discovery, troubleshooting |
| Registry | Private registries, security, automation, and management |

Labs are designed to simulate real-world DevOps scenarios and progressively build your expertise.

---

## 🌐 Full Lab Roadmap

The full lab list is available in the [ROADMAP.md](./ROADMAP.md) file.

Tracks:
- Docker Basics (10 Labs)
- Docker Compose (10 Labs)
- Docker Swarm (10 Labs)
- Docker Networking (10 Labs)
- Docker Registry (10 Labs)

---

## 🤝 Contributing

We welcome contributions to expand and improve these labs:

1. Fork the repository
2. Create a feature branch (`feature/lab-new-topic`)
3. Add a new lab folder following the existing structure
4. Submit a pull request with clear explanations

---

## 🙏 Acknowledgments

- Docker documentation and community
- Open-source projects used in lab examples
- Contributors who helped design and validate these labs

---

## 🌟 Master Containerization with Confidence

These Docker Labs will help you:
- Automate deployments
- Build resilient cloud-native applications
- Master container networking and security
- Operate private registries and scalable clusters

Happy containerizing! 🐳🚀


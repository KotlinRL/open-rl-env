# Open RL Env

[![Docker Pulls](https://img.shields.io/docker/pulls/kotlinrl/open-rl-gymnasium-grpc-server)](https://hub.docker.com/r/kotlinrl/open-rl-gymnasium-grpc-server)
[![GitHub](https://img.shields.io/badge/source-GitHub-blue?logo=github)](https://github.com/KotlinRL/open-rl-env-bridge)

A cross-platform, production-ready **gRPC server for OpenAI Gymnasium** environments, enabling RL agents in any language (Kotlin, Python, Java, Go, etc) to interact with Gymnasium environments over the network.

- 🚀 **Run Gymnasium envs anywhere—local, cloud, cluster**
- ⚡ **Connect via gRPC—low-latency, strongly-typed**
- 🔁 **Step, reset, close, and stream rendered frames**
- 🐳 **Docker-ready: works out-of-the-box**

---

## ✨ Features

- **Standardized gRPC API** for RL environment interaction (step, reset, action_space/observation_space, render)
- **Supports both discrete and continuous action spaces**
- **Frame streaming endpoint** for visual debugging and agent monitoring
- **Isolated environment instances per client**
- **Deploy anywhere with Docker**

---

## 🚀 Quickstart

### **Run with Docker**

```bash
docker pull kotlinrl/open-rl-gymnasium-grpc-server:latest
docker run --rm -p 50051:50051 kotlinrl/open-rl-gymnasium-grpc-server:latest

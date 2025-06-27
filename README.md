
# 🧩 RL Environment Protocol Buffers (Env.proto)

This repository defines the **universal Protocol Buffers (protobuf) specification for reinforcement learning (RL) environments.**  
Our mission: **Seamless, cross-language, cross-framework interoperability for RL environments, actions, and observations.**

---

## 🚀 **What’s Inside?**

### **Env.proto: Your Gateway to Standardized RL**

- **Spaces**  
  Describe observation and action spaces in a flexible, composable way:
    - Continuous (`BoxSpace`), discrete (`DiscreteSpace`), graph, text, tuple, dictionary, and more.
    - Model any RL environment—from Atari to robotics—with precise constraints.

- **Observations & Actions**  
  Unified representations for all environment I/O:
    - NDArray (multi-dimensional arrays), scalars, strings, tuples, maps—whatever your RL use case needs.
    - Supports both simple and highly-structured data, including multi-agent/multi-modal scenarios.

- **Messages & Services**  
  The `Env` service makes it easy to:
    - Create, reset, and close environments
    - Query action/observation spaces
    - Step the environment and receive rich responses
    - Render or stream frames for visualization

---

## 🌍 **Why Use This Protocol?**

- **Standardizes** RL environment APIs across platforms and frameworks
- **Enables distributed and cloud-based RL**: connect agents and environments over gRPC, from any language (Python, Kotlin, Java, Go, etc.)
- **Perfect for research and production:** plug-and-play with Gymnasium, PettingZoo, Unity, custom envs, and more
- **Facilitates reproducibility and integration** in multi-team, multi-stack environments

---

## 🔗 **How to Use**

- Implement this proto in your environment server or RL agent—generate code for your favorite language using `protoc`.
- Build your RL pipeline or service on top of a strong, forward-compatible foundation.
- Future-proof your research or product by adopting the emerging RL environment standard!

---

## 💡 **Example Use Cases**

- Running RL environments in containers or on the cloud, with agents in any language
- Multi-user or multi-agent research infrastructure
- Sharing environments between frameworks or teams without rewriting glue code

---

## 📄 **See More**

Check out [`Env.proto`](./Env.proto) for the complete specification and detailed message/service docs.

---

**Questions or suggestions? PRs and issues welcome—join us in building a standardized RL future!**

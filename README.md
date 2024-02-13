# Njord's Ledger: Cloud-Native Personal Expense Tracker

## About

Njord's Ledger is a cloud-based personal expense tracking app that helps users track their spending, by making them more financially responsible. Named after the Norse god of the sea, sailors, and wealth.

## Architecture

Njord's Ledger frontend application, hosted on App Engine, provides an interface for managing expenses and visualize your spending through informative dashboards.

Behind the scenes, a backend built on the microservices architecture, consists of three specialized services, each running on Cloud Run for efficient resource utilization: 
- Metadata Service: Stores all your labels, subscriptions, preferences, etc.
- Analytical Service: Stores all your submitted expenses to be tracked.
- Authentication Service: An auxiliary service to label your expenses.

Cloud Monitoring and Logging work complement to provide comprehensive insights into system health and pinpoint root causes of issues. Cloud Monitoring collects and charts key performance metrics, offering real-time visibility into resource utilization, application performance, and overall system health. If anomalies emerge, Cloud Logging captures detailed logs containing specific error messages and timestamps, enabling granular analysis to identify the exact source of the problem.

<img src="./docs/Njords-Ledger-architecture.png" alt="Njord's Ledger Architecture" width="792"/>

A DevOps approach is leverage to streamline application deployment and infrastructure management. Docker automatically builds container images for its backend services, ensuring consistency and portability. Terraform, on the other hand, automates the provisioning and configuration of necessary Google Cloud resources. This integrated solution efficiently deploys services and facilitates infrastructure management, saving time and ensuring consistency.

### Why Cloud Run for microservices?

Given the microservices architecture of our backend, a Kubernetes cluster is an excelent solution for orchestrating all services through deployment manifests, ensuring efficient operation and scalability. However, minimizing infrastructure costs was paramount, this lead us to Cloud Run. Its focus on containerized applications, just like Kubernetes, and its free tier made it the ideal choice for achieving optimal cost-effectiveness in our deployment strategy.

## License

This project is licensed under the AGPL-3.0 License - see [LICENSE](LICENSE) file for details.

# Okta + AWS Federation Governance Diagrams

This folder contains diagrams for the Okta-to-AWS identity federation workflow with drift detection and incident prevention controls.

## Incident & Resolution Diagram

```mermaid
flowchart TD
    subgraph Incident["Wrong Role Mapping Incident (Original)"]
        A1["Engineer maps prod-database-admin role<br/>to dev-app-read Okta group"]
        A2["4 hours of undetected privilege escalation"]
        A3["CloudWatch alert on unusual API calls"]
    end

    subgraph Solution["Governance Solution (Post-Incident)"]
        B1["Role mapping in source-of-truth repo"]
        B2["Peer review gate on all changes"]
        B3["Drift detection Lambda<br/>runs every 15 min"]
        B4["Mismatch detected & alerted<br/>within 15 minutes"]
        B5["Slack alert sent to security team"]
    end

    A1 -->|Before| A2
    A2 --> A3
    A3 -->|4-hour window| Incident

    B1 --> B2
    B2 --> B3
    B3 --> B4
    B4 --> B5

    Incident -->|Lesson learned| Solution
```

## Okta-AWS Federation Architecture

```mermaid
flowchart LR
    subgraph OktaLevel["Okta (Identity Provider)"]
        direction TB
        OG1["Okta Group: platform-dba"]
        OG2["Okta Group: developers"]
        OG3["Okta Group: qa-team"]
    end

    subgraph SourceOfTruth["Source-of-Truth Repo<br/>(GitHub)"]
        direction TB
        SOT1["prod-database-admin<br/>→ platform-dba"]
        SOT2["prod-application-read<br/>→ developers, qa-team"]
        SOT3["Peer review required"]
    end

    subgraph DriftDetection["Drift Detection<br/>(Lambda + CloudWatch)"]
        direction TB
        DD1["Compare Okta mappings<br/>vs Source-of-Truth"]
        DD2["Alert if mismatch"]
    end

    subgraph AWSLevel["AWS IAM Identity Center"]
        direction TB
        AR1["prod-database-admin role"]
        AR2["prod-application-read role"]
    end

    OG1 -->|SCIM sync| AR1
    OG2 -->|SCIM sync| AR2
    OG3 -->|SCIM sync| AR2

    SOT1 -.->|defines| AR1
    SOT2 -.->|defines| AR2

    AR1 -->|queried by| DD1
    AR2 -->|queried by| DD1
    SOT1 -->|compared to| DD1
    SOT2 -->|compared to| DD1

    DD1 --> DD2
```

Use these diagrams to show the incident scenario and the layered controls that prevent privilege escalation through role misassignment.


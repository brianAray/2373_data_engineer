# Week 6 Notes

## DataOps lifecycle and key practices (collaboration, automation, monitoring)

- **Collaboration :** * **Practice:** Every change to a data model or orchestration DAG starts with a Pull Request (PR).
    - **Example:** A data analyst wants to change how "Active Users" is calculated. Instead of editing a script on a server, they create a Git branch, update the SQL, and another analyst reviews the logic before it ever touches production.
- **Automation:**
    - **Practice:** Automated triggers removes human errors.
    - **Example:** When code is merged into the `main` branch, a GitHub Action automatically pushes the new dbt models to the Snowflake/Databricks environment.
- **Monitoring & Observability:**
    - **Infrastructure Monitoring:** Tools like Datadog or CloudWatch alert you if the Airflow worker is out of memory.
    - **Data Observability:** Tools like Monte Carlo or Elementary alert you if a table that usually receives 1M rows only got 100 rows today (a "volume anomaly").

## CI/CD pipelines for dbt and Airflow

| **Tool** | **CI (Continuous Integration)** | **CD (Continuous Deployment)** |
| --- | --- | --- |
| **dbt** | **Slim CI:** Only runs and tests the models that were modified in the PR. This saves compute costs and time. | **Production Deployment:** Deploys the manifest to a production environment and refreshes the auto-generated documentation site. |
| **Airflow** | **Pytest & DAG Integrity:** Runs scripts to ensure all DAGs are importable and that there are no "cycles" (A depends on B, which depends on A). | **Image/S3 Sync:** Automatically syncs the `.py` DAG files to the production folder or builds a new Docker image for the Kubernetes executor. |

## Automated testing in data workflows

Data quality is measured through four primary dimensions:

- **Accuracy:** Does the data reflect reality? (e.g., Is a birthdate in 2099?)
- **Completeness:** Are there missing values or dropped rows in the pipeline?
- **Timeliness:** Is the data fresh enough for the business use case? (SLA vs. SLO).
- **Consistency:** Does the "Revenue" column in the Finance table match "Revenue" in the Sales table?

## Dimensions of data quality: accuracy, completeness, timeliness, consistency

- **Accuracy:** Does it match the source?
    - *Example:* If the source CRM says a deal is for **$10,000**, but the warehouse says **$1,000**, the accuracy is compromised.
- **Completeness:** Are there "holes" in the dataset?
    - *Example:* A mandatory `email_address` field that is **40% null** is an incomplete dataset for a marketing campaign.
- **Timeliness (SLA/SLO):** Is it fresh?
    - *Example:* A dashboard for "Real-time Fraud" is useless if the data is **24 hours old**.
- **Consistency:** Do different tables agree?
    - *Example:* The `total_revenue` in the Executive Dashboard should match the `sum(revenue)` in the Transactions table.

## Writing test cases for raw and transformed data

### Raw Data (Source Alignment)

- **Unique/Primary Key Checks:** Ensure no duplicate records were sent by a buggy API.
- **Type Validation:** Did a field that used to be a `numeric` price suddenly arrive as a `string` containing "N/A"?
- **Accepted Values:** Checking if a `status` column only contains "Shipped," "Pending," or "Cancelled."

### Transformed Data (Logic Validation)

- **Relationship Tests:** Ensuring every `transaction_record` has a corresponding `customer_id` in the master table.
- **Financial Sanity:** Total tax should never be greater than the total order amount.
- **Regression Testing:** Comparing the results of a new version of a model against the old version to see if any totals changed unexpectedly.

## Data lineage types: technical vs business lineage

Lineage tells you where data came from and who it affects if it breaks.

- **Technical Lineage:** The "Guts." It tracks column-level transformations, SQL joins, and physical file paths. Used by engineers for **impact analysis** (e.g., "If I rename this column, which 10 downstream tables will break?").
    - *Focus:* Tables, Views, Python scripts, and SQL joins.
    - *Use Case:* "If I delete this `staging_orders` table, which downstream reports will break?"
- **Business Lineage:** The "Context." It maps technical assets to business terms (e.g., "This Snowflake table represents 'Active Subscribers' as defined by the 2024 Marketing Charter"). Used by stakeholders for **trust and discovery**.
    - *Focus:* Business concepts and KPIs.
    - *Use Case:* "How is 'Churn Rate' calculated, and which departments own the inputs for it?"

## Data governance pillars: ownership, security, cataloging, quality

Data Governance is the framework that ensures data is a controlled asset, not a liability.

### The Four Pillars

1. **Ownership:** Every table must have a "Data Steward" (the person who understands the data) and a "Data Owner" (the person accountable for it).
2. **Security:** Implementing **Role-Based Access Control (RBAC)**. Instead of granting access to "Bob," you grant access to the "Junior Analyst" role, which Bob inherits.
3. **Cataloging:** A searchable inventory (like Atlan, Amundsen, or Unity Catalog) so users can find data without asking in Slack.
4. **Quality:** The ongoing monitoring of the dimensions mentioned above.

## Role-based access control (RBAC) in data warehouses

Instead of giving permissions to individuals, you give them to "Roles." This makes scaling a team much easier.

![image.png](attachment:a4a8b212-6804-4f4d-9b55-b0a91daf8afd:image.png)

**Hierarchy Example:**

- **Admin:** Full control (Create/Delete databases).
- **Data Engineer:** Read/Write to Raw and Transformed schemas; can manage pipelines.
- **Data Analyst:** Read-only access to Transformed schemas; can create temporary tables in a "Sandbox."
- **Business User:** Access only to the final BI tool (Tableau/PowerBI), no direct SQL access.

## PII handling and masking

Personally Identifiable Information (PII) must be protected to prevent legal disasters.

- **Dynamic Masking:** The data remains unencrypted in the disk, but the database hides it based on who is looking.
    - *Example:* An HR manager sees `Social Security: 123-456-7890`, but a Data Analyst sees `Social Security: XXX-XX-XXXX`.
- **Hashing (SHA-256):** Turning a name into a unique string of characters.
    - *Example:* `John Doe` becomes `e3b0c44298fc...`. You can still count unique users, but you don't know who they are.
- **Tokenization:** Replacing sensitive data with a randomly generated "token" that can only be reversed using a highly secure "vault."

## Compliance standards: GDPR, HIPAA, SOC 2

- **GDPR (General Data Protection Regulation):**
    - **Key Focus:** Privacy for EU citizens.
    - **Requirement:** "The Right to be Forgotten." You must have a process to delete a user's data from all your backups and tables within 30 days if they ask.
- **HIPAA (Health Insurance Portability and Accountability Act):**
    - **Key Focus:** US Healthcare data.
    - **Requirement:** Any data containing Protected Health Information (PHI) must be encrypted at rest and in transit, with strict audit logs of who accessed it.
- **SOC 2 (System and Organization Controls):**
    - **Key Focus:** Service providers handling customer data.
    - **Requirement:** An audit that proves your company follows five "trust service principles": Security, Availability, Processing Integrity, Confidentiality, and Privacy.

## Data stewardship roles and responsibilities

The Steward is the "Librarian" of the data world.

- **Defining Metadata:** They write the definitions for every column so a new hire doesn't have to guess what `attr_1_val` means.
- **Data Quality Advocacy:** If a quality test fails, the Steward decides if the data is "good enough" to release or if the pipeline should be shut down.
- **Access Gatekeeping:** They review and approve who gets access to specific "High-Risk" datasets (like financial records or PII).

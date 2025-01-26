# README: SQL Server Ingestor for Warehouse Data

This repository contains a Python-based ingestor designed to load CSV files into a SQL Server database, simulating a data warehouse environment. All CSVs were generated using [Mockaroo](https://mockaroo.com/) to ensure realistic and diverse sample data.

---

## Schema Overview
The ingestor loads data into the following schema, modeled as a data warehouse:

![Database Schema](![image](https://github.com/user-attachments/assets/0f023a91-8934-4fa2-a125-ad4dfe3874f7))

The schema includes the following tables:

### Level 1: Core Dimension Tables
- **SUCURSALES**: Branch information.
- **PROVEEDORES**: Supplier details.
- **CATALOGO_GASTOS**: Expense categories.
- **TURNO**: Work shifts.
- **ESTATUS**: Employee statuses.
- **PUESTO**: Job positions.

### Level 2: Transaction and Fact Tables
- **PRODUCTOS**: Product catalog.
- **COMPRAS**: Purchases.
- **GASTOS**: Expenses.
- **CAJAS**: Cash registers.
- **EMPLEADOS**: Employee details.

### Level 3: Derived Fact Tables
- **COMPRA_POR_PRODUCTO**: Product-specific purchase details.
- **ALMACEN_POR_SUCURSAL**: Inventory per branch.
- **TICKETS**: Sales tickets.

### Level 4: Ticket Details
- **TICKETS_DETALLE**: Line-item details for tickets.

---

## Python Script Functionality
The `ingestor.py` script automates the process of importing CSV files into the database. It reads the files, detects their encoding, and inserts the data into corresponding tables in the SQL Server database.

### Key Features
- **Encoding Detection**: Uses the `chardet` library to avoid encoding issues during file reading.
- **Dynamic Ingestion**: Automatically maps CSV files to database tables.
- **SQLAlchemy Integration**: Leverages SQLAlchemy for seamless database interaction.

### Script Logic
1. The script loops through table levels (`tablelperlevel`) to maintain loading order and enforce referential integrity.
2. Each CSV file is read into a Pandas DataFrame with the correct encoding.
3. Data is appended to the corresponding SQL Server table using SQLAlchemy's `to_sql` method.

---

## Setting Up the Warehouse

### Prerequisites
- **Python 3.8+**
- **SQL Server** with `ODBC Driver 17 for SQL Server`
- Python libraries:
  - `pandas`
  - `pyodbc`
  - `sqlalchemy`
  - `chardet`

### Configuration
1. Clone the repository and navigate to the project directory.
2. Place all CSV files in the `csvs/` folder.
3. Modify the following variables in the script if necessary:
   ```python
   server = platform.node()  # Adjust to your SQL Server instance
   database = 'Upysusa'  # Replace with your database name
   driver = 'ODBC Driver 17 for SQL Server'  # Ensure the driver is installed
   ```

### Running the Script
Run the following command to execute the ingestion:
```bash
python ingestor.py
```
The script will:
- Read each CSV file in the `csvs/` folder.
- Detect its encoding and load the data into the corresponding table.
- Maintain order to preserve relationships and dependencies.

---

## Querying the Warehouse
Once the data is loaded, the warehouse supports analytical queries such as:

### Example Queries
1. **Total Sales by Branch**:
   ```sql
   SELECT b.name AS branch_name, SUM(t.total_sale) AS total_sales
   FROM TICKETS t
   JOIN SUCURSALES b ON t.id_branch = b.id
   GROUP BY b.name;
   ```

2. **Top 5 Selling Products**:
   ```sql
   SELECT p.name AS product_name, SUM(td.quantity) AS total_quantity
   FROM TICKETS_DETALLE td
   JOIN PRODUCTOS p ON td.id_product = p.id
   GROUP BY p.name
   ORDER BY total_quantity DESC
   LIMIT 5;
   ```

3. **Monthly Expense Report**:
   ```sql
   SELECT FORMAT(g.date, 'yyyy-MM') AS month, SUM(g.cost) AS total_expense
   FROM GASTOS g
   GROUP BY FORMAT(g.date, 'yyyy-MM')
   ORDER BY month;
   ```

4. **Employee Salaries by Branch**:
   ```sql
   SELECT s.name AS branch_name, SUM(e.salary) AS total_salaries
   FROM EMPLEADOS e
   JOIN SUCURSALES s ON e.id_branch = s.id
   GROUP BY s.name;
   ```

5. **Inventory Status per Branch**:
   ```sql
   SELECT b.name AS branch_name, p.name AS product_name, a.stock_quantity
   FROM ALMACEN_POR_SUCURSAL a
   JOIN SUCURSALES b ON a.id_branch = b.id
   JOIN PRODUCTOS p ON a.id_product = p.id;
   ```

---

## Notes
- Ensure that all CSVs match the database schema to prevent data ingestion errors.
- Modify the query examples as needed to fit specific analytical requirements.

---

## Future Work
- Automate error handling and logging for failed ingestions.
- Extend support for incremental data updates.
- Add visualization tools for reporting.

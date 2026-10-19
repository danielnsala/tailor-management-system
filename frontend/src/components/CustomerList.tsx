
import { useState } from "react";
import type { Customer } from "../api/customers";

type CustomerListProps = {
  customers: Customer[];
  onEdit: (customer: Customer) => void;
  onDelete: (customer: Customer) => void;
  deletingCustomerId: number | null;
};

function CustomerList({
  customers,
  onEdit,
  onDelete,
  deletingCustomerId
}: CustomerListProps) {
  const [search, setSearch] = useState("");

  const filteredCustomers = customers.filter((customer) => {
    const searchText = search.toLowerCase().trim();

    return (
      `${customer.first_name} ${customer.last_name}`
        .toLowerCase()
        .includes(searchText) ||
      customer.phone.includes(searchText) ||
      (customer.email ?? "")
        .toLowerCase()
        .includes(searchText)
    );
  });

  return (
    <section className="customer-list">
      <h2>Customers</h2>

      <input
        type="search"
        placeholder="Search by name, phone, or email"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
      />

      <p>
        Showing {filteredCustomers.length} of {customers.length} customers
      </p>

      {filteredCustomers.length === 0 && (
        <p>No matching customers found.</p>
      )}

      {filteredCustomers.map((customer) => (
        <div className="customer-item" key={customer.id}>
          <div>
            <strong>
              {customer.first_name} {customer.last_name}
            </strong>
            <p>{customer.phone}</p>
            {customer.email && <p>{customer.email}</p>}
          </div>

          <div className="customer-actions">
            <button
              type="button"
              onClick={() => onEdit(customer)}
            >
              Edit
            </button>

            <button
              type="button"
              disabled={deletingCustomerId !== null}
              onClick={() => onDelete(customer)}
            >
                {deletingCustomerId === customer.id ? "Deleting..." : "Delete"}
            </button>
          </div>
        </div>
      ))}
    </section>
  );
}

export default CustomerList;

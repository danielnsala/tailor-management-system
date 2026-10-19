
import { useEffect, useState } from "react";
import StatCard from "./components/StatCard";
import CustomerForm from "./components/CustomerForm";
import LoginForm from "./components/LoginForm";
import { getCustomers } from "./api/customers";
import type { Customer } from "./api/customers";
import CustomerList from "./components/CustomerList";
import EditCustomerForm from "./components/EditCustomerForm";
import { deleteCustomer } from "./api/customers";
import "./App.css";


function App() {
  const [token, setToken] = useState<string | null>(null);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loadingCustomers, setLoadingCustomers] = useState(false);
  const [customerError, setCustomerError] = useState("");
  const [editingCustomer, setEditingCustomer] = useState<Customer | null>(null);
  const [deletingCustomerId, setDeletingCustomerId] =
  useState<number | null>(null);
  const [deleteError, setDeleteError] = useState("");

  useEffect(() => {
    if (!token) return;

    let cancelled = false;

    async function loadCustomers() {
      setLoadingCustomers(true);
      setCustomerError("");

      try {
        const data = await getCustomers(token!);

        if (!cancelled) {
          setCustomers(data);
        }
      } catch (err) {
        if (!cancelled) {
          setCustomerError(
            err instanceof Error ? err.message : "Unable to load customers."
          );
        }
      } finally {
        if (!cancelled) {
          setLoadingCustomers(false);
        }
      }
    }

    loadCustomers();

    return () => {
      cancelled = true;
    };
  }, [token]);

  function handleLogout() {
    setToken(null);
    setCustomers([]);
    setCustomerError("");
    setEditingCustomer(null);
    setDeletingCustomerId(null);
    setDeleteError("");
  }

  if (!token) {
    return (
      <main className="dashboard">
        <h1>Tailor Management System</h1>
        <LoginForm onLogin={setToken} />
      </main>
    );
  }

  return (
    <main className="dashboard">
      <h1>Tailor Management System</h1>
      <p>Welcome to your business dashboard!</p>

      <button onClick={handleLogout}>Logout</button>

      <section className="stats-grid">
        <StatCard title="Total Customers" value={customers.length} />
        <StatCard title="Active Orders" value={8} />
        <StatCard title="Pending Jobs" value={5} />
        <StatCard title="Completed Jobs" value={16} />
      </section>

      {loadingCustomers && <p>Loading customers...</p>}
      {customerError && <p role="alert">{customerError}</p>}

      <CustomerForm
        token={token}
        onCustomerCreated={(newCustomer) => {
          setCustomers((previous) => [...previous, newCustomer]);
        }}
      />

      <CustomerList
        customers={customers}
        onEdit={(customer) => { setEditingCustomer(customer); } }
        onDelete={handleDeleteCustomer} deletingCustomerId={null}      
      />
      
      {deleteError && <p role="alert">{deleteError}</p>}

      {editingCustomer && (
        <EditCustomerForm
          key={editingCustomer.id}
          customer={editingCustomer}
          token={token}
          onUpdated={(updatedCustomer) => {
            setCustomers((previous) =>
              previous.map((customer) =>
                customer.id === updatedCustomer.id
                  ? updatedCustomer
                  : customer
              )
            );

            setEditingCustomer(null);
          }}
          onCancel={() => setEditingCustomer(null)}
        />
      )}
    </main>
  );

  
async function handleDeleteCustomer(customer: Customer) {
  if (deletingCustomerId !== null) return;

  const confirmed = window.confirm(
    `Are you sure you want to delete ${customer.first_name} ${customer.last_name}?`
  );

  if (!confirmed || !token) return;

  setDeletingCustomerId(customer.id);
  setDeleteError("");

  try {
    await deleteCustomer(customer.id, token);

    setCustomers((previous) =>
      previous.filter((item) => item.id !== customer.id)
    );

    setEditingCustomer((previous) =>
      previous?.id === customer.id ? null : previous
    );
  } catch (err) {
    setDeleteError(
      err instanceof Error ? err.message : "Deletion failed."
    );
  } finally {
    setDeletingCustomerId(null);
  }
}

}

export default App;

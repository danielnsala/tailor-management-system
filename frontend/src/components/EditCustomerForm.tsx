
import { useState } from "react";
import type { FormEvent } from "react";
import { updateCustomer } from "../api/customers";
import type { Customer } from "../api/customers";

type EditCustomerFormProps = {
  customer: Customer;
  token: string;
  onUpdated: (customer: Customer) => void;
  onCancel: () => void;
};

function EditCustomerForm({
  customer,
  token,
  onUpdated,
  onCancel,
}: EditCustomerFormProps) {
  const [formData, setFormData] = useState({
    first_name: customer.first_name,
    last_name: customer.last_name,
    phone: customer.phone,
    email: customer.email ?? "",
    notes: customer.notes ?? "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (loading) return;

    setLoading(true);
    setError("");

    try {
      const updated = await updateCustomer(
        customer.id,
        {
          ...formData,
          email: formData.email.trim() || null,
          notes: formData.notes.trim() || null,
        },
        token
      );

      onUpdated(updated);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Update failed."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="edit-customer-form">
      <h2>Edit Customer</h2>

      <label>
        First name
        <input
          required
          value={formData.first_name}
          onChange={(e) =>
            setFormData({ ...formData, first_name: e.target.value })
          }
        />
      </label>

      <label>
        Last name
        <input
          required
          value={formData.last_name}
          onChange={(e) =>
            setFormData({ ...formData, last_name: e.target.value })
          }
        />
      </label>

      <label>
        Phone
        <input
          type="tel"
          required
          value={formData.phone}
          onChange={(e) =>
            setFormData({ ...formData, phone: e.target.value })
          }
        />
      </label>

      <label>
        Email
        <input
          type="email"
          value={formData.email}
          onChange={(e) =>
            setFormData({ ...formData, email: e.target.value })
          }
        />
      </label>

      <label>
        Notes
        <textarea
          value={formData.notes}
          onChange={(e) =>
            setFormData({ ...formData, notes: e.target.value })
          }
        />
      </label>

      {error && <p role="alert">{error}</p>}

      <button type="submit" disabled={loading}>
        {loading ? "Saving..." : "Save Changes"}
      </button>

      <button type="button" onClick={onCancel} disabled={loading}>
        Cancel
      </button>
    </form>
  );
}

export default EditCustomerForm;

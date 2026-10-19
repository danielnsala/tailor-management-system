
import { useState } from "react";
import type { FormEvent } from "react";
import { createCustomer } from "../api/customers";
import type { Customer } from "../api/customers";

type CustomerFormProps = {
  token: string;
  onCustomerCreated: (customer: Customer) => void;
};

type FormData = {
  first_name: string;
  last_name: string;
  phone: string;
  email: string;
  notes: string;
};

const emptyForm: FormData = {
  first_name: "",
  last_name: "",
  phone: "",
  email: "",
  notes: "",
};

function CustomerForm({
  token,
  onCustomerCreated,
}: CustomerFormProps) {
  const [formData, setFormData] = useState<FormData>(emptyForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (loading) return;

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const newCustomer = await createCustomer(
        {
          first_name: formData.first_name.trim(),
          last_name: formData.last_name.trim(),
          phone: formData.phone.trim(),
          email: formData.email.trim() || null,
          notes: formData.notes.trim() || null,
        },
        token
      );

      onCustomerCreated(newCustomer);
      setSuccess("Customer created successfully!");
      setFormData({ ...emptyForm });
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add New Customer</h2>

      <input
        type="text"
        placeholder="First name"
        required
        value={formData.first_name}
        onChange={(e) =>
          setFormData({ ...formData, first_name: e.target.value })
        }
      />

      <input
        type="text"
        placeholder="Last name"
        required
        value={formData.last_name}
        onChange={(e) =>
          setFormData({ ...formData, last_name: e.target.value })
        }
      />

      <input
        type="tel"
        placeholder="Phone number"
        required
        value={formData.phone}
        onChange={(e) =>
          setFormData({ ...formData, phone: e.target.value })
        }
      />

      <input
        type="email"
        placeholder="Email (optional)"
        value={formData.email}
        onChange={(e) =>
          setFormData({ ...formData, email: e.target.value })
        }
      />

      <textarea
        placeholder="Additional notes (optional)"
        value={formData.notes}
        onChange={(e) =>
          setFormData({ ...formData, notes: e.target.value })
        }
      />

      {error && <p role="alert">{error}</p>}
      {success && <p role="status">{success}</p>}

      <button type="submit" disabled={loading}>
        {loading ? "Saving..." : "Save Customer"}
      </button>
    </form>
  );
}

export default CustomerForm;

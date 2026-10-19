
const API_BASE_URL = "http://127.0.0.1:8000";

export type CustomerCreate = {
  first_name: string;
  last_name: string;
  phone: string;
  email: string | null;
  notes: string | null;
};

export type Customer = CustomerCreate & {
  id: number;
  created_at: string;
};

export async function createCustomer(
  customer: CustomerCreate,
  token: string
): Promise<Customer> {
  const response = await fetch(`${API_BASE_URL}/customers/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(customer),
  });

  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      throw new Error("Your session is invalid or you lack permission.");
    }

    const error = await response.json().catch(() => null);

    throw new Error(
      typeof error?.detail === "string"
        ? error.detail
        : "Failed to create customer."
    );
  }

  return response.json();
}


export async function getCustomers(
  token: string
): Promise<Customer[]> {
  const response = await fetch(`${API_BASE_URL}/customers/`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(
      response.status === 401 || response.status === 403
        ? "Your session is invalid or you lack permission."
        : "Failed to load customers."
    );
  }

  return response.json();
}


export async function updateCustomer(
  customerId: number,
  updates: Partial<CustomerCreate>,
  token: string
): Promise<Customer> {
  const response = await fetch(
    `${API_BASE_URL}/customers/${customerId}`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(updates),
    }
  );

  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      throw new Error("Session expired or access denied.");
    }

    if (response.status === 404) {
      throw new Error("Customer not found.");
    }

    throw new Error("Failed to update customer.");
  }

  return response.json();
}


export async function deleteCustomer(
  customerId: number,
  token: string
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/customers/${customerId}`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    if (response.status === 409) {
      throw new Error(
        typeof error?.detail === "string"
          ? error.detail
          : "This customer has related business records."
      );
    }

    if (response.status === 401 || response.status === 403) {
      throw new Error("Session expired or access denied.");
    }

    if (response.status === 404) {
      throw new Error("Customer not found.");
    }

    throw new Error("Failed to delete customer.");
  }
}



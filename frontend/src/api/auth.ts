
const API_BASE_URL = "http://127.0.0.1:8000";

export type LoginCredentials = {
  email: string;
  password: string;
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
};

export async function loginAdmin(
  credentials: LoginCredentials
): Promise<TokenResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    throw new Error(
      response.status === 401
        ? "Invalid email or password"
        : "Unable to log in. Please try again."
    );
  }

  return response.json();
}

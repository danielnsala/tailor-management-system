
const API_BASE_URL = "http://127.0.0.1:8000";

export type MeasurementUnit = "INCHES" | "CENTIMETERS";

export type Measurement = {
  id: number;
  measurement_type: string;
  value: string;
};

export type MeasurementSet = {
  id: number;
  customer_id: number;
  date_taken: string;
  unit: MeasurementUnit;
  notes: string | null;
  measurements: Measurement[];
};

export type MeasurementSetCreate = {
  date_taken: string;
  unit: MeasurementUnit;
  notes: string | null;
  measurements: {
    measurement_type: string;
    value: string;
  }[];
};

function measurementSetsUrl(customerId: number) {
  return `${API_BASE_URL}/customers/${customerId}/measurement-sets`;
}

async function readApiError(response: Response): Promise<Error> {
  const data = await response.json().catch(() => null);

  if (response.status === 401 || response.status === 403) {
    return new Error("Session expired or access denied.");
  }

  if (typeof data?.detail === "string") {
    return new Error(data.detail);
  }

  return new Error(`Request failed (${response.status}).`);
}

export async function getMeasurementSets(
  customerId: number,
  token: string
): Promise<MeasurementSet[]> {
  const response = await fetch(
    `${measurementSetsUrl(customerId)}/`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw await readApiError(response);
  }

  return response.json();
}

export async function createMeasurementSet(
  customerId: number,
  data: MeasurementSetCreate,
  token: string
): Promise<MeasurementSet> {
  const response = await fetch(
    `${measurementSetsUrl(customerId)}/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw await readApiError(response);
  }

  return response.json();
}

export async function updateMeasurement(
  customerId: number,
  setId: number,
  measurementId: number,
  updates: {
    measurement_type?: string;
    value?: string;
  },
  token: string
): Promise<Measurement> {
  const response = await fetch(
    `${measurementSetsUrl(customerId)}/${setId}/measurements/${measurementId}`,
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
    throw await readApiError(response);
  }

  return response.json();
}

export async function deleteMeasurement(
  customerId: number,
  setId: number,
  measurementId: number,
  token: string
): Promise<void> {
  const response = await fetch(
    `${measurementSetsUrl(customerId)}/${setId}/measurements/${measurementId}`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw await readApiError(response);
  }
}

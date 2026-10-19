
import { useState } from "react";
import type { FormEvent } from "react";

import {
  updateMeasurement,
  deleteMeasurement,
} from "../api/measurements";

import type { Measurement } from "../api/measurements";

type MeasurementItemProps = {
  measurement: Measurement;
  customerId: number;
  setId: number;
  unit: string;
  token: string;
  onUpdated: (measurement: Measurement) => void;
  onDeleted: (measurementId: number) => void;
};

function MeasurementItem({
  measurement,
  customerId,
  setId,
  unit,
  token,
  onUpdated,
  onDeleted,
}: MeasurementItemProps) {
  const [editing, setEditing] = useState(false);

  const [measurementType, setMeasurementType] = useState(
    measurement.measurement_type
  );

  const [value, setValue] = useState(measurement.value);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function cancelEditing() {
    setMeasurementType(measurement.measurement_type);
    setValue(measurement.value);
    setError("");
    setEditing(false);
  }

  async function handleUpdate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (loading) return;

    if (!measurementType.trim()) {
      setError("Measurement name cannot be empty.");
      return;
    }

    if (
      !value.trim() ||
      !Number.isFinite(Number(value)) ||
      Number(value) <= 0
    ) {
      setError("Measurement value must be positive.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const updated = await updateMeasurement(
        customerId,
        setId,
        measurement.id,
        {
          measurement_type: measurementType.trim(),
          value: value.trim(),
        },
        token
      );

      onUpdated(updated);
      setEditing(false);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Update failed."
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete() {
    if (loading) return;

    const confirmed = window.confirm(
      `Delete the ${measurement.measurement_type} measurement?`
    );

    if (!confirmed) return;

    setLoading(true);
    setError("");

    try {
      await deleteMeasurement(
        customerId,
        setId,
        measurement.id,
        token
      );

      onDeleted(measurement.id);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Deletion failed."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="measurement-item">
      {editing ? (
        <form onSubmit={handleUpdate}>
          <input
            type="text"
            value={measurementType}
            onChange={(event) =>
              setMeasurementType(event.target.value)
            }
            required
          />

          <input
            type="number"
            min="0.01"
            step="0.01"
            value={value}
            onChange={(event) =>
              setValue(event.target.value)
            }
            required
          />

          <button type="submit" disabled={loading}>
            {loading ? "Saving..." : "Save"}
          </button>

          <button
            type="button"
            onClick={cancelEditing}
            disabled={loading}
          >
            Cancel
          </button>
        </form>
      ) : (
        <div className="measurement-item-content">
          <span>
            <strong>{measurement.measurement_type}</strong>:{" "}
            {measurement.value}{" "}
            {unit === "INCHES" ? "in" : "cm"}
          </span>

          <div className="measurement-actions">
            <button
              type="button"
              onClick={() => setEditing(true)}
              disabled={loading}
            >
              Edit
            </button>

            <button
              type="button"
              onClick={handleDelete}
              disabled={loading}
            >
              {loading ? "Deleting..." : "Delete"}
            </button>
          </div>
        </div>
      )}

      {error && <p role="alert">{error}</p>}
    </div>
  );
}

export default MeasurementItem;

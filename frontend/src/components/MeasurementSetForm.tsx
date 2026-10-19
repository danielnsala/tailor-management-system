
import { useState } from "react";
import type { FormEvent } from "react";

import {
  createMeasurementSet,
} from "../api/measurements";

import type {
  MeasurementSet,
  MeasurementUnit,
} from "../api/measurements";

type MeasurementSetFormProps = {
  customerId: number;
  token: string;
  onCreated: (measurementSet: MeasurementSet) => void;
};

type MeasurementInput = {
  measurement_type: string;
  value: string;
};

function MeasurementSetForm({
  customerId,
  token,
  onCreated,
}: MeasurementSetFormProps) {
  const [dateTaken, setDateTaken] = useState(
    new Date().toLocaleDateString("en-CA")
  );

  const [unit, setUnit] = useState<MeasurementUnit>("INCHES");
  const [notes, setNotes] = useState("");

  const [measurements, setMeasurements] = useState<MeasurementInput[]>([
    { measurement_type: "", value: "" },
  ]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  function addMeasurement() {
    setMeasurements((previous) => [
      ...previous,
      { measurement_type: "", value: "" },
    ]);
  }

  function removeMeasurement(index: number) {
    setMeasurements((previous) =>
      previous.filter((_, i) => i !== index)
    );
  }

  function updateField(
    index: number,
    field: keyof MeasurementInput,
    value: string
  ) {
    setMeasurements((previous) =>
      previous.map((measurement, i) =>
        i === index
          ? { ...measurement, [field]: value }
          : measurement
      )
    );
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (loading) return;

    setError("");
    setSuccess("");

    const cleanedMeasurements = measurements.map((measurement) => ({
      measurement_type: measurement.measurement_type.trim(),
      value: measurement.value.trim(),
    }));

    if (
      cleanedMeasurements.some(
        (measurement) =>
          !measurement.measurement_type ||
          !measurement.value ||
          !Number.isFinite(Number(measurement.value)) ||
          Number(measurement.value) <= 0
      )
    ) {
      setError("Every measurement needs a name and a positive value.");
      return;
    }

    const names = cleanedMeasurements.map(
      (measurement) => measurement.measurement_type.toLowerCase()
    );

    if (new Set(names).size !== names.length) {
      setError("Measurement types must be unique within a set.");
      return;
    }

    setLoading(true);

    try {
      const created = await createMeasurementSet(
        customerId,
        {
          date_taken: dateTaken,
          unit,
          notes: notes.trim() || null,
          measurements: cleanedMeasurements,
        },
        token
      );

      onCreated(created);

      setMeasurements([{ measurement_type: "", value: "" }]);
      setNotes("");
      setSuccess("Measurement set saved successfully!");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to save measurements."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="measurement-form">
      <h3>New Measurement Set</h3>

      <label>
        Date taken
        <input
          type="date"
          required
          value={dateTaken}
          onChange={(event) => setDateTaken(event.target.value)}
        />
      </label>

      <label>
        Unit
        <select
          value={unit}
          onChange={(event) =>
            setUnit(event.target.value as MeasurementUnit)
          }
        >
          <option value="INCHES">Inches</option>
          <option value="CENTIMETERS">Centimeters</option>
        </select>
      </label>

      <h4>Measurements</h4>

      {measurements.map((measurement, index) => (
        <div className="measurement-row" key={index}>
          <input
            type="text"
            placeholder="e.g. Chest"
            required
            value={measurement.measurement_type}
            onChange={(event) =>
              updateField(
                index,
                "measurement_type",
                event.target.value
              )
            }
          />

          <input
            type="number"
            placeholder="Value"
            min="0.01"
            step="0.01"
            required
            value={measurement.value}
            onChange={(event) =>
              updateField(index, "value", event.target.value)
            }
          />

          <button
            type="button"
            onClick={() => removeMeasurement(index)}
            disabled={measurements.length === 1 || loading}
          >
            Remove
          </button>
        </div>
      ))}

      <button type="button" onClick={addMeasurement} disabled={loading}>
        + Add Measurement
      </button>

      <label>
        Notes
        <textarea
          value={notes}
          onChange={(event) => setNotes(event.target.value)}
          placeholder="Additional fitting notes"
        />
      </label>

      {error && <p role="alert">{error}</p>}
      {success && <p role="status">{success}</p>}

      <button type="submit" disabled={loading}>
        {loading ? "Saving..." : "Save Measurement Set"}
      </button>
    </form>
  );
}

export default MeasurementSetForm;

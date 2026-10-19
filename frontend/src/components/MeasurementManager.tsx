
import { useEffect, useState } from "react";

import type { Customer } from "../api/customers";
import MeasurementItem from "./MeasurementItem";

import {
  getMeasurementSets,
} from "../api/measurements";

import type {
  Measurement,
  MeasurementSet,
} from "../api/measurements";

import MeasurementSetForm from "./MeasurementSetForm";

type MeasurementManagerProps = {
  customers: Customer[];
  token: string;
};

function MeasurementManager({
  customers,
  token,
}: MeasurementManagerProps) {
  const [selectedCustomerId, setSelectedCustomerId] =
    useState<number | null>(null);

  const [measurementSets, setMeasurementSets] =
    useState<MeasurementSet[]>([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (selectedCustomerId === null) {
      return;
    }

    let cancelled = false;

    async function loadMeasurementSets(customerId: number) {
      setLoading(true);
      setError("");
      setMeasurementSets([]);

      try {
        const data = await getMeasurementSets(customerId, token);

        if (!cancelled) {
          setMeasurementSets(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Failed to load measurements."
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadMeasurementSets(selectedCustomerId);

    return () => {
      cancelled = true;
    };
  }, [selectedCustomerId, token]);

  function handleMeasurementUpdated(
        setId: number,
        updatedMeasurement: Measurement
        ) {
        setMeasurementSets((previous) =>
            previous.map((set) =>
            set.id === setId
                ? {
                    ...set,
                    measurements: set.measurements.map((measurement) =>
                    measurement.id === updatedMeasurement.id
                        ? updatedMeasurement
                        : measurement
                    ),
                }
                : set
            )
        );
        }

    function handleMeasurementDeleted(
        setId: number,
        measurementId: number
        ) {
        setMeasurementSets((previous) =>
            previous.map((set) =>
            set.id === setId
                ? {
                    ...set,
                    measurements: set.measurements.filter(
                    (measurement) => measurement.id !== measurementId
                    ),
                }
                : set
            )
        );
        }

  const selectedCustomer = customers.find(
    (customer) => customer.id === selectedCustomerId
  );

  return (
    <section className="measurement-manager">
      <h2>Measurements Management</h2>

      <label htmlFor="measurement-customer">
        Select Customer
      </label>

      <select
        id="measurement-customer"
        value={selectedCustomerId ?? ""}
        onChange={(event) => {
          const value = event.target.value;

          setSelectedCustomerId(
            value === "" ? null : Number(value)
          );

          setMeasurementSets([]);
          setError("");
        }}
      >
        <option value="">Choose a customer</option>

        {customers.map((customer) => (
          <option key={customer.id} value={customer.id}>
            {customer.first_name} {customer.last_name}
          </option>
        ))}
      </select>

      {selectedCustomer && (
        <>
          <h3>
            Measurements for {selectedCustomer.first_name}{" "}
            {selectedCustomer.last_name}
          </h3>

          <MeasurementSetForm
            key={selectedCustomer.id}
            customerId={selectedCustomer.id}
            token={token}
            onCreated={(newSet) => {
              setMeasurementSets((previous) => [
                newSet,
                ...previous,
              ]);
            }}
          />

          <h3>Measurement History</h3>

          {loading && <p>Loading measurements...</p>}

          {error && <p role="alert">{error}</p>}

          {!loading && !error && measurementSets.length === 0 && (
            <p>No measurement sets recorded yet.</p>
          )}

          {measurementSets.map((set) => (
            <div className="measurement-set-card" key={set.id}>
              <h4>Measurements taken on {set.date_taken}</h4>

              <p>
                Unit:{" "}
                {set.unit === "INCHES"
                  ? "Inches"
                  : "Centimeters"}
              </p>

              {set.notes && <p>Notes: {set.notes}</p>}
                
        <div className="measurements-list">
            {set.measurements.map((measurement) => (
                <MeasurementItem
                key={measurement.id}
                measurement={measurement}
                customerId={set.customer_id}
                setId={set.id}
                unit={set.unit}
                token={token}
                onUpdated={(updated) =>
                    handleMeasurementUpdated(set.id, updated)
                }
                onDeleted={(measurementId) =>
                    handleMeasurementDeleted(set.id, measurementId)
                }
                />
            ))}

            {set.measurements.length === 0 && (
                <p>No measurements in this set.</p>
            )}
        </div>

            </div>
          ))}
        </>
      )}
    </section>
  );
}

export default MeasurementManager;

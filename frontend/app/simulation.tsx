"use client";

import React, { useEffect, useState } from "react";
import Head from "next/head";

interface SimulationRecord {
  id: number;
  num_rounds: number;
  num_clients: number;
  fraction_fit: number;
  started_at: string;
  finished_at: string | null;
  status: string;
}

export default function SimulationsPage() {
  const [simulations, setSimulations] = useState<SimulationRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    const fetchSimulations = async () => {
      try {
        const res = await fetch("/api/simulations/"); // using trailing slash
        if (!res.ok) {
          const data = await res.json();
          throw new Error(data.detail || "Failed to fetch simulations");
        }
        const data: SimulationRecord[] = await res.json();
        setSimulations(data);
      } catch (err: unknown) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An unexpected error occurred");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchSimulations();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Simulations Dashboard</title>
      </Head>
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-6">Simulations Dashboard</h1>
        {loading && <p>Loading simulation records...</p>}
        {error && <p className="text-red-500">{error}</p>}
        {!loading && !error && simulations.length === 0 && (
          <p>No simulation records found.</p>
        )}
        {!loading && !error && simulations.length > 0 && (
          <div className="space-y-4">
            {simulations.map((sim) => (
              <div key={sim.id} className="p-4 bg-white shadow rounded">
                <p className="text-lg font-semibold">Simulation ID: {sim.id}</p>
                <p>Rounds: {sim.num_rounds}</p>
                <p>Clients: {sim.num_clients}</p>
                <p>Fraction Fit: {sim.fraction_fit}</p>
                <p>
                  Started at:{" "}
                  {new Date(sim.started_at).toLocaleString()}
                </p>
                <p>
                  Finished at:{" "}
                  {sim.finished_at
                    ? new Date(sim.finished_at).toLocaleString()
                    : "In Progress"}
                </p>
                <p>Status: {sim.status}</p>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

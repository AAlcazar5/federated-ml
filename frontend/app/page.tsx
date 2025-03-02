"use client";

import React, { useState, useRef, useEffect } from "react";
import Head from "next/head";
// import { useRouter } from "next/navigation";

export default function HomePage() {
  // const router = useRouter();
  const [simulationLogs, setSimulationLogs] = useState<string[]>([]);
  const [trainingResult, setTrainingResult] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const logsContainerRef = useRef<HTMLDivElement>(null);

  const handleTriggerSimulation = () => {
    setLoading(true);
    setError("");
    setSimulationLogs([]);
    setTrainingResult("");

    const numRounds = 10;
    const numClients = 2;
    const fractionFit = 0.5;
    const url = `http://localhost:8000/api/simulations/stream?num_rounds=${numRounds}&num_clients=${numClients}&fraction_fit=${fractionFit}`;

    const eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
      console.log("Received event:", event.data);
      setSimulationLogs((prevLogs) => [...prevLogs, event.data]);

      // Append summary messages to trainingResult state.
      if (
        event.data.startsWith("Calculated reward:") ||
        event.data.startsWith("Simulation record saved with ID:")
      ) {
        setTrainingResult((prev) => prev + event.data + "\n");
      }
    };

    // Modified error handler: simply close connection and stop loading.
    eventSource.onerror = () => {
      // Removed console.error to avoid unnecessary error logging.
      eventSource.close();
      setLoading(false);
    };

    eventSource.onopen = () => {
      console.log("EventSource connection established.");
    };

    // Close connection when stream ends.
    eventSource.addEventListener("close", () => {
      eventSource.close();
      setLoading(false);
    });
  };

  // Scroll to the bottom of the logs container when simulationLogs update.
  useEffect(() => {
    if (logsContainerRef.current) {
      logsContainerRef.current.scrollTop = logsContainerRef.current.scrollHeight;
    }
  }, [simulationLogs]);

  // Scroll back to the top when trainingResult is updated.
  useEffect(() => {
    if (trainingResult && trainingResult.length > 0) {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }, [trainingResult]);

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <Head>
        <title>Federated Learning Simulation Dashboard</title>
      </Head>
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-6">
          Federated Learning Simulation Dashboard
        </h1>

        {/* Simulation Trigger Section */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Trigger Simulation</h2>
          <button
            onClick={handleTriggerSimulation}
            disabled={loading}
            className="bg-green-500 text-white px-6 py-3 rounded hover:bg-green-600"
          >
            {loading ? "Running Simulations..." : "Start Simulation"}
          </button>
          {error && <p className="mt-4 text-red-500">{error}</p>}
        </section>

        {/* Training Results Section */}
        {trainingResult && (
          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Training Results</h2>
            <div className="p-4 bg-white shadow rounded">
              <pre className="whitespace-pre-wrap">{trainingResult}</pre>
            </div>
          </section>
        )}

        {/* Simulation Logs Section */}
        {simulationLogs.length > 0 && (
          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Simulation Logs</h2>
            <div
              ref={logsContainerRef}
              className="h-64 overflow-y-auto p-4 bg-white shadow rounded"
            >
              {simulationLogs.map((log, index) => (
                <p key={index} className="whitespace-pre-wrap">
                  {log}
                </p>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

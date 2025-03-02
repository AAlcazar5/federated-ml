// frontend/components/Rewards.tsx
"use client";

import React, { useEffect, useState } from "react";

interface Transaction {
  timestamp: string;
  amount: number;
  description: string;
}

interface LedgerData {
  user_id: number;
  balance: number;
  transactions: Transaction[];
}

export default function Rewards() {
  const [ledger, setLedger] = useState<LedgerData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    const fetchLedger = async () => {
      try {
        // Use the full URL to ensure you're hitting the backend
        const res = await fetch("http://localhost:8000/api/incentives/ledger?user_id=1");
        if (!res.ok) {
          const errorText = await res.text();
          console.error("Error response text:", errorText);
          throw new Error("Failed to fetch ledger: " + res.statusText);
        }
        const data: LedgerData = await res.json();
        // Optionally round the balance
        data.balance = Math.round(data.balance * 100) / 100;
        setLedger(data);
      } catch (err: unknown) {
        console.error("Error fetching ledger:", err);
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An unexpected error occurred");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchLedger();
  }, []);

  // Helper to convert UTC to local time
  const formatDate = (utcTime: string) =>
    new Date(utcTime).toLocaleString("en-US", { timeZone: "America/Los_Angeles" });

  return (
    <div className="p-4 bg-white shadow rounded">
      <h2 className="text-2xl font-semibold mb-4">Token Rewards Ledger</h2>
      {loading && <p>Loading rewards...</p>}
      {error && <p className="text-red-500">{error}</p>}
      {ledger && (
        <>
          <p className="text-xl mb-4">
            Current Balance: <span className="font-bold">{ledger.balance.toFixed(2)}</span>
          </p>
          {ledger.transactions.length > 0 ? (
            <ul className="space-y-2">
              {ledger.transactions.map((tx, index) => (
                <li key={index} className="border p-2 rounded">
                  <p>
                    <strong>Date:</strong> {formatDate(tx.timestamp)}
                  </p>
                  <p>
                    <strong>Amount:</strong> {tx.amount.toFixed(2)}
                  </p>
                  <p>
                    <strong>Description:</strong> {tx.description}
                  </p>
                </li>
              ))}
            </ul>
          ) : (
            <p>No transactions recorded.</p>
          )}
        </>
      )}
    </div>
  );
}

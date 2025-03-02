"use client";

import React, { useEffect, useState } from "react";
import Head from "next/head";

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

export default function IncentivesPage() {
  const [ledger, setLedger] = useState<LedgerData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    const fetchLedger = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/incentives/ledger?user_id=1");
        if (!res.ok) {
          const errorText = await res.text();
          console.error("Error response text:", errorText);
          throw new Error("Failed to fetch ledger: " + res.statusText);
        }
        const data: LedgerData = await res.json();
        // Optionally round the balance:
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

  // Helper to convert UTC to local time (optional)
  const formatDate = (utcTime: string) =>
    new Date(utcTime).toLocaleString("en-US", { timeZone: "America/Los_Angeles" });

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <Head>
        <title>Token Rewards</title>
      </Head>
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-6">Token Rewards Ledger</h1>
        {loading && <p>Loading ledger data...</p>}
        {error && <p className="text-red-500">{error}</p>}
        {ledger && (
          <div>
            <p className="text-xl mb-4">
              Current Balance: <span className="font-semibold">{ledger.balance}</span>
            </p>
            <h2 className="text-2xl font-semibold mb-2">Recent Transactions</h2>
            {ledger.transactions.length > 0 ? (
              <ul className="space-y-2">
                {ledger.transactions.map((tx, index) => (
                  <li key={index} className="border p-2 rounded">
                    <p>
                      <strong>Date:</strong> {formatDate(tx.timestamp)}
                    </p>
                    <p>
                      <strong>Amount:</strong> {Math.round(tx.amount * 100) / 100}
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
          </div>
        )}
      </main>
    </div>
  );
}

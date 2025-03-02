// components/SimulationCard.tsx
import React from "react";
import Link from "next/link";

interface SimulationCardProps {
  simulationId: number;
  simulationName: string;
  status: string;
  progress: number;
  startDate: string;
}

const SimulationCard: React.FC<SimulationCardProps> = ({
  simulationId,
  simulationName,
  status,
  progress,
  startDate,
}) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-2">
        {simulationName}
      </h2>
      <p className="text-gray-600 mb-1">
        <span className="font-semibold">Status:</span> {status}
      </p>
      <p className="text-gray-600 mb-1">
        <span className="font-semibold">Progress:</span> {progress}%
      </p>
      <p className="text-gray-600 mb-4">
        <span className="font-semibold">Started on:</span> {startDate}
      </p>
      <Link
        href={`/simulation/${simulationId}`}
        className="text-blue-500 hover:underline"
      >
        View Details
      </Link>
    </div>
  );
};

export default SimulationCard;

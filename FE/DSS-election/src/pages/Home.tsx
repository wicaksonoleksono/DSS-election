import React, { useState, useEffect } from "react";
import { calculateSaw } from "../services/sawService";
import { calculateWp } from "../services/wpService";
import Results from "../components/home/Results";
import DynamicMatrix from "../components/home/DynamicMatrix";

const Home: React.FC = () => {
  const [scores, setScores] = useState<number[]>([]);
  const [alternativeNames, setAlternativeNames] = useState<string[]>([]);
  const [method, setMethod] = useState<"saw" | "wp">("saw"); // To keep track of selected method
  const [error, setError] = useState<string | null>(null); // To handle error messages

  const handleCalculation = async (data: {
    criteria_weights: number[];
    decision_matrix: number[][];
    criteria_types: string[];
    alternative_names: string[];
  }) => {
    const hasZero = data.decision_matrix.some((row) => row.includes(0));

    if (hasZero) {
      setError("Error: Tidak boleh diisi 0 , utk menghindari zerodiv error!.");
      return;
    }

    setError(null);
    let result;

    if (method === "saw") {
      console.log(data);
      result = await calculateSaw(data);
    } else if (method === "wp") {
      console.log(data);
      result = await calculateWp(data);
    }

    setScores(result?.scores || []);
    setAlternativeNames(data.alternative_names);
  };

  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        setError(null);
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [error]);

  return (
    <div>
      <h2>Select Calculation Method</h2>
      <div className="mb-4">
        <button
          className={`bg-blue-500 text-white px-4 py-2 mr-2 rounded hover:bg-blue-600 ${
            method === "saw" ? "bg-blue-700" : ""
          }`}
          onClick={() => setMethod("saw")}
        >
          Simple Additive Weighting (SAW)
        </button>
        <button
          className={`bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 ${
            method === "wp" ? "bg-blue-700" : ""
          }`}
          onClick={() => setMethod("wp")}
        >
          Weighted Product (WP)
        </button>
      </div>

      <div className="mb-4 p-4 bg-black-100 rounded">
        {method === "saw" && (
          <div>
            <h3 className="text-lg font-bold">
              Instruksi penggunaan Simple additive Weighting
            </h3>
            <p>
              Pembobotan menggunakan Persentasi yang bernilai 100% Contoh:
              <br />
              criteria 1 berbobot 25% maka masukan 0.25 dst.
            </p>
          </div>
        )}
        {method === "wp" && (
          <div>
            <h3 className="text-lg font-bold">
              Instruksi penggunaan weighted products
            </h3>
            <p>
              Gunakan range nilai tingkat kepentingan 1-5 dimana : <br />
              1: sangat rendah,
              <br />
              2: rendah, <br />
              3: cukup,
              <br />
              4: tinggi,
              <br />
              5: sangat tinggi. <br />
            </p>
          </div>
        )}
      </div>

      {error && (
        <div className="bg-red-100 text-red-700 p-4 rounded mb-4">{error}</div>
      )}

      <DynamicMatrix onSubmit={handleCalculation} />

      {scores.length > 0 && (
        <Results scores={scores} alternativeNames={alternativeNames} />
      )}
    </div>
  );
};

export default Home;

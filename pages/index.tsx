import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function ArbitrageDashboard() {
  const [data, setData] = useState(null);
  const [executing, setExecuting] = useState(false);

  const fetchArbitrageData = async () => {
    const res = await fetch("/api/arbitrage");
    const result = await res.json();
    setData(result);
  };

  const handleExecute = async () => {
    setExecuting(true);
    const res = await fetch("/api/execute", { method: "POST" });
    const result = await res.json();
    alert(`Trade executed: ${result.executed} | Profit: ${result.profit_percentage.toFixed(2)}%`);
    fetchArbitrageData();
    setExecuting(false);
  };

  useEffect(() => {
    fetchArbitrageData();
    const interval = setInterval(fetchArbitrageData, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4 grid gap-4">
      <Card>
        <CardContent className="p-4">
          <h1 className="text-xl font-bold">AL-AHAL Arbitrage Bot</h1>
          {data && (
            <div className="mt-2">
              <p>Profit: {data.profit_percentage.toFixed(4)}%</p>
              <p>Final Amount: {data.final_amount.toFixed(6)}</p>
              <p>Status: {data.opportunity ? "✅ Opportunity" : "❌ No Opportunity"}</p>
              <Button className="mt-4" onClick={handleExecute} disabled={executing}>
                {executing ? "Executing..." : "Execute Trade"}
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

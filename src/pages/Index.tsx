import { useState } from "react";
import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import PredictionResults from "@/components/PredictionResults";
import LoadingSpinner from "@/components/LoadingSpinner";


const Index = () => {
  const [query, setQuery] = useState("");
  const [predictions, setPredictions] = useState<Array<{ word: string; probability: number }>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) {
      toast({
        title: "Error",
        description: "Please enter a query",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    setPredictions([]);

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: query.trim() }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Transform the data to expected format
      const formattedPredictions = Object.entries(data.predictions || {}).map(([word, probability]) => ({
        word,
        probability: Number(probability)
      })).sort((a, b) => b.probability - a.probability);
      
      setPredictions(formattedPredictions);
      
      if (formattedPredictions.length === 0) {
        toast({
          title: "No predictions",
          description: "No predictions found for this query",
        });
      }
    } catch (error) {
      console.error("Error fetching predictions:", error);
      toast({
        title: "Connection Error",
        description: "Failed to connect to the prediction service. Make sure your Flask server is running on localhost:5000",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-16 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-foreground mb-4">
            Word Prediction
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Enter a word or sentence to predict the most likely next words based on the corpus analysis
          </p>
        </div>

        {/* Search Form */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="text-xl font-semibold">Enter Your Query</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="flex gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                <Input
                  type="text"
                  placeholder="Type a word or sentence..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="pl-10"
                  disabled={isLoading}
                />
              </div>
              <Button type="submit" disabled={isLoading || !query.trim()}>
                {isLoading ? "Predicting..." : "Predict"}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Loading State */}
        {isLoading && <LoadingSpinner />}

        {/* Results */}
        {!isLoading && predictions.length > 0 && (
          <PredictionResults predictions={predictions} query={query} />
        )}

        {/* Instructions */}
        <Card className="mt-8 border-dashed">
          <CardContent className="pt-6">
            <div className="text-center text-sm text-muted-foreground">
              <p className="mb-2">
                <strong>Instructions:</strong> Make sure your Flask server is running on localhost:5000
              </p>
              <p className="text-xs">
                The system analyzes documents in your corpus folder to predict the next most likely words
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Index;
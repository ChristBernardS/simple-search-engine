import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

interface Prediction {
  word: string;
  probability: number;
}

interface PredictionResultsProps {
  predictions: Prediction[];
  query: string;
}

const PredictionResults = ({ predictions, query }: PredictionResultsProps) => {
  const maxProbability = Math.max(...predictions.map(p => p.probability));

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-xl font-semibold">
          Next Word Predictions for "{query}"
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          {predictions.length} predictions found, sorted by probability
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {predictions.slice(0, 10).map((prediction, index) => {
            const percentage = maxProbability > 0 ? (prediction.probability / maxProbability) * 100 : 0;
            
            return (
              <div key={index} className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="font-medium text-foreground">
                    {prediction.word}
                  </span>
                  <span className="text-sm text-muted-foreground">
                    {(prediction.probability * 100).toFixed(2)}%
                  </span>
                </div>
                <Progress value={percentage} className="h-2" />
              </div>
            );
          })}
          
          {predictions.length > 10 && (
            <div className="text-center text-sm text-muted-foreground mt-4 pt-4 border-t">
              Showing top 10 of {predictions.length} predictions
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default PredictionResults;
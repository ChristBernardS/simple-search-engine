import { Card, CardContent } from "@/components/ui/card";

const LoadingSpinner = () => {
  return (
    <Card>
      <CardContent className="py-12">
        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          <p className="text-sm text-muted-foreground">
            Analyzing corpus and generating predictions...
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default LoadingSpinner;
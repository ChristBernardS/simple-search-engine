import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface RelevantDocument {
  document: string;
  score: number;
  snippet: string;
}

interface DocumentMatchesProps {
  documents: RelevantDocument[];
  query: string;
}

const DocumentMatches = ({ documents, query }: DocumentMatchesProps) => {
  if (!documents || documents.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-xl font-semibold">
            Document Matches for "{query}"
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">No documents found containing the query.</p>
        </CardContent>
      </Card>
    );
  }

  // Memecah query menjadi array kata kunci untuk perbandingan
  const queryKeywords = query.toLowerCase().split(/\s+/);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-xl font-semibold">
          Relevant Documents for "{query}"
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          Showing top {documents.length} relevant document(s)
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Header Tabel */}
          <div className="grid grid-cols-[1fr,auto,3fr] gap-4 px-4 pb-2 border-b font-semibold text-muted-foreground">
            <div>Dokumen</div>
            <div className="text-right">Skor</div>
            <div>Preview</div>
          </div>
          
          {/* Baris Data */}
          {documents.map((doc, index) => (
            <div key={index} className="grid grid-cols-[1fr,auto,3fr] gap-4 px-4 py-2 items-center hover:bg-muted/50 rounded-lg">
              <span className="font-medium text-foreground truncate" title={doc.document}>
                {doc.document}
              </span>
              <span className="font-mono text-sm text-right text-muted-foreground">
                {doc.score.toFixed(4)}
              </span>
              
              {/* --- PERUBAHAN LOGIKA DI SINI --- */}
              <p className="text-sm text-muted-foreground" dangerouslySetInnerHTML={{ 
                  __html: doc.snippet.replace(/\b([A-Z]{2,})\b/g, (match) => {
                    const lowercasedMatch = match.toLowerCase();
                    // Cek apakah kata yang ditemukan (setelah diubah ke huruf kecil) ada di dalam query
                    if (queryKeywords.includes(lowercasedMatch)) {
                      // Jika cocok, berikan style stabilo
                      return `<span class="bg-muted text-foreground px-1.5 py-0.5 rounded-md mx-0.5">${lowercasedMatch}</span>`;
                    }
                    // Jika tidak cocok, kembalikan kata aslinya tanpa style
                    return match;
                  })
              }}/>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default DocumentMatches;
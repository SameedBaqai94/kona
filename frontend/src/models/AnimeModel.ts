export interface AnimeResult {
    id: number;
    title: string;
    description: string | null;
    genres: string | null;
    tags: string | null;
    score: number | null;
}

export interface RecommendResponse {
    query: string;
    results: AnimeResult[];
}
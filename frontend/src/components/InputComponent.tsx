import { useState, useEffect } from "react";
import type { AnimeResult, RecommendResponse } from "../models/AnimeModel";
import "./InputComponent.css";

interface InputComponentsProps {
    onResults: (results: AnimeResult[]) => void;
    onQueryChange: (query: string) => void;
}

export default function InputComponent({ onResults, onQueryChange }: InputComponentsProps) {
    const [query, setQuery] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!query.trim()) {
            onResults([]);
            return;
        }

        const debounceTimer = setTimeout(() => {
            fetchRecommendations(query);
        }, 500);

        return () => clearTimeout(debounceTimer);
    }, [query]);

    const fetchRecommendations = async (q: string) => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(
                `http://localhost:8000/recommend/?q=${encodeURIComponent(q)}&limit=10`
            );

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data: RecommendResponse = await response.json();
            onResults(data.results);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Something went wrong");
            onResults([]);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = () => {
        if (query.trim()) fetchRecommendations(query);
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") handleSearch();
    };

    return (
        <div className="search-container">
            <div className="search-wrapper">
                <input
                    className="search-input"
                    type="text"
                    placeholder="anime that feels like Chainsaw Man..."
                    value={query}
                    onChange={(e) => {
                        setQuery(e.target.value);
                        onQueryChange(e.target.value);
                    }}
                    onKeyDown={handleKeyDown}
                />
                <button className="search-btn" onClick={handleSearch} disabled={loading}>
                    {loading ? "..." : "→"}
                </button>
            </div>

            {error && <p className="search-error">{error}</p>}
        </div>
    );
}
import "./ResultsTable.css";
import type { AnimeResult } from "../models/AnimeModel";

interface ResultsTableProps {
    results: AnimeResult[];
    query: string;
}

export default function ResultsTable({ results, query }: ResultsTableProps) {
    if (results.length === 0) return null;

    return (
        <div className="results">
            <p className="results__meta">
                {results.length} results for <span className="results__query">"{query}"</span>
            </p>

            <div className="results__table">
                <div className="results__header">
                    <span>#</span>
                    <span>Title</span>
                    <span>Genres</span>
                    <span>Tags</span>
                    <span>Score</span>
                </div>

                {results.map((anime, index) => (
                    <div className="results__row" key={anime.id} style={{ animationDelay: `${index * 0.05}s` }}>
                        <span className="results__index">{String(index + 1).padStart(2, "0")}</span>

                        <div className="results__title-cell">
                            <span className="results__title">{anime.title}</span>
                            {anime.description && (
                                <p className="results__description">
                                    {anime.description.slice(0, 120)}
                                    {anime.description.length > 120 ? "..." : ""}
                                </p>
                            )}
                        </div>

                        <div className="results__genres">
                            {anime.genres
                                ? anime.genres.split(", ").map((g) => (
                                    <span className="results__tag results__tag--genre" key={g}>{g}</span>
                                ))
                                : <span className="results__empty">—</span>}
                        </div>

                        <div className="results__tags">
                            {anime.tags
                                ? anime.tags.split(", ").slice(0, 4).map((t) => (
                                    <span className="results__tag" key={t}>{t}</span>
                                ))
                                : <span className="results__empty">—</span>}
                        </div>

                        <span className="results__score">
                            {anime.score ? anime.score.toFixed(1) : "—"}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
}
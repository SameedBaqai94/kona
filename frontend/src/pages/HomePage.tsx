import InputComponent from "../components/InputComponent";
import { useState } from "react";
import "./HomePage.css";
import ResultsTable from "../components/ResultsTable";
import type { AnimeResult } from "../models/AnimeModel";

export default function HomePage() {
    const [results, setResults] = useState<AnimeResult[]>([]);
    const [query, setQuery] = useState("");

    return (
        <div className="home">
            <div className="home__center">
                <header className="home__header">
                    <span className="home__logo">鬼</span>
                    <h1 className="home__title">Kona</h1>
                    <p className="home__subtitle">Find anime by feeling, not by filter.</p>
                </header>

                <InputComponent onResults={setResults} onQueryChange={setQuery} />

                <div className="home__content">
                    <ResultsTable results={results} query={query} />
                </div>
            </div>
        </div>
    );
}
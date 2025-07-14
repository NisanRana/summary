import React from 'react';
import { format } from 'date-fns';

interface NewsArticle {
  id: string;
  title: string;
  description: string;
  url: string;
  source: string;
  publishedAt: string;
  summary?: string;
  imageUrl?: string;
}

interface NewsCardProps {
  article: NewsArticle;
}

const NewsCard: React.FC<NewsCardProps> = ({ article }) => {
  return (
    <div className="group h-64 w-full [perspective:1000px]">
      <div className="relative h-full w-full rounded-xl shadow-xl transition-all duration-500 [transform-style:preserve-3d] group-hover:[transform:rotateY(180deg)]">
        {/* Front of card */}
        <div className="absolute inset-0">
          <img
            className="h-full w-full rounded-xl object-cover shadow-xl shadow-black/40"
            src={article.imageUrl || `https://picsum.photos/seed/${article.id}/400/300`}
            alt={article.title}
          />
          <div className="absolute bottom-0 w-full bg-black/60 text-white p-4 rounded-b-xl">
            <h3 className="text-lg font-bold">{article.title}</h3>
          </div>
        </div>
        {/* Back of card */}
        <div className="absolute inset-0 h-full w-full rounded-xl bg-black/80 px-12 text-center text-slate-200 [transform:rotateY(180deg)] [backface-visibility:hidden]">
          <div className="flex min-h-full flex-col items-center justify-center">
            <h1 className="text-3xl font-bold">{article.title}</h1>
            <p className="text-lg">{article.source}</p>
            <p className="text-base mt-2">{article.summary || article.description}</p>
            <a href={article.url} target="_blank" rel="noopener noreferrer" className="mt-4 rounded-md bg-accent-600 py-2 px-6 text-sm hover:bg-accent-700">
              Read More
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NewsCard; 
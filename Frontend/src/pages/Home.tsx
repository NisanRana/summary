import React from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';
import { format } from 'date-fns';
import NewsCard from '../components/NewsCard';

interface NewsArticle {
  id: string;
  title: string;
  description: string;
  url: string;
  source: string;
  publishedAt: string;
  summary?: string;
}

// Mock data for development
const mockArticles: NewsArticle[] = [
  {
    id: '1',
    title: 'Sample News Article 1',
    description: 'This is a sample news article description for development purposes.',
    url: 'https://example.com/news/1',
    source: 'Sample News',
    publishedAt: new Date().toISOString(),
    summary: 'A brief summary of the sample news article.',
  },
  {
    id: '2',
    title: 'Sample News Article 2',
    description: 'Another sample news article description for development.',
    url: 'https://example.com/news/2',
    source: 'Sample News',
    publishedAt: new Date().toISOString(),
    summary: 'A brief summary of another sample news article.',
  },
  {
    id: '3',
    title: 'Sample News Article 3',
    description: 'Third sample news article for UI demonstration.',
    url: 'https://example.com/news/3',
    source: 'Demo News',
    publishedAt: new Date().toISOString(),
    summary: 'A short summary for the third sample article.',
  },
  {
    id: '4',
    title: 'Sample News Article 4',
    description: 'Fourth sample article to fill the grid.',
    url: 'https://example.com/news/4',
    source: 'Demo News',
    publishedAt: new Date().toISOString(),
    summary: 'A short summary for the fourth sample article.',
  },
  {
    id: '5',
    title: 'Sample News Article 5',
    description: 'Fifth sample article for testing.',
    url: 'https://example.com/news/5',
    source: 'Test News',
    publishedAt: new Date().toISOString(),
    summary: 'A short summary for the fifth sample article.',
  },
  {
    id: '6',
    title: 'Sample News Article 6',
    description: 'Sixth sample article for a complete set.',
    url: 'https://example.com/news/6',
    source: 'Test News',
    publishedAt: new Date().toISOString(),
    summary: 'A short summary for the sixth sample article.',
  },
];

const Home: React.FC = () => {
  const { data: articles, isLoading, error } = useQuery<NewsArticle[]>(
    'news',
    async () => {
      try {
        // TODO: Replace with actual API endpoint
        const response = await axios.get('/api/news');
        return response.data;
      } catch (error) {
        // For development, return mock data if API fails
        console.warn('Using mock data due to API error:', error);
        return mockArticles;
      }
    },
    {
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    }
  );

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">
          Error loading news articles. Please try again later.
        </div>
        <button
          onClick={() => window.location.reload()}
          className="btn btn-primary"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!articles || articles.length === 0) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">No News Available</h2>
        <p className="text-gray-600">
          There are no news articles available at the moment.
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-full">
      {mockArticles.concat(mockArticles).slice(0, 6).map((article, i) => (
        <div key={i} className="group h-64 w-full [perspective:1000px]">
          <div className="relative h-full w-full rounded-xl shadow-xl transition-all duration-500 [transform-style:preserve-3d] group-hover:[transform:rotateY(180deg)]">
            {/* Front of card */}
            <div className="absolute inset-0">
              <img
                className="h-full w-full rounded-xl object-cover shadow-xl shadow-black/40"
                src={`https://picsum.photos/seed/${article.id}/400/300`}
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
      ))}
    </div>
  );
};

export default Home; 

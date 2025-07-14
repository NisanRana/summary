import React from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';
import { format } from 'date-fns';

interface NewsArticle {
  id: string;
  title: string;
  description: string;
  url: string;
  source: string;
  publishedAt: string;
  summary?: string;
}

interface Cluster {
  id: string;
  name: string;
  articles: NewsArticle[];
}

// Mock data for development
const mockClusters: Cluster[] = [
  {
    id: '1',
    name: 'Technology',
    articles: [
      {
        id: '1',
        title: 'New AI Breakthrough',
        description: 'Scientists achieve breakthrough in artificial intelligence research.',
        url: 'https://example.com/news/1',
        source: 'Tech News',
        publishedAt: new Date().toISOString(),
        summary: 'A significant advancement in AI technology has been made.',
      },
      {
        id: '2',
        title: 'Quantum Computing Milestone',
        description: 'Researchers reach new milestone in quantum computing.',
        url: 'https://example.com/news/2',
        source: 'Science Daily',
        publishedAt: new Date().toISOString(),
        summary: 'Quantum computing achieves new breakthrough in processing power.',
      },
    ],
  },
  {
    id: '2',
    name: 'Business',
    articles: [
      {
        id: '3',
        title: 'Market Trends 2024',
        description: 'Analysis of emerging market trends for the coming year.',
        url: 'https://example.com/news/3',
        source: 'Business Insider',
        publishedAt: new Date().toISOString(),
        summary: 'Key market trends to watch in 2024.',
      },
    ],
  },
];

const Clusters: React.FC = () => {
  const { data: clusters, isLoading, error } = useQuery<Cluster[]>(
    'clusters',
    async () => {
      try {
        // TODO: Replace with actual API endpoint
        const response = await axios.get('/api/clusters');
        return response.data;
      } catch (error) {
        // For development, return mock data if API fails
        console.warn('Using mock data due to API error:', error);
        return mockClusters;
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
          Error loading news clusters. Please try again later.
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

  if (!clusters || clusters.length === 0) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">No Clusters Available</h2>
        <p className="text-gray-600">
          There are no news clusters available at the moment.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">News Clusters</h2>
        <button
          onClick={() => window.location.reload()}
          className="btn btn-secondary"
        >
          Refresh
        </button>
      </div>
      <div className="space-y-12">
        {clusters.map((cluster) => (
          <div key={cluster.id} className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-6">{cluster.name}</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {cluster.articles.map((article) => (
                <article
                  key={article.id}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-300"
                >
                  <h4 className="text-lg font-medium text-gray-900 mb-2">
                    <a
                      href={article.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-primary-600"
                    >
                      {article.title}
                    </a>
                  </h4>
                  <p className="text-gray-600 text-sm mb-3">
                    {article.source} • {format(new Date(article.publishedAt), 'MMM d, yyyy')}
                  </p>
                  <p className="text-gray-700 text-sm mb-3">{article.description}</p>
                  {article.summary && (
                    <div className="bg-gray-50 p-3 rounded-md">
                      <p className="text-sm text-gray-600 italic">{article.summary}</p>
                    </div>
                  )}
                </article>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Clusters; 
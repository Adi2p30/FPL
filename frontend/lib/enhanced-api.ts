/**
 * Enhanced FPL API Client
 * Additional endpoints for enhanced metrics
 */

import api from './api';

// Enhanced metrics endpoints

export const getAllEnhancedMetrics = async () => {
  const response = await api.get('/api/enhanced/all-metrics');
  return response.data.metrics;
};

export const getTopPicks = async (position?: number, n: number = 20) => {
  const response = await api.get('/api/enhanced/top-picks', {
    params: { position, n },
  });
  return response.data.top_picks;
};

export const getTransfersIn = async (maxCost: number = 15.0, position?: number, n: number = 20) => {
  const response = await api.get('/api/enhanced/transfers-in', {
    params: { max_cost: maxCost, position, n },
  });
  return response.data.transfers_in;
};

export const getEnhancedDifferentials = async (
  maxOwnership: number = 10.0,
  minPoints: number = 30,
  n: number = 20
) => {
  const response = await api.get('/api/enhanced/differentials', {
    params: { max_ownership: maxOwnership, min_points: minPoints, n },
  });
  return response.data.differentials;
};

export const comparePlayersEnhanced = async (playerIds: number[]) => {
  const response = await api.post('/api/enhanced/compare', playerIds);
  return {
    comparison: response.data.comparison,
    descriptions: response.data.metric_descriptions,
  };
};

export const getMetricDescriptions = async () => {
  const response = await api.get('/api/enhanced/metric-descriptions');
  return response.data.descriptions;
};

// Team planning & save/load

export interface SavedTeam {
  name: string;
  formation: string;
  players: number[];  // player IDs
  budget: number;
  created_at: string;
  gameweek: number;
}

export const saveTeamToJSON = (team: SavedTeam): string => {
  return JSON.stringify(team, null, 2);
};

export const loadTeamFromJSON = (jsonString: string): SavedTeam => {
  return JSON.parse(jsonString);
};

export const downloadTeamJSON = (team: SavedTeam, filename: string = 'fpl-team.json') => {
  const jsonString = saveTeamToJSON(team);
  const blob = new Blob([jsonString], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

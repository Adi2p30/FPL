/**
 * FPL API Client
 * Connects to FastAPI backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface Player {
  id: number;
  web_name: string;
  first_name: string;
  second_name: string;
  element_type: number;
  team: number;
  team_name?: string;
  now_cost: number;
  cost: number;
  total_points: number;
  form: number;
  points_per_game: number;
  minutes: number;
  goals_scored: number;
  assists: number;
  clean_sheets: number;
  goals_conceded: number;
  saves: number;
  bonus: number;
  bps: number;
  selected_by_percent: number;
  position?: string;
}

export interface Team {
  id: number;
  name: string;
  short_name: string;
  strength: number;
}

export interface FamousManager {
  name: string;
  team_id: number;
  youtube_channel: string;
  description: string;
}

export interface TeamData {
  team_id: number;
  gameweek: number;
  info: {
    player_first_name: string;
    player_last_name: string;
    name: string;
    summary_overall_points: number;
    summary_overall_rank: number;
    current_event: number;
  };
  picks: {
    picks: Array<{
      element: number;
      position: number;
      multiplier: number;
      is_captain: boolean;
      is_vice_captain: boolean;
    }>;
    active_chip: string | null;
    entry_history: {
      event: number;
      points: number;
      total_points: number;
      rank: number;
      overall_rank: number;
    };
  };
  history: any;
  transfers: any;
  manager_info?: {
    name: string;
    youtube_channel: string;
    description: string;
  };
}

// API Functions

// Players
export const getAllPlayers = async (): Promise<Player[]> => {
  const response = await api.get('/api/players');
  return response.data.players;
};

export const getPlayer = async (playerId: number): Promise<Player> => {
  const response = await api.get(`/api/players/${playerId}`);
  return response.data.player;
};

// Teams
export const getAllTeams = async (): Promise<Team[]> => {
  const response = await api.get('/api/teams');
  return response.data.teams;
};

// Metrics
export const getComprehensiveMetrics = async () => {
  const response = await api.get('/api/metrics/comprehensive');
  return response.data.analysis;
};

export const getCaptainPicks = async () => {
  const response = await api.get('/api/metrics/captains');
  return response.data.captains;
};

export const getDifferentials = async (maxOwnership: number = 10, minPoints: number = 30) => {
  const response = await api.get('/api/metrics/differentials', {
    params: { max_ownership: maxOwnership, min_points: minPoints },
  });
  return response.data.differentials;
};

export const getPositionMetrics = async (position: string) => {
  const response = await api.get(`/api/metrics/position/${position}`);
  return response.data.metrics;
};

// Team Import
export const importTeam = async (teamId?: number, url?: string, gameweek?: number): Promise<TeamData> => {
  const response = await api.post('/api/team/import', {
    team_id: teamId,
    url: url,
    gameweek: gameweek,
  });
  return response.data.team;
};

export const getTeam = async (teamId: number, gameweek?: number): Promise<TeamData> => {
  const response = await api.get(`/api/team/${teamId}`, {
    params: { gameweek },
  });
  return response.data.team;
};

export const getTeamPicks = async (teamId: number, gameweek?: number) => {
  const response = await api.get(`/api/team/${teamId}/picks`, {
    params: { gameweek },
  });
  return response.data;
};

// Famous Managers
export const getFamousManagers = async (): Promise<FamousManager[]> => {
  const response = await api.get('/api/famous-managers');
  return response.data.managers;
};

export const getFamousTeams = async (): Promise<TeamData[]> => {
  const response = await api.get('/api/famous-teams');
  return response.data.teams;
};

export const getFamousTeam = async (managerName: string): Promise<TeamData> => {
  const response = await api.get(`/api/famous-teams/${managerName}`);
  return response.data.team;
};

// Utility
export const getCurrentGameweek = async (): Promise<number> => {
  const response = await api.get('/api/gameweek/current');
  return response.data.current_gameweek;
};

export default api;

'use client'

import { useState, useEffect } from 'react'
import { getAllPlayers, getFamousManagers, importTeam, type Player, type FamousManager, type TeamData } from '@/lib/api'

export default function Home() {
  const [players, setPlayers] = useState<Player[]>([])
  const [famousManagers, setFamousManagers] = useState<FamousManager[]>([])
  const [loading, setLoading] = useState(true)
  const [importModalOpen, setImportModalOpen] = useState(false)
  const [teamInput, setTeamInput] = useState('')
  const [importedTeam, setImportedTeam] = useState<TeamData | null>(null)
  const [activeTab, setActiveTab] = useState<'home' | 'import' | 'famous' | 'compare'>('home')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [playersData, managersData] = await Promise.all([
        getAllPlayers(),
        getFamousManagers()
      ])
      setPlayers(playersData.slice(0, 50)) // Top 50 for performance
      setFamousManagers(managersData)
      setLoading(false)
    } catch (error) {
      console.error('Error loading data:', error)
      setLoading(false)
    }
  }

  const handleImportTeam = async () => {
    try {
      setLoading(true)
      let team: TeamData

      if (teamInput.includes('fantasy.premierleague.com')) {
        // URL provided
        team = await importTeam(undefined, teamInput)
      } else {
        // Team ID provided
        const teamId = parseInt(teamInput)
        if (isNaN(teamId)) {
          alert('Invalid team ID or URL')
          setLoading(false)
          return
        }
        team = await importTeam(teamId)
      }

      setImportedTeam(team)
      setImportModalOpen(false)
      setActiveTab('import')
      setLoading(false)
    } catch (error) {
      console.error('Error importing team:', error)
      alert('Failed to import team. Check ID/URL and try again.')
      setLoading(false)
    }
  }

  const loadFamousTeam = async (manager: FamousManager) => {
    try {
      setLoading(true)
      const team = await importTeam(manager.team_id)
      setImportedTeam(team)
      setActiveTab('import')
      setLoading(false)
    } catch (error) {
      console.error('Error loading famous team:', error)
      setLoading(false)
    }
  }

  if (loading && players.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="spinner mb-4"></div>
          <p className="text-gray-400">Loading FPL data...</p>
        </div>
      </div>
    )
  }

  return (
    <main className="min-h-screen">
      {/* Navigation */}
      <nav className="border-b border-border bg-background-card/50 backdrop-blur-lg sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 rounded bg-gradient-primary flex items-center justify-center">
                <span className="text-xl font-bold">⚽</span>
              </div>
              <h1 className="text-xl font-bold text-glow">FPL ANALYTICS</h1>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setActiveTab('home')}
                className={`tab ${activeTab === 'home' ? 'tab-active' : ''}`}
              >
                Home
              </button>
              <button
                onClick={() => setActiveTab('famous')}
                className={`tab ${activeTab === 'famous' ? 'tab-active' : ''}`}
              >
                YouTubers
              </button>
              <button
                onClick={() => setActiveTab('compare')}
                className={`tab ${activeTab === 'compare' ? 'tab-active' : ''}`}
              >
                Compare
              </button>
              <a href="/dashboard" className="btn btn-secondary btn-sm ml-4">
                📊 Dashboard
              </a>
              <button
                onClick={() => setImportModalOpen(true)}
                className="btn btn-primary btn-sm"
              >
                Import Team
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        {/* Home Tab */}
        {activeTab === 'home' && (
          <div className="animate-fade-in">
            <div className="mb-8">
              <h2 className="text-3xl font-bold mb-2 text-glow">Welcome to FPL Analytics</h2>
              <p className="text-gray-400">EA FC-style dashboard with team import and YouTuber teams</p>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
              <div className="card card-glow p-6">
                <div className="stat-label mb-2">Total Players</div>
                <div className="stat-value">{players.length}+</div>
              </div>
              <div className="card card-glow p-6">
                <div className="stat-label mb-2">Famous Managers</div>
                <div className="stat-value">{famousManagers.length}</div>
              </div>
              <div className="card card-glow p-6">
                <div className="stat-label mb-2">Metrics</div>
                <div className="stat-value">20+</div>
              </div>
              <div className="card card-glow p-6">
                <div className="stat-label mb-2">Live Data</div>
                <div className="stat-value text-accent-pink">✓</div>
              </div>
            </div>

            {/* Top Players Preview */}
            <div>
              <h3 className="text-2xl font-bold mb-4">Top Players</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {players.slice(0, 6).map((player) => (
                  <div key={player.id} className="player-card">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <div className={`badge badge-${
                          player.element_type === 1 ? 'gkp' :
                          player.element_type === 2 ? 'def' :
                          player.element_type === 3 ? 'mid' : 'fwd'
                        } mb-2`}>
                          {player.element_type === 1 ? 'GKP' :
                           player.element_type === 2 ? 'DEF' :
                           player.element_type === 3 ? 'MID' : 'FWD'}
                        </div>
                        <h4 className="font-bold text-lg">{player.web_name}</h4>
                        <p className="text-sm text-gray-400">{player.team_name || `Team ${player.team}`}</p>
                      </div>
                      <div className="text-right">
                        <div className="text-xl font-bold text-accent-pink">
                          £{(player.now_cost / 10).toFixed(1)}m
                        </div>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-2 text-center">
                      <div>
                        <div className="text-lg font-bold">{player.total_points}</div>
                        <div className="text-xs text-gray-500">Points</div>
                      </div>
                      <div>
                        <div className="text-lg font-bold">{player.form}</div>
                        <div className="text-xs text-gray-500">Form</div>
                      </div>
                      <div>
                        <div className="text-lg font-bold">{player.selected_by_percent}%</div>
                        <div className="text-xs text-gray-500">Own</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Famous Teams Tab */}
        {activeTab === 'famous' && (
          <div className="animate-fade-in">
            <h2 className="text-3xl font-bold mb-6 text-glow">Famous FPL YouTubers</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {famousManagers.map((manager) => (
                <div key={manager.team_id} className="card card-hover card-glow p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-bold mb-1">{manager.name}</h3>
                      <p className="text-sm text-gray-400">{manager.youtube_channel}</p>
                    </div>
                    <div className="w-12 h-12 rounded-full bg-gradient-primary flex items-center justify-center">
                      <span className="text-2xl">🎮</span>
                    </div>
                  </div>
                  <p className="text-sm text-gray-300 mb-4">{manager.description}</p>
                  <button
                    onClick={() => loadFamousTeam(manager)}
                    className="btn btn-secondary btn-sm w-full"
                    disabled={loading}
                  >
                    {loading ? 'Loading...' : 'View Team'}
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Imported Team View */}
        {activeTab === 'import' && importedTeam && (
          <div className="animate-fade-in">
            <div className="mb-6">
              <h2 className="text-3xl font-bold mb-2 text-glow">
                {importedTeam.info.name}
              </h2>
              <p className="text-gray-400">
                {importedTeam.info.player_first_name} {importedTeam.info.player_last_name}
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
              <div className="card p-6">
                <div className="stat-label mb-2">Overall Points</div>
                <div className="stat-value">{importedTeam.info.summary_overall_points}</div>
              </div>
              <div className="card p-6">
                <div className="stat-label mb-2">Overall Rank</div>
                <div className="stat-value">{importedTeam.info.summary_overall_rank?.toLocaleString()}</div>
              </div>
              <div className="card p-6">
                <div className="stat-label mb-2">Gameweek</div>
                <div className="stat-value">{importedTeam.gameweek}</div>
              </div>
              <div className="card p-6">
                <div className="stat-label mb-2">GW Points</div>
                <div className="stat-value text-accent-pink">
                  {importedTeam.picks?.entry_history?.points || 0}
                </div>
              </div>
            </div>

            {importedTeam.picks && importedTeam.picks.picks && (
              <div className="card p-6">
                <h3 className="text-xl font-bold mb-4">Team Picks (GW {importedTeam.gameweek})</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {importedTeam.picks.picks.slice(0, 11).map((pick, idx) => {
                    const player = players.find(p => p.id === pick.element)
                    if (!player) return null

                    return (
                      <div key={idx} className={`player-card ${pick.is_captain ? 'player-card-selected' : ''}`}>
                        <div className="flex items-center justify-between mb-2">
                          <div className={`badge badge-${
                            player.element_type === 1 ? 'gkp' :
                            player.element_type === 2 ? 'def' :
                            player.element_type === 3 ? 'mid' : 'fwd'
                          }`}>
                            {player.element_type === 1 ? 'GKP' :
                             player.element_type === 2 ? 'DEF' :
                             player.element_type === 3 ? 'MID' : 'FWD'}
                          </div>
                          {pick.is_captain && (
                            <span className="badge bg-accent-pink text-white">C</span>
                          )}
                          {pick.is_vice_captain && (
                            <span className="badge bg-accent-purple text-white">VC</span>
                          )}
                        </div>
                        <h4 className="font-bold">{player.web_name}</h4>
                        <p className="text-sm text-gray-400">{player.team_name || `Team ${player.team}`}</p>
                        <div className="mt-2 text-sm">
                          <span className="text-accent-pink font-semibold">{player.total_points}</span> pts
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Player Comparison Tab */}
        {activeTab === 'compare' && (
          <div className="animate-fade-in">
            <h2 className="text-3xl font-bold mb-6 text-glow">Player Comparison</h2>
            <p className="text-gray-400 mb-8">Feature coming soon...</p>
          </div>
        )}
      </div>

      {/* Import Modal */}
      {importModalOpen && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="card w-full max-w-md p-6 animate-slide-up">
            <h3 className="text-2xl font-bold mb-4">Import FPL Team</h3>
            <p className="text-sm text-gray-400 mb-6">
              Enter a team ID or paste the FPL URL
            </p>

            <input
              type="text"
              value={teamInput}
              onChange={(e) => setTeamInput(e.target.value)}
              placeholder="Team ID or URL"
              className="input w-full mb-4"
              onKeyPress={(e) => e.key === 'Enter' && handleImportTeam()}
            />

            <div className="flex gap-3">
              <button
                onClick={handleImportTeam}
                className="btn btn-primary flex-1"
                disabled={loading || !teamInput}
              >
                {loading ? 'Importing...' : 'Import'}
              </button>
              <button
                onClick={() => setImportModalOpen(false)}
                className="btn btn-ghost flex-1"
                disabled={loading}
              >
                Cancel
              </button>
            </div>

            <div className="mt-6 pt-6 border-t border-border">
              <p className="text-xs text-gray-500 mb-2">Examples:</p>
              <code className="text-xs text-accent-pink">123456</code> or
              <br />
              <code className="text-xs text-accent-pink">
                https://fantasy.premierleague.com/entry/123456/event/10
              </code>
            </div>
          </div>
        </div>
      )}
    </main>
  )
}

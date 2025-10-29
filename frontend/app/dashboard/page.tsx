'use client'

import { useState, useEffect } from 'react'
import { getAllPlayers, type Player } from '@/lib/api'
import { getAllEnhancedMetrics, downloadTeamJSON, type SavedTeam } from '@/lib/enhanced-api'
import AIAssistant from '@/components/AIAssistant'

export default function DashboardPage() {
  const [players, setPlayers] = useState<any[]>([])
  const [enhancedMetrics, setEnhancedMetrics] = useState<any[]>([])
  const [myTeam, setMyTeam] = useState<number[]>([])
  const [activeTab, setActiveTab] = useState<'players' | 'metrics' | 'planner' | 'compare'>('players')
  const [loading, setLoading] = useState(true)
  const [selectedPlayers, setSelectedPlayers] = useState<number[]>([])

  // Team planner state
  const [teamName, setTeamName] = useState('My FPL Team')
  const [formation, setFormation] = useState('3-4-3')
  const [budget, setBudget] = useState(100)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [playersData, metricsData] = await Promise.all([
        getAllPlayers(),
        getAllEnhancedMetrics()
      ])
      setPlayers(playersData.slice(0, 100))
      setEnhancedMetrics(metricsData.slice(0, 100))
      setLoading(false)
    } catch (error) {
      console.error('Error:', error)
      setLoading(false)
    }
  }

  const handleSaveTeam = () => {
    const team: SavedTeam = {
      name: teamName,
      formation,
      players: myTeam,
      budget,
      created_at: new Date().toISOString(),
      gameweek: 1
    }
    downloadTeamJSON(team, `${teamName.replace(/\s+/g, '-')}.json`)
  }

  const handleLoadTeam = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        try {
          const team = JSON.parse(e.target?.result as string)
          setMyTeam(team.players)
          setTeamName(team.name)
          setFormation(team.formation)
          setBudget(team.budget)
        } catch (error) {
          alert('Invalid team file')
        }
      }
      reader.readAsText(file)
    }
  }

  const togglePlayerSelection = (playerId: number) => {
    setSelectedPlayers(prev =>
      prev.includes(playerId)
        ? prev.filter(id => id !== playerId)
        : [...prev, playerId]
    )
  }

  const addToMyTeam = (playerId: number) => {
    if (!myTeam.includes(playerId) && myTeam.length < 15) {
      setMyTeam([...myTeam, playerId])
    }
  }

  const removeFromMyTeam = (playerId: number) => {
    setMyTeam(myTeam.filter(id => id !== playerId))
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    )
  }

  const myTeamPlayers = players.filter(p => myTeam.includes(p.id))
  const teamCost = myTeamPlayers.reduce((sum, p) => sum + (p.now_cost / 10), 0)

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b border-border bg-background-card/50 backdrop-blur-lg sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-glow">FPL DASHBOARD</h1>
        </div>
      </div>

      {/* Main Layout: Team Center, Tabs Right */}
      <div className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-12 gap-6">

          {/* Left/Center: My Team */}
          <div className="col-span-12 lg:col-span-8">
            <div className="card p-6 mb-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-2xl font-bold">{teamName}</h2>
                  <p className="text-sm text-gray-400">Formation: {formation}</p>
                </div>
                <div className="text-right">
                  <div className="stat-value">£{teamCost.toFixed(1)}m</div>
                  <div className="stat-label">of £{budget}m</div>
                </div>
              </div>

              {/* Team Display */}
              <div className="pitch p-8 min-h-[400px] relative">
                {myTeamPlayers.length === 0 ? (
                  <div className="absolute inset-0 flex items-center justify-center">
                    <p className="text-gray-500">No players selected. Add players from the table →</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-11 gap-2">
                    {myTeamPlayers.map((player, idx) => (
                      <div key={player.id} className="text-center">
                        <div className="w-12 h-12 mx-auto rounded-full bg-gradient-primary flex items-center justify-center mb-1">
                          <span className="text-xs font-bold">{player.web_name.substring(0, 3).toUpperCase()}</span>
                        </div>
                        <p className="text-xs">{player.web_name}</p>
                        <button
                          onClick={() => removeFromMyTeam(player.id)}
                          className="text-xs text-red-400 hover:text-red-300"
                        >
                          ✕
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Team Actions */}
              <div className="flex gap-2 mt-4">
                <button onClick={handleSaveTeam} className="btn btn-primary btn-sm">
                  💾 Save Team
                </button>
                <label className="btn btn-secondary btn-sm cursor-pointer">
                  📂 Load Team
                  <input type="file" accept=".json" onChange={handleLoadTeam} className="hidden" />
                </label>
                <button onClick={() => setMyTeam([])} className="btn btn-ghost btn-sm">
                  🗑️ Clear
                </button>
              </div>
            </div>

            {/* Player Table with ALL Metrics */}
            <div className="card p-6">
              <h3 className="text-xl font-bold mb-4">Player Database</h3>

              {/* Tabs for different views */}
              <div className="flex gap-2 mb-4 border-b border-border">
                <button
                  onClick={() => setActiveTab('players')}
                  className={`tab ${activeTab === 'players' ? 'tab-active' : ''}`}
                >
                  Players
                </button>
                <button
                  onClick={() => setActiveTab('metrics')}
                  className={`tab ${activeTab === 'metrics' ? 'tab-active' : ''}`}
                >
                  Enhanced Metrics
                </button>
                <button
                  onClick={() => setActiveTab('compare')}
                  className={`tab ${activeTab === 'compare' ? 'tab-active' : ''}`}
                >
                  Compare ({selectedPlayers.length})
                </button>
              </div>

              {/* Player List */}
              {activeTab === 'players' && (
                <div className="overflow-x-auto custom-scrollbar">
                  <table className="w-full text-sm">
                    <thead className="bg-background-hover sticky top-0">
                      <tr>
                        <th className="p-2 text-left">Select</th>
                        <th className="p-2 text-left">Player</th>
                        <th className="p-2 text-left">Pos</th>
                        <th className="p-2 text-right">Cost</th>
                        <th className="p-2 text-right">Pts</th>
                        <th className="p-2 text-right">Form</th>
                        <th className="p-2 text-right">Own%</th>
                        <th className="p-2">Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {players.map((player) => (
                        <tr key={player.id} className="border-b border-border hover:bg-background-hover">
                          <td className="p-2">
                            <input
                              type="checkbox"
                              checked={selectedPlayers.includes(player.id)}
                              onChange={() => togglePlayerSelection(player.id)}
                              className="w-4 h-4"
                            />
                          </td>
                          <td className="p-2">
                            <div className="font-semibold">{player.web_name}</div>
                            <div className="text-xs text-gray-500">{player.team_name}</div>
                          </td>
                          <td className="p-2">
                            <div className={`badge badge-${
                              player.element_type === 1 ? 'gkp' :
                              player.element_type === 2 ? 'def' :
                              player.element_type === 3 ? 'mid' : 'fwd'
                            }`}>
                              {player.element_type === 1 ? 'GKP' :
                               player.element_type === 2 ? 'DEF' :
                               player.element_type === 3 ? 'MID' : 'FWD'}
                            </div>
                          </td>
                          <td className="p-2 text-right font-semibold text-accent-pink">
                            £{(player.now_cost / 10).toFixed(1)}m
                          </td>
                          <td className="p-2 text-right font-bold">{player.total_points}</td>
                          <td className="p-2 text-right">{player.form}</td>
                          <td className="p-2 text-right text-xs">{player.selected_by_percent}%</td>
                          <td className="p-2">
                            <button
                              onClick={() => addToMyTeam(player.id)}
                              disabled={myTeam.includes(player.id) || myTeam.length >= 15}
                              className="btn btn-sm btn-primary"
                            >
                              +
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {/* Enhanced Metrics View */}
              {activeTab === 'metrics' && (
                <div className="overflow-x-auto custom-scrollbar">
                  <table className="w-full text-sm">
                    <thead className="bg-background-hover sticky top-0">
                      <tr>
                        <th className="p-2 text-left">Player</th>
                        <th className="p-2 text-right" title="Points per Million">PPM</th>
                        <th className="p-2 text-right" title="Form Rating">Form</th>
                        <th className="p-2 text-right" title="Expected GI per 90">xGI</th>
                        <th className="p-2 text-right" title="Overall Score">Score</th>
                        <th className="p-2 text-right" title="Buy Score">Buy</th>
                        <th className="p-2 text-right" title="Captain Score">Capt</th>
                      </tr>
                    </thead>
                    <tbody>
                      {enhancedMetrics.map((metric) => (
                        <tr key={metric.id} className="border-b border-border hover:bg-background-hover">
                          <td className="p-2">
                            <div className="font-semibold">{metric.web_name}</div>
                            <div className="text-xs text-gray-500">£{metric.cost?.toFixed(1)}m</div>
                          </td>
                          <td className="p-2 text-right font-semibold text-green-400">
                            {metric.ppm?.toFixed(1) || '-'}
                          </td>
                          <td className="p-2 text-right">{metric.form_rating?.toFixed(1) || '-'}</td>
                          <td className="p-2 text-right">{metric.xgi_per_90?.toFixed(2) || '-'}</td>
                          <td className="p-2 text-right font-bold text-accent-pink">
                            {metric.overall_score?.toFixed(0) || '-'}
                          </td>
                          <td className="p-2 text-right">{metric.buy_score?.toFixed(1) || '-'}</td>
                          <td className="p-2 text-right">{metric.captain_score?.toFixed(1) || '-'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {/* Comparison View */}
              {activeTab === 'compare' && (
                <div>
                  {selectedPlayers.length === 0 ? (
                    <p className="text-gray-500 text-center py-8">Select players to compare</p>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {selectedPlayers.map(playerId => {
                        const player = players.find(p => p.id === playerId)
                        const metrics = enhancedMetrics.find(m => m.id === playerId)
                        if (!player) return null

                        return (
                          <div key={playerId} className="card p-4">
                            <div className="flex justify-between items-start mb-3">
                              <div>
                                <h4 className="font-bold">{player.web_name}</h4>
                                <p className="text-xs text-gray-400">{player.team_name}</p>
                              </div>
                              <button
                                onClick={() => togglePlayerSelection(playerId)}
                                className="text-red-400 hover:text-red-300"
                              >
                                ✕
                              </button>
                            </div>

                            <div className="space-y-2 text-sm">
                              <div className="flex justify-between">
                                <span className="text-gray-400">Cost</span>
                                <span className="font-semibold text-accent-pink">£{(player.now_cost/10).toFixed(1)}m</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-400">Points</span>
                                <span className="font-semibold">{player.total_points}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-400">Form</span>
                                <span>{player.form}</span>
                              </div>
                              {metrics && (
                                <>
                                  <div className="flex justify-between">
                                    <span className="text-gray-400">PPM</span>
                                    <span className="text-green-400">{metrics.ppm?.toFixed(1)}</span>
                                  </div>
                                  <div className="flex justify-between">
                                    <span className="text-gray-400">Overall Score</span>
                                    <span className="font-bold text-accent-pink">{metrics.overall_score?.toFixed(0)}</span>
                                  </div>
                                  <div className="flex justify-between">
                                    <span className="text-gray-400">Buy Score</span>
                                    <span>{metrics.buy_score?.toFixed(1)}</span>
                                  </div>
                                </>
                              )}
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Right Sidebar: Quick Actions */}
          <div className="col-span-12 lg:col-span-4">
            <div className="space-y-4 sticky top-20">

              {/* Team Stats */}
              <div className="card p-4">
                <h3 className="font-bold mb-3">Team Stats</h3>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Players</span>
                    <span className="font-semibold">{myTeam.length}/15</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Budget</span>
                    <span className={teamCost > budget ? 'text-red-400' : 'text-green-400'}>
                      £{teamCost.toFixed(1)}m / £{budget}m
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Remaining</span>
                    <span className="font-semibold">£{(budget - teamCost).toFixed(1)}m</span>
                  </div>
                </div>
              </div>

              {/* Quick Filters */}
              <div className="card p-4">
                <h3 className="font-bold mb-3">Quick Filters</h3>
                <div className="space-y-2">
                  <button className="w-full btn btn-secondary btn-sm">🔥 In Form</button>
                  <button className="w-full btn btn-secondary btn-sm">💎 Differentials</button>
                  <button className="w-full btn btn-secondary btn-sm">👑 Captains</button>
                  <button className="w-full btn btn-secondary btn-sm">💰 Value</button>
                </div>
              </div>

              {/* Position Breakdown */}
              <div className="card p-4">
                <h3 className="font-bold mb-3">Position Breakdown</h3>
                {['GKP', 'DEF', 'MID', 'FWD'].map(pos => {
                  const posPlayers = myTeamPlayers.filter(p => {
                    if (pos === 'GKP') return p.element_type === 1
                    if (pos === 'DEF') return p.element_type === 2
                    if (pos === 'MID') return p.element_type === 3
                    return p.element_type === 4
                  })
                  return (
                    <div key={pos} className="flex justify-between text-sm mb-2">
                      <span className={`badge badge-${pos.toLowerCase()}`}>{pos}</span>
                      <span className="font-semibold">{posPlayers.length}</span>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* AI Assistant */}
      <AIAssistant context={{
        team: myTeamPlayers.map(p => ({
          id: p.id,
          name: p.web_name,
          position: p.element_type,
          cost: p.now_cost / 10,
          points: p.total_points
        })),
        budget_remaining: budget - teamCost,
        selected_players: selectedPlayers.map(id =>
          players.find(p => p.id === id)?.web_name
        ).filter(Boolean),
        current_gameweek: 1
      }} />
    </div>
  )
}

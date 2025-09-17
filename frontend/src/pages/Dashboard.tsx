import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { useAuth } from '../context/AuthContext'

export default function Dashboard() {
  const { logout } = useAuth()
  const [me, setMe] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [skills, setSkills] = useState<any[]>([])
  const [skillsError, setSkillsError] = useState<string | null>(null)
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [uploadMsg, setUploadMsg] = useState<string | null>(null)
  const [savingId, setSavingId] = useState<number | null>(null)
  const [deletingId, setDeletingId] = useState<number | null>(null)
  const [roadmap, setRoadmap] = useState<any | null>(null)
  const [roadmapMsg, setRoadmapMsg] = useState<string | null>(null)
  const [pendingDeletes, setPendingDeletes] = useState<Record<number, any>>({})
  const [history, setHistory] = useState<any[]>([])
  const [historyError, setHistoryError] = useState<string | null>(null)
  const [viewedPath, setViewedPath] = useState<any | null>(null)
  const [compareA, setCompareA] = useState<number | ''>('')
  const [compareB, setCompareB] = useState<number | ''>('')
  const [compareResult, setCompareResult] = useState<any | null>(null)

  useEffect(() => {
    api
      .get('/users/me')
      .then((res) => setMe(res.data))
      .catch((err) => setError(err?.response?.data?.detail || 'Failed to load profile'))
      .finally(() => setLoading(false))

    api
      .get('/users/me/skills')
      .then((res) => setSkills(res.data))
      .catch((err) => setSkillsError(err?.response?.data?.detail || 'Failed to load skills'))

    api
      .get('/roadmap/current')
      .then((res) => setRoadmap(res.data))
      .catch(() => setRoadmap(null))

    api
      .get('/roadmap/history')
      .then((res) => setHistory(res.data))
      .catch((err) => setHistoryError(err?.response?.data?.detail || 'Failed to load history'))
  }, [])

  if (loading) return <div className="page"><div className="card">Loading...</div></div>
  if (error) return <div className="page"><div className="card error">{error}</div></div>

  return (
    <div className="page">
      <div className="card">
        <div className="row space-between">
          <h2>Welcome, {me?.full_name}</h2>
          <button onClick={logout}>Log out</button>
        </div>
        <p><strong>Username:</strong> {me?.username}</p>
        <p><strong>Email:</strong> {me?.email}</p>
        <div className="row gap">
          <a className="button secondary" href="/docs" target="_blank">API Docs</a>
        </div>
      </div>

      <div className="card" style={{ marginTop: 16 }}>
        <h3>Your Skills</h3>
        <form
          onSubmit={async (e) => {
            e.preventDefault()
            setUploadMsg(null)
            setSkillsError(null)
            if (!file) {
              setUploadMsg('Please select a PDF, DOCX, or TXT resume to upload.')
              return
            }
            try {
              setUploading(true)
              const form = new FormData()
              form.append('file', file)
              const res = await api.post('/resume/upload', form, {
                headers: { 'Content-Type': 'multipart/form-data' }
              })
              setUploadMsg(`Uploaded successfully. Detected ${res.data?.length ?? 0} skills.`)
              // refresh skills list
              const skillsRes = await api.get('/users/me/skills')
              setSkills(skillsRes.data)
            } catch (err: any) {
              setUploadMsg(err?.response?.data?.detail || 'Upload failed')
            } finally {
              setUploading(false)
              setFile(null)
            }
          }}
          className="row gap"
          style={{ margin: '8px 0 16px', alignItems: 'center', flexWrap: 'wrap' }}
        >
          <input
            type="file"
            accept=".pdf,.docx,.txt,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            style={{ maxWidth: 360 }}
          />
          <button type="submit" disabled={uploading}>
            {uploading ? 'Uploading…' : 'Upload Resume'}
          </button>
          {uploadMsg && <div className="muted">{uploadMsg}</div>}
        </form>
        {skillsError && <div className="error">{skillsError}</div>}
        {(!skills || skills.length === 0) ? (
          <p className="muted">No skills detected yet. Upload your resume via API to get started.</p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left', padding: '8px 6px' }}>Skill</th>
                  <th style={{ textAlign: 'left', padding: '8px 6px' }}>Category</th>
                  <th style={{ textAlign: 'left', padding: '8px 6px' }}>Proficiency (%)</th>
                  <th style={{ textAlign: 'left', padding: '8px 6px' }}>Confidence (%)</th>
                  <th style={{ textAlign: 'left', padding: '8px 6px' }}>Priority</th>
                  <th style={{ textAlign: 'left', padding: '8px 6px' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {skills.map((us: any, idx: number) => {
                  const isPendingDelete = !!pendingDeletes[us.id]
                  return (
                  <tr key={us.id} style={{ opacity: isPendingDelete ? 0.5 : 1 }}>
                    <td style={{ padding: '6px' }}>{us.skill?.name}</td>
                    <td style={{ padding: '6px' }}>{us.skill?.category}{us.skill?.subcategory ? ` / ${us.skill.subcategory}` : ''}</td>
                    <td style={{ padding: '6px', minWidth: 120 }}>
                      <input
                        type="number"
                        min={0}
                        max={100}
                        value={Math.round(us.proficiency_level ?? 0)}
                        onChange={(e) => {
                          const v = Number(e.target.value)
                          setSkills((prev) => prev.map((row, i) => i === idx ? { ...row, proficiency_level: v } : row))
                        }}
                        style={{ width: 90 }}
                      />
                    </td>
                    <td style={{ padding: '6px', minWidth: 120 }}>
                      <input
                        type="number"
                        min={0}
                        max={100}
                        value={Math.round(us.confidence_level ?? 0)}
                        onChange={(e) => {
                          const v = Number(e.target.value)
                          setSkills((prev) => prev.map((row, i) => i === idx ? { ...row, confidence_level: v } : row))
                        }}
                        style={{ width: 90 }}
                      />
                    </td>
                    <td style={{ padding: '6px', minWidth: 140 }}>
                      <select
                        value={us.priority || 'medium'}
                        onChange={(e) => {
                          const v = e.target.value
                          setSkills((prev) => prev.map((row, i) => i === idx ? { ...row, priority: v } : row))
                        }}
                        style={{ width: 120 }}
                      >
                        <option value="low">low</option>
                        <option value="medium">medium</option>
                        <option value="high">high</option>
                        <option value="critical">critical</option>
                      </select>
                    </td>
                    <td style={{ padding: '6px' }}>
                      <div className="row gap">
                        <button
                          className="button secondary"
                          onClick={async () => {
                            setSavingId(us.id)
                            try {
                              const payload: any = {
                                proficiency_level: Number(us.proficiency_level) || 0,
                                confidence_level: Number(us.confidence_level) || 0,
                                priority: us.priority || 'medium',
                              }
                              const res = await api.patch(`/users/me/skills/${us.id}`, payload)
                              // replace updated row with response
                              setSkills((prev) => prev.map((row) => row.id === us.id ? res.data : row))
                            } catch (err) {
                              alert('Failed to save changes')
                            } finally {
                              setSavingId(null)
                            }
                          }}
                          disabled={savingId === us.id}
                        >
                          {savingId === us.id ? 'Saving…' : 'Save'}
                        </button>
                        <button
                          style={{ background: '#b54957', color: '#fff' }}
                          onClick={() => {
                            // Soft-delete UX: stage deletion, allow Undo within 5s
                            if (pendingDeletes[us.id]) return
                            const timeout = setTimeout(async () => {
                              setDeletingId(us.id)
                              try {
                                await api.delete(`/users/me/skills/${us.id}`)
                                setSkills((prev) => prev.filter((row) => row.id !== us.id))
                              } catch (err) {
                                alert('Failed to delete skill')
                                // Cancel pending delete if failed
                                setPendingDeletes((prev) => {
                                  const p = { ...prev }
                                  delete p[us.id]
                                  return p
                                })
                              } finally {
                                setDeletingId(null)
                              }
                            }, 5000)
                            setPendingDeletes((prev) => ({ ...prev, [us.id]: timeout }))
                          }}
                          disabled={deletingId === us.id || isPendingDelete}
                        >
                          {isPendingDelete ? 'Deleting in 5s…' : (deletingId === us.id ? 'Removing…' : 'Delete')}
                        </button>
                        {isPendingDelete && (
                          <button
                            className="button secondary"
                            onClick={() => {
                              const t = pendingDeletes[us.id]
                              if (t) clearTimeout(t)
                              setPendingDeletes((prev) => {
                                const p = { ...prev }
                                delete p[us.id]
                                return p
                              })
                            }}
                          >
                            Undo
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="card" style={{ marginTop: 16 }}>
        <div className="row space-between">
          <h3>Your Roadmap</h3>
          <button
            onClick={async () => {
              setRoadmapMsg(null)
              try {
                const res = await api.post('/roadmap/generate', {})
                setRoadmap(res.data)
                setRoadmapMsg('Roadmap generated successfully.')
              } catch (err: any) {
                setRoadmapMsg(err?.response?.data?.detail || 'Failed to generate roadmap')
              }
            }}
          >
            Generate Roadmap
          </button>
        </div>
        {roadmapMsg && <div className="muted" style={{ marginBottom: 8 }}>{roadmapMsg}</div>}
        {!roadmap ? (
          <p className="muted">No active roadmap yet. Click "Generate Roadmap" to create one based on your skills.</p>
        ) : (
          <div>
            <p><strong>Title:</strong> {roadmap.title}</p>
            <p><strong>Goal:</strong> {roadmap.goal}</p>
            <p><strong>Difficulty:</strong> {roadmap.difficulty_level} · <strong>Duration:</strong> {roadmap.estimated_duration_weeks} weeks</p>
            <div style={{ margin: '10px 0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#9aa4b2' }}>
                <span>Overall Progress</span>
                <span>{Math.round(roadmap.progress_percentage || 0)}%</span>
              </div>
              <div style={{ width: '100%', background: '#1f2740', borderRadius: 8, height: 10, overflow: 'hidden' }}>
                <div style={{ width: `${Math.min(100, Math.max(0, Math.round(roadmap.progress_percentage || 0)))}%`, background: '#6e8efb', height: '100%' }} />
              </div>
            </div>
            <div style={{ marginTop: 8 }}>
              <h4 style={{ margin: '8px 0' }}>Steps</h4>
              <ol>
                {Array.isArray(roadmap.steps) && roadmap.steps
                  .slice()
                  .sort((a:any,b:any)=>(a.step_number||0)-(b.step_number||0))
                  .map((st: any, idx: number) => (
                  <li key={st.id} style={{ marginBottom: 10 }}>
                    <div className="row space-between" style={{ alignItems: 'flex-start' }}>
                      <div>
                        <div><strong>{st.title}</strong> <span className="muted">({st.step_type}, ~{st.estimated_duration_hours || 0}h)</span></div>
                        {st.content_url && (
                          <div style={{ marginTop: 4 }}>
                            <a href={st.content_url} target="_blank" rel="noreferrer" className="button secondary">
                              {st.content_provider ? `${st.content_provider} link` : 'Open resource'}
                            </a>
                          </div>
                        )}
                        {st.description && <div className="muted">{st.description}</div>}
                      </div>
                      <div className="row gap" style={{ flexWrap: 'wrap' }}>
                        <label style={{ fontSize: 12 }}>Status</label>
                        <select
                          value={st.status || 'not_started'}
                          onChange={(e) => {
                            const v = e.target.value
                            setRoadmap((prev:any) => ({
                              ...prev,
                              steps: prev.steps.map((s:any) => s.id === st.id ? { ...s, status: v } : s)
                            }))
                          }}
                        >
                          <option value="not_started">not_started</option>
                          <option value="in_progress">in_progress</option>
                          <option value="completed">completed</option>
                          <option value="skipped">skipped</option>
                        </select>
                        <label style={{ fontSize: 12 }}>Progress %</label>
                        <input
                          type="number"
                          min={0}
                          max={100}
                          value={Math.round(st.progress_percentage ?? 0)}
                          onChange={(e) => {
                            const v = Number(e.target.value)
                            setRoadmap((prev:any) => ({
                              ...prev,
                              steps: prev.steps.map((s:any) => s.id === st.id ? { ...s, progress_percentage: v } : s)
                            }))
                          }}
                          style={{ width: 90 }}
                        />
                        <button
                          className="button secondary"
                          onClick={async () => {
                            try {
                              const payload: any = {
                                status: st.status,
                                progress_percentage: Number(st.progress_percentage) || 0
                              }
                              const res = await api.patch(`/roadmap/steps/${st.id}`, payload)
                              setRoadmap(res.data)
                            } catch (err) {
                              alert('Failed to update step')
                            }
                          }}
                        >
                          Save
                        </button>
                      </div>
                    </div>
                  </li>
                ))}
              </ol>
            </div>
          </div>
        )}
      </div>

      <div className="card" style={{ marginTop: 16 }}>
        <div className="row space-between">
          <h3>Roadmap History</h3>
          <button
            className="button secondary"
            onClick={async () => {
              try {
                const res = await api.get('/roadmap/history')
                setHistory(res.data)
              } catch (err: any) {
                setHistoryError(err?.response?.data?.detail || 'Failed to load history')
              }
            }}
          >
            Refresh
          </button>
        </div>
        {historyError && <div className="error">{historyError}</div>}
        {(!history || history.length === 0) ? (
          <p className="muted">No history yet. Generate a roadmap to create entries.</p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left', padding: '8px 6px' }}>Title</th>
                  <th style={{ textAlign: 'left', padding: '8px 6px' }}>Status</th>
                  <th style={{ textAlign: 'left', padding: '8px 6px' }}>Created</th>
                  <th style={{ textAlign: 'left', padding: '8px 6px' }}>Progress</th>
                  <th style={{ textAlign: 'left', padding: '8px 6px' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {history.map((h: any) => (
                  <tr key={h.id}>
                    <td style={{ padding: '6px' }}>{h.title}</td>
                    <td style={{ padding: '6px' }}>{h.status}</td>
                    <td style={{ padding: '6px' }}>{h.created_at ? new Date(h.created_at).toLocaleString() : ''}</td>
                    <td style={{ padding: '6px' }}>{Math.round(h.progress_percentage || 0)}%</td>
                    <td style={{ padding: '6px' }}>
                      <div className="row gap">
                        <button
                          className="button secondary"
                          onClick={async () => {
                            try {
                              const res = await api.get(`/roadmap/${h.id}`)
                              setViewedPath(res.data)
                            } catch (err) {
                              alert('Failed to load path')
                            }
                          }}
                        >
                          View
                        </button>
                        {h.status !== 'active' && (
                          <button
                            onClick={async () => {
                              try {
                                await api.post(`/roadmap/${h.id}/restore`, {})
                                // refresh current and history
                                const [cur, hist] = await Promise.all([
                                  api.get('/roadmap/current'),
                                  api.get('/roadmap/history')
                                ])
                                setRoadmap(cur.data)
                                setHistory(hist.data)
                              } catch (err) {
                                alert('Failed to restore path')
                              }
                            }}
                          >
                            Restore
                          </button>
                        )}
                        <label style={{ fontSize: 12 }}>Compare A</label>
                        <input
                          type="radio"
                          name="cmpA"
                          checked={compareA === h.id}
                          onChange={() => setCompareA(h.id)}
                          />
                        <label style={{ fontSize: 12 }}>Compare B</label>
                        <input
                          type="radio"
                          name="cmpB"
                          checked={compareB === h.id}
                          onChange={() => setCompareB(h.id)}
                          />
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="row gap" style={{ marginTop: 8 }}>
              <button
                className="button secondary"
                onClick={async () => {
                  setCompareResult(null)
                  if (!compareA || !compareB || compareA === compareB) {
                    alert('Select two different paths (A and B) to compare')
                    return
                  }
                  try {
                    const res = await api.post(`/roadmap/compare?a_id=${compareA}&b_id=${compareB}`)
                    setCompareResult(res.data)
                  } catch (err) {
                    alert('Failed to compare paths')
                  }
                }}
              >
                Compare Selected
              </button>
            </div>
            {compareResult && (
              <div style={{ marginTop: 12 }}>
                <h4 style={{ margin: '6px 0' }}>Comparison</h4>
                <div className="row gap" style={{ alignItems: 'flex-start', flexWrap: 'wrap' }}>
                  <div style={{ minWidth: 260 }}>
                    <strong>Overlap</strong>
                    <ul>
                      {(compareResult.overlap_titles || []).map((t: string, i: number) => <li key={i}>{t}</li>)}
                    </ul>
                  </div>
                  <div style={{ minWidth: 260 }}>
                    <strong>Only A ({compareResult.a?.title})</strong>
                    <ul>
                      {(compareResult.only_a_titles || []).map((t: string, i: number) => <li key={i}>{t}</li>)}
                    </ul>
                  </div>
                  <div style={{ minWidth: 260 }}>
                    <strong>Only B ({compareResult.b?.title})</strong>
                    <ul>
                      {(compareResult.only_b_titles || []).map((t: string, i: number) => <li key={i}>{t}</li>)}
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
        {viewedPath && (
          <div style={{ marginTop: 12 }}>
            <h4 style={{ margin: '8px 0' }}>Viewed Path: {viewedPath.title}</h4>
            <ol>
              {Array.isArray(viewedPath.steps) && viewedPath.steps
                .slice()
                .sort((a:any,b:any)=>(a.step_number||0)-(b.step_number||0))
                .map((st:any) => (
                  <li key={st.id} style={{ marginBottom: 6 }}>
                    <div><strong>{st.title}</strong> <span className="muted">({st.step_type}, ~{st.estimated_duration_hours || 0}h)</span></div>
                  </li>
                ))}
            </ol>
          </div>
        )}
      </div>
    </div>
  )
}

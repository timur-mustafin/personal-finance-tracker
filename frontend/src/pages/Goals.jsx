
import React, { useEffect, useState } from 'react'
import api from '../api/axios'

export default function Goals() {
  const [goals, setGoals] = useState([])
  const [title, setTitle] = useState('')
  const [target, setTarget] = useState('')
  const [deadline, setDeadline] = useState('')

  useEffect(() => {
    api.get('goals/')
      .then(res => setGoals(res.data))
  }, [])

  const createGoal = (e) => {
    e.preventDefault()
    api.post('goals/', {
      title,
      target_amount: target,
      deadline
    }).then(res => {
      setGoals([...goals, res.data])
      setTitle('')
      setTarget('')
      setDeadline('')
    })
  }

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-2xl font-bold">My Goals</h1>

      <form onSubmit={createGoal} className="bg-white shadow rounded p-4 space-y-2">
        <h2 className="text-xl font-semibold">Create New Goal</h2>
        <input type="text" placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} className="w-full border rounded p-2" required />
        <input type="number" placeholder="Target Amount" value={target} onChange={e => setTarget(e.target.value)} className="w-full border rounded p-2" required />
        <input type="date" value={deadline} onChange={e => setDeadline(e.target.value)} className="w-full border rounded p-2" />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Create</button>
      </form>

      <div className="space-y-4">
        {goals.map(goal => (
          <div key={goal.id} className="bg-white p-4 rounded shadow">
            <h3 className="text-lg font-semibold">{goal.title}</h3>
            <p>Progress: {Math.round((goal.current_amount / goal.target_amount) * 100)}%</p>
            <div className="w-full bg-gray-200 rounded h-4 mt-1">
              <div className="bg-green-500 h-4 rounded" style={{ width: `${(goal.current_amount / goal.target_amount) * 100}%` }}></div>
            </div>
            {goal.deadline && <p className="text-sm text-gray-500 mt-1">Deadline: {goal.deadline}</p>}
          </div>
        ))}
      </div>
    </div>
  )
}

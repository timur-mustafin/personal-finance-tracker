
import React, { useEffect, useState } from 'react'
import api from '../api/axios'

export default function Reminders() {
  const [reminders, setReminders] = useState([])
  const [message, setMessage] = useState('')
  const [remindAt, setRemindAt] = useState('')

  useEffect(() => {
    api.get('reminders/').then(res => setReminders(res.data))
  }, [])

  const createReminder = (e) => {
    e.preventDefault()
    api.post('reminders/', {
      message,
      remind_at: remindAt
    }).then(res => {
      setReminders([...reminders, res.data])
      setMessage('')
      setRemindAt('')
    })
  }

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-2xl font-bold">Reminders</h1>

      <form onSubmit={createReminder} className="bg-white shadow rounded p-4 space-y-2">
        <h2 className="text-xl font-semibold">New Reminder</h2>
        <input type="text" placeholder="Reminder message" value={message} onChange={e => setMessage(e.target.value)} className="w-full border rounded p-2" required />
        <input type="datetime-local" value={remindAt} onChange={e => setRemindAt(e.target.value)} className="w-full border rounded p-2" required />
        <button type="submit" className="bg-indigo-600 text-white px-4 py-2 rounded">Save Reminder</button>
      </form>

      <div className="space-y-4">
        {reminders.map(reminder => (
          <div key={reminder.id} className="bg-white p-4 rounded shadow">
            <h3 className="text-lg font-semibold">{reminder.message}</h3>
            <p className="text-sm text-gray-500">Will remind at: {new Date(reminder.remind_at).toLocaleString()}</p>
            {reminder.is_sent && <p className="text-green-600 text-sm">✅ Already sent</p>}
          </div>
        ))}
      </div>
    </div>
  )
}

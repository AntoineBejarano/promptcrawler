'use client'

import { useEffect, useState } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import api from '@/lib/api'
import { Job } from '@/types/job'

export default function DashboardPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)
  const [prompt, setPrompt] = useState('')
  const [creating, setCreating] = useState(false)

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/login')
    }
  }, [status, router])

  useEffect(() => {
    if (session) {
      loadJobs()
    }
  }, [session])

  const loadJobs = async () => {
    try {
      const response = await api.get('/jobs')
      setJobs(response.data.jobs || [])
    } catch (error) {
      console.error('Error loading jobs:', error)
    } finally {
      setLoading(false)
    }
  }

  const createJob = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!prompt.trim()) return

    setCreating(true)
    try {
      const response = await api.post('/jobs', { prompt })
      setPrompt('')
      loadJobs()
      router.push(`/jobs/${response.data.id}`)
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error creando job')
    } finally {
      setCreating(false)
    }
  }

  if (status === 'loading' || loading) {
    return <div className="container mx-auto px-4 py-20 text-center">Cargando...</div>
  }

  if (!session) {
    return null
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <Link href="/auth/logout">
          <Button variant="outline">Cerrar sesión</Button>
        </Link>
      </div>

      {/* Crear Job */}
      <div className="mb-8 p-6 border rounded-lg">
        <h2 className="text-xl font-semibold mb-4">Crear nuevo job</h2>
        <form onSubmit={createJob}>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Escribe tu prompt aquí. Ej: 'Dame una lista de clubes de cannabis en Sudáfrica'"
            className="w-full p-3 border rounded-md mb-4 min-h-[100px]"
            disabled={creating}
          />
          <Button type="submit" disabled={creating || !prompt.trim()}>
            {creating ? 'Creando...' : 'Crear Job'}
          </Button>
        </form>
      </div>

      {/* Lista de Jobs */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Mis Jobs</h2>
        {jobs.length === 0 ? (
          <p className="text-muted-foreground">No tienes jobs todavía. Crea uno para comenzar.</p>
        ) : (
          <div className="space-y-4">
            {jobs.map((job) => (
              <Link
                key={job.id}
                href={`/jobs/${job.id}`}
                className="block p-4 border rounded-lg hover:bg-muted/50"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <p className="font-medium mb-2">{job.prompt.substring(0, 100)}...</p>
                    <div className="flex gap-4 text-sm text-muted-foreground">
                      <span>Status: {job.status}</span>
                      <span>Items: {job.items_processed}/{job.total_items}</span>
                      <span>Creado: {new Date(job.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                    job.status === 'completed' ? 'bg-green-100 text-green-800' :
                    job.status === 'running' ? 'bg-blue-100 text-blue-800' :
                    job.status === 'failed' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {job.status}
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}


'use client'

import { useEffect, useState } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter, useParams } from 'next/navigation'
import { Button } from '@/components/ui/button'
import api from '@/lib/api'
import { Job } from '@/types/job'

export default function JobDetailPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const params = useParams()
  const jobId = params.id as string

  const [job, setJob] = useState<Job | null>(null)
  const [loading, setLoading] = useState(true)
  const [results, setResults] = useState<any[]>([])

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/auth/login')
    }
  }, [status, router])

  useEffect(() => {
    if (session && jobId) {
      loadJob()
      // Polling para actualizar status
      const interval = setInterval(() => {
        loadJob()
      }, 3000)
      return () => clearInterval(interval)
    }
  }, [session, jobId])

  const loadJob = async () => {
    try {
      const response = await api.get(`/jobs/${jobId}`)
      setJob(response.data)
      
      // Cargar resultados si está completado
      if (response.data.status === 'completed') {
        const resultsResponse = await api.get(`/jobs/${jobId}/results?format=json`)
        setResults(resultsResponse.data.results || [])
      }
    } catch (error) {
      console.error('Error loading job:', error)
    } finally {
      setLoading(false)
    }
  }

  const downloadResults = async (format: 'json' | 'csv') => {
    try {
      const response = await api.get(`/jobs/${jobId}/results?format=${format}`)
      
      if (format === 'json') {
        const blob = new Blob([JSON.stringify(response.data.results, null, 2)], {
          type: 'application/json',
        })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `job-${jobId}-results.json`
        a.click()
        URL.revokeObjectURL(url)
      } else {
        const blob = new Blob([response.data.csv], { type: 'text/csv' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `job-${jobId}-results.csv`
        a.click()
        URL.revokeObjectURL(url)
      }
    } catch (error) {
      console.error('Error downloading results:', error)
      alert('Error descargando resultados')
    }
  }

  if (status === 'loading' || loading) {
    return <div className="container mx-auto px-4 py-20 text-center">Cargando...</div>
  }

  if (!session || !job) {
    return null
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <Button variant="outline" onClick={() => router.push('/dashboard')}>
          ← Volver al Dashboard
        </Button>
      </div>

      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-4">Job #{job.id}</h1>
        <div className="p-4 border rounded-lg bg-muted/50">
          <p className="font-medium mb-2">Prompt:</p>
          <p className="text-muted-foreground">{job.prompt}</p>
        </div>
        <div className="mt-4 flex gap-4 text-sm">
          <span>
            <strong>Status:</strong>{' '}
            <span className={`px-2 py-1 rounded ${
              job.status === 'completed' ? 'bg-green-100 text-green-800' :
              job.status === 'running' ? 'bg-blue-100 text-blue-800' :
              job.status === 'failed' ? 'bg-red-100 text-red-800' :
              'bg-gray-100 text-gray-800'
            }`}>
              {job.status}
            </span>
          </span>
          <span><strong>Items procesados:</strong> {job.items_processed}/{job.total_items}</span>
          {job.error_message && (
            <span className="text-red-600"><strong>Error:</strong> {job.error_message}</span>
          )}
        </div>
      </div>

      {job.status === 'completed' && results.length > 0 && (
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-semibold">Resultados ({results.length})</h2>
            <div className="flex gap-2">
              <Button onClick={() => downloadResults('json')} variant="outline">
                Descargar JSON
              </Button>
              <Button onClick={() => downloadResults('csv')} variant="outline">
                Descargar CSV
              </Button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse border">
              <thead>
                <tr className="bg-muted">
                  {Object.keys(results[0]?.data || {}).map((key) => (
                    <th key={key} className="border p-2 text-left">
                      {key}
                    </th>
                  ))}
                  <th className="border p-2 text-left">Source URL</th>
                </tr>
              </thead>
              <tbody>
                {results.slice(0, 100).map((result, idx) => (
                  <tr key={idx}>
                    {Object.keys(results[0]?.data || {}).map((key) => (
                      <td key={key} className="border p-2">
                        {typeof result.data[key] === 'object'
                          ? JSON.stringify(result.data[key])
                          : String(result.data[key] || '')}
                      </td>
                    ))}
                    <td className="border p-2">
                      <a
                        href={result.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline"
                      >
                        {result.source_url}
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {results.length > 100 && (
              <p className="mt-2 text-sm text-muted-foreground">
                Mostrando primeros 100 de {results.length} resultados
              </p>
            )}
          </div>
        </div>
      )}

      {job.status === 'completed' && results.length === 0 && (
        <p className="text-muted-foreground">No se encontraron resultados para este job.</p>
      )}

      {(job.status === 'pending' || job.status === 'running') && (
        <div className="text-center py-12">
          <p className="text-lg mb-2">Procesando job...</p>
          <p className="text-muted-foreground">
            {job.status === 'running' ? 'Crawleando y extrayendo datos...' : 'Esperando en cola...'}
          </p>
        </div>
      )}

      {job.status === 'failed' && (
        <div className="p-4 border border-red-300 rounded-lg bg-red-50">
          <p className="font-medium text-red-800 mb-2">Job falló</p>
          <p className="text-red-600">{job.error_message || 'Error desconocido'}</p>
        </div>
      )}
    </div>
  )
}


export interface Job {
  id: number
  prompt: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  owner_id: number
  project_id: number | null
  total_items: number
  items_processed: number
  error_message: string | null
  created_at: string
  updated_at: string | null
  completed_at: string | null
  results?: JobResult[]
}

export interface JobResult {
  id: number
  job_id: number
  data: Record<string, any>
  source_url: string | null
  created_at: string
}


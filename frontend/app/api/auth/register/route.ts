import { NextResponse } from 'next/server'
import { API_URL } from '@/lib/utils'
import axios from 'axios'

export async function POST(request: Request) {
  try {
    const body = await request.json()
    
    const response = await axios.post(`${API_URL}/api/auth/register`, body)
    
    return NextResponse.json(response.data)
  } catch (error: any) {
    return NextResponse.json(
      { detail: error.response?.data?.detail || 'Error al registrar' },
      { status: error.response?.status || 500 }
    )
  }
}


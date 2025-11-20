'use client'

import { useEffect } from 'react'
import { signOut } from 'next-auth/react'
import { useRouter } from 'next/navigation'

export default function LogoutPage() {
  const router = useRouter()

  useEffect(() => {
    signOut({ redirect: false }).then(() => {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token')
      }
      router.push('/')
    })
  }, [router])

  return (
    <div className="min-h-screen flex items-center justify-center">
      <p>Cerrando sesión...</p>
    </div>
  )
}


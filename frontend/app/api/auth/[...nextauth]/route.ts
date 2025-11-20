import NextAuth, { type NextAuthOptions } from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import { API_URL } from '@/lib/utils'
import axios from 'axios'

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null
        }

        try {
          const formData = new URLSearchParams()
          formData.append('username', credentials.email)
          formData.append('password', credentials.password)

          const response = await axios.post(
            `${API_URL}/api/auth/login`,
            formData,
            {
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
              },
            }
          )

          if (response.data?.access_token) {
            // Guardar token
            if (typeof window !== 'undefined') {
              localStorage.setItem('token', response.data.access_token)
            }

            // Obtener info del usuario
            const userResponse = await axios.get(`${API_URL}/api/users/me`, {
              headers: {
                Authorization: `Bearer ${response.data.access_token}`,
              },
            })

            return {
              id: userResponse.data.id.toString(),
              email: userResponse.data.email,
              name: userResponse.data.full_name,
              token: response.data.access_token,
            }
          }

          return null
        } catch (error) {
          console.error('Auth error:', error)
          return null
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.accessToken = (user as any).token
      }
      return token
    },
    async session({ session, token }) {
      if (token) {
        ;(session as any).accessToken = token.accessToken
      }
      return session
    },
  },
  pages: {
    signIn: '/auth/login',
  },
  session: {
    strategy: 'jwt',
  },
}

const handler = NextAuth(authOptions)

export { handler as GET, handler as POST }


import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl font-bold mb-6">
          Convierte cualquier prompt en un dataset real
        </h1>
        <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
          PromptCrawler usa IA para descubrir fuentes, crawlear webs y extraer datos estructurados.
          De prompt a dataset, directamente desde la web.
        </p>
        <div className="flex gap-4 justify-center">
          <Button asChild size="lg">
            <Link href="/dashboard">Comenzar gratis</Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="#como-funciona">Ver cómo funciona</Link>
          </Button>
        </div>
      </section>

      {/* Cómo funciona */}
      <section id="como-funciona" className="container mx-auto px-4 py-20">
        <h2 className="text-3xl font-bold text-center mb-12">Cómo funciona</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center p-6 border rounded-lg">
            <div className="text-4xl mb-4">1️⃣</div>
            <h3 className="text-xl font-semibold mb-2">Escribe tu prompt</h3>
            <p className="text-muted-foreground">
              Describe qué datos necesitas en lenguaje natural
            </p>
          </div>
          <div className="text-center p-6 border rounded-lg">
            <div className="text-4xl mb-4">2️⃣</div>
            <h3 className="text-xl font-semibold mb-2">Descubrimos fuentes</h3>
            <p className="text-muted-foreground">
              Usamos Perplexity para encontrar URLs relevantes
            </p>
          </div>
          <div className="text-center p-6 border rounded-lg">
            <div className="text-4xl mb-4">3️⃣</div>
            <h3 className="text-xl font-semibold mb-2">Extraemos datos</h3>
            <p className="text-muted-foreground">
              Crawleamos y extraemos datos estructurados con IA
            </p>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="container mx-auto px-4 py-20 bg-muted/50">
        <h2 className="text-3xl font-bold text-center mb-12">Pricing</h2>
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="border rounded-lg p-6">
            <h3 className="text-2xl font-bold mb-2">Free</h3>
            <p className="text-3xl font-bold mb-4">€0</p>
            <ul className="space-y-2 mb-6">
              <li>✅ 5 jobs / mes</li>
              <li>✅ 200 items / job</li>
            </ul>
            <Button asChild className="w-full">
              <Link href="/dashboard">Comenzar</Link>
            </Button>
          </div>
          <div className="border rounded-lg p-6 border-primary">
            <h3 className="text-2xl font-bold mb-2">Pro</h3>
            <p className="text-3xl font-bold mb-4">€29</p>
            <ul className="space-y-2 mb-6">
              <li>✅ 100 jobs / mes</li>
              <li>✅ 2000 items / job</li>
              <li>✅ API access</li>
            </ul>
            <Button asChild className="w-full" variant="default">
              <Link href="/dashboard">Comenzar</Link>
            </Button>
          </div>
          <div className="border rounded-lg p-6">
            <h3 className="text-2xl font-bold mb-2">Team</h3>
            <p className="text-3xl font-bold mb-4">€99</p>
            <ul className="space-y-2 mb-6">
              <li>✅ 500 jobs / mes</li>
              <li>✅ 10k items / job</li>
            </ul>
            <Button asChild className="w-full" variant="outline">
              <Link href="/dashboard">Comenzar</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-8 border-t text-center text-muted-foreground">
        <p>© 2024 PromptCrawler. Todos los derechos reservados.</p>
      </footer>
    </div>
  )
}


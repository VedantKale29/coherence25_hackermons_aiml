import Navbar from "@/components/navbar"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { SparklesCore } from "@/components/ui/sparkles"
import { TextGenerateEffect } from "@/components/ui/text-generate-effect"

export default function Home() {
  const heroText = "Transform your hiring process with AI-powered candidate screening"

  return (
    <main className="relative min-h-screen flex flex-col">
      <Navbar />
      <div className="absolute inset-0 z-0 overflow-hidden">
        <video autoPlay loop muted playsInline className="absolute min-w-full min-h-full object-cover">
          <source src="/videos/background.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        <div className="absolute inset-0 bg-black/60" />
      </div>

      <div className="absolute inset-0 z-1">
        <SparklesCore
          id="tsparticles"
          background="transparent"
          minSize={0.6}
          maxSize={1.4}
          particleDensity={70}
          className="w-full h-full"
          particleColor="#B3B4BD"
        />
      </div>

      <div className="relative z-10 flex-1 flex flex-col items-center justify-center text-center px-4">
        <div className="animate-fade-in-up">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">HireSense AI</h1>
          <div className="text-xl md:text-2xl text-white/90 max-w-2xl mb-12">
            <TextGenerateEffect words={heroText} />
          </div>
          <Link href="/upload">
            <Button
              size="lg"
              className="bg-[#0A21C0] hover:bg-[#050A44] text-white text-lg px-8 py-6 animate-pulse-slow"
            >
              Get Started
            </Button>
          </Link>
        </div>
      </div>
    </main>
  )
}


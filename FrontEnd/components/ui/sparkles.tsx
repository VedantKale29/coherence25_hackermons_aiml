"use client"
import React, { useEffect, useState } from "react"
import { cn } from "@/lib/utils"

export const SparklesCore = ({
  id,
  background,
  minSize,
  maxSize,
  speed,
  particleColor,
  className,
  particleDensity,
}: {
  id?: string
  background?: string
  minSize?: number
  maxSize?: number
  speed?: number
  particleColor?: string
  className?: string
  particleDensity?: number
}) => {
  const [particles, setParticles] = useState<Array<any>>([])
  const [width, setWidth] = useState(0)
  const [height, setHeight] = useState(0)
  const [canvas, setCanvas] = useState<HTMLCanvasElement | null>(null)
  const canvasRef = React.useRef<HTMLCanvasElement>(null)

  // Initialize particles
  useEffect(() => {
    if (canvasRef.current) {
      const ctx = canvasRef.current.getContext("2d")
      if (ctx) {
        setCanvas(canvasRef.current)
        setWidth(canvasRef.current.offsetWidth)
        setHeight(canvasRef.current.offsetHeight)

        const particleCount = Math.min(
          Math.floor((canvasRef.current.offsetWidth * canvasRef.current.offsetHeight) / 8000) * (particleDensity || 1),
          1000,
        )

        const newParticles = []
        for (let i = 0; i < particleCount; i++) {
          newParticles.push({
            x: Math.random() * canvasRef.current.offsetWidth,
            y: Math.random() * canvasRef.current.offsetHeight,
            size: Math.random() * (maxSize || 3 - minSize || 1) + (minSize || 1),
            speedX: (Math.random() - 0.5) * (speed || 0.1),
            speedY: (Math.random() - 0.5) * (speed || 0.1),
          })
        }
        setParticles(newParticles)
      }
    }

    function handleResize() {
      if (canvasRef.current) {
        setWidth(canvasRef.current.offsetWidth)
        setHeight(canvasRef.current.offsetHeight)
      }
    }

    window.addEventListener("resize", handleResize)
    return () => {
      window.removeEventListener("resize", handleResize)
    }
  }, [maxSize, minSize, particleDensity, speed])

  // Animation loop
  useEffect(() => {
    if (!canvas) return

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    let animationFrameId: number

    const render = () => {
      if (canvas && ctx) {
        ctx.clearRect(0, 0, canvas.width, canvas.height)

        particles.forEach((particle, i) => {
          // Update
          particle.x += particle.speedX
          particle.y += particle.speedY

          // Wrap around canvas
          if (particle.x > canvas.width) particle.x = 0
          else if (particle.x < 0) particle.x = canvas.width
          if (particle.y > canvas.height) particle.y = 0
          else if (particle.y < 0) particle.y = canvas.height

          // Draw
          ctx.beginPath()
          ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2)
          ctx.fillStyle = particleColor || "#B3B4BD"
          ctx.fill()
        })
      }

      animationFrameId = window.requestAnimationFrame(render)
    }

    render()

    return () => {
      window.cancelAnimationFrame(animationFrameId)
    }
  }, [canvas, particles, particleColor])

  return (
    <canvas
      ref={canvasRef}
      id={id || "sparkles-canvas"}
      width={width}
      height={height}
      className={cn("h-full w-full", className)}
      style={{
        background: background || "transparent",
      }}
    />
  )
}

